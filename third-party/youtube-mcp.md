# youtube-mcp

YouTube channel management for AI assistants — search, comment, reply, upload, analytics, transcripts via official API v3.

- **Repository**: https://github.com/pauling-ai/youtube-mcp-server
- **License**: MIT
- **Language**: Python (FastMCP)
- **API**: YouTube Data API v3 + Analytics API + Reporting API (OAuth 2.0)

## Features

- 40 MCP tools covering full YouTube workflow
- Search videos, trending, suggestions
- Read and post comments, reply to comments
- Upload/update/delete videos, set thumbnails
- Channel analytics, audience insights, revenue reporting
- Transcript extraction
- Playlist management
- Bulk reporting

## MCP Tools (40 total)

| Category | Tools |
|----------|-------|
| Auth | `youtube_auth`, `youtube_auth_status` |
| Channel & Video | `youtube_get_channel`, `youtube_list_videos`, `youtube_get_video` |
| Search & SEO | `youtube_search`, `youtube_search_suggestions`, `youtube_trending`, `youtube_get_categories` |
| Transcripts | `youtube_get_transcript`, `youtube_list_captions` |
| Analytics | `youtube_analytics_overview`, `youtube_analytics_top_videos`, `youtube_analytics_top_shorts`, `youtube_analytics_video_detail`, `youtube_analytics_traffic_sources`, `youtube_analytics_demographics`, `youtube_analytics_geography`, `youtube_analytics_daily`, `youtube_analytics_day_of_week`, `youtube_analytics_content_type_breakdown`, `youtube_analytics_revenue`, `youtube_analytics_revenue_by_video`, `youtube_analytics_retention` |
| Publishing | `youtube_upload_video`, `youtube_update_video`, `youtube_set_thumbnail`, `youtube_delete_video` |
| Playlists | `youtube_list_playlists`, `youtube_create_playlist`, `youtube_add_to_playlist`, `youtube_remove_from_playlist` |
| Comments | `youtube_list_comments`, `youtube_post_comment`, `youtube_reply_to_comment` |
| Bulk Reporting | `youtube_reporting_list_types`, `youtube_reporting_create_job`, `youtube_reporting_list_jobs`, `youtube_reporting_list_reports`, `youtube_reporting_download` |

## API Quota (Free)

Default: 10,000 units/day (free, no payment required).

| Operation | Cost | Daily capacity |
|-----------|------|---------------|
| Search videos | 100 units | ~100 |
| Read video/comment | 1 unit | ~10,000 |
| Post/reply comment | 50 units | ~200 |
| Upload video | 1,600 units | ~6 |

Quota resets at midnight Pacific Time. Can apply for increases (free) via Google Cloud Console.

## Prerequisites

1. Google Cloud project with YouTube Data API v3 enabled
2. OAuth 2.0 credentials (Desktop app type)
3. Save `client_secret.json` to `~/.youtube-mcp/`
4. First run triggers browser login, token auto-refreshes

## Configuration

### Claude Code

```bash
claude mcp add youtube -- uvx youtube-mcp-server
```

### Claude Desktop

```json
{
  "mcpServers": {
    "youtube": {
      "command": "uvx",
      "args": ["youtube-mcp-server"]
    }
  }
}
```

### Cursor

Edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "youtube": {
      "command": "uvx",
      "args": ["youtube-mcp-server"]
    }
  }
}
```

## Why youtube-mcp-server

Evaluated multiple candidates (2026-03):

| Candidate | Verdict |
|-----------|---------|
| **pauling-ai/youtube-mcp-server** | Python + FastMCP (matches our stack), 40 tools, full API coverage, OAuth 2.0, free quota. Best fit. |
| IA-Programming/Youtube-MCP | No official API, scraping-based, limited tools. |
| ShawhinT/yt-mcp-agent | Transcript-focused only, not full channel management. |
| ZubeidHendricks/youtube-mcp-server | Broad but less documented. |
