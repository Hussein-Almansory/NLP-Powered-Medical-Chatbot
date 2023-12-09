# Medical Chatbot

## Introduction
Welcome to the Medical Chatbot project! This Python application leverages Natural Language Processing (NLP) techniques and Artificial Intelligence to provide accurate preliminary diagnoses based on user-input symptoms. The chatbot extracts information from medical PDFs and uses two advanced language models, ChatOpenAI and Flan-T5-SMALL, for effective communication.

## Table of Contents
1. [Introduction](#introduction)
2. [How It Works](#how-it-works)
3. [Project Structure](#project-structure)
4. [Getting Started](#getting-started)
5. [Dependencies](#dependencies)
6. [Usage](#usage)
7. [Contributing](#contributing)
8. [License](#license)

## How It Works
The chatbot operates by processing medical PDFs, extracting relevant information, and utilizing two advanced language models, ChatOpenAI and Flan-T5-SMALL, for generating responses. The LangChain framework facilitates efficient text processing, allowing real-time interaction with users.

## Project Structure
- `main.py`: Entry point for running the Streamlit application.
- `app.py`: Streamlit application code for the chatbot user interface.
- `text_extraction.py`: Module for extracting text from medical PDFs.
- `langchain.py`: Implementation of the LangChain framework for text processing.
- `requirements.txt`: List of Python dependencies.
- `.env.example`: Example template for the environment variables file.

## Getting Started
1. Clone the repository to your local machine.
   ```bash
   git clone https://github.com/yourusername/medical-chatbot.git
   cd medical-chatbot
