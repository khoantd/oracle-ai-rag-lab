from sentence_transformers import SentenceTransformer

from openai import OpenAI

from db import get_connection



# ==================================================
# CONFIG
# ==================================================

EMBED_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


OLLAMA_MODEL = "qwen2.5:7b"


TOP_K = 5



# ==================================================
# Load Embedding Model
# ==================================================

print("Loading embedding model...")


embedding_model = SentenceTransformer(
    EMBED_MODEL
)


print("Embedding model ready")



# ==================================================
# Ollama Client
# ==================================================

client = OpenAI(

    base_url=
    "http://localhost:11434/v1",

    api_key="ollama"

)



# ==================================================
# Vector Search
# ==================================================

def search_knowledge(question):


    # Question embedding

    vector = embedding_model.encode(
        question
    ).tolist()



    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
    """
    SELECT

        title,

        category,

        content,

        embedding <=> %s::vector
        AS distance


    FROM oracle_docs


    ORDER BY distance


    LIMIT %s

    """,
    (
        vector,
        TOP_K
    )
    )



    results = cursor.fetchall()


    cursor.close()

    conn.close()


    return results



# ==================================================
# Build RAG Context
# ==================================================

def build_context(results):


    context = ""


    for r in results:


        context += f"""

Title:
{r[0]}


Category:
{r[1]}


Knowledge:
{r[2]}


----------------------

"""


    return context




# ==================================================
# Ask Ollama
# ==================================================

def ask_ollama(
        question,
        context
):


    prompt = f"""

You are an Oracle Database Expert AI Assistant.


Answer the question using ONLY the provided Oracle DBA knowledge.


If the knowledge does not contain the answer,
say:

"I don't have enough Oracle knowledge."


=====================
Oracle DBA Knowledge
=====================

{context}


=====================
Question
=====================

{question}


Provide:

1. Root cause

2. Diagnosis steps

3. Recommended solution


"""



    response = client.chat.completions.create(

        model=OLLAMA_MODEL,


        messages=[

            {
                "role":"system",
                "content":
                "You are an Oracle DBA expert."
            },


            {
                "role":"user",
                "content":prompt
            }

        ],


        temperature=0.2

    )



    return (
        response
        .choices[0]
        .message
        .content
    )



# ==================================================
# Main Chat Loop
# ==================================================

print("\nOracle AI DBA RAG Chatbot")

print(
"Type exit to stop\n"
)



while True:


    question = input(
        "\nDBA Question: "
    )


    if question.lower() == "exit":

        break



    # 1. Search vector database

    docs = search_knowledge(
        question
    )



    # 2. Build context

    context = build_context(
        docs
    )



    # 3. Ask LLM

    answer = ask_ollama(
        question,
        context
    )



    print(
        "\n========== AI DBA =========="
    )


    print(answer)


    print(
        "============================"
    )