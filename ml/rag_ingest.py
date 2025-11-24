from xml.dom.minidom import Document
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
PUA_MAP = {
    "\ue088": "-",    
    "\ue092": ": ",    
    "\ue097": "-",     
    "\ue1d7": "->",    
}

def load_pdf_documents():
    loader = PyPDFLoader("knowledge_base/politicas.pdf")
    return loader.load()

def normalize_text(text):
    for pua_char, replacement in PUA_MAP.items():
        text = text.replace(pua_char, replacement)
    return text.strip()

def load_vector_store(embeddings, save_path):
    if os.path.exists(os.path.join(save_path, "index.faiss")):
        print(f"Loading existing vector store from {save_path}...")
        return FAISS.load_local(save_path, embeddings, allow_dangerous_deserialization=True)
    else:
        print(f"No existing vector store found in {save_path}. Loading an empty store...")
        return FAISS([], embeddings)
    
def create_vector_store(documents):
    emb =HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(documents, embedding=emb)
    vector_store.save_local("vector_store/faiss_index")
    return vector_store
if __name__ == "__main__":
    docs = load_pdf_documents()
    
    full_text = normalize_text(docs[0].page_content)
    emb = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2")

    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    chunks = text_splitter.split_text(full_text)

    vector_store = create_vector_store(chunks)
    print(f"Vector store created with {len(chunks)} documents.")

    
    