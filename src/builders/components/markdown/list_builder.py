from typing import List
from core.domain.models import ListItem


class MarkdownListBuilder:
    @staticmethod
    def build(items: List[ListItem]) -> str:
        """Converte listas para sintaxe Markdown"""
        list_items = []
        for item in items:
            prefix = '- ' if item.list_type == 'ul' else '1. '
            list_items.append(f"{prefix}{item.text.strip()}")
        return '\n'.join(list_items) + '\n'
