import logging
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from config import settings

logger = logging.getLogger(__name__)

class RAGSpecialist:
    """Agent specializing in FAQ and policy retrieval using RAG."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0.5
        )
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            api_key=settings.openai_api_key,
            model=settings.vector_embedding_model
        )
        
        # Initialize vector store (using Chroma for simplicity)
        try:
            self.vectorstore = Chroma(
                collection_name=settings.vector_db_name,
                embedding_function=self.embeddings,
                persist_directory="./data/vectorstore"
            )
        except Exception as e:
            logger.warning(f"Could not initialize vector store: {e}. Using empty store.")
            self.vectorstore = None
        
        # RAG prompt template
        self.qa_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a helpful banking assistant. Use the provided context to answer the customer's question accurately.

Context: {context}

Question: {question}

Provide a clear, concise answer based on the context. If the context doesn't contain the answer, say 'I don't have that information.'"""
        )
    
    def handle_query(self, query: str) -> str:
        """Handle FAQ and policy-related queries using RAG."""
        try:
            logger.info(f"RAG Specialist handling query: {query}")
            
            if self.vectorstore:
                # Retrieve relevant documents
                docs = self.vectorstore.similarity_search(query, k=3)
                context = "\n".join([doc.page_content for doc in docs])
            else:
                context = "No knowledge base available. "
                logger.warning("Vector store not available, using generic response.")
            
            # Generate response using LLM
            prompt = self.qa_template.format(context=context, question=query)
            response = self.llm.invoke(prompt)
            
            return response.content
        except Exception as e:
            logger.error(f"Error in RAG Specialist: {str(e)}")
            return f"I encountered an error retrieving information: {str(e)}"
