# email-mcp

MCP server that gives AI assistants email access via the [himalaya](https://github.com/pimalaya/himalaya) CLI.

## Prerequisites

Install the himalaya CLI:

```bash
# macOS
brew install himalaya

# Other platforms: https://github.com/pimalaya/himalaya/releases
```

## Installation

### Claude Desktop

Edit config file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "email": {
      "command": "uvx",
      "args": ["email-mcp"]
    }
  }
}
```

### Claude Code

```bash
claude mcp add email -- uvx email-mcp
```

### Cursor

Edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "email": {
      "command": "uvx",
      "args": ["email-mcp"]
    }
  }
}
```

### Windsurf

Edit `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "email": {
      "command": "uvx",
      "args": ["email-mcp"]
    }
  }
}
```

### VS Code (GitHub Copilot)

Edit `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "email": {
      "type": "stdio",
      "command": "uvx",
      "args": ["email-mcp"]
    }
  }
}
```

### Cline (VS Code Extension)

Open Cline MCP settings (`cline_mcp_settings.json`):

```json
{
  "mcpServers": {
    "email": {
      "command": "uvx",
      "args": ["email-mcp"],
      "disabled": false
    }
  }
}
```

### Cherry Studio

1. Go to **Settings > MCP Servers > Add Server**
2. Fill in:
   - **Name**: `email`
   - **Type**: `STDIO`
   - **Command**: `uvx`
   - **Arguments**: `email-mcp`
3. Click **Save**

## Tools

| Tool | Description |
|------|-------------|
| `email_add_account` | Add an email account (gmail, qq, 163, outlook, yahoo, icloud, custom) |
| `email_list_accounts` | List configured accounts |
| `email_list_folders` | List mailbox folders |
| `email_list_envelopes` | List/search emails with filtering |
| `email_read_message` | Read full email content |
| `email_send_message` | Send a new email |
| `email_reply_message` | Reply to an email |
| `email_mark_read` | Mark emails as read |

## Supported Providers

Built-in presets for: **Gmail**, **QQ Mail**, **163 Mail**, **Outlook**, **Yahoo**, **iCloud**.

Custom IMAP/SMTP servers are also supported via the `custom` provider type.

## Usage

Once configured, ask your AI assistant to:

- "List my emails"
- "Read the latest email from John"
- "Send an email to alice@example.com about the meeting"
- "Search for emails with subject 'invoice'"
- "Reply to the last email"

On first use, the assistant will help you set up an account using the `email_add_account` tool.

## License

MIT
