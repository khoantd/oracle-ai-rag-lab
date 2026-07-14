import psycopg2
def get_connection():
    conn = psycopg2.connect(
        host="10.0.0.177",
        port=5432,
        database="oracle_ai",
        user="ai_dba",
        password="oracle_4U"
    )
    return conn