from typing import List, Tuple, Dict
from pdf_converter.core.contracts.ipage_formatter import IFormatter
from pdf_converter.core.domain.models import TextBlock, TextLine, TextSpan


class HtmlFormatter(IFormatter):
    @staticmethod
    def format(block: TextBlock) -> str:
        """Formata um bloco de texto completo para HTML"""
        lines_html = [
            HtmlFormatter._format_line(line, block.bbox) 
            for line in block.lines
        ]
        bx0, by0, bx1, by1 = block.bbox
        
        return f'''
            <div class="text-block" 
                style="
                    left:{bx0}px; 
                    top:{by0}px; 
                    width:{(bx1-bx0)}px; 
                    height:{(by1-by0)}px;
                "
            >
                {"".join(lines_html)}
            </div>
        '''
    
    @staticmethod
    def process_block(block: Dict) -> str:
        """Formata um bloco de texto em HTML"""
        formatted_text = []
        for line in block.get("lines", []):
            line_html = HtmlFormatter._format_line(line, block['bbox'])
            if line_html:
                formatted_text.append(line_html)
        return ''.join(formatted_text).strip()


    @staticmethod
    def _format_line(line: TextLine, block_bbox: Tuple[float, float, float, float]) -> str:
        """Formata uma única linha de texto"""
        spans_html = [HtmlFormatter._format_span(span) for span in line.spans]
        x = line.bbox[0] - block_bbox[0]
        y = line.bbox[1] - block_bbox[1]
        return f'''
        <div class="text-line" style="left:{x}px; top:{y}px">
            {''.join(spans_html)}
        </div>
        '''
        

    @staticmethod
    def _build_span_style(span: TextSpan) -> str:
        """Constrói o estilo CSS para um span"""
        style = [
            f"font-family: {span.font}",
            f"font-size: {span.size}px",
            f"line-height: {span.text_height}px"
        ]

        if span.color:
            style.append(f"color:#{span['color']:06x}")
        if span.flags & 2**1:
            style.append("font-style: italic")
        if span.flags & 2**4:
            style.append("font-weight: bold")

        
        return ';'.join(style)

    @staticmethod
    def _format_span(span: TextSpan) -> str:
        """Formata um span individual com estilos CSS"""
        
        style_str = HtmlFormatter._build_span_style(span)
        return f'<span class="line" style="{style_str}">{span.text}</span>'

