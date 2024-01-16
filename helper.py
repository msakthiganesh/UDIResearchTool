import os
from typing import List


def db_filenames(vectordb:str="faiss") -> List[str]:
    if vectordb == "faiss":
        files = os.listdir(os.getenv('PDF_DIR_PATH'))
        with open("./db/openai/faiss/faiss_files.txt", 'w+') as f:
            f.write(str(files))
        return files  