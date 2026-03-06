"""Thin wrapper around the himalaya CLI."""

import asyncio
import json
import shutil
from typing import Any


def _find_himalaya() -> str:
    path = shutil.which("himalaya")
    if not path:
        raise RuntimeError(
            "himalaya CLI not found in PATH. Install it: brew install himalaya"
        )
    return path


async def run_himalaya(
    *args: str,
    stdin_data: str | None = None,
    json_output: bool = True,
) -> Any:
    """Run a himalaya command and return parsed output.

    Uses create_subprocess_exec (not shell) to avoid command injection.

    Args:
        *args: Command arguments (e.g. "envelope", "list", "-f", "INBOX")
        stdin_data: Optional data to pipe via stdin
        json_output: If True, add --output json and parse the result

    Returns:
        Parsed JSON (if json_output) or raw stdout string
    """
    cmd = [_find_himalaya(), "--quiet"]
    if json_output:
        cmd.extend(["--output", "json"])
    cmd.extend(args)

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE if stdin_data else None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout_bytes, stderr_bytes = await proc.communicate(
        stdin_data.encode() if stdin_data else None
    )

    stdout = stdout_bytes.decode().strip()
    stderr = stderr_bytes.decode().strip()

    if proc.returncode != 0:
        msg = stderr or stdout or f"himalaya exited with code {proc.returncode}"
        raise RuntimeError(f"himalaya error: {msg}")

    if not json_output:
        return stdout

    if not stdout:
        return []

    return json.loads(stdout)
