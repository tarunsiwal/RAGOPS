import os
import logging
import chardet
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import CohereEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI


class Chatbot:
    def __init__(self, document_paths, prompt):
        self.document_paths = document_paths
        self.chat_models = []
        self.prompt = prompt
        for document_path in document_paths:
            self.chat_models.append(self._setup_chat_model(document_path))

    def _read_document(self, document_path):
        with open(document_path, 'rb') as f:
            result = chardet.detect(f.read())
            logging.info(f"Detected encoding for {document_path}: {result['encoding']}")
        encoding = result['encoding'] or 'utf-8'  # Use 'utf-8' as default

        with open(document_path, encoding=encoding, errors='replace') as f:
            doc = f.read()
        return doc

    def _create_text_chunks(self, doc):
        text_splitter = RecursiveCharacterTextSplitter(chunk_overlap=20)
        texts = text_splitter.create_documents([doc])
        return texts

    def _initialize_embeddings(self):
        embeddings = CohereEmbeddings(cohere_api_key=Config.cohere_api_key)
        return embeddings

    def _create_vector_store(self, texts):
        embeddings = self._initialize_embeddings()
        docs = FAISS.from_documents(texts, embeddings)
        return docs

    def _setup_chat_model(self, document_path):
        doc = self._read_document(document_path)
        texts = self._create_text_chunks(doc)
        vector_store = self._create_vector_store(texts)
        llm = ChatOpenAI(openai_api_key=Config.openai_api_key)
        return llm, vector_store

    def _setup_qa_chain(self, llm, vector_store):
        prompt_template = f'{self.prompt}'+"""

            {context}

        Question: {question}

        """
        print(prompt_template)
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain_type_kwargs = {"prompt": PROMPT}
        qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=vector_store.as_retriever())
        return qa

    def respond(self, query):
        responses = []

        for i, (llm, vector_store) in enumerate(self.chat_models):
            qa = self._setup_qa_chain(llm, vector_store)
            response = qa.run(query)
            # responses.append((self.document_paths[i], response))
            responses.append(response)
 
        return responses