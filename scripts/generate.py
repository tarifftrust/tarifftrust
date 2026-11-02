#!/usr/bin/env python3
"""Generate the types and the operations of both packages from openapi.json, the API's contract.

    python scripts/generate.py          write the generated files
    python scripts/generate.py --check  fail when a generated file is out of date
    python scripts/generate.py --live   fail when the contract the API serves is another
    python scripts/generate.py --sync   copy the contract the API serves here, and generate

Uses only the standard library, so that it runs anywhere.
"""

import json
import keyword
import re
import sys
import textwrap
import urllib.request
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACT_FILE = ROOT / "openapi.json"
LIVE_CONTRACT = "https://api.tarifftrust.com/v1/openapi.json"
PYTHON_TYPES = ROOT / "python/src/tarifftrust/types.py"
PYTHON_OPERATIONS = ROOT / "python/src/tarifftrust/_operations.py"
NODE_TYPES = ROOT / "node/src/types.ts"
NODE_OPERATIONS = ROOT / "node/src/operations.ts"
READMES = [ROOT / "README.md", ROOT / "python/README.md", ROOT / "node/README.md"]
HEADER = "Generated from openapi.json by scripts/generate.py: do not edit."
PYTHON_WIDTH = 96


@dataclass
class Operation:
    name: str
    method: str
    path: str
    summary: str
    description: str
    path_parameters: list
    query_parameters: list
    idempotent: bool
    body: str | None
    answer: str
    auth: bool

    @property
    def camel(self):
        first, *rest = self.name.split("_")
        return first + "".join(word.title() for word in rest)


def reference(schema):
    return schema["$ref"].rsplit("/", 1)[-1]


def body_schema(operation):
    content = operation.get("requestBody", {}).get("content", {})
    schema = content.get("application/json", {}).get("schema")
    return reference(schema) if schema else None


def read_operations(contract):
    found = []
    for path, item in contract["paths"].items():
        for method, operation in item.items():
            parameters = operation.get("parameters", [])
            answer = operation["responses"]["200"]["content"]["application/json"]["schema"]
            found.append(
                Operation(
                    name=operation["operationId"],
                    method=method.upper(),
                    path=path,
                    summary=operation["summary"],
                    description=operation.get("description", ""),
                    path_parameters=[item for item in parameters if item["in"] == "path"],
                    query_parameters=[item for item in parameters if item["in"] == "query"],
                    idempotent=any(item["name"] == "Idempotency-Key" for item in parameters),
                    body=body_schema(operation),
                    answer=reference(answer),
                    auth=bool(operation.get("security")),
                )
            )
    return found


def only_requires(schema):
    """A oneOf that only says which fields exclude each other, by their presence or their value:
    their types stay as they are, and the API refuses a wrong choice by naming them."""
    not_null = {"not": {"type": "null"}}
    return all(
        set(item) <= {"required", "properties"}
        and all(field == not_null for field in item.get("properties", {}).values())
        for item in schema["oneOf"]
    )


def unsupported(contract, operations):
    """What this generator would get wrong: better to stop than to publish wrong types."""
    schemas = contract["components"]["schemas"]
    problems = []
    if contract.get("security"):
        problems.append("a security at the contract's top level: declare it per operation")

    def visit(where, schema):
        for shape in ("allOf", "oneOf", "not", "discriminator", "patternProperties"):
            if shape in schema and not (shape == "oneOf" and only_requires(schema)):
                problems.append(f"{where}: {shape}")
        if isinstance(schema.get("type"), list):
            problems.append(f"{where}: a list of types")
        for name, field in schema.get("properties", {}).items():
            visit(f"{where}.{name}", field)
        for item in schema.get("anyOf", []):
            visit(where, item)
        for child in ("items", "additionalProperties"):
            if isinstance(schema.get(child), dict):
                visit(where, schema[child])

    for name, schema in schemas.items():
        visit(name, schema)
    inputs = input_schemas(contract, operations)
    for name in nested_inputs(contract, operations):
        for field in schemas[name].get("properties", {}):
            if keyword.iskeyword(field):
                problems.append(f"{name}.{field}: a Python keyword in a request's nested object")
    for operation in operations:
        if operation.body and operation.query_parameters:
            problems.append(f"{operation.name}: a body and a query")
        if any(item.get("required") for item in operation.query_parameters):
            problems.append(f"{operation.name}: a required query argument")
    answers = {operation.answer for operation in operations}
    for name in sorted(answers & set(inputs)):
        problems.append(f"{name}: both a request and an answer")
    return problems


