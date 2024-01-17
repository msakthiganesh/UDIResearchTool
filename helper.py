import os
from typing import List
import shutil

def db_filenames(vectordb:str="faiss") -> List[str]:
    if vectordb == "faiss":
        files = os.listdir(os.getenv('PDF_DIR_PATH'))
        with open("./db/openai/faiss/faiss_files.txt", 'w+') as f:
            f.write(str(files))
        return files  
    

def create_or_merge(vector_db:str) -> bool:
    """_summary_

    Args:
        db (str): Type of Vector Database

    Returns:
        bool: Returns True if Vector DB already exists. Else, returns False.
    """
    if vector_db == "faiss":
        if "index.faiss" in os.listdir(os.getenv('VECTORDB_OPENAI_FAISS')):
            return True
        return False
    
def move_files_to_db(source:str, destination:str) -> bool:
    files_to_move = os.listdir(source)
    if len(files_to_move)>0:
        try:
            for file in files_to_move:
                shutil.move(
                    os.path.join(source, file),
                    os.path.join(destination, file)
                            )
            return True
        except Exception as e:
            print(f"Error while moving files - {e}")
    return False