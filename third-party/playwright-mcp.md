# playwright-mcp

Browser automation for AI assistants — navigate, click, fill forms, take screenshots, and generate reusable test scripts.

- **Repository**: https://github.com/microsoft/playwright-mcp
- **Maintainer**: Microsoft (official)
- **License**: Apache 2.0
- **Language**: Node.js
- **npm**: [@playwright/mcp](https://www.npmjs.com/package/@playwright/mcp)

## Features

- Accessibility tree based (no vision model needed, structured data)
- Supports Chromium, Firefox, WebKit (use `--browser chrome` for Chrome)
- Persistent browser profiles or isolated sessions
- Code generation: outputs TypeScript/Python scripts from AI operations, reusable as automated tests
- stdio / SSE / Browser Extension transports

## Configuration

### Claude Code

```bash
claude mcp add playwright -- npx @playwright/mcp@latest --browser chrome
```

### Claude Desktop

Edit config file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--browser", "chrome"]
    }
  }
}
```

### Cursor

Edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--browser", "chrome"]
    }
  }
}
```

## Token Efficiency Note

Playwright MCP returns the full accessibility tree on each action (~32k tokens/task). For token-sensitive scenarios, consider batching operations. Despite higher token cost than code-execution approaches, accessibility tree provides the most reliable element targeting.

## Why Playwright MCP

Evaluated 3 candidates (2026-03):

| Candidate | Verdict |
|-----------|---------|
| **Playwright MCP** | Microsoft official, 28k+ stars, most mature ecosystem, code generation capability. Best fit. |
| Chrome DevTools MCP | Google official, strong on debugging/performance, but heavier on tokens (6x) and Chrome-only without added benefit. |
| OpenBrowser | 6x more token efficient, but 168 stars, personal project, too young for production use. |
