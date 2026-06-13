import logging
import re
from typing import Dict, Tuple, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class PIIEntity:
    """Represents a PII entity with its mask and original value."""
    entity_type: str
    original: str
    masked: str

class PIIMasker:
    """Handles automatic masking and unmasking of Personally Identifiable Information."""
    
    def __init__(self):
        self.pii_patterns = {
            "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
            "CREDIT_CARD": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
            "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "PHONE": r"\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b",
            "ACCOUNT_NUMBER": r"\b\d{10,12}\b",
            "DOB": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
        }
        
        self.mask_map: Dict[str, str] = {}  # Maps masked values back to original
        self.counter = 0
    
    def mask_input(self, text: str) -> str:
        """Mask PII in user input."""
        try:
            masked_text = text
            self.mask_map.clear()
            
            for pii_type, pattern in self.pii_patterns.items():
                matches = re.finditer(pattern, masked_text)
                for match in matches:
                    original_value = match.group(0)
                    masked_value = self._generate_mask(pii_type)
                    self.mask_map[masked_value] = original_value
                    masked_text = masked_text.replace(original_value, masked_value, 1)
            
            if self.mask_map:
                logger.info(f"Masked {len(self.mask_map)} PII entities")
            
            return masked_text
        except Exception as e:
            logger.error(f"Error masking input: {str(e)}")
            return text
    
    def unmask_output(self, text: str) -> str:
        """Unmask PII in system output."""
        try:
            unmasked_text = text
            for masked, original in self.mask_map.items():
                unmasked_text = unmasked_text.replace(masked, original)
            return unmasked_text
        except Exception as e:
            logger.error(f"Error unmasking output: {str(e)}")
            return text
    
    def _generate_mask(self, pii_type: str) -> str:
        """Generate unique mask for PII value."""
        self.counter += 1
        return f"[{pii_type}_MASKED_{self.counter}]"
    
    def extract_pii_entities(self, text: str) -> list:
        """Extract all PII entities from text."""
        entities = []
        for pii_type, pattern in self.pii_patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                entities.append(PIIEntity(
                    entity_type=pii_type,
                    original=match.group(0),
                    masked=self._generate_mask(pii_type)
                ))
        return entities
