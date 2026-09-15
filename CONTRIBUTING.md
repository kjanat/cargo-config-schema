# Contributing

Contributions are accepted through pull requests only. Issues are disabled.

For corrections or additions, open a pull request with the proposed change,
relevant Cargo documentation references, and a test case where applicable.

## Repository layout

- `schemas/`: modular schema sources.
- `src/cargo_config_schema/`: bundle and validation commands.
- `cargo-config.json`: generated schema for editors.
- `tests/`: validation cases, formatter fixture and sample configuration.
- `docs/`: reference material retained from the original gist.

## Development

Edit the modular sources in `schemas/`, then regenerate and validate the bundle:

```sh
uv sync --locked
uv run dprint fmt
uv run cargo-schema-bundle
uv run cargo-schema-check
```

Include the regenerated `cargo-config.json` in your pull request.

Development dependencies include dprint and Tombi.
The pinned [JSON Schema sorter](https://github.com/kjanat/dprint-plugin-json-schema-sort)
sorts schema keywords while preserving property order for Tombi.
`uv run dprint fmt` also formats TOML through Tombi and Python through Ruff.

The tests compare the modular and bundled schemas and verify deterministic
generation, actual Tombi field ordering and preservation of argument arrays.
