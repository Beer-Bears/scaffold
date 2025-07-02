import os

from langchain_chroma import Chroma
from tqdm import tqdm

from src.core.vector.splitter import get_splitter


def chunk_and_load_to_vectorstore(vector_store: Chroma, root_dir: str):
    """
    Processes all files in a directory, splits them into chunks, and loads into ChromaDB
    """

    all_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            all_files.append(full_path)

    documents = []
    metadatas = []

    for file_path in tqdm(all_files, desc="Processing files"):
        try:
            ext = os.path.splitext(file_path)[1]

            splitter = get_splitter(file_identifier=file_path)

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            chunks = splitter.split_text(content)

            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append(
                    {"source": file_path, "chunk_index": i, "file_extension": ext}
                )

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

    if documents:
        vector_store.add_texts(texts=documents, metadatas=metadatas)
        print(
            f"\n✅ Loaded {len(documents)} chunks from {len(all_files)} files into ChromaDB"
        )
    else:
        print("❌ No documents to load")


if __name__ == "__main__":
    chunk_and_load_to_vectorstore(
        root_dir="codebase/syntatic-1",
    )
