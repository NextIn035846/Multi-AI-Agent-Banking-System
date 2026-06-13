import logging
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from api.banking_client import BankingAPIClient
from config import settings

logger = logging.getLogger(__name__)

class OnboardingAgent:
    """Agent for handling new account creation and lead generation."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0.6
        )
        
        self.banking_client = BankingAPIClient(
            base_url=settings.banking_api_url,
            api_key=settings.banking_api_key,
            timeout=settings.banking_api_timeout
        )
        
        self.onboarding_template = PromptTemplate(
            input_variables=["query", "slot_state"],
            template="""You are an onboarding assistant helping customers open new accounts.

Customer Query: {query}
Current Slot State: {slot_state}

Guide the customer through the account opening process. Ask for missing information and confirm details."""
        )
    
    def handle_query(self, query: str) -> str:
        """Handle onboarding and new account creation."""
        try:
            logger.info(f"Onboarding Agent handling query: {query}")
            
            # Initialize slot-filling state if not exists
            slot_state = {
                "full_name": None,
                "email": None,
                "phone": None,
                "account_type": None,
                "initial_deposit": None
            }
            
            # Generate response for slot filling
            prompt = self.onboarding_template.format(
                query=query,
                slot_state=str(slot_state)
            )
            response = self.llm.invoke(prompt)
            
            return response.content
        except Exception as e:
            logger.error(f"Error in Onboarding Agent: {str(e)}")
            return f"I encountered an error during onboarding. Error: {str(e)}"
    
    def create_account(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new customer account."""
        try:
            result = self.banking_client.create_account(customer_data)
            logger.info(f"Account created: {result}")
            return result
        except Exception as e:
            logger.error(f"Error creating account: {str(e)}")
            raise
