import os
import sqlite3
import pymysql
import pymysql.cursors
from config import Config

def get_mysql_connection():
    """Attempt connecting to MySQL via unix_socket or host:port."""
    # Check if socket file exists
    socket_path = Config.MYSQL_UNIX_SOCKET
    if socket_path and os.path.exists(socket_path):
        try:
            return pymysql.connect(
                unix_socket=socket_path,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            ), 'mysql'
        except Exception:
            pass
            
    # Try TCP connection
    try:
        return pymysql.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=3,
            autocommit=False
        ), 'mysql'
    except Exception:
        pass
        
    return None, None


def get_sqlite_connection():
    """Fallback connection using SQLite with dictionary row factory."""
    conn = sqlite3.connect(Config.SQLITE_DB)
    conn.row_factory = sqlite3.Row
    return conn, 'sqlite'


def get_db():
    """Get database connection: prefers MySQL, falls back to SQLite seamlessly."""
    conn, db_type = get_mysql_connection()
    if conn:
        return conn, db_type
    return get_sqlite_connection()


def query_db(query, args=(), one=False, commit=False, return_id=False):
    """
    Executes a query safely against MySQL or SQLite fallback.
    Returns dictionary results or last inserted id.
    """
    conn, db_type = get_db()
    cursor = conn.cursor()
    
    # Translate placeholder syntax if needed:
    # MySQL uses %s, SQLite uses ?
    formatted_query = query
    if db_type == 'sqlite':
        formatted_query = query.replace('%s', '?')
        # Translate date arithmetic functions if present
        formatted_query = formatted_query.replace('CURDATE()', "date('now')")
        formatted_query = formatted_query.replace('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP', 'CURRENT_TIMESTAMP')
    
    try:
        cursor.execute(formatted_query, args)
        
        if commit:
            conn.commit()
            if return_id:
                last_id = cursor.lastrowid
                cursor.close()
                conn.close()
                return last_id
            cursor.close()
            conn.close()
            return True
            
        if one:
            row = cursor.fetchone()
            result = dict(row) if row else None
        else:
            rows = cursor.fetchall()
            result = [dict(r) for r in rows]
            
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        if commit:
            conn.rollback()
        cursor.close()
        conn.close()
        raise e


def init_db():
    """
    Initializes database tables if they do not exist.
    Runs database.sql if MySQL is empty, or creates SQLite schema if fallback.
    """
    conn, db_type = get_db()
    if db_type == 'mysql':
        try:
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES LIKE 'farmers'")
            table_exists = cursor.fetchone()
            if not table_exists:
                sql_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.sql')
                if os.path.exists(sql_path):
                    with open(sql_path, 'r', encoding='utf-8') as f:
                        sql_commands = f.read().split(';')
                        for cmd in sql_commands:
                            cmd_clean = cmd.strip()
                            if cmd_clean and not cmd_clean.lower().startswith('create database') and not cmd_clean.lower().startswith('use '):
                                cursor.execute(cmd_clean)
                    conn.commit()
            cursor.close()
            conn.close()
            print("[INFO] Connected to MySQL database successfully.")
        except Exception as e:
            conn.close()
            print(f"[WARN] MySQL init check: {e}")
    else:
        # SQLite initialization
        cursor = conn.cursor()
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            mobile TEXT NOT NULL UNIQUE,
            email TEXT,
            password_hash TEXT NOT NULL,
            state TEXT NOT NULL DEFAULT 'Telangana',
            district TEXT NOT NULL DEFAULT 'Nirmal',
            village TEXT,
            land_size_acres REAL NOT NULL DEFAULT 2.50,
            soil_type TEXT NOT NULL DEFAULT 'Black Soil',
            preferred_language TEXT NOT NULL DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            crop_name TEXT NOT NULL,
            variety TEXT,
            sowing_date TEXT NOT NULL,
            area_acres REAL NOT NULL DEFAULT 1.00,
            soil_type TEXT NOT NULL DEFAULT 'Black Soil',
            stage TEXT NOT NULL DEFAULT 'Vegetative',
            health_status TEXT NOT NULL DEFAULT 'Healthy',
            expected_harvest_date TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_id) REFERENCES farmers (id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS crop_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_id INTEGER NOT NULL,
            activity_type TEXT NOT NULL,
            activity_date TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (crop_id) REFERENCES crops (id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS emergency_sos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER,
            farmer_name TEXT NOT NULL,
            contact_number TEXT NOT NULL,
            district TEXT NOT NULL,
            village TEXT NOT NULL,
            issue_type TEXT NOT NULL,
            severity TEXT NOT NULL DEFAULT 'High',
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            language TEXT NOT NULL DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("[INFO] SQLite fallback database initialized.")