def nested_inputs(contract, operations):
    """The objects sent inside a request; the fields of a body itself are arguments in Python."""
    schemas = contract["components"]["schemas"]
    found = {}

    def visit(schema):
        if "$ref" in schema:
            name = reference(schema)
            if name not in found:
                found[name] = schemas[name]
                for field in schemas[name].get("properties", {}).values():
                    visit(field)
        for item in schema.get("anyOf", []):
            visit(item)
        if "items" in schema:
            visit(schema["items"])

    for operation in operations:
        if operation.body:
            for field in schemas[operation.body].get("properties", {}).values():
                visit(field)
    return dict(sorted(found.items()))


def input_schemas(contract, operations):
    """Every object a request may carry, the bodies included."""
    schemas = contract["components"]["schemas"]
    names = set(nested_inputs(contract, operations))
    names.update(operation.body for operation in operations if operation.body)
    return {name: schemas[name] for name in sorted(names)}


def text_of(value):
    return " ".join((value or "").split())


def paragraphs(value):
    return [text_of(part) for part in (value or "").split("\n\n") if part.strip()]


# ---------- Python ----------


def python_name(name):
    return f"{name}_" if keyword.iskeyword(name) else name


def python_parts(schema, inputs):
    if "$ref" in schema:
        return [reference(schema)]
    if "anyOf" in schema:
        return [part for item in schema["anyOf"] for part in python_parts(item, inputs)]
    if "const" in schema:
        return [f"Literal[{json.dumps(schema['const'])}]"]
    if "enum" in schema:
        return [f"Literal[{', '.join(json.dumps(value) for value in schema['enum'])}]"]
    kind = schema.get("type")
    if kind == "null":
        return ["None"]
    if kind == "string":
        if inputs and schema.get("format") == "date":
            return ["str", "date"]
        if inputs and schema.get("format") == "date-time":
            return ["str", "datetime"]
        return ["str"]
    if kind == "integer":
        return ["int"]
    if kind == "number":
        return ["int", "float", "Decimal"] if inputs else ["float"]
    if kind == "boolean":
        return ["bool"]
    if kind == "array":
        item = python_type(schema.get("items", {}), inputs)
        return [f"Sequence[{item}]" if inputs else f"list[{item}]"]
    if kind == "object" or "additionalProperties" in schema:
        values = schema.get("additionalProperties")
        value = python_type(values, inputs) if isinstance(values, dict) else "Any"
        return [f"Mapping[str, {value}]" if inputs else f"dict[str, {value}]"]
    return ["Any"]


def python_type(schema, inputs):
    return " | ".join(dict.fromkeys(python_parts(schema, inputs)))


def python_nested(schema, schemas):
    """How an answer's field becomes objects: a name, [of a list], {"*": of a map}, (a union)."""
    if "$ref" in schema:
        return reference(schema)
    if "anyOf" in schema:
        kinds = [item for item in schema["anyOf"] if item.get("type") != "null"]
        if len(kinds) == 1:
            return python_nested(kinds[0], schemas)
        names = tuple(reference(item) for item in kinds if "$ref" in item)
        return names if len(names) == len(kinds) else None
    if schema.get("type") == "array":
        item = python_nested(schema.get("items", {}), schemas)
        return [item] if item else None
    if isinstance(schema.get("additionalProperties"), dict):
        item = python_nested(schema["additionalProperties"], schemas)
        return {"*": item} if item else None
    return None


