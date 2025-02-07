from abc import ABC, abstractmethod
from pdf_converter.core.domain.models import TextBlock


class IFormatter(ABC):
    
    @abstractmethod
    def format(self, text_bloco: TextBlock) -> str:
        pass