from services.converters.pdf_html_converter import PdfToHtmlConverter
from services.converters.pdf_markdown_converter import PdfToMarkdownConverter

def main():
    
    pdf_path = '/Users/gabrieloliveiradesouza/Downloads/0010798-95.2019.8.09.0044.pdf'
    output_path = 'sample.md'
    margin_x = 40
    margin_y = 60
    
    # PdfToHtmlConverter.convert(pdf_path, output_path, margin_x, margin_y)
    PdfToMarkdownConverter.convert(pdf_path, output_path, margin_x, margin_y)
    
if __name__ == '__main__':
    main()