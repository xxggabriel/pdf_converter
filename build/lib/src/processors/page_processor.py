from ast import Dict
from typing import Tuple
import fitz
from pdf_converter.core.contracts.ipage_formatter import IFormatter
from pdf_converter.core.domain.models import ListItem, PageData , Table, TextBlock, TextLine, TextSpan
from pdf_converter.formatters.html_formatter import HtmlFormatter
from pdf_converter.detectors.list_detector import ListDetector

class PageProcessor:
    def __init__(self, page, margin_x: float, margin_y: float, formatter: IFormatter):
        self.page = page
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.formatter = formatter

    def process_page(self) -> PageData:
        """Processa uma única página do PDF"""
        page_data = PageData(
            width=self.page.rect.width,
            height=self.page.rect.height,
            text_blocks=[],
            tables=[],
            lists=[]
        )

        self._extract_tables(page_data)
        self._process_text_content(page_data)

        return page_data

    def _extract_tables(self, page_data: PageData):
        """Extrai tabelas da página"""
        tables = self.page.find_tables(
            strategy="lines_strict",
        )
        for table in tables:
            page_data.tables.append(
                Table(
                    content=table.extract(),
                    bbox=table.bbox
                )
            )

    def _process_text_content(self, page_data: PageData):
        """Processa o conteúdo textual da página"""
        boundary = self._calculate_boundary()
        blocks = self.page.get_text("dict", clip=boundary, sort=True)["blocks"]
        text_blocks = []
        for block in blocks:
            if self._is_valid_text_block(block):
                text_blocks.append(
                    self._create_text_block(block)
                )

        for block in text_blocks:

            formatted_text = self.formatter.format(block)
            list_type = ListDetector.detect(block)

            if list_type:
                page_data.lists.append(
                    ListItem(
                        text=formatted_text,
                        bbox=block.bbox,
                        list_type=list_type
                    )
                )
            else:
                page_data.text_blocks.append(
                    block
                )

    def _calculate_boundary(self) -> fitz.Rect:
        """Calcula a área útil da página considerando as margens"""
        page_rect = self.page.rect
        return fitz.Rect(
            page_rect.x0 + self.margin_x,
            page_rect.y0 + self.margin_y,
            page_rect.x1 - self.margin_x,
            page_rect.y1 - self.margin_y
        )

    def _create_text_block(self, block) -> TextBlock:
        """Cria um objeto TextBlock a partir de um bloco processado"""
        
        if not self._is_valid_text_block(block):
            return None
        
        spans = [span for line in block["lines"] for span in line["spans"]]
        return TextBlock(
            bbox=block['bbox'],
            lines=[self._create_text_line(line) for line in block["lines"]]
        )
    def _create_text_line(self, line) -> TextLine:
        """Cria um objeto TextLine a partir de uma linha processada"""
        return TextLine(
            spans=[self._create_text_span(span) for span in line["spans"]],
            bbox=line["bbox"]
        )
        
    def _create_text_span(self, span) -> TextSpan:
        """Cria um objeto TextSpan a partir de um span processado"""
        return TextSpan(
            text=span["text"],
            font=span["font"],
            size=span["size"],
            text_height=span['ascender'] + span['descender'],
            color=span["color"],
            flags=span["flags"],
            origin=(span["bbox"][0], span["bbox"][1])
        )
    @staticmethod
    def _is_valid_text_block(block: Dict) -> bool:
        """Verifica se o bloco é um bloco de texto válido"""
        return block.get('type', 0) == 0 and 'lines' in block