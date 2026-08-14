import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "..", "prisent.db")

def run_migration():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Add columns if not existing
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]

    if "linkedin_display_name" not in columns:
        print("Adding linkedin_display_name column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN linkedin_display_name VARCHAR(255)")

    if "sidebar_collapsed" not in columns:
        print("Adding sidebar_collapsed column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN sidebar_collapsed BOOLEAN DEFAULT 0 NOT NULL")

    conn.commit()

    # 2. Backfill existing records with pipe-separated linkedin_person_id
    cursor.execute("SELECT id, linkedin_person_id FROM users WHERE linkedin_person_id LIKE '%|%'")
    rows = cursor.fetchall()
    print(f"Found {len(rows)} user rows with '|' in linkedin_person_id for backfilling.")

    for row_id, full_val in rows:
        parts = full_val.split("|")
        sub_id = parts[0]
        display_name = parts[1] if len(parts) > 1 else None
        cursor.execute(
            "UPDATE users SET linkedin_person_id = ?, linkedin_display_name = ? WHERE id = ?",
            (sub_id, display_name, row_id)
        )
        print(f"Backfilled user {row_id}: linkedin_person_id='{sub_id}', linkedin_display_name='{display_name}'")

    conn.commit()
    conn.close()
    print("Migration and backfill completed successfully!")

if __name__ == "__main__":
    run_migration()
