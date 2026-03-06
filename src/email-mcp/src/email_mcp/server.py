"""himalaya MCP server — email access for AI assistants."""

import os
from pathlib import Path
from typing import Optional

import tomlkit
from mcp.server.fastmcp import FastMCP

from .cli import run_himalaya

mcp = FastMCP("himalaya_mcp")

# --- Provider presets ---

PROVIDER_PRESETS: dict[str, dict] = {
    "gmail": {
        "imap": {"host": "imap.gmail.com", "port": 993},
        "smtp": {"host": "smtp.gmail.com", "port": 465},
    },
    "qq": {
        "imap": {"host": "imap.qq.com", "port": 993},
        "smtp": {"host": "smtp.qq.com", "port": 465},
    },
    "163": {
        "imap": {"host": "imap.163.com", "port": 993},
        "smtp": {"host": "smtp.163.com", "port": 465},
    },
    "outlook": {
        "imap": {"host": "outlook.office365.com", "port": 993},
        "smtp": {"host": "smtp.office365.com", "port": 587},
    },
    "yahoo": {
        "imap": {"host": "imap.mail.yahoo.com", "port": 993},
        "smtp": {"host": "smtp.mail.yahoo.com", "port": 465},
    },
    "icloud": {
        "imap": {"host": "imap.mail.me.com", "port": 993},
        "smtp": {"host": "smtp.mail.me.com", "port": 587},
    },
}

HIMALAYA_CONFIG = Path(
    os.environ.get("HIMALAYA_CONFIG", Path.home() / ".config" / "himalaya" / "config.toml")
)


def _account_args(account: Optional[str]) -> list[str]:
    return ["-a", account] if account else []


def _folder_args(folder: Optional[str]) -> list[str]:
    return ["-f", folder] if folder else []


# ============================================================
# Setup
# ============================================================


