"""PostgreSQL connection helper."""

from __future__ import annotations

import psycopg2
from psycopg2.extensions import connection as PgConnection

from oracle_ai_rag.config import Settings


def get_connection(settings: Settings) -> PgConnection:
    """Open a psycopg2 connection using Settings (no hardcoded secrets)."""
    settings.require_db_password()
    return psycopg2.connect(
        host=settings.pg_host,
        port=settings.pg_port,
        database=settings.pg_database,
        user=settings.pg_user,
        password=settings.pg_password,
    )
