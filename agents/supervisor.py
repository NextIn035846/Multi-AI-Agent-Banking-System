import logging
from typing import Dict, Any, Optional
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from agents.rag_specialist import RAGSpecialist
from agents.core_banking import CoreBankingAgent
from agents.onboarding import OnboardingAgent
from agents.fallback import FallbackAgent
from config import settings

logger = logging.getLogger(__name__)

class SupervisorAgent:
    """Central routing agent that coordinates all specialist agents."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=settings.openai_temperature
        )
        
        # Initialize specialist agents
        self.rag_specialist = RAGSpecialist()
        self.core_banking = CoreBankingAgent()
        self.onboarding = OnboardingAgent()
        self.fallback = FallbackAgent()
        
        # Initialize routing template
        self.routing_template = PromptTemplate(
            input_variables=["query"],
            template="""You are an intelligent routing supervisor for a banking system. 
Analyze the customer query and determine which specialist agent should handle it.

Possible agents:
1. RAG_SPECIALIST - For questions about policies, FAQs, products, and general banking information
2. CORE_BANKING - For account details, transaction history, balances, and account management
3. ONBOARDING - For new account creation, lead generation, and registration
4. FALLBACK - For complex issues or when other agents cannot help

Query: {query}

Respond with ONLY the agent name (e.g., RAG_SPECIALIST) and a confidence score (0-1).
Format: AGENT_NAME|confidence_score"""
        )
    
    def route_query(self, query: str) -> str:
        """Route query to appropriate agent and return response."""
        try:
            logger.info(f"Supervisor routing query: {query}")
            
            # Get routing decision
            routing_prompt = self.routing_template.format(query=query)
            routing_response = self.llm.invoke(routing_prompt)
            routing_text = routing_response.content.strip()
            
            # Parse routing response
            parts = routing_text.split("|")
            agent_name = parts[0].strip()
            confidence = float(parts[1].strip()) if len(parts) > 1 else 0.5
            
            logger.info(f"Routing decision: {agent_name} (confidence: {confidence})")
            
            # Route to appropriate agent
            if agent_name == "RAG_SPECIALIST":
                response = self.rag_specialist.handle_query(query)
            elif agent_name == "CORE_BANKING":
                response = self.core_banking.handle_query(query)
            elif agent_name == "ONBOARDING":
                response = self.onboarding.handle_query(query)
            else:
                response = self.fallback.handle_query(query)
            
            return response
        except Exception as e:
            logger.error(f"Error in supervisor routing: {str(e)}")
            return self.fallback.handle_query(query)
