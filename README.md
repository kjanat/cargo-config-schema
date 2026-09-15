# Cargo configuration schema

JSON Schema for `.cargo/config.toml` and `.cargo/config`, covering stable and
explicitly labelled unstable Cargo settings.

## Use

```toml
#:schema https://raw.githubusercontent.com/kjanat/cargo-config-schema/master/cargo-config.json
```

Tombi orders known fields using deliberate schema property order.
Dynamic maps such as aliases sort alphabetically.
Nested settings keep related fields together: TLS `min` before `max`, environment
`value` before `force` and `relative`. Command arguments, compiler flags, includes
and credential-provider chains retain their order.

Cargo configuration files can inherit values; partial configurations
are supported. Runtime-dependent behavior is not fully expressible in JSON Schema.

For changes and development instructions, see [Contributing](CONTRIBUTING.md).

The source audit targets Cargo commit
[`cc5596f`](https://github.com/rust-lang/cargo/tree/cc5596f058e623d22be718adf541a9bd766d9417).
