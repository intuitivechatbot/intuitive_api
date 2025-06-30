import os
import glob
from qdrant_client import QdrantClient, models
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()  # Loads .env if running locally
BLOG_DIR = "../data/processed/intuitive_soul_posts/"
txt_paths = sorted(glob.glob(os.path.join(BLOG_DIR, "*.txt")))
print(f"🔍 Found {len(txt_paths)} .txt files in {BLOG_DIR}")

# 1) Make sure we're actually seeing your files
if len(txt_paths) == 0:
    raise RuntimeError(f"No .txt files found in {BLOG_DIR}. Check your path!")


texts = []
payload = []
for idx, path in enumerate(txt_paths):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    # You can also parse front-matter or derive date/tags from filename here
    filename = os.path.basename(path)
    doc_id = os.path.splitext(filename)[0]
    
    texts.append(content)
    payload.append({
        "filename": filename,
        "doc_id": doc_id,
        "page_content": content
        # add any other metadata you want, e.g.:
        # "source": "my-blog",
        # "imported_at": datetime.utcnow().isoformat()
    })

# Use OpenAI embeddings (1536-dim)
embedder = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
vectors = embedder.embed_documents(texts)

# Connect to Qdrant Cloud
client = QdrantClient(
    url= os.getenv("QDRANT_URL"),
    api_key= os.getenv("QDRANT_API_KEY")
)

collection_name = "blogs"
dim = len(vectors[0])  

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=dim,
        distance=models.Distance.COSINE
    )
)

# 5. Upload everything
client.upload_collection(
    collection_name=collection_name,
    vectors=vectors,
    payload=payload,
    ids=[int(i) for i in range(len(texts))]
)

print(f"✅ Uploaded {len(texts)} blog posts to Qdrant collection '{collection_name}'.")