def python_doc(value, indent):
    """A docstring's lines, wrapped, for a description of the contract."""
    pad = " " * indent
    blocks = [
        textwrap.fill(part, PYTHON_WIDTH - indent, initial_indent=pad, subsequent_indent=pad)
        for part in paragraphs(value)
    ]
    text = "\n\n".join(blocks).strip().replace("\\", "\\\\").replace('"""', "'''")
    if text.endswith('"'):
        text += " "
    return f'{pad}"""{text}"""' if "\n" not in text else f'{pad}"""{text}\n{pad}"""'


def python_input_class(name, schema):
    required = schema.get("required", [])
    properties = schema.get("properties", {})

    def fields(names):
        lines = []
        for field in names:
            lines.append(f"    {field}: {python_type(properties[field], True)}")
            if text_of(properties[field].get("description")):
                lines.append(python_doc(properties[field]["description"], 4))
        return lines

    optional = [field for field in properties if field not in required]
    bases = []
    if required:
        bases += [f"class _{name}Required(TypedDict):", *fields(required), "", ""]
        head = f"class {name}(_{name}Required, total=False):"
    else:
        head = f"class {name}(TypedDict, total=False):"
    body = [python_doc(schema.get("description") or name, 4), *fields(optional)]
    return "\n".join([*bases, head, *body])


def python_model_class(name, schema, schemas):
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    nested = {
        field: python_nested(value, schemas)
        for field, value in properties.items()
        if python_nested(value, schemas)
    }
    defaults = {
        field: value["default"]
        for field, value in properties.items()
        if value.get("default") is not None
    }
    lines = [f"class {name}(Model):", python_doc(schema.get("description") or name, 4), ""]
    lines.append(f"    _fields: ClassVar[frozenset[str]] = frozenset({sorted(properties)!r})")
    lines.append(f"    _required: ClassVar[frozenset[str]] = frozenset({sorted(required)!r})")
    if nested:
        lines.append(f"    _nested: ClassVar[dict[str, Any]] = {nested!r}")
    if defaults:
        lines.append(f"    _defaults: ClassVar[dict[str, Any]] = {defaults!r}")
    for field, value in properties.items():
        lines.append("")
        lines.append(f"    {python_name(field)}: {python_type(value, False)}")
        if text_of(value.get("description")):
            lines.append(python_doc(value["description"], 4))
    return "\n".join(lines)


def python_types(contract, operations):
    schemas = contract["components"]["schemas"]
    nested = nested_inputs(contract, operations)
    inputs = input_schemas(contract, operations)
    blocks = [
        f'"""The objects of the TariffTrust API. {HEADER}"""',
        "from __future__ import annotations\n\n"
        "from collections.abc import Mapping, Sequence\n"
        "from datetime import date, datetime\n"
        "from decimal import Decimal\n"
        "from typing import Any, ClassVar, Literal, TypedDict\n\n"
        "from ._model import Model",
    ]
    blocks += [python_input_class(name, schema) for name, schema in nested.items()]
    blocks += [
        python_model_class(name, schema, schemas)
        for name, schema in schemas.items()
        if name not in inputs
    ]
    return "\n\n\n".join(blocks) + "\n"


def python_signature_parts(operation, schemas):
    """The arguments of an operation in Python: the path's, then its body's or query's fields,
    those required first, as (argument, annotation, sent as, description, required)."""
    fields = []
    if operation.body:
        schema = schemas[operation.body]
        required = schema.get("required", [])
        ordered = sorted(schema["properties"], key=lambda name: name not in required)
        for name in ordered:
            value = schema["properties"][name]
            fields.append(
                (
                    python_name(name),
                    python_type(value, True),
                    name,
                    text_of(value.get("description")),
                    name in required,
                )
            )
    for parameter in operation.query_parameters:
        fields.append(
            (
                python_name(parameter["name"]),
                python_type(parameter["schema"], True),
                parameter["name"],
                text_of(parameter.get("description")),
                False,
            )
        )
    return fields


