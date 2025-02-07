from formatters.markdown_formatter import MarkdownFormatter
from processors.pdf_processor import PdfProcessor
from builders.markdown_builder import MarkdownBuilder
from handlers.file_handler import FileHandler

class PdfToMarkdownConverter:
    @staticmethod
    def convert(pdf_path: str, output_path: str, margin_x: float, margin_y: float):
        """Coordena o processo de conversão completo"""
        processor = PdfProcessor(margin_x, margin_y, MarkdownFormatter())
        pages, metadata = processor.process(pdf_path)
        
        builder = MarkdownBuilder()
        markdown = builder.build(pages, metadata)
        
        FileHandler.save(markdown, output_path)