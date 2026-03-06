# mac-use-mcp

macOS desktop automation for AI assistants — screenshot, click, type, window management, accessibility inspection, clipboard, and menu bar control.

- **Repository**: https://github.com/antbotlab/mac-use-mcp
- **License**: MIT
- **Language**: Node.js + Swift
- **macOS**: 13+ (Intel and Apple Silicon)

## Features

- 18 MCP tools for full desktop control
- Hybrid mode: screenshots (vision) + accessibility tree (structured text, low token)
- Zero native dependencies, pre-compiled Swift binaries ship with npm
- Unicode/CJK/emoji text input
- Menu bar navigation (`click_menu "File > Save As"`)
- Clipboard read/write
- Multi-display support

## MCP Tools (18)

| Category | Tools |
|----------|-------|
| Screen | `screenshot`, `get_screen_info` |
| Input | `click`, `move_mouse`, `scroll`, `drag`, `type_text`, `press_key` |
| Window | `list_windows`, `focus_window`, `open_application`, `click_menu` |
| Accessibility | `get_ui_elements` |
| Clipboard | `clipboard_read`, `clipboard_write` |
| Utility | `wait`, `check_permissions`, `get_cursor_position` |

## Token Efficiency

Two interaction modes:

| Mode | Method | Token cost |
|------|--------|-----------|
| **Accessibility tree** | `get_ui_elements` returns structured text | Low |
| **Screenshot** | `screenshot` + AI vision analysis | High (vision tokens) |

Use accessibility tree when possible; fall back to screenshots for visual-only content.

## Prerequisites

macOS permissions required (System Settings > Privacy & Security):
1. **Accessibility** — for mouse/keyboard control
2. **Screen Recording** — for screenshots

## Configuration

### Claude Code

```bash
claude mcp add mac-use -- npx mac-use-mcp
```

### Claude Desktop

```json
{
  "mcpServers": {
    "mac-use": {
      "command": "npx",
      "args": ["mac-use-mcp"]
    }
  }
}
```

### Cursor

Edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "mac-use": {
      "command": "npx",
      "args": ["mac-use-mcp"]
    }
  }
}
```

## Known Limitations

- Screen Recording permission prompts recur monthly on macOS Sequoia
- Secure input fields (passwords) block synthetic keyboard events
- System dialogs unreachable due to macOS security
- Headless/CI environments not supported

## Why mac-use-mcp

Evaluated 3 candidates (2026-03):

| Candidate | Verdict |
|-----------|---------|
| **mac-use-mcp** | 18 tools, npx install, hybrid a11y+screenshot, CJK support, menu bar control. Most complete. |
| automation-mcp | 377 stars, but screenshot-only (high token), needs Bun runtime, no a11y tree. |
| mcp-server-macos-use | A11y-first (low token), but only 5 tools, requires manual Swift compilation. |