def python_method(operation, schemas, asynchronous):
    fields = python_signature_parts(operation, schemas)
    head = ["self"]
    head += [f"{item['name']}: str" for item in operation.path_parameters]
    keywords = []
    for name, annotation, _, _, required in fields:
        if required:
            keywords.append(f"{name}: {annotation}")
        else:
            optional = annotation if "None" in annotation.split(" | ") else f"{annotation} | None"
            keywords.append(f"{name}: {optional} = None")
    if operation.idempotent:
        keywords.append("idempotency_key: str | None = None")
    if keywords:
        head.append("*")
    arguments = "".join(f"        {item},\n" for item in [*head, *keywords])
    prefix = "async def" if asynchronous else "def"
    lines = [f"    {prefix} {operation.name}(\n{arguments}    ) -> {operation.answer}:"]

    documented = [
        (item["name"], text_of(item.get("description"))) for item in operation.path_parameters
    ]
    documented += [(field[0], field[3]) for field in fields]
    if operation.idempotent:
        documented.append(
            (
                "idempotency_key",
                "Makes a retry of this call safe; a new one is generated for each call otherwise.",
            )
        )
    doc = [text_of(operation.summary) + ".", *paragraphs(operation.description)]
    pad = " " * 8
    text = "\n\n".join(textwrap.fill(part, PYTHON_WIDTH - 8) for part in doc)
    if documented:
        text += "\n\nArgs:"
        for name, description in documented:
            text += "\n" + textwrap.fill(
                f"{name}: {description}",
                PYTHON_WIDTH - 8,
                initial_indent="    ",
                subsequent_indent="        ",
            )
    text = text.replace("\\", "\\\\").replace('"""', "'''")
    docstring = textwrap.indent(text, pad).strip()
    lines.append(f'{pad}"""{docstring}\n{pad}"""')

    path = operation.path
    for item in operation.path_parameters:
        path = path.replace("{" + item["name"] + "}", "{quote(" + item["name"] + ", safe='')}")
    path_literal = f'f"{path}"' if operation.path_parameters else f'"{path}"'
    call = [f'"{operation.method}"', path_literal, f"model={operation.answer}"]
    if operation.body:
        sent = ", ".join(f'"{field[2]}": {field[0]}' for field in fields)
        call.append(f"body={{{sent}}}")
    elif fields:
        sent = ", ".join(f'"{field[2]}": {field[0]}' for field in fields)
        call.append(f"query={{{sent}}}")
    if not operation.auth:
        call.append("auth=False")
    if operation.idempotent:
        call += ["idempotent=True", "idempotency_key=idempotency_key"]
    joined = "".join(f"            {item},\n" for item in call)
    keyword_return = "return await" if asynchronous else "return"
    lines.append(f"{pad}{keyword_return} self._request(\n{joined}{pad})")
    return "\n".join(lines)


def python_operations(contract, operations):
    schemas = contract["components"]["schemas"]
    names = sorted({operation.answer for operation in operations})
    names += sorted(nested_inputs(contract, operations))
    imports = "".join(f"    {name},\n" for name in sorted(set(names)))
    blocks = [
        f'"""The operations of the TariffTrust API, as methods. {HEADER}"""',
        "from __future__ import annotations\n\n"
        "from collections.abc import Mapping, Sequence\n"
        "from datetime import date, datetime\n"
        "from decimal import Decimal\n"
        "from typing import Any, Literal, TypeVar\n"
        "from urllib.parse import quote\n\n"
        "from ._model import Model\n"
        f"from .types import (\n{imports})\n\n"
        '_M = TypeVar("_M", bound=Model)',
    ]
    for class_name, asynchronous in (("Operations", False), ("AsyncOperations", True)):
        prefix = "async def" if asynchronous else "def"
        head = (
            f"class {class_name}:\n"
            f'    """Each operation of the contract, under its operationId."""\n\n'
            f"    {prefix} _request(\n"
            "        self,\n"
            "        method: str,\n"
            "        path: str,\n"
            "        *,\n"
            "        model: type[_M],\n"
            "        query: Mapping[str, Any] | None = None,\n"
            "        body: Mapping[str, Any] | None = None,\n"
            "        auth: bool = True,\n"
            "        idempotent: bool = False,\n"
            "        idempotency_key: str | None = None,\n"
            "    ) -> _M:\n"
            "        raise NotImplementedError"
        )
        methods = [python_method(item, schemas, asynchronous) for item in operations]
        blocks.append("\n\n".join([head, *methods]))
    return "\n\n\n".join(blocks) + "\n"


