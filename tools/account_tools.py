"""Tools for account-related operations."""
import logging
from typing import Optional, Dict, Any
from api.banking_client import BankingAPIClient

logger = logging.getLogger(__name__)

class AccountTools:
    """Tools for managing customer accounts."""
    
    def __init__(self, banking_client: BankingAPIClient):
        self.banking_client = banking_client
    
    def get_balance(self, account_id: Optional[str] = None) -> str:
        """Get account balance."""
        try:
            result = self.banking_client.get_account_balance(account_id)
            if "error" in result:
                return f"Error: {result['error']}"
            return f"Your account balance is ${result.get('balance', 0):.2f}"
        except Exception as e:
            logger.error(f"Error getting balance: {str(e)}")
            return f"Unable to retrieve balance: {str(e)}"
    
    def get_details(self, account_id: Optional[str] = None) -> str:
        """Get detailed account information."""
        try:
            result = self.banking_client.get_account_details(account_id)
            if "error" in result:
                return f"Error: {result['error']}"
            
            details_str = "Account Details:\n"
            for key, value in result.items():
                details_str += f"  {key}: {value}\n"
            return details_str
        except Exception as e:
            logger.error(f"Error getting account details: {str(e)}")
            return f"Unable to retrieve account details: {str(e)}"
