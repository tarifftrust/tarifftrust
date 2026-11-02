"""An object of an answer: its fields as attributes, built from the JSON when first read."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, ClassVar


class Model:
    """An object of the API. A field the answer leaves out reads as its default in the contract,
    or None; a field newer than this package reads as an attribute too; ``to_dict()`` gives the
    object as the API sent it."""

    _registry: ClassVar[dict[str, type[Model]]] = {}
    _fields: ClassVar[frozenset[str]] = frozenset()
    _required: ClassVar[frozenset[str]] = frozenset()
    _nested: ClassVar[dict[str, Any]] = {}
    _defaults: ClassVar[dict[str, Any]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        Model._registry[cls.__name__] = cls

    def __init__(self, data: Mapping[str, Any]) -> None:
        self._data = data
        self._read: dict[str, Any] = {}

    def __getattr__(self, name: str) -> Any:
        # Only for what is not found otherwise; a private name is never a field.
        if name.startswith("_"):
            raise AttributeError(name)
        field = name.removesuffix("_")
        if field in self._read:
            return self._read[field]
        if field in self._data:
            value = _build(self._nested.get(field), self._data[field])
        elif field in self._fields:
            value = _copy(self._defaults.get(field))
        else:
            raise AttributeError(f"{type(self).__name__} has no field {name!r}")
        self._read[field] = value
        return value

    def __dir__(self) -> list[str]:
        return sorted({*object.__dir__(self), *self._fields, *self._data})

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, type(self))
            and type(other) is type(self)
            and other._data == self._data
        )

    __hash__ = None  # type: ignore[assignment]

    def __repr__(self) -> str:
        scalars = [
            f"{field}={value!r}"
            for field, value in self._data.items()
            if not isinstance(value, (dict, list))
        ]
        return f"{type(self).__name__}({', '.join(scalars[:6])}{', ...' if scalars[6:] else ''})"

    def to_dict(self) -> dict[str, Any]:
        """The object as the API sent it, as plain JSON values."""
        return dict(self._data)


def _copy(value: Any) -> Any:
    return list(value) if isinstance(value, list) else value


def _build(spec: Any, value: Any) -> Any:
    """A JSON value as the objects ``spec`` names: a name, [of a list], {"*": of a map}, (union)."""
    if spec is None or value is None:
        return value
    if isinstance(spec, str):
        return Model._registry[spec](value) if isinstance(value, Mapping) else value
    if isinstance(spec, list):
        return [_build(spec[0], item) for item in value] if isinstance(value, list) else value
    if isinstance(spec, dict):
        if not isinstance(value, Mapping):
            return value
        return {key: _build(spec["*"], item) for key, item in value.items()}
    if isinstance(value, Mapping):
        for name in spec:
            if Model._registry[name]._required <= value.keys():
                return Model._registry[name](value)
    return value
