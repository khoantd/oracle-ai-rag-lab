from sentence_transformers import SentenceTransformer
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)
text = "Oracle SQL has high buffer gets"
vector = model.encode(text)
print("Vector size:")
print(len(vector))
print(vector[:10])