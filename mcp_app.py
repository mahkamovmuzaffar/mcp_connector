"""Standalone MCP server exposing the Django `notes` app over MCP.

Run the Django site separately with `manage.py runserver` for the normal
web app; run this file (`python mcp_app.py`) to serve the MCP endpoint on
its own port, using the official MCP Python SDK against Django's ORM.
"""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from mcp.server.fastmcp import FastMCP

from notes.models import Note

mcp = FastMCP("Django Notes MCP")


@mcp.tool()
def list_notes() -> list[dict]:
    """List all notes, most recent first."""
    return [
        {"id": n.id, "title": n.title, "body": n.body, "created_at": n.created_at.isoformat()}
        for n in Note.objects.order_by("-created_at")
    ]


@mcp.tool()
def get_note(note_id: int) -> dict:
    """Fetch a single note by id."""
    n = Note.objects.get(id=note_id)
    return {"id": n.id, "title": n.title, "body": n.body, "created_at": n.created_at.isoformat()}


@mcp.tool()
def create_note(title: str, body: str = "") -> dict:
    """Create a new note and return it."""
    n = Note.objects.create(title=title, body=body)
    return {"id": n.id, "title": n.title, "body": n.body, "created_at": n.created_at.isoformat()}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
