from typing import List, Dict
from pdf_converter.builders.components.markdown.list_builder import MarkdownListBuilder
from pdf_converter.builders.components.markdown.table_builder import MarkdownTableBuilder
from pdf_converter.core.domain.models import PageData, Table, ListItem, TextBlock
from pdf_converter.formatters.markdown_formatter import MarkdownFormatter

class MarkdownBuilder:
    def __init__(self):
        self.components = {
            'table': MarkdownTableBuilder(),
            'list': MarkdownListBuilder(),
            'text': MarkdownFormatter()
        }

    def build(self, pages: List[PageData], metadata: Dict) -> str:
        """Constrói documento Markdown a partir dos dados processados"""
        md_content = []
        
        # Cabeçalho do documento
        md_content.append(f"# {metadata.get('title', 'PDF Conversion')}\n")
        
        # Conteúdo das páginas
        for page in pages:
            md_content.extend(self._build_page(page))
        
        return '\n'.join(md_content)

    def _build_page(self, page: PageData) -> List[str]:
        """Processa elementos de uma página individual"""
        page_content = []
        
        # Ordem de renderização: Texto -> Tabelas -> Listas
        page_content.extend(
            self.components['text'].format(block)
            for block in page.text_blocks
        )
        
        page_content.extend(
            self.components['table'].build(table)
            for table in page.tables
        )
        
        if page.lists:
            page_content.append(
                self.components['list'].build(page.lists)
            )
        
        return page_content