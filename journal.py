from fastmcp import FastMCP
import os
import json
import sqlite3
import aiosqlite
import tempfile

TEMP_DIR = tempfile.gettempdir()
DB_PATH = os.path.join(TEMP_DIR, "journal.db")

DAY_RATINGS_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "day_ratings.json")
MOODS_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "moods.json")

print(f"Database path: {DB_PATH}")

mcp = FastMCP("JournalTracker")

def init_db():
    try:
        with sqlite3.connect(DB_PATH) as c:
            c.execute("PRAGMA journal_mode=WAL")
            c.execute("CREATE TABLE IF NOT EXISTS journal_entries (id INTEGER PRIMARY KEY AUTOINCREMENT, entry_date TEXT NOT NULL, title TEXT DEFAULT '', content TEXT NOT NULL, day_rating TEXT NOT NULL, mood TEXT DEFAULT '', tags TEXT DEFAULT '', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            c.execute("INSERT OR IGNORE INTO journal_entries (entry_date, content, day_rating) VALUES ('2000-01-01', 'test', 'test')")
            c.execute("DELETE FROM journal_entries WHERE content='test'")
            print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")
        raise

init_db()

@mcp.tool()
async def add_entry(entry_date, content, day_rating, title="", mood="", tags=""):
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            cur = await c.execute("INSERT INTO journal_entries (entry_date, title, content, day_rating, mood, tags) VALUES (?, ?, ?, ?, ?, ?)", (entry_date, title, content, day_rating, mood, tags))
            await c.commit()
            return {"status": "ok", "id": cur.lastrowid}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def list_entries(start_date, end_date):
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            cur = await c.execute("SELECT id, entry_date, title, content, day_rating, mood, tags, created_at FROM journal_entries WHERE entry_date BETWEEN ? AND ? ORDER BY entry_date ASC", (start_date, end_date))
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in await cur.fetchall()]
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def get_entry(entry_id):
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            cur = await c.execute("SELECT id, entry_date, title, content, day_rating, mood, tags, created_at FROM journal_entries WHERE id = ?", (entry_id,))
            row = await cur.fetchone()

            if not row:
                return None

            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def update_entry(entry_id, entry_date=None, title=None, content=None, day_rating=None, mood=None, tags=None):
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            cur = await c.execute("SELECT entry_date, title, content, day_rating, mood, tags FROM journal_entries WHERE id = ?", (entry_id,))
            row = await cur.fetchone()

            if not row:
                return {"status": "error", "message": f"Entry {entry_id} not found"}

            entry_date = entry_date if entry_date is not None else row[0]
            title = title if title is not None else row[1]
            content = content if content is not None else row[2]
            day_rating = day_rating if day_rating is not None else row[3]
            mood = mood if mood is not None else row[4]
            tags = tags if tags is not None else row[5]

            await c.execute("UPDATE journal_entries SET entry_date=?, title=?, content=?, day_rating=?, mood=?, tags=? WHERE id=?", (entry_date, title, content, day_rating, mood, tags, entry_id))
            await c.commit()

            return {"status": "ok", "id": entry_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def delete_entry(entry_id):
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            cur = await c.execute("SELECT id FROM journal_entries WHERE id = ?", (entry_id,))
            row = await cur.fetchone()

            if not row:
                return {"status": "error", "message": f"Entry {entry_id} not found"}

            await c.execute("DELETE FROM journal_entries WHERE id = ?", (entry_id,))
            await c.commit()

            return {"status": "ok", "id": entry_id, "message": "Journal entry deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def summarize_days(start_date, end_date):
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            cur = await c.execute("SELECT day_rating, COUNT(*) AS total_days FROM journal_entries WHERE entry_date BETWEEN ? AND ? GROUP BY day_rating ORDER BY total_days DESC", (start_date, end_date))
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in await cur.fetchall()]
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def summarize_moods(start_date, end_date):
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            cur = await c.execute("SELECT mood, COUNT(*) AS total_entries FROM journal_entries WHERE entry_date BETWEEN ? AND ? GROUP BY mood ORDER BY total_entries DESC", (start_date, end_date))
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in await cur.fetchall()]
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def summarize_tags(start_date, end_date):
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            cur = await c.execute("SELECT tags, COUNT(*) AS total_entries FROM journal_entries WHERE entry_date BETWEEN ? AND ? GROUP BY tags ORDER BY total_entries DESC", (start_date, end_date))
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in await cur.fetchall()]
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def get_entries_for_summary(start_date, end_date):
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            cur = await c.execute("SELECT entry_date, title, content, day_rating, mood, tags FROM journal_entries WHERE entry_date BETWEEN ? AND ? ORDER BY entry_date ASC", (start_date, end_date))
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in await cur.fetchall()]
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.resource("journal://day-ratings")
def day_ratings():
    try:
        with open(DAY_RATINGS_CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["day_ratings"]
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("journal://moods")
def moods():
    try:
        with open(MOODS_CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["moods"]
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)