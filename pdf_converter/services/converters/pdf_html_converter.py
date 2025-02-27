from pdf_converter.formatters.html_formatter import HtmlFormatter
from pdf_converter.processors.pdf_processor import PdfProcessor
from pdf_converter.builders.html_builder import HtmlBuilder
from pdf_converter.handlers.file_handler import FileHandler

class PdfToHtmlConverter:
    @staticmethod
    def convert(pdf_path: str, output_path: str, margin_x: float, margin_y: float):
        """Coordena o processo de conversão completo"""
        processor = PdfProcessor(margin_x, margin_y, HtmlFormatter())
        pages, metadata = processor.process(pdf_path)
        
        builder = HtmlBuilder()
        html = builder.build(pages, metadata)
        
        FileHandler.save(html, output_path)