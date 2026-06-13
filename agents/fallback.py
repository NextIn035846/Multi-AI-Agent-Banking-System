import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config import settings

logger = logging.getLogger(__name__)

class FallbackAgent:
    """Fallback agent for handling escalations and complex queries."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0.7
        )
        
        self.escalation_template = PromptTemplate(
            input_variables=["query"],
            template="""You are a helpful banking support agent handling escalated queries.

Customer Query: {query}

Provide a helpful response or escalation message. If needed, offer to transfer to a human agent."""
        )
    
    def handle_query(self, query: str) -> str:
        """Handle fallback queries and escalations."""
        try:
            logger.info(f"Fallback Agent handling query: {query}")
            
            prompt = self.escalation_template.format(query=query)
            response = self.llm.invoke(prompt)
            
            return response.content
        except Exception as e:
            logger.error(f"Error in Fallback Agent: {str(e)}")
            return "I apologize, but I'm unable to process your request at this moment. Please contact our support team for assistance."
