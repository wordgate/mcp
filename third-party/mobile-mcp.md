# mobile-mcp

Mobile device automation for AI assistants — control Android/iOS apps via native accessibility tree, no vision model needed.

- **Repository**: https://github.com/mobile-next/mobile-mcp
- **Maintainer**: Mobile Next
- **License**: Apache 2.0
- **Language**: Node.js
- **npm**: [@mobilenext/mobile-mcp](https://www.npmjs.com/package/@mobilenext/mobile-mcp)

## Features

- Accessibility tree as default interaction mode (low token, no vision model)
- Screenshot fallback only when a11y labels unavailable
- Platform-agnostic: iOS + Android, real devices + emulators/simulators
- App lifecycle management (install, launch, terminate)
- UI interaction (tap, swipe, type, press buttons)

## Supported Platforms

| Platform | Status |
|----------|--------|
| Android real device | Supported |
| Android emulator | Supported |
| iOS real device | Supported |
| iOS simulator | Supported (macOS only) |

## Token Efficiency

Accessibility tree mode returns structured text (~low token cost per interaction). Screenshots are only used as fallback when accessibility data is unavailable. No computer vision model required in a11y mode.

## Prerequisites

- Node.js v22+
- Xcode command-line tools (for iOS)
- Android Platform Tools / ADB (for Android)

## Configuration

### Claude Code

```bash
claude mcp add mobile -- npx -y @mobilenext/mobile-mcp@latest
```

### Claude Desktop

```json
{
  "mcpServers": {
    "mobile": {
      "command": "npx",
      "args": ["-y", "@mobilenext/mobile-mcp@latest"]
    }
  }
}
```

### Cursor

Edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "mobile": {
      "command": "npx",
      "args": ["-y", "@mobilenext/mobile-mcp@latest"]
    }
  }
}
```

## Why mobile-mcp

Evaluated 4 candidates (2026-03):

| Candidate | Verdict |
|-----------|---------|
| **mobile-mcp** | 3.7k stars, a11y-first (low token), full platform coverage. Best fit. |
| ios-simulator-mcp | iOS simulator only, no Android, no real device. |
| mobile-use (Minitap) | Screenshot-first (high token), no iOS real device. |
| MobAI | Requires separate desktop app, small community (46 stars). |
