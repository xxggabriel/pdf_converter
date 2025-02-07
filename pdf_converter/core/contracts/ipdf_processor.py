from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from pdf_converter.core.domain.models import PageData

class iPdfProcessor(ABC):
    
    @abstractmethod
    def __init__(self, margin_x: float, margin_y: float):
        pass
    
    @abstractmethod
    def process(self, pdf_path: str) -> Tuple[List[PageData], Dict]:
        pass