// The CommonJS build sits under a package of "type": "module": it says what it is.
import { writeFileSync } from "node:fs";

writeFileSync(new URL("../dist/cjs/package.json", import.meta.url), '{\n  "type": "commonjs"\n}\n');