@mcp.tool(
    name="email_add_account",
    annotations={
        "title": "Add Email Account",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def email_add_account(
    provider: str,
    email: str,
    password: str,
    display_name: Optional[str] = None,
    imap_host: Optional[str] = None,
    imap_port: Optional[int] = None,
    smtp_host: Optional[str] = None,
    smtp_port: Optional[int] = None,
) -> str:
    """Add an email account to himalaya configuration.

    Supports providers: gmail, qq, 163, outlook, yahoo, icloud, custom.
    For custom provider, imap_host and smtp_host are required.
    After writing config, runs connectivity check.

    Args:
        provider: Email provider (gmail, qq, 163, outlook, yahoo, icloud, custom)
        email: Full email address
        password: Password or app-specific authorization code
        display_name: Sender display name (defaults to email)
        imap_host: Override IMAP host (required for custom)
        imap_port: Override IMAP port (default 993)
        smtp_host: Override SMTP host (required for custom)
        smtp_port: Override SMTP port (default 465)
    """
    provider = provider.lower()

    if provider == "custom":
        if not imap_host or not smtp_host:
            return "Error: imap_host and smtp_host are required for custom provider."
    elif provider not in PROVIDER_PRESETS:
        return f"Error: Unknown provider '{provider}'. Use: {', '.join(PROVIDER_PRESETS)} or custom."

    # Resolve host/port
    preset = PROVIDER_PRESETS.get(provider, {})
    imap_h = imap_host or preset.get("imap", {}).get("host", "")
    imap_p = imap_port or preset.get("imap", {}).get("port", 993)
    smtp_h = smtp_host or preset.get("smtp", {}).get("host", "")
    smtp_p = smtp_port or preset.get("smtp", {}).get("port", 465)

    # Derive account name from email local part + domain
    local, domain = email.split("@")
    account_name = f"{local}-{domain.split('.')[0]}"

    # Load or create config
    HIMALAYA_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    if HIMALAYA_CONFIG.exists():
        doc = tomlkit.parse(HIMALAYA_CONFIG.read_text())
    else:
        doc = tomlkit.document()

    if "accounts" not in doc:
        doc["accounts"] = tomlkit.table(is_super_table=True)

    # Check if first account (make it default)
    is_first = len(doc["accounts"]) == 0

    # Build account table
    acct = tomlkit.table()
    if is_first:
        acct["default"] = True
    acct["email"] = email
    acct["display-name"] = display_name or email

    # IMAP section
    imap = tomlkit.table()
    imap["host"] = imap_h
    imap["port"] = imap_p
    imap["encryption"] = "tls"
    login = tomlkit.table()
    login["type"] = "password"
    login["raw"] = password
    imap["login"] = login
    acct["imap"] = imap

    # SMTP section
    smtp = tomlkit.table()
    smtp["host"] = smtp_h
    smtp["port"] = smtp_p
    smtp["encryption"] = "ssl" if smtp_p == 465 else "starttls"
    smtp_login = tomlkit.table()
    smtp_login["type"] = "password"
    smtp_login["raw"] = password
    smtp["login"] = smtp_login
    acct["smtp"] = smtp

    doc["accounts"][account_name] = acct
    HIMALAYA_CONFIG.write_text(tomlkit.dumps(doc))

    # Verify connectivity
    try:
        result = await run_himalaya("account", "doctor", "-a", account_name, json_output=False)
        return f"Account '{account_name}' added and verified.\n\n{result}"
    except RuntimeError as e:
        return f"Account '{account_name}' added to config but connectivity check failed:\n{e}\n\nConfig written to {HIMALAYA_CONFIG}. You may need to adjust settings."


# ============================================================
# Reading
# ============================================================


@mcp.tool(
    name="email_list_accounts",
    annotations={
        "title": "List Email Accounts",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def email_list_accounts() -> str:
    """List all configured email accounts."""
    result = await run_himalaya("account", "list")
    return _format_json(result)


@mcp.tool(
    name="email_list_folders",
    annotations={
        "title": "List Email Folders",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def email_list_folders(account: Optional[str] = None) -> str:
    """List all folders (mailboxes) for an email account.

    Args:
        account: Account name. Omit to use default account.
    """
    result = await run_himalaya("folder", "list", *_account_args(account))
    return _format_json(result)


@mcp.tool(
    name="email_list_envelopes",
    annotations={
        "title": "List/Search Emails",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def email_list_envelopes(
    account: Optional[str] = None,
    folder: Optional[str] = None,
    query: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> str:
    """List and search email envelopes (headers only — token efficient).

    Returns: id, from, to, subject, date, flags for each message.

    Supports himalaya filter queries:
    - from <pattern>: filter by sender
    - subject <pattern>: filter by subject
    - body <pattern>: filter by body content
    - flag <flag>: filter by flag (seen, answered, flagged, deleted, draft)
    - before/after <yyyy-mm-dd>: filter by date
    - Combine with: and, or, not
    - Example: "from john and subject invoice and not flag seen"

    Args:
        account: Account name. Omit to use default.
        folder: Folder name. Defaults to INBOX.
        query: Search/filter query string.
        page: Page number (starts at 1).
        page_size: Number of results per page.
    """
    args = [
        "envelope", "list",
        *_account_args(account),
        *_folder_args(folder),
        "-p", str(page),
        "-s", str(page_size),
    ]
    if query:
        args.extend(query.split())

    result = await run_himalaya(*args)
    return _format_json(result)


@mcp.tool(
    name="email_read_message",
    annotations={
        "title": "Read Email Message",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def email_read_message(
    id: str,
    account: Optional[str] = None,
    folder: Optional[str] = None,
    mark_read: bool = False,
) -> str:
    """Read the full content of a specific email message.

    Args:
        id: Envelope ID (from email_list_envelopes).
        account: Account name. Omit to use default.
        folder: Folder name. Defaults to INBOX.
        mark_read: If false (default), reads without marking as seen.
    """
    args = [
        "message", "read",
        *_account_args(account),
        *_folder_args(folder),
    ]
    if not mark_read:
        args.append("--preview")
    args.append(id)

    result = await run_himalaya(*args, json_output=False)
    return result


# ============================================================
# Sending
# ============================================================


@mcp.tool(
    name="email_send_message",
    annotations={
        "title": "Send Email",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def email_send_message(
    to: str,
    subject: str,
    body: str,
    account: Optional[str] = None,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
) -> str:
    """Send a new email message.

    Args:
        to: Recipient(s), comma-separated.
        subject: Email subject line.
        body: Plain text email body.
        account: Account name. Omit to use default.
        cc: CC recipient(s), comma-separated.
        bcc: BCC recipient(s), comma-separated.
    """
    # Build MML template
    headers = [f"To: {to}", f"Subject: {subject}"]
    if cc:
        headers.append(f"Cc: {cc}")
    if bcc:
        headers.append(f"Bcc: {bcc}")
    template = "\n".join(headers) + "\n\n" + body

    result = await run_himalaya(
        "template", "send",
        *_account_args(account),
        stdin_data=template,
        json_output=False,
    )
    return result or "Message sent successfully."


@mcp.tool(
    name="email_reply_message",
    annotations={
        "title": "Reply to Email",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def email_reply_message(
    id: str,
    body: str,
    account: Optional[str] = None,
    folder: Optional[str] = None,
    reply_all: bool = False,
) -> str:
    """Reply to an email message.

    Generates a reply template from the original message, injects your reply body, and sends.

    Args:
        id: Envelope ID of the message to reply to.
        body: Your reply text.
        account: Account name. Omit to use default.
        folder: Folder name. Defaults to INBOX.
        reply_all: If true, reply to all recipients.
    """
    # Generate reply template
    reply_args = [
        "template", "reply",
        *_account_args(account),
        *_folder_args(folder),
    ]
    if reply_all:
        reply_args.append("--all")
    reply_args.append(id)

    template = await run_himalaya(*reply_args, json_output=False)

    # Inject body: replace everything after the blank line (headers separator)
    # Template format: headers\n\n> quoted original
    parts = template.split("\n\n", 1)
    headers = parts[0]
    quoted = parts[1] if len(parts) > 1 else ""
    final_template = f"{headers}\n\n{body}\n\n{quoted}"

    # Send
    result = await run_himalaya(
        "template", "send",
        *_account_args(account),
        stdin_data=final_template,
        json_output=False,
    )
    return result or "Reply sent successfully."


# ============================================================
# Management
# ============================================================


@mcp.tool(
    name="email_mark_read",
    annotations={
        "title": "Mark Email as Read",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def email_mark_read(
    id: str,
    account: Optional[str] = None,
    folder: Optional[str] = None,
) -> str:
    """Mark one or more email messages as read (adds 'seen' flag).

    Args:
        id: Envelope ID(s) to mark as read. Space-separated for multiple.
        account: Account name. Omit to use default.
        folder: Folder name. Defaults to INBOX.
    """
    args = [
        "flag", "add",
        *_account_args(account),
        *_folder_args(folder),
    ]
    args.extend(id.split())
    args.append("seen")

    await run_himalaya(*args, json_output=False)
    return f"Message(s) {id} marked as read."


# ============================================================
# Helpers
# ============================================================


def _format_json(data) -> str:
    """Format JSON data as compact string for token efficiency."""
    import json
    return json.dumps(data, ensure_ascii=False, indent=2)


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    mcp.run(transport="stdio")
