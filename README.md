# Wordgate MCP Servers

A collection of MCP (Model Context Protocol) servers for AI assistants.

## Servers

### Self-built

| Server | Description |
|--------|-------------|
| [email-mcp](src/email-mcp/) | Email access via himalaya CLI |

### Third-party (recommended)

| Server | Description |
|--------|-------------|
| [otp-mcp](third-party/otp-mcp.md) | TOTP/HOTP one-time password generation |
| [playwright-mcp](third-party/playwright-mcp.md) | Browser automation via Playwright |
| [mobile-mcp](third-party/mobile-mcp.md) | Mobile device automation (iOS/Android) |
| [x-mcp](third-party/x-mcp.md) | Twitter/X posting, search, and engagement |

## Development

This is a [uv workspace](https://docs.astral.sh/uv/concepts/workspaces/) monorepo.

```bash
# Install all workspace deps
uv sync

# Run a specific server locally
uv run --package email-mcp email-mcp

# Build a specific package
cd src/email-mcp && uv build
```

## License

MIT
