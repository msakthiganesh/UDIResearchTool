import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
import helper


def create_vectorstore(doc_chunks, embedding_type: str = "openai", save_db: bool = True):
    """Generates embeddings using the 'embedding_type' and stores the embeddings to FAISS Vector Database

    Args:
        doc_chunks (_type_): Document chunks after performing text splitting.
        embedding_type (str, optional): Type of Embedding API to call. Defaults to "openai".
        :param doc_chunks:
        :param embedding_type:
        :param save_db:
    """

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(
        documents=doc_chunks,
        embedding=embeddings
    )
    filenames = helper.vectordb_filenames(vectordb="faiss")
    if save_db:
        vectorstore.save_local(folder_path=os.getenv('VECTORDB_OPENAI_FAISS'))
    else:
        return vectorstore


def update_vectorstore(upload_vector, embedding_type: str = "openai") -> None:
    if embedding_type == "openai":
        embedding = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(folder_path=os.getenv('VECTORDB_OPENAI_FAISS'), embeddings=embedding)
        vectorstore.merge_from(upload_vector)
        vectorstore.save_local(folder_path=os.getenv('VECTORDB_OPENAI_FAISS'))
        helper.move_files_to_store(source=os.getenv('UPLOAD_DIR'), destination=os.getenv('DATASTORE_DIR'))

