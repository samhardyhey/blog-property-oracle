from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from llm import llm
from vectore_store.chroma import vectordb
from utils import logger

if __name__ == "__main__":
    logger.info("Welcome to Property Oracle! Please ask me a question.")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(llm, vectordb.as_retriever(), memory=memory)
    while True:
        question = input("n\You: ")
        result = qa({"question": question})
        print(f"\nProperty Oracle: {result['answer']}")

