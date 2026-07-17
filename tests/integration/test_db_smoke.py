"""Optional live-DB smoke checks (skipped unless PGHOST is set)."""

from __future__ import annotations

import os

import pytest

pytestmark = pytest.mark.integration


@pytest.mark.skipif(not os.environ.get("PGHOST"), reason="PGHOST not set")
def test_can_connect_and_count() -> None:
    from oracle_ai_rag.config import load_settings
    from oracle_ai_rag.db import get_connection
    from oracle_ai_rag.repository import OracleDocsRepository

    settings = load_settings()
    conn = get_connection(settings)
    try:
        count = OracleDocsRepository(conn).count()
        assert count >= 0
    finally:
        conn.close()
