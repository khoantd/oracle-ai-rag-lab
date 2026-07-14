import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from db import get_connection
# ==================================================
# CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

# ==================================================
# Load Embedding Model
# ==================================================
print("\nLoading embedding model...")
model = SentenceTransformer(
    MODEL_NAME
)
print("Embedding model loaded")
# ==================================================
# Connect PostgreSQL
# ==================================================
print("\nConnecting PostgreSQL...")
conn = get_connection()
cursor = conn.cursor()
print("PostgreSQL connected")
# ==================================================
# Clean old data
# ==================================================
print("\nCleaning old documents...")
cursor.execute(
    """
    DELETE FROM oracle_docs;
    """
)
conn.commit()



# ==================================================
# Scan JSON documents
# ==================================================
print("\nScanning knowledge folder...")
documents = []
for json_file in KNOWLEDGE_DIR.rglob("*.json"):

    print(
        "Found:",
        json_file.name
    )

    with open(
        json_file,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

        documents.append(data)
print(
    "\nTotal documents found:",
    len(documents)
)

# ==================================================
# Generate Embedding + Insert
# ==================================================
print("\nGenerating embeddings...\n")
for index, doc in enumerate(
        documents,
        start=1
):
    text = f"""
Title:
{doc['title']}

Category:
{doc['category']}

Content:
{doc['content']}
"""


    # Generate vector

    embedding = model.encode(
        text
    ).tolist()



    # Insert PostgreSQL

    cursor.execute(
        """
        INSERT INTO oracle_docs
        (
            title,
            category,
            content,
            embedding
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
        """,
        (
            doc["title"],
            doc["category"],
            doc["content"],
            embedding
        )
    )


    print(
        f"[{index}/{len(documents)}] "
        f"Inserted: {doc['title']}"
    )



# Commit

conn.commit()



# ==================================================
# Verify
# ==================================================

cursor.execute(
    """
    SELECT COUNT(*)
    FROM oracle_docs;
    """
)


count = cursor.fetchone()[0]


print("\n==============================")
print(
    "Documents in database:",
    count
)
print("==============================")



# Close

cursor.close()

conn.close()


print("\nLoad completed successfully!")