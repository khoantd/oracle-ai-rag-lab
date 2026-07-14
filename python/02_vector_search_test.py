from sentence_transformers import SentenceTransformer

from db import get_connection



# ==========================================
# CONFIG
# ==========================================

MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


TOP_K = 5



# ==========================================
# Load Embedding Model
# ==========================================

print("\nLoading embedding model...")


model = SentenceTransformer(
    MODEL_NAME
)


print("Model loaded")



# ==========================================
# Vector Search Function
# ==========================================


def vector_search(question):


    # Convert question to embedding

    query_embedding = model.encode(
        question
    ).tolist()



    conn = get_connection()

    cursor = conn.cursor()



    sql = """
    SELECT

        id,

        title,

        category,

        content,

        embedding <=> %s::vector
        AS distance


    FROM oracle_docs


    ORDER BY distance


    LIMIT %s;

    """



    cursor.execute(
        sql,
        (
            query_embedding,
            TOP_K
        )
    )


    results = cursor.fetchall()


    cursor.close()

    conn.close()


    return results




# ==========================================
# Test Questions
# ==========================================


questions = [

    "Why SQL has high buffer gets?",


    "How to fix ORA-01555 snapshot too old?",


    "Why Oracle chooses full table scan?",


    "Data Guard standby database has apply lag",


    "RMAN backup failed yesterday",


    "How to analyze AWR report?",


    "Oracle RAC gc buffer busy wait problem",


    "ORA-04031 shared pool memory error",


    "Find blocking session in Oracle database",


    "SQL execution plan changed after statistics gathering"

]



# ==========================================
# Run Test
# ==========================================


for question in questions:


    print("\n")
    print("=" * 70)

    print(
        "QUESTION:"
    )

    print(question)


    print("-" * 70)



    results = vector_search(
        question
    )



    for row in results:


        print(
        f"""
ID:
{row[0]}

Title:
{row[1]}

Category:
{row[2]}

Similarity Distance:
{round(row[4],4)}

Content:
{row[3][:200]}...

"""
        )