# rag_processor.py
import os
import numpy as np
from sentence_transformers import SentenceTransformer

class RAGProcessor:
    def __init__(self):
        self.model = SentenceTransformer('all-mpnet-base-v2')
        self.documents = []
        self.data_folder = "extracted_data"

    def chunk_text(self, text, chunk_size=200):
        """Splits text into overlapping chunks for better semantic search."""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        return chunks

    def index_documents(self):
        if not os.path.exists(self.data_folder):
            print(f"Error: Data folder {self.data_folder} not found")
            return False

        self.documents = []

        for filename in os.listdir(self.data_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.data_folder, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        text_content = f.read()

                    chunks = self.chunk_text(text_content)
                    for chunk in chunks:
                        embedding = self.model.encode(chunk, convert_to_tensor=False)
                        self.documents.append({
                            "text_data": chunk,
                            "source": filename,
                            "embedding": embedding
                        })

                except Exception as e:
                    print(f"Error processing {filename}: {e}")

        print(f"Indexed {len(self.documents)} chunks from TXT files")
        return True

    def retrieve(self, query, top_k=3, threshold=0.25):  # Lowered threshold
        if not self.documents:
            print("No documents indexed yet.")
            return []

        query_embedding = self.model.encode(query, convert_to_tensor=False)

        similarities = []
        for doc in self.documents:
            doc_embedding = doc["embedding"]
            sim = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            similarities.append(sim)

        results = []
        for i, sim in enumerate(similarities):
            if sim >= threshold:
                doc = self.documents[i].copy()
                doc["similarity"] = sim
                results.append(doc)

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
