
from abc import ABC, abstractmethod
from typing import Dict, List

from core.domain.models import PageData


class IHtmlBuilder(ABC):
    
    @abstractmethod
    def __init__(self, metadata: Dict):
        pass

    @abstractmethod
    def build(self, pages: List[PageData]) -> str:
        pass