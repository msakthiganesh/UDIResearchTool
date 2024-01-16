import os
from dotenv import load_dotenv
from preprocessing import get_pdf_text, get_text_chunks
from faiss_vectorstore import create_vectorstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS


pdf_docs = get_pdf_text(pdf_dir_path=os.getenv('PDF_DIR_PATH'))
document_chunks = get_text_chunks(py_pdf_docs=pdf_docs)
vectorstore = create_vectorstore(doc_chunks=document_chunks, embedding_type="openai")

