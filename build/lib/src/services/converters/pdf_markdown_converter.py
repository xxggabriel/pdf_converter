from pdf_converter.formatters.markdown_formatter import MarkdownFormatter
from pdf_converter.processors.pdf_processor import PdfProcessor
from pdf_converter.builders.markdown_builder import MarkdownBuilder
from pdf_converter.handlers.file_handler import FileHandler

class PdfToMarkdownConverter:
    @staticmethod
    def convert(pdf_path: str, output_path: str, margin_x: float, margin_y: float):
        """Coordena o processo de conversão completo"""
        processor = PdfProcessor(margin_x, margin_y, MarkdownFormatter())
        pages, metadata = processor.process(pdf_path)
        
        builder = MarkdownBuilder()
        markdown = builder.build(pages, metadata)
        
        FileHandler.save(markdown, output_path)