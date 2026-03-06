# Wordgate MCP Servers

Python monorepo of MCP servers for AI assistants. Mix of self-built and curated third-party.

## Structure

```
src/
  email-mcp/            # Self-built: email access via himalaya CLI
third-party/
  otp-mcp.md            # Third-party: TOTP/HOTP (docs + config only)
```

## Development

- **Runtime**: Python >=3.11
- **Package manager**: uv workspace
- **Build system**: hatchling with src/ layout

```bash
uv sync                                    # Install all deps
uv run --package email-mcp email-mcp       # Run locally
cd src/email-mcp && uv build               # Build package
```

## Conventions

- Package names: `<name>-mcp` (hyphenated)
- Module names: `<name>_mcp` (underscored)
- Entry point: `<name>-mcp = "<name>_mcp.server:mcp.run"`
- Server variable: `mcp = FastMCP("<name>_mcp")`
- Transport: stdio
- Tool annotations: always set readOnlyHint, destructiveHint, etc.
- External CLI calls: use `create_subprocess_exec` (not shell) to avoid injection

## Third-party policy

Third-party MCP servers are documented in `third-party/{name}.md` (install, config, selection rationale). No code vendored — docs and config references only.
