import sqlite3

# # SQLite 데이터베이스 연결
# conn = sqlite3.connect('discord_logs.db')
# c = conn.cursor()

# # 서버 로그 테이블 생성
# c.execute('''
# CREATE TABLE IF NOT EXISTS server_logging (
#     datetime TEXT,
#     total_members INTEGER,
#     members_joined INTEGER,
#     members_left INTEGER,
#     total_count INTEGER,
#     access_nickname TEXT,
#     daily_chat_count INTEGER
# )
# ''')

# # 통화방 로그 테이블 생성
# c.execute('''
# CREATE TABLE IF NOT EXISTS voice_logging (
#     datetime TEXT,
#     nickname TEXT,
#     joined TEXT,
#     left TEXT,
#     total_duration TEXT
# )
# ''')

# # 변경사항 저장
# conn.commit()
# conn.close()
def create_server_logging_table():
    try:
        conn = sqlite3.connect('discord_logs.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS server_logging (
                datetime TEXT PRIMARY KEY,
                members_joined INTEGER DEFAULT 0,
                members_left INTEGER DEFAULT 0,
                total_members INTEGER,
                access_usernames TEXT DEFAULT '',
                daily_chat_count INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def add_missing_columns():
    try:
        conn = sqlite3.connect('discord_logs.db')
        c = conn.cursor()
        c.execute('''
            ALTER TABLE server_logging ADD COLUMN access_usernames TEXT DEFAULT ''
        ''')
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

create_server_logging_table()
add_missing_columns()