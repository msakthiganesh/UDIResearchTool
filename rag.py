from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain, RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI


def get_conversation_chain(vectorstore, model_type: str = 'openai'):
    if model_type == 'openai':
        llm = ChatOpenAI()
        memory = ConversationBufferMemory(
            memory='chat_history',
            return_messages=True,
            input_key='question',
            output_key='answer'
        )
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory,
            return_source_documents=True
        )
        return conversation_chain
