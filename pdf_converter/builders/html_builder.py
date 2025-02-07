from typing import Dict, List

from pdf_converter.core.domain.models import PageData
from pdf_converter.core.contracts.ihtml_builder import IHtmlBuilder
from pdf_converter.builders.components.html.table_builder import TableBuilder
from pdf_converter.builders.components.html.list_builder import ListBuilder

from pdf_converter.formatters.html_formatter import HtmlFormatter


class HtmlBuilder(IHtmlBuilder):
    def __init__(self):
        self.html_formatter = HtmlFormatter()
        self.table_builder = TableBuilder()
        self.list_builder = ListBuilder()

    def build(self, pages: List[PageData], metadata: Dict) -> str:
        """Constrói o documento HTML completo a partir dos dados processados"""
        body_content = []
        
        for page in pages:
            page_elements = self._build_page_elements(page)
            page_html = self._wrap_page(page, page_elements)
            body_content.append(page_html)
        
        return self._wrap_document(
            content=''.join(body_content),
            metadata=metadata
        )

    def _build_page_elements(self, page: PageData) -> List[str]:
        """Processa todos os elementos de uma página"""
        elements = []
        
        # Processar tabelas
        elements.extend(
            self.table_builder.build(table) 
            for table in page.tables
        )
        
        # Processar listas
        if page.lists:
            elements.append(
                self.list_builder.build(page.lists)
            )
        
        # Processar blocos de texto
        elements.extend(
            self.html_formatter.format(block)
            for block in page.text_blocks
        )
        
        return elements

    def _wrap_page(self, page: PageData, elements: List[str]) -> str:
        """Cria o container da página com posicionamento absoluto"""
        return f'''
        <div class="page" 
            style="position:relative;
                   width:{page.width}px;
                   height:{page.height}px">
            {''.join(elements)}
        </div>
        '''

    def _wrap_document(self, content: str, metadata: Dict) -> str:
        """Cria a estrutura HTML completa"""
        return f'''
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
                <title>{metadata.get('title', 'PDF Conversion')}</title>
                {self._global_styles()}
            </head>
            <body>
                {content}
            </body>
        </html>
        '''

    def _global_styles(self) -> str:
        """Define os estilos CSS globais"""
        return '''
        <style>
            
        .page {
            position: relative;
            background: white;
            margin: 20px auto;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .line {
            white-space: pre;
            transform-origin: 0% 0%;
        }

        .text-block {
            position: absolute;
        }

        .text-line {
            position: absolute;
            display: inline;
        }

        .pdf-table {
            position: absolute;
            border-collapse: collapse;
        }

        .pdf-table td {
            border: 1px solid #ddd;
            padding: 4px;
        }

        .pdf-list {
            position: absolute;
            list-style-position: inside;
        }
        </style>
        '''
