import datetime
from datetime import timezone
import json
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from preprocessing import get_pdf_text, get_text_chunks
from faiss_vectorstore import create_vectorstore, update_vectorstore
from rag import get_conversation_chain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
import helper
import sys
import logging

app = Flask(__name__)
file_handler = logging.FileHandler(filename='logs.log')
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    handlers=handlers
                    )
logger = logging.getLogger('LOGGER_NAME')

load_dotenv()
logger.info("Environment Variables loaded.")

with app.app_context():
    db, db_connection_status = helper.init_db()
    logger.info(f"Connection to DB: {db_connection_status.status}")

@app.route("/")
def home():
    return "Successfully started - UDI Research Tool Backend"


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No File Found!"
        try:
            uploaded_files = request.files.getlist("file")  # Get a list of uploaded files
            for file in uploaded_files:
                pdf_name = file.filename
                save_path = os.path.join(os.getenv('UPLOAD_DIR'), pdf_name)
                file.save(save_path)
            return jsonify(status=200, success=True, message='File uploaded successfully.')
        except Exception as e:
            return jsonify(status=500, success=False, message=e)


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
                return jsonify(status=200, success=True, message='Vector DB updated successfully.')
            except Exception as e:
                return jsonify(status=500, success=False, message='Error occurred while updating Vector Database.')

        elif upload_flag:  # Create a new vector DB
            try:
                pdf_docs = get_pdf_text(pdf_dir_path=os.getenv('DATASTORE_DIR'))
                document_chunks = get_text_chunks(py_pdf_docs=pdf_docs)
                create_vectorstore(doc_chunks=document_chunks, embedding_type='openai', save_db=True)
                return jsonify(status=200, success=True, message='Vector DB created successfully.')
            except Exception as e:
                return jsonify(status=500, success=False, message='Error occurred while creating Vector Database.')

        else:
            return jsonify(status=500, success=False, message='No file found. Please upload files to ingest.')


@app.route("/fetch", methods=['GET'])
# ! TODO:Add params: embedding, vectordb
def fetch():
    if request.method == 'GET':
        # Fetch all the filenames in the database and return the list
        with open(os.path.join(os.getenv('VECTORDB_OPENAI_FAISS'), 'faiss_files.txt'), 'r') as f:
            faiss_files = f.read()
        return jsonify(faiss_files)


@app.route("/generate", methods=['POST'])
# ! TODO: Add params: model_type, vectordb.
# ! TODO: Option to reset conversation.
# ! TODO: Add chat history
def generate():
    if request.method == 'POST':
        if request.form.get('query'):
            logger.info(f"Query: {request.form.get('query')}")
            chat_history = ''
            # RAG system using the input query - without chat history
            embedding = OpenAIEmbeddings()
            vectordb = FAISS.load_local(os.getenv('VECTORDB_OPENAI_FAISS'), embeddings=embedding)
            conversation_chain = get_conversation_chain(vectorstore=vectordb, model_type='openai')
            response = conversation_chain({"question": request.form.get('query'), "chat_history": chat_history})
            response["source_documents"][0].metadata['page'] += 1
            response["source_documents"][0].metadata['source'] = response["source_documents"][0].metadata['source'][19:]
            answer = f'{response["answer"]} \n\n Source: {response["source_documents"][0].metadata}'
            db.insert_one({
                "question": request.form.get('query'),
                "answer": response["answer"],
                "metadata": response["source_documents"][0].metadata,
                "timestamp": datetime.datetime.now(timezone.utc)
            })
            logger.info(f"Answer: {json.dumps(answer)}")

            return jsonify(answer)
        else:
            return jsonify("Please type your question.")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001, debug=True, use_reloader=True)
