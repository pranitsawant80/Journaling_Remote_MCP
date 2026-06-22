from fastmcp import FastMCP
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "journal.db")
DAY_RATINGS_CONFIG_PATH= os.path.join(os.path.dirname(__file__), "day_ratings.json")
MOODS_CONFIG_PATH= os.path.join(os.path.dirname(__file__), "moods.json")

mcp = FastMCP("JournalTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("CREATE TABLE IF NOT EXISTS journal_entries (id INTEGER PRIMARY KEY AUTOINCREMENT, entry_date TEXT NOT NULL, title TEXT DEFAULT '', content TEXT NOT NULL, day_rating TEXT NOT NULL, mood TEXT DEFAULT '', tags TEXT DEFAULT '', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

init_db()

@mcp.tool()
def add_entry(entry_date, content, day_rating, title="", mood="", tags=""):
    '''Add a new journal entry.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO journal_entries (entry_date, title, content, day_rating, mood, tags) VALUES (?, ?, ?, ?, ?, ?)",
            (entry_date, title, content, day_rating, mood, tags)
        )

        return {
            "status": "ok",
            "id": cur.lastrowid
        }

@mcp.tool()
def list_entries(start_date, end_date):
    '''List journal entries within a date range.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "SELECT id, entry_date, title, content, day_rating, mood, tags, created_at FROM journal_entries WHERE entry_date BETWEEN ? AND ? ORDER BY entry_date ASC",
            (start_date, end_date)
        )

        cols = [d[0] for d in cur.description]

        return [dict(zip(cols, row)) for row in cur.fetchall()]

@mcp.tool()
def get_entry(entry_id):
    '''Get a journal entry by ID.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "SELECT id, entry_date, title, content, day_rating, mood, tags, created_at FROM journal_entries WHERE id = ?",
            (entry_id,)
        )

        row = cur.fetchone()

        if not row:
            return None

        cols = [d[0] for d in cur.description]

        return dict(zip(cols, row))

@mcp.tool()
def update_entry(entry_id, entry_date=None, title=None, content=None, day_rating=None, mood=None, tags=None):
    '''Update a journal entry.'''

    with sqlite3.connect(DB_PATH) as c:

        cur = c.execute(
            "SELECT entry_date, title, content, day_rating, mood, tags FROM journal_entries WHERE id = ?",
            (entry_id,)
        )

        row = cur.fetchone()

        if not row:
            return {
                "status": "error",
                "message": f"Entry {entry_id} not found"
            }

        entry_date = entry_date if entry_date is not None else row[0]
        title = title if title is not None else row[1]
        content = content if content is not None else row[2]
        day_rating = day_rating if day_rating is not None else row[3]
        mood = mood if mood is not None else row[4]
        tags = tags if tags is not None else row[5]

        c.execute(
            "UPDATE journal_entries SET entry_date = ?, title = ?, content = ?, day_rating = ?, mood = ?, tags = ? WHERE id = ?",
            (entry_date, title, content, day_rating, mood, tags, entry_id)
        )

        return {
            "status": "ok",
            "id": entry_id
        }

@mcp.tool()
def delete_entry(entry_id):
    '''Delete a journal entry.'''

    with sqlite3.connect(DB_PATH) as c:

        cur = c.execute(
            "SELECT id FROM journal_entries WHERE id = ?",
            (entry_id,)
        )

        if not cur.fetchone():
            return {
                "status": "error",
                "message": f"Entry {entry_id} not found"
            }

        c.execute(
            "DELETE FROM journal_entries WHERE id = ?",
            (entry_id,)
        )

        return {
            "status": "ok",
            "id": entry_id,
            "message": "Journal entry deleted successfully"
        }

@mcp.tool()
def summarize_days(start_date, end_date):
    '''Summarize entries by day rating.'''

    with sqlite3.connect(DB_PATH) as c:

        cur = c.execute(
            "SELECT day_rating, COUNT(*) AS total_days FROM journal_entries WHERE entry_date BETWEEN ? AND ? GROUP BY day_rating ORDER BY total_days DESC",
            (start_date, end_date)
        )

        cols = [d[0] for d in cur.description]

        return [dict(zip(cols, row)) for row in cur.fetchall()]

@mcp.tool()
def summarize_moods(start_date, end_date):
    '''Summarize entries by mood.'''

    with sqlite3.connect(DB_PATH) as c:

        cur = c.execute(
            "SELECT mood, COUNT(*) AS total_entries FROM journal_entries WHERE entry_date BETWEEN ? AND ? GROUP BY mood ORDER BY total_entries DESC",
            (start_date, end_date)
        )

        cols = [d[0] for d in cur.description]

        return [dict(zip(cols, row)) for row in cur.fetchall()]

@mcp.tool()
def summarize_tags(start_date, end_date):
    '''List tags used during a date range.'''

    with sqlite3.connect(DB_PATH) as c:

        cur = c.execute(
            "SELECT tags, COUNT(*) AS total_entries FROM journal_entries WHERE entry_date BETWEEN ? AND ? GROUP BY tags ORDER BY total_entries DESC",
            (start_date, end_date)
        )

        cols = [d[0] for d in cur.description]

        return [dict(zip(cols, row)) for row in cur.fetchall()]

@mcp.tool()
def get_entries_for_summary(start_date, end_date):
    '''Get entries for AI summarization.'''

    with sqlite3.connect(DB_PATH) as c:

        cur = c.execute(
            "SELECT entry_date, title, content, day_rating, mood, tags FROM journal_entries WHERE entry_date BETWEEN ? AND ? ORDER BY entry_date ASC",
            (start_date, end_date)
        )

        cols = [d[0] for d in cur.description]

        return [dict(zip(cols, row)) for row in cur.fetchall()]


@mcp.resource("journal://day-ratings")
def day_ratings():
    with open(DAY_RATINGS_CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["day_ratings"]


@mcp.resource("journal://moods")
def moods():
    with open(MOODS_CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["moods"]


if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
