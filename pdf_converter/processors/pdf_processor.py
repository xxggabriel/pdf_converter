import fitz
from typing import List, Dict, Tuple

from pdf_converter.core.contracts.ipage_formatter import IFormatter
from pdf_converter.core.domain.models import PageData
from pdf_converter.core.contracts.ipdf_processor import iPdfProcessor
from pdf_converter.processors.page_processor import PageProcessor


class PdfProcessor(iPdfProcessor):
    def __init__(self, margin_x: float, margin_y: float, formatter: IFormatter):
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.formatter = formatter

    def process(self, pdf_path: str) -> Tuple[List[PageData], Dict]:
        """Processa o PDF e retorna dados estruturados e metadados"""
        doc = fitz.open(pdf_path)
        pages_data = []

        for page in doc:
            page_processor = PageProcessor(page, self.margin_x, self.margin_y, self.formatter)
            pages_data.append(page_processor.process_page())

        return pages_data, doc.metadata

