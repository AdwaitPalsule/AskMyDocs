# src/db.py
import sqlite3

DB_PATH = "chat_history.db"

def init_db():
    """Initialize the database and ensure all columns exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            user_id TEXT
        )
    """)
    
    # Check if user_id column exists (for old DB versions)
    cursor.execute("PRAGMA table_info(messages)")
    columns = [col[1] for col in cursor.fetchall()]
    if "user_id" not in columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN user_id TEXT DEFAULT 'guest'")
        print("✅ Added 'user_id' column to existing DB.")

    conn.commit()
    conn.close()


def save_message(session_id, role, content, user_id="guest"):
    """Save a single message to DB."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (session_id, role, content, user_id) VALUES (?, ?, ?, ?)",
        (session_id, role, content, user_id)
    )
    conn.commit()
    conn.close()


def get_chat_history(session_id, user_id="guest"):
    """Get messages for a specific session."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM messages WHERE session_id = ? AND user_id = ? ORDER BY id ASC",
        (session_id, user_id)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]


def get_all_sessions(user_id="guest"):
    """Get list of session IDs for a given user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT session_id FROM messages WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    )
    sessions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return sessions


def delete_session(session_id, user_id="guest"):
    """Delete all messages for a given session."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM messages WHERE session_id = ? AND user_id = ?",
        (session_id, user_id)
    )
    conn.commit()
    conn.close()
