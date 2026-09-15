---
source: https://taplo.tamasfe.dev/configuration/developing-schemas.html
created: 2026-05-05T17:52
_meta:
  extension: https://github.com/kjanat/snipsnip
---

# Developing Schemas

## Writing Schemas

All features from the [Draft 4](https://json-schema.org/specification-links.html#draft-4) specification are supported, the schemas may contain external and even recursive references as well.

All schemas must be in JSON format. YAML schemas must be converted before use by Taplo.

### Schema Extension

All schema objects might contain an `x-taplo` extension field that allows attaching additional information to the schema.

> The `x-taplo` field (and any other fields) are ignored if `$ref` is present in an object.

The example below contains all the currently supported extension fields:

```jsonc
{
	"type": "string",
	"title": "My Type",
	"enum": ["one", "two", "three"],
	"default": "one",
	// All keys in the extension are optional.
	"x-taplo": {
		// Hide the schema from completion and similar hints.
		"hidden": true,
		"docs": {
			// Main documentation for the schema, expected to be markdown.
			// If omitted, the description will be used.
			"main": "This is [My Schema](https://example.com/mySchema)",
			// Documentation for enum values, used in completion or hover.
			// Indices match the enum values. Use null for missing entries.
			"enumValues": [
				"Documentation of 'one'.",
				null,
				"Documentation of 'three'.",
			],
			// Documentation of the default value, same as enum docs.
			"defaultValue": "Documentation of 'one'.",
		},
		"links": {
			// URL the key will point to if the schema is part of a table.
			"key": "https://example.com/mySchema",
			// Different enum values can also have URLs they point to.
			// Same rules as enum docs.
			"enumValues": ["https://example.com/one", "https://example.com/two"],
		},
		// For object schemas, hint which fields are typically important.
		// These are auto-created along with required properties during autocompletion.
		"initKeys": ["importantKey"],
	},
}
```

## Publishing

Submitting schemas directly to Taplo is not possible anymore — all JSON schemas should be submitted to the [JSON Schema Store](https://www.schemastore.org/json/).

Earlier versions used a separate Taplo-specific catalog still available [here](https://taplo.tamasfe.dev/schema_index.json).

### Visual Studio Code extensions

Similarly to `jsonValidation`, extensions can contribute their own schemas via `tomlValidation`. Both `fileMatch` and `regexMatch` (against the entire document URI) are supported:

```json
{
	"contributes": {
		"tomlValidation": [
			{
				"regexMatch": "^.*foo.toml$",
				"url": "https://json.schemastore.org/foo.json"
			}
		]
	}
}
```

## IntelliJ-compatible extensions also honored by Tombi/Taplo IDEs

These appear alongside `x-taplo` in many community schemas:

- `x-intellij-language-injection` — embed-language hints for IntelliJ.
- `x-intellij-html-description` — HTML-formatted description.
- `x-intellij-enum-metadata` — per-enum-value metadata; common shape:

```jsonc
{
	"enum": ["git", "hg"],
	"x-intellij-enum-metadata": {
		"git": { "description": "Use Git." },
		"hg": { "description": "Use Mercurial." },
	},
}
```

This restores per-variant docs for plain `enum` schemas (where stock JSON Schema only allows one description on the enum as a whole).
