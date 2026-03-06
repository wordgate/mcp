# x-mcp

Twitter/X automation for AI assistants — post, search, read timeline, reply, engage, and upload media via official API v2.

- **Repository**: https://github.com/Infatoshi/x-mcp
- **License**: MIT
- **Language**: TypeScript
- **API**: X API v2 (OAuth 1.0a)

## Features

- Full tweet lifecycle: post, reply, quote, delete
- Search tweets, read timeline, get mentions
- User info, followers, following
- Like and retweet
- Media upload (images)
- Analytics / metrics

## MCP Tools

| Tool | Description |
|------|-------------|
| `post_tweet` | Post a new tweet |
| `reply_to_tweet` | Reply to a specific tweet |
| `quote_tweet` | Quote tweet |
| `delete_tweet` | Delete a tweet |
| `get_tweet` | Read a specific tweet |
| `search_tweets` | Search tweets by query |
| `get_timeline` | Read home timeline |
| `get_mentions` | Get mentions of your account |
| `get_user` | Get user profile info |
| `get_followers` | List followers |
| `get_following` | List following |
| `like_tweet` | Like a tweet |
| `retweet` | Retweet |
| `upload_media` | Upload image for tweet |

## Prerequisites

1. X Developer Account at https://developer.x.com
2. Create an App in Developer Portal
3. Enable "Read and write" permissions
4. Generate all 5 keys/tokens

## API Pricing

| Tier | Price | Post/month | Read/month | Search |
|------|-------|-----------|-----------|--------|
| Free | $0 | 1,500 | 0 | No |
| Basic | $200/mo | 50,000 | 15,000 | Yes |
| Pro | $5,000/mo | 300,000 | 1,000,000 | Yes |

**Note:** Free tier is write-only (no read/search). "Browse + reply" workflow requires Basic tier ($200/mo) minimum.

## Configuration

### Environment Variables

```
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret
X_BEARER_TOKEN=your_bearer_token
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
```

### Claude Code

```bash
claude mcp add x-mcp -- node /path/to/x-mcp/build/index.js
```

### Claude Desktop

```json
{
  "mcpServers": {
    "x": {
      "command": "node",
      "args": ["/path/to/x-mcp/build/index.js"],
      "env": {
        "X_API_KEY": "your_api_key",
        "X_API_SECRET": "your_api_secret",
        "X_BEARER_TOKEN": "your_bearer_token",
        "X_ACCESS_TOKEN": "your_access_token",
        "X_ACCESS_TOKEN_SECRET": "your_access_token_secret"
      }
    }
  }
}
```

## Safe Usage Guidelines

- 2-5 tweets/day is normal, 30+/day raises flags
- Automated follow/unfollow is banned (even via API)
- Automated bulk liking/retweeting is banned
- Personalized replies are fine; template spam is not
- Add random delays between actions

## Why x-mcp

Evaluated 3 candidates (2026-03):

| Candidate | Verdict |
|-----------|---------|
| **x-mcp** | 14 tools, full read+write+engage coverage, only option with timeline/mentions/reply chain. Best fit. |
| twitter-mcp (EnesCinr) | 367 stars but only 2 tools (post + search), no reply capability. |
| x-mcp-server (mbelinky) | OAuth 2.0 + rate limiting, but only 3 tools, no timeline/mentions. |
