import os
from file_processor import process_file
from rag_processor import RAGProcessor
from llama_cpp import Llama

# Load the GGUF model using llama-cpp
llm = Llama(
    model_path="models/llama-2-7b.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=4,
    n_gpu_layers=0
)

# Generate answer using llama-cpp
def generate_answer(query, context):
    prompt = create_prompt(query, context)
    response = llm(prompt, max_tokens=512, stop=["\n\n"])
    return response["choices"][0]["text"]

def create_prompt(query, context):
    return f"Given the context below, answer the question.\n\nContext: {context}\n\nQuestion: {query}\nAnswer:"

# Function to clear all files in a folder
def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    else:
        os.makedirs(folder_path)

def main():
    rag_processor = RAGProcessor()
    indexed = False

    while True:
        action = input("\nChoose action: 'upload', 'query', or 'exit': ").strip().lower()

        if action == "exit":
            print("Exiting program.")
            break

        elif action == "upload":
            file_path = input("Enter file path: ").strip()

            if not os.path.exists(file_path):
                print(f"Error: File not found - {file_path}")
                continue

            # Automatically clear old uploads and extracted data
            print("⚙️ Clearing old uploaded and extracted files...")
            clear_folder("uploads")
            clear_folder("extracted_data")

            print("⚙️ Processing file...")
            txt_file_path, _ = process_file(file_path)

            if txt_file_path:
                indexed = rag_processor.index_documents()
                if indexed:
                    print("✅ File processed and indexed successfully!")
            else:
                print("❌ Failed to process file.")

        elif action == "query":
            if not indexed:
                indexed = rag_processor.index_documents()
                if not indexed:
                    print("⚠️ No documents available to search.")
                    continue

            query = input("Enter your question: ").strip()
            results = rag_processor.retrieve(query)

            if results:
                print("\n📄 Relevant documents found:")
                for idx, doc in enumerate(results, 1):
                    print(f"\n--- Document {idx}: {doc['source']} ---")
                    preview = doc.get("text_data", "")[:500].replace("\n", " ")
                    print(preview + ("..." if len(preview) == 500 else ""))

                context = "\n".join([doc.get("text_data", "") for doc in results])
                answer = generate_answer(query, context)
                print(f"\n💬 Answer: {answer}")
            else:
                print("❌ No relevant information found.")

        else:
            print("❗ Invalid option. Please choose 'upload', 'query', or 'exit'.")

if __name__ == "__main__":
    main()
