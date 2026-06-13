import logging
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from api.banking_client import BankingAPIClient
from config import settings

logger = logging.getLogger(__name__)

class CoreBankingAgent:
    """Agent for handling core banking operations (accounts, transactions, etc.)."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0.3
        )
        
        self.banking_client = BankingAPIClient(
            base_url=settings.banking_api_url,
            api_key=settings.banking_api_key,
            timeout=settings.banking_api_timeout
        )
        
        self.response_template = PromptTemplate(
            input_variables=["query", "account_data"],
            template="""You are a banking assistant providing account information.

Customer Query: {query}
Account Data: {account_data}

Provide a helpful response based on the account data. Be concise and accurate."""
        )
    
    def handle_query(self, query: str) -> str:
        """Handle account and transaction queries."""
        try:
            logger.info(f"Core Banking Agent handling query: {query}")
            
            # Extract intent from query
            intent = self._extract_intent(query)
            
            account_data = {}
            if "balance" in intent.lower():
                account_data = self.banking_client.get_account_balance()
            elif "transaction" in intent.lower():
                account_data = self.banking_client.get_transaction_history()
            elif "account" in intent.lower():
                account_data = self.banking_client.get_account_details()
            
            # Generate response
            prompt = self.response_template.format(
                query=query,
                account_data=str(account_data)
            )
            response = self.llm.invoke(prompt)
            
            return response.content
        except Exception as e:
            logger.error(f"Error in Core Banking Agent: {str(e)}")
            return f"I couldn't retrieve your account information. Error: {str(e)}"
    
    def _extract_intent(self, query: str) -> str:
        """Extract intent from query."""
        query_lower = query.lower()
        if any(word in query_lower for word in ["balance", "how much"]):
            return "balance"
        elif any(word in query_lower for word in ["transaction", "history", "recent"]):
            return "transactions"
        elif any(word in query_lower for word in ["account", "details"]):
            return "account_details"
        return "general"
