
from app.rag.embedding import get_embeddings
from app.config.settings import settings

embeddings = get_embeddings()


vector = embeddings.embed_query("How many days of annual leave do I get?")

print("Vector length:", len(vector))
print("Expected length:", settings.embedding_dimension)
print("Match:", len(vector) == settings.embedding_dimension)