# ---------- TypeScript ----------


def ts_type(schema):
    if "$ref" in schema:
        return reference(schema)
    if "anyOf" in schema:
        return " | ".join(dict.fromkeys(ts_type(item) for item in schema["anyOf"]))
    if "const" in schema:
        return json.dumps(schema["const"])
    if "enum" in schema:
        return " | ".join(json.dumps(value) for value in schema["enum"])
    kind = schema.get("type")
    if kind == "null":
        return "null"
    if kind == "string":
        return "string"
    if kind in ("integer", "number"):
        return "number"
    if kind == "boolean":
        return "boolean"
    if kind == "array":
        item = ts_type(schema.get("items", {}))
        return f"({item})[]" if " | " in item else f"{item}[]"
    if kind == "object" or "additionalProperties" in schema:
        values = schema.get("additionalProperties")
        value = ts_type(values) if isinstance(values, dict) else "unknown"
        return f"Record<string, {value}>"
    return "unknown"


def ts_doc(value, indent, extra=()):
    pad = " " * indent
    text = [*paragraphs(value), *extra]
    if not text:
        return []
    blocks = []
    for number, part in enumerate(text):
        if number:
            blocks.append(f"{pad} *")
        wrapped = textwrap.wrap(part.replace("*/", "* /"), 96 - indent - 3) or [""]
        blocks += [f"{pad} * {line}" for line in wrapped]
    return [f"{pad}/**", *blocks, f"{pad} */"]


def ts_property_name(name):
    return name if re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", name) else json.dumps(name)


def ts_interface(name, schema):
    required = schema.get("required", [])
    lines = [*ts_doc(schema.get("description"), 0), f"export interface {name} {{"]
    for field, value in schema.get("properties", {}).items():
        mark = "" if field in required else "?"
        default = value.get("default")
        extra = [f"Default: {json.dumps(default)}."] if default not in (None, "", []) else []
        lines += ts_doc(value.get("description"), 2, extra)
        lines.append(f"  {ts_property_name(field)}{mark}: {ts_type(value)};")
    lines.append("}")
    return "\n".join(lines)


def ts_query_name(operation):
    return f"{operation.camel[0].upper()}{operation.camel[1:]}Query"


def ts_types(contract, operations):
    schemas = contract["components"]["schemas"]
    blocks = [f"// The objects of the TariffTrust API. {HEADER}"]
    blocks += [ts_interface(name, schema) for name, schema in schemas.items()]
    for operation in operations:
        if operation.query_parameters:
            schema = {
                "description": f"What {operation.name} takes in its query.",
                "properties": {
                    item["name"]: {**item["schema"], "description": item.get("description")}
                    for item in operation.query_parameters
                },
            }
            blocks.append(ts_interface(ts_query_name(operation), schema))
    return "\n\n".join(blocks) + "\n"


def ts_method(operation):
    arguments = [f"{item['name']}: string" for item in operation.path_parameters]
    fields = [f'method: "{operation.method}"']
    path = operation.path
    for item in operation.path_parameters:
        path = path.replace("{" + item["name"] + "}", "${encodeURIComponent(" + item["name"] + ")}")
    fields.append(f"path: `{path}`" if operation.path_parameters else f'path: "{path}"')
    if operation.body:
        arguments.append(f"body: {operation.body}")
        fields.append("body")
    if operation.query_parameters:
        arguments.append(f"query: {ts_query_name(operation)} = {{}}")
        fields.append("query: query as Record<string, unknown>")
    arguments.append("options?: RequestOptions")
    if not operation.auth:
        fields.append("auth: false")
    if operation.idempotent:
        fields.append("idempotent: true")
    fields.append("options")
    signature = ", ".join(arguments)
    fragments = [
        *ts_doc(f"{text_of(operation.summary)}.\n\n{operation.description}", 2),
        f"  {operation.camel}({signature}): Promise<{operation.answer}> {{",
        "    return this.request<" + operation.answer + ">({",
        *[f"      {field}," for field in fields],
        "    });",
        "  }",
    ]
    return "\n".join(fragments)


