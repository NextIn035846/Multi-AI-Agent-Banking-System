"""Tools for transaction-related operations."""
import logging
from typing import Optional, List, Dict, Any
from api.banking_client import BankingAPIClient

logger = logging.getLogger(__name__)

class TransactionTools:
    """Tools for managing transactions."""
    
    def __init__(self, banking_client: BankingAPIClient):
        self.banking_client = banking_client
    
    def get_recent_transactions(self, limit: int = 10) -> str:
        """Get recent transactions."""
        try:
            transactions = self.banking_client.get_transaction_history(limit=limit)
            if not transactions:
                return "No recent transactions found."
            
            result = "Recent Transactions:\n"
            for txn in transactions:
                result += f"  {txn.get('date', 'N/A')}: {txn.get('description', 'N/A')} - ${txn.get('amount', 0):.2f}\n"
            return result
        except Exception as e:
            logger.error(f"Error getting transactions: {str(e)}")
            return f"Unable to retrieve transactions: {str(e)}"
