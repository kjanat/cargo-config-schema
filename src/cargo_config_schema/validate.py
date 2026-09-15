"""Validate schemas and fixtures from the repository root."""

import json
import subprocess
import sys
import tomllib
from pathlib import Path
from tempfile import TemporaryDirectory

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


def check_references(node, resolver):
    if isinstance(node, dict):
        if "$ref" in node:
            resolver.lookup(node["$ref"])
        for value in node.values():
            check_references(value, resolver)
    elif isinstance(node, list):
        for value in node:
            check_references(value, resolver)


def main() -> None:
    root = Path.cwd()
    schemas = {
        path.name: json.loads(path.read_text(encoding="utf-8"))
        for path in (root / "schemas").glob("*.schema.json")
    }
    source = schemas["cargo-config.schema.json"]
    bundle_path = root / "cargo-config.json"
    bundle_bytes = bundle_path.read_bytes()
    bundle = json.loads(bundle_bytes)
    formatting = (root / "tests/formatting.txt").read_text(encoding="utf-8")
    formatted = subprocess.run(
        [
            "tombi",
            "format",
            "--stdin-filename",
            str(root / "tests/formatting.toml"),
            "-",
        ],
        input=formatting,
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout
    parsed = tomllib.loads(formatted)
    if parsed != tomllib.loads(formatting):
        raise SystemExit("Tombi changed configuration values or array order")
    orders = {
        ("net",): ["retry", "git-fetch-with-cli", "offline"],
        ("http", "ssl-version"): ["min", "max"],
        ("env", "TEST"): ["value", "force", "relative"],
        ("alias",): ["aaa", "zzz"],
    }
    for path, expected in orders.items():
        table = parsed
        for key in path:
            table = table[key]
        if list(table) != expected:
            raise SystemExit(
                f"Tombi order for {'.'.join(path)}: {list(table)} != {expected}"
            )
    for schema in [*schemas.values(), bundle]:
        Draft202012Validator.check_schema(schema)
    uri = source["$id"].rsplit("/", 1)[0] + "/"
    registry = Registry().with_resources(
        (uri + name, Resource.from_contents(schema)) for name, schema in schemas.items()
    )
    validators = {
        "modules": Draft202012Validator(source, registry=registry),
        "bundle": Draft202012Validator(bundle),
    }
    cases = json.loads((root / "tests/cases.json").read_text(encoding="utf-8"))
    for index, case in enumerate(cases, start=1):
        for label, validator in validators.items():
            errors = list(validator.iter_errors(case["config"]))
            if (not errors) != case["valid"]:
                raise SystemExit(f"Case {index}, {label}: unexpected result: {errors}")
    for name, schema in schemas.items():
        check_references(schema, registry.resolver(uri + name))
    with TemporaryDirectory(prefix="cargo-schema-") as directory:
        generated = Path(directory) / "cargo-config.json"
        subprocess.run(
            [
                sys.executable,
                "-m",
                "cargo_config_schema.bundle",
                "--output",
                str(generated),
            ],
            check=True,
        )
        if generated.read_bytes() != bundle_bytes:
            raise SystemExit("Bundle is stale: run uv run cargo-schema-bundle")
    print(
        f"{len(cases)} cases x modules/bundle; references, {len(schemas) + 1} metaschemas, generation and Tombi ordering passed"
    )


if __name__ == "__main__":
    main()
