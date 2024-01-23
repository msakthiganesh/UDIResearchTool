import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from preprocessing import get_pdf_text, get_text_chunks
from faiss_vectorstore import create_vectorstore, update_vectorstore
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


@app.route('/ingest', methods=['GET'])
# ! TODO: Change embedding_type to param and pass as input in API call
def ingest_to_db():
    if request.method == 'GET':
        upload_flag = helper.move_files_to_store(source=os.getenv('UPLOAD_DIR'), destination=os.getenv('DATASTORE_DIR'))
        merge_flag = helper.create_or_merge(vector_db='faiss')

        if upload_flag and merge_flag:  # Merge new uploads to vector DB
            try:
                pdf_docs = get_pdf_text(pdf_dir_path=os.getenv('UPLOAD_DIR'))
                document_chunks = get_text_chunks(py_pdf_docs=pdf_docs)
                upload_vectors = create_vectorstore(doc_chunks=document_chunks, embedding_type='openai', save_db=False)
                update_vectorstore(upload_vector=upload_vectors, embedding_type='openai')
                return "Vector DB updated successfully."
            except Exception as e:
                return f"Error occurred while updating Vector Database."

        elif upload_flag:  # Create a new vector DB
            try:
                pdf_docs = get_pdf_text(pdf_dir_path=os.getenv('DATASTORE_DIR'))
                document_chunks = get_text_chunks(py_pdf_docs=pdf_docs)
                create_vectorstore(doc_chunks=document_chunks, embedding_type='openai', save_db=True)
                return "FAISS Vector DB created successfully."
            except Exception as e:
                return f"Error occurred while creating Vector Database."

        else:
            return "No file found. Please upload files to ingest."


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
    app.run(host='127.0.0.1', port=8001, debug=True, use_reloader=True)