def ts_operations(contract, operations):
    names = {operation.answer for operation in operations}
    names |= {operation.body for operation in operations if operation.body}
    names |= {ts_query_name(operation) for operation in operations if operation.query_parameters}
    imports = "".join(f"  {name},\n" for name in sorted(names))
    methods = "\n\n".join(ts_method(operation) for operation in operations)
    return (
        f"// The operations of the TariffTrust API, as methods. {HEADER}\n\n"
        'import type { Call, RequestOptions } from "./call.js";\n'
        f'import type {{\n{imports}}} from "./types.js";\n\n'
        "/** Each operation of the contract, under its operationId in camelCase. */\n"
        "export abstract class Operations {\n"
        "  protected abstract request<T>(call: Call): Promise<T>;\n\n"
        f"{methods}\n"
        "}\n"
    )


# ---------- README ----------


def operations_table(operations, language):
    head = "| Method | Route | What it does |\n| --- | --- | --- |\n"
    if language == "both":
        head = "| Python | Node.js | Route | What it does |\n| --- | --- | --- | --- |\n"
    rows = []
    for operation in operations:
        if language == "both":
            cells = [f"`{operation.name}`", f"`{operation.camel}`"]
        elif language == "python":
            cells = [f"`client.{operation.name}()`"]
        else:
            cells = [f"`client.{operation.camel}()`"]
        slug = operation.name.replace("_", "-")
        route = f"`{operation.method} {operation.path}`"
        cells.append(f"[{route}](https://tarifftrust.com/api/reference/#{slug})")
        cells.append(text_of(operation.summary))
        rows.append("| " + " | ".join(cells) + " |")
    return head + "\n".join(rows)


def with_table(text, table):
    start, end = "<!-- operations:start -->", "<!-- operations:end -->"
    if start not in text:
        return text
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return f"{before}{start}\n{table}\n{end}{after}"


# ---------- Files ----------


def generated_files(contract):
    operations = read_operations(contract)
    problems = unsupported(contract, operations)
    if problems:
        sys.exit(
            "The contract has what this generator does not handle:\n  " + "\n  ".join(problems)
        )
    files = {
        PYTHON_TYPES: python_types(contract, operations),
        PYTHON_OPERATIONS: python_operations(contract, operations),
        NODE_TYPES: ts_types(contract, operations),
        NODE_OPERATIONS: ts_operations(contract, operations),
    }
    languages = dict(zip(READMES, ("both", "python", "node"), strict=True))
    for path, language in languages.items():
        if path.exists():
            files[path] = with_table(path.read_text(), operations_table(operations, language))
    return files


def live_contract():
    request = urllib.request.Request(
        LIVE_CONTRACT, headers={"User-Agent": "tarifftrust-sdk-generate"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main(arguments):
    command = arguments[0] if arguments else ""
    if command == "--live":
        if live_contract() != json.loads(CONTRACT_FILE.read_text()):
            print(
                "The contract the API serves changed: run python scripts/generate.py --sync, "
                "commit, and publish a new version."
            )
            return 1
        print("openapi.json is the contract the API serves.")
        return 0
    if command == "--sync":
        CONTRACT_FILE.write_text(json.dumps(live_contract(), indent=2, sort_keys=True) + "\n")
    files = generated_files(json.loads(CONTRACT_FILE.read_text()))
    if command == "--check":
        stale = [
            path.relative_to(ROOT).as_posix()
            for path, text in files.items()
            if not path.exists() or path.read_text() != text
        ]
        if stale:
            print("Out of date, run python scripts/generate.py: " + ", ".join(stale))
            return 1
        print("The generated files follow openapi.json.")
        return 0
    for path, text in files.items():
        path.write_text(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
