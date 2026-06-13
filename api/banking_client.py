import logging
import aiohttp
import asyncio
from typing import Dict, Any, Optional, List
import requests
from config import settings

logger = logging.getLogger(__name__)

class BankingAPIClient:
    """Client for interacting with banking backend APIs."""
    
    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_account_balance(self, account_id: Optional[str] = None) -> Dict[str, Any]:
        """Fetch account balance."""
        try:
            endpoint = f"{self.base_url}/api/accounts/balance"
            params = {"account_id": account_id} if account_id else {}
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            logger.info(f"Retrieved account balance: {response.json()}")
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching account balance: {str(e)}")
            return {"error": str(e)}
    
    def get_transaction_history(self, account_id: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch transaction history."""
        try:
            endpoint = f"{self.base_url}/api/transactions"
            params = {
                "limit": limit,
                "account_id": account_id
            }
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            logger.info(f"Retrieved {len(response.json())} transactions")
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching transaction history: {str(e)}")
            return []
    
    def get_account_details(self, account_id: Optional[str] = None) -> Dict[str, Any]:
        """Fetch account details."""
        try:
            endpoint = f"{self.base_url}/api/accounts/details"
            params = {"account_id": account_id} if account_id else {}
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            logger.info(f"Retrieved account details")
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching account details: {str(e)}")
            return {"error": str(e)}
    
    def create_account(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new account."""
        try:
            endpoint = f"{self.base_url}/api/accounts/create"
            
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=customer_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            logger.info(f"Account created successfully")
            return response.json()
        except Exception as e:
            logger.error(f"Error creating account: {str(e)}")
            return {"error": str(e)}
    
    def health_check(self) -> bool:
        """Check if banking API is healthy."""
        try:
            endpoint = f"{self.base_url}/health"
            response = requests.get(endpoint, timeout=self.timeout)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False
