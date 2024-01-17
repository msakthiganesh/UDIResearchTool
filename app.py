import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from preprocessing import get_pdf_text, get_text_chunks
from faiss_vectorstore import create_vectorstore
import helper

app = Flask(__name__)

load_dotenv()


@app.route("/")
def home():
    return render_template("chatbot.html")

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No File Found!"
        try:
            pdf_file = request.files['file']
            pdf_name = pdf_file.filename
            save_path = os.path.join(os.getenv('UPLOAD_DIR'), pdf_name)
            pdf_file.save(save_path, )
        except Exception as e:
            return f"Error while storing the file."
        return f"File - {pdf_name} uploaded."


@app.route("/injest", methods=['GET'])
def injest_to_db():
    if request.method == 'GET':
        update_flag = helper.move_files_to_db(
                source=os.getenv('UPLOAD_DIR'), 
                destination=os.getenv('PDF_DIR')
                )
        merge_flag = helper.create_or_merge(vector_db="faiss")
        if update_flag and merge_flag: # Merge new uploads to vector DB
            try:
                pdf_docs = get_pdf_text(pdf_dir_path=os.getenv('UPLOAD_DIR'))
                document_chunks = get_text_chunks(py_pdf_docs=pdf_docs)
                vectorstore = create_vectorstore(doc_chunks=document_chunks, embedding_type="openai")   
                # ! Implement - Logic to merge
            except Exception as e:
                return e
        elif update_flag: # Create a new vector DB
            try:            
                pdf_docs = get_pdf_text(pdf_dir_path=os.getenv('PDF_DIR'))
                document_chunks = get_text_chunks(py_pdf_docs=pdf_docs)
                vectorstore = create_vectorstore(doc_chunks=document_chunks, embedding_type="openai")   
                vectorstore.save_local(os.getenv('VECTORDB_OPENAI_FAISS'))
                return "FAISS Vector DB created successfully."
            except Exception as e:
                return f"Error occurred while creating FAISS Vector DB - {e}"
        return "No file found to injest."


@app.route("/fetch", methods=['GET'])
def fetch():
    if request.method == 'GET':
        # Fetch all the filenames in the database and return the list
        return "Fetch method executed."


@app.route("/generate", methods=['POST'])
def generate():
    if request.method == 'POST':
        # RAG system using the input query
        return "Generate Method executed."


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001, debug=True, use_reloader = True)
