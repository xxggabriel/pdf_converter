from core.contracts.ipage_formatter import IFormatter
from core.domain.models import TextBlock


class MarkdownFormatter(IFormatter):
    @staticmethod
    def format(block: TextBlock) -> str:
        """Formata blocos de texto para Markdown com estilos básicos"""
        formatted_text = []
        for line in block.lines:
            line_text = ''
            for span in line.spans:
                text = span.text
                # Aplicar estilos básicos
                if span.flags & 2**1:  # Itálico
                    text = f'*{text}*'
                if span.flags & 2**4:     # Negrito (flags 2**2)
                    text = f'**{text}**'
                line_text += text
            formatted_text.append(line_text)
        
        # Preservar quebras de linha originais
        return '\n'.join(formatted_text) + '\n\n'

class AdvancedMarkdownFormatter(MarkdownFormatter):
    """Extensão com features avançadas de Markdown"""
    
    @staticmethod
    def format(block: TextBlock) -> str:
        """Adiciona suporte a blocos de código e citações"""
        base_text = super().format(block)
        
        # Detectar blocos de código por fonte monospace
        if any(span.font.lower() in ['courier', 'monospace'] for line in block.lines for span in line.spans):
            return f'```\n{base_text}\n```\n'
            
        # Detectar citações por indentação
        if block.bbox[0] > 50:  # Margem esquerda maior
            return '> ' + base_text.replace('\n', '\n> ')
            
        return base_text