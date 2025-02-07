
from pdf_converter.core.contracts.ifile_handler import IFileHandler

class FileHandler(IFileHandler):
    @staticmethod
    def save(content: str, output_path: str):
        """Salva o conteúdo em arquivo"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)