import os
from contextlib import contextmanager
import psycopg

def _dsn():
    user = os.environ["POSTGRES_USER"]
    pwd = os.environ["POSTGRES_PASSWORD"]
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    db = os.environ["POSTGRES_DB"]
    return f"postgresql://{user}:{pwd}@{host}:{port}/{db}"

@contextmanager
def get_conn():
    with psycopg.connect(_dsn(), autocommit=True) as conn:
        yield conn

def insert_events(events: list[dict]):
    if not events:
        return
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """
                insert into transit_event (source, line, status, severity, message, started_at)
                values (%(source)s, %(line)s, %(status)s, %(severity)s, %(message)s, %(started_at)s)
                """,
                events,
            )

def get_history(line: str, limit: int = 200):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            select line, status, message, observed_at
            from transit_event
            where line = %s
            order by observed_at desc
            limit %s
            """,
            (line, limit),
        )
        rows = cur.fetchall()
    return [
        {"line": r[0], "status": r[1], "message": r[2], "observed_at": r[3].isoformat()}
        for r in rows
    ]
