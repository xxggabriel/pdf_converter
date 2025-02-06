from services.converters.pdf_html_converter import PdfToHtmlConverter

def main():
    
    pdf_path = '/Users/gabrieloliveiradesouza/Downloads/0010798-95.2019.8.09.0044.pdf'
    output_path = 'sample.html'
    margin_x = 40
    margin_y = 60
    
    PdfToHtmlConverter.convert(pdf_path, output_path, margin_x, margin_y)
    
if __name__ == '__main__':
    main()