"""Standalone MCP server exposing the Django `notes` app over MCP.

Run the Django site separately with `manage.py runserver` for the normal
web app; run this file (`python mcp_app.py`) to serve the MCP endpoint on
its own port, using the official MCP Python SDK against Django's ORM.
"""

import os

import django

# Must run before importing anything that touches Django models (e.g. notes.models) —
# app registry isn't populated until django.setup() completes.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from asgiref.sync import sync_to_async
from mcp.server.fastmcp import FastMCP

from notes.models import Note

mcp = FastMCP("Django Notes MCP", port=8001)


def _serialize(n: Note) -> dict:
    return {"id": n.id, "title": n.title, "body": n.body, "created_at": n.created_at.isoformat()}


@mcp.tool()
async def list_notes() -> list[dict]:
    """List all notes, most recent first."""
    # FastMCP tools run on the asyncio event loop, but Django's ORM is sync-only;
    # sync_to_async hops to a worker thread so the ORM call doesn't block the loop.
    notes = await sync_to_async(list)(Note.objects.order_by("-created_at"))
    return [_serialize(n) for n in notes]


@mcp.tool()
async def get_note(note_id: int) -> dict:
    """Fetch a single note by id."""
    n = await sync_to_async(Note.objects.get)(id=note_id)
    return _serialize(n)


@mcp.tool()
async def create_note(title: str, body: str = "") -> dict:
    """Create a new note and return it."""
    n = await sync_to_async(Note.objects.create)(title=title, body=body)
    return _serialize(n)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
