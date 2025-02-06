from abc import ABC, abstractmethod
from core.domain.models import TextBlock


class IFormatter(ABC):
    
    @abstractmethod
    def format(self, text_bloco: TextBlock) -> str:
        pass