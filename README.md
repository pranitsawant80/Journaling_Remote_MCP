# Journal Tracker MCP Server

A Model Context Protocol (MCP) server built with FastMCP that allows users to maintain a daily journal, record diary entries, track moods and day ratings, and generate summaries from their journal history.

## Features

* Create daily journal entries
* Update existing entries
* Delete entries
* Retrieve entries by ID
* List entries within a date range
* Track mood and day ratings
* Summarize journal activity
* Analyze mood trends
* Generate data for AI-powered reflections and summaries

---

# Prerequisites

* Python 3.8+
* UV Package Manager
* Claude Desktop

---

# Install UV

## Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Or
```powershell
pip install uv
```

## macOS/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify installation:

```bash
uv --version
```

---

# Clone or Create Project

Create a new project directory:

```bash
mkdir journal_tracker_server
cd journal_tracker_server
```

---

# Initialize Project

Create a UV project:

```bash
uv init
```

This creates:

```text
journal_tracker_server/
├── pyproject.toml
├── README.md
└── src/
```

---

# Configure pyproject.toml

Give description if any:

```toml
[project]
name = "journal_tracker_server"
version = "0.1.0"
description = "An MCP server that helps users maintain a daily journal, record thoughts, track moods and day ratings, and generate summaries and insights from journal entries."
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastmcp>=3.4.2"
]
```
(Note: when we install dependencies those will be automatically updated here. No need to update manually)

---

# Install Dependencies

```bash
uv sync
```
(Note: UV automatically manages the virtual environment. You do not need to manually activate `.venv` when using `uv run`)

```bash
uv add fastmcp
```

---

# Project Structure

```text
journal_tracker_server/
│
├── journal.py
├── journal.db
├── pyproject.toml
├── README.md
└── .venv/
```

Where:

* `journal.py` contains the MCP server code
* `journal.db` is automatically created by SQLite
* `.venv` contains project dependencies

---

# Run MCP Server Locally

From the project root:

```bash
uv run journal.py
```

You should see the MCP server start successfully.

---

# Test MCP Inspector (Optional)

Install MCP Inspector:

```bash
npx @modelcontextprotocol/inspector
```

Run:

```bash
uv run journal.py
npx @modelcontextprotocol/inspector 
```

This opens a browser interface where you can test tools.

---

# Configure Claude Desktop

Locate Claude Desktop configuration file.

## Windows

```text
%APPDATA%\Claude\claude_desktop_config.json
```
(Note: To locate the configuration file path, open Claude Desktop and navigate to:
Profile → Settings → Developer → Edit Config)
## macOS

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

---

# Example Configuration

Replace paths with your actual project location.

```json
{
  "mcpServers": {
    "journal-tracker": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\YourName\\journal_tracker_server",
        "run",
        "journal.py"
      ]
    }
  }
}
```

Example for macOS/Linux:

```json
{
  "mcpServers": {
    "journal-tracker": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/yourname/journal_tracker_server",
        "run",
        "journal.py"
      ]
    }
  }
}
```

---

# Restart Claude Desktop

After updating the configuration:

1. Close Claude Desktop
2. Reopen Claude Desktop
3. Open a new chat

Claude should automatically detect the Journal Tracker MCP server.

---

# Available Tools

## add_entry

Create a journal entry.

Example:

```text
Add a journal entry for today.
Title: Productive Day
Mood: Happy
Rating: Good
Content: Completed my MCP server project.
```

---

## list_entries

List journal entries between dates.

Example:

```text
Show my journal entries from 2026-06-01 to 2026-06-30.
```

---

## get_entry

Retrieve a journal entry by ID.

Example:

```text
Get journal entry 5.
```

---

## update_entry

Update an existing journal entry.

Example:

```text
Update entry 5 and change mood to Excited.
```

---

## delete_entry

Delete a journal entry.

Example:

```text
Delete journal entry 5.
```

---

## summarize_days

Summarize entries by rating.

Example:

```text
How many Good, Average, and Bad days did I have this month?
```

---

## summarize_moods

Analyze mood trends.

Example:

```text
Show mood statistics for June 2026.
```

---

## get_entries_for_summary

Retrieve entries for AI-generated summaries.

Example:

```text
Summarize my journal entries from the last 30 days.
```

---

# Recommended Day Ratings

Use one of:

```text
Excellent
Good
Average
Bad
Terrible
```

Or a numeric scale:

```text
5 = Excellent
4 = Good
3 = Average
2 = Bad
1 = Terrible
```

---

# Database

The server automatically creates:

```text
journal.db
```

with a table:

```sql
journal_entries
```

containing:

```text
id
entry_date
title
content
day_rating
mood
tags
created_at
```

---

# Example Journal Entry

```text
Date: 2026-06-11
Title: Learning MCP
Mood: Motivated
Rating: Good

Today I completed my first FastMCP journaling server and successfully integrated it with Claude Desktop.
```

---

# Troubleshooting

## Verify UV

```bash
uv --version
```

## Verify FastMCP

```bash
uv pip list
```

## Run Server Directly

```bash
uv run main.py
```

## Check Claude Desktop Logs

If Claude cannot connect, verify:

* Project path is correct
* UV is installed
* Dependencies are installed
* JSON configuration is valid
* Claude Desktop has been restarted

---

# License

MIT License 
 