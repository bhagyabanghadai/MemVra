import psycopg2
import sys

try:
    print("Attempting to connect as 'memvra' to 127.0.0.1:5433...")
    conn = psycopg2.connect(
        dbname="memvra",
        user="memvra",
        password="password",
        host="127.0.0.1",
        port="5433"
    )
    print("SUCCESS: Connection established as 'memvra'!")
    conn.close()
except Exception as e:
    print(f"FAILURE: 'memvra' connection failed: {e}")

try:
    print("Attempting to connect as 'postgres' to 127.0.0.1:5433...")
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="password",
        host="127.0.0.1",
        port="5433"
    )
    print("SUCCESS: Connection established as 'postgres'!")
    conn.close()
except Exception as e:
    print(f"FAILURE: 'postgres' connection failed: {e}")
