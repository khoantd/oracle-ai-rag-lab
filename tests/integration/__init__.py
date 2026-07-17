# Integration tests require a live PostgreSQL + pgvector instance.
# They are skipped in default CI. Set PGHOST (and related env) to enable:
#   pytest -m integration
