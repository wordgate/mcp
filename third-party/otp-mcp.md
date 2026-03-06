# otp-mcp

TOTP/HOTP/SecurID one-time password generation for AI assistants.

- **Repository**: https://github.com/andreax79/otp-mcp
- **License**: MIT
- **Language**: Python (FastMCP)
- **PyPI**: [otp-mcp-server](https://pypi.org/project/otp-mcp-server/)

## Features

- TOTP (time-based) and HOTP (counter-based) code generation
- SecurID token support
- Add / list / delete / query tokens via MCP tools
- Local SQLite token database (path configurable via `OTP_MCP_SERVER_DB` env var)
- Supports stdio, SSE, and HTTP Stream transports

## MCP Tools

| Tool | Description |
|------|-------------|
| `list_otp_tokens` | List all stored OTP tokens |
| `get_details` | Get token details by name or ID |
| `calculate_otp_codes` | Generate OTP code for matching tokens |
| `add_token` | Add a new TOTP/HOTP token (base32 secret) |
| `delete_token` | Delete a token by name or ID |

## Installation

```bash
# Run directly
uvx otp-mcp-server

# Or install
pip install otp-mcp-server
```

## Configuration

### Claude Code

```bash
claude mcp add otp -- uvx otp-mcp-server
```

### Claude Desktop

Edit config file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "otp": {
      "command": "uvx",
      "args": ["otp-mcp-server"]
    }
  }
}
```

### Cursor

Edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "otp": {
      "command": "uvx",
      "args": ["otp-mcp-server"]
    }
  }
}
```

## Why otp-mcp

Evaluated 4 candidates (2026-03):

| Candidate | Verdict |
|-----------|---------|
| **otp-mcp** | Python + FastMCP, self-contained, full CRUD, uvx install. Best fit. |
| firstorderai/authenticator_mcp | Requires proprietary desktop app. Node.js. |
| Stig-Johnny/totp-mcp | Minimal features, plaintext secrets, Node.js. |
| Authn8 | Commercial SaaS, paid plan required. |
