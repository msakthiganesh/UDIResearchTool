import os
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter


def get_pdf_text(pdf_dir_path:str):
    """Loading the PDFs in the 'pdf_dir_path' and extracting the text from the PDFs 

    Args:
        pdf_dir_path (str): Path to the directory containing the PDF Files / PDF Database
    """
    
    pdf_loader = PyPDFDirectoryLoader(os.getenv('PDF_DIR_PATH'))
    pdf_docs = pdf_loader.load()
    return pdf_docs

def get_text_chunks(py_pdf_docs, **kwargs):
    """Returns text chunks from the loaded & extracted PDF documents and returns text chunks

    Args:
        py_pdf_docs (_type_): _description_
        Keyword Arguments (**kwargs):
            text_splitter_method: Choose between 'RecursiveCharacterTextSplitter' or 'CharacterTextSplitter'. Default: 'CharacterTextSplitter' 
            separator (str): Escape character or sequence to split the text. 
            chunk_size (int): Maximum Token Length of the chunks
            chunk_overlap (int): No. of Token overlap between two chunks to account for loss of information while splitting
            length_function (method): Python Method/Function to utilize for text splitting. Default: len
    """
    if kwargs.get("text_splitter_method", "CharacterTextSplitter") == "RecursiveCharacterTextSplitter":
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2500,
            chunk_overlap=200
        )
    else:
        text_splitter = CharacterTextSplitter(
            separator='\n',
            chunk_size=2500,
            chunk_overlap=200,
            length_function=len
        )
        document_chunks = text_splitter.split_documents(py_pdf_docs)
        return document_chunks

