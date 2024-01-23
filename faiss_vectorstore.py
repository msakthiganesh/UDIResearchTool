import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
import helper

def create_vectorstore(doc_chunks, embedding_type:str = "openai", save_db:bool=True):
    """Generates embeddings using the 'embedding_type' and stores the embeddings to FAISS Vector Database

    Args:
        doc_chunks (_type_): Document chunks after performing text splitting.
        embedding_type (str, optional): Type of Embedding API to call. Defaults to "openai".
    """
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(
        documents=doc_chunks,
        embedding=embeddings
    )
    filenames = helper.db_filenames(vectordb="faiss")
    if save_db:
        vectorstore.save_local(folder_path=os.getenv('VECTORDB_OPENAI_FAISS'), index_name='faiss')
    return vectorstore


def update_vectorstore(embedding_type:str="openai"):
    if embedding_type == "openai":
        vectorstore = FAISS.load_local(folder_path=os.getenv('VECTORDB_OPENAI_FAISS'), index_name='faiss')
        
        
        
        
        
    