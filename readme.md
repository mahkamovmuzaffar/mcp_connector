# mcp_connector

Django project (`core`) with a `notes` app, plus a standalone MCP server
(`mcp_app.py`) that exposes the `notes` app over the
[Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)
using the official [Python MCP SDK](https://py.sdk.modelcontextprotocol.io/).

The MCP server runs as its own process, separate from the Django dev
server, and talks to the same Django app via the ORM (wrapped in
`sync_to_async` since Django's ORM is sync-only and FastMCP tools run in
an async context).

## Setup

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip django mcp
.\.venv\Scripts\python.exe manage.py migrate
```

## Running

Django site (admin, etc.) on port 8000:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

MCP server (streamable-http transport) on port 8000 by default — run on a
different port if running both at once, e.g. `mcp.run(transport="streamable-http", port=8001)`:

```powershell
.\.venv\Scripts\python.exe mcp_app.py
```

The MCP endpoint is served at `http://127.0.0.1:8000/mcp`.

## Tools exposed

- `list_notes()` — list all notes, most recent first
- `get_note(note_id)` — fetch a single note
- `create_note(title, body="")` — create a note

## Project layout

- `core/` — Django project settings/urls
- `notes/` — Django app with the `Note` model
- `mcp_app.py` — standalone MCP server (official SDK, `FastMCP`)
