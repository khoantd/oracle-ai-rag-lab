import psycopg2
conn = psycopg2.connect(
    host="10.0.0.177",
    port=5432,
    database="oracle_ai",
    user="ai_dba",
    password="oracle_4U"
)
print("PostgreSQL connected")
cursor=conn.cursor()
cursor.execute(
"SELECT count(*) FROM oracle_docs"
)
print(cursor.fetchone())
conn.close()