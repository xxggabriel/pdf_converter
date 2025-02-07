import re
from core.domain.models import TextBlock

class ListDetector:
    LIST_PATTERNS = {
        'ul': re.compile(r'^[\u2022\u2023\u25E6•]'),
        'ol': re.compile(r'^\d+\.')
    }

    @staticmethod
    def detect(block: TextBlock) -> str:
        """Detecta se o bloco é um item de lista"""
        if len(block.lines) == 0 or len(block.lines[0].spans) == 0:
            return ''

        first_span = block.lines[0].spans[0]
        text = first_span.text.strip()

        for list_type, pattern in ListDetector.LIST_PATTERNS.items():
            if pattern.match(text):
                return list_type
        return ''