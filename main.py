import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
import os 
import pyttsx3


def load_pdf_files_from_directory(directory):
    pdf_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".pdf")]
    return pdf_files

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    
    # The best one
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,  
        max_tokens=150
    )
    
    # Normal results 
    # llm = ChatOpenAI(
    #     model_name="gpt-3.5-turbo-1106",
    #     temperature=0.9,  # Example hyperparameter, you can customize these values
    #     max_tokens=150# Example hyperparameter, you can customize these values
    # )
    
    # From google bad results
    # llm = HuggingFaceHub(repo_id="google/flan-t5-small", 
    #                      model_kwargs={"temperature":0.5, 
    #                                    "max_length":512})

    
    # Memory configuration remains the same
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    print(f"Before conversation call: st.session_state.conversation={st.session_state.conversation}")
    
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    # Initialize text-to-speech engine with slower rate
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust the rate value as needed

    for i, message in enumerate(st.session_state.chat_history):
        print(f"Processing message {i}: {message.content}")

        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            bot_response = bot_template.replace("{{MSG}}", message.content)
            st.write(bot_response, unsafe_allow_html=True)

            # Add text-to-speech for the bot's response
            engine.say(message.content)
            engine.runAndWait()

    print("After conversation call")


def main():
    load_dotenv()
    
    st.set_page_config(page_title="Medical ChatBot 🩺",
                       page_icon="🩺")
    
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Medical ChatBot 🩺")
    user_question = st.text_input("What can I help you? ")
    if user_question:
        handle_userinput(user_question)

    # Load PDF files directly from a local directory
    pdf_directory = ".\data"
    pdf_files = load_pdf_files_from_directory(pdf_directory)

    # Process the PDF files
    raw_text = get_pdf_text(pdf_files)
    text_chunks = get_text_chunks(raw_text)
    
    # Check if vectorstore and conversation_chain need to be created
    if "conversation" not in st.session_state or st.session_state.conversation is None:
        vectorstore = get_vectorstore(text_chunks)
        st.session_state.conversation = get_conversation_chain(vectorstore)

if __name__ == '__main__':
    main()
    
    