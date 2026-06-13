import pytest
from agents.supervisor import SupervisorAgent
from agents.rag_specialist import RAGSpecialist
from security.pii_masking import PIIMasker

class TestSupervisorAgent:
    """Test cases for SupervisorAgent."""
    
    def test_initialization(self):
        agent = SupervisorAgent()
        assert agent is not None
        assert agent.rag_specialist is not None
        assert agent.core_banking is not None

class TestPIIMasking:
    """Test cases for PII masking."""
    
    def test_ssn_masking(self):
        masker = PIIMasker()
        text = "My SSN is 123-45-6789"
        masked = masker.mask_input(text)
        assert "123-45-6789" not in masked
        assert "SSN_MASKED" in masked
    
    def test_email_masking(self):
        masker = PIIMasker()
        text = "Contact me at john@example.com"
        masked = masker.mask_input(text)
        assert "john@example.com" not in masked
    
    def test_phone_masking(self):
        masker = PIIMasker()
        text = "Call me at 555-123-4567"
        masked = masker.mask_input(text)
        assert "555-123-4567" not in masked
