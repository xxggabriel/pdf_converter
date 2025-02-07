from pdf_converter.core.domain.models import Table


class MarkdownTableBuilder:
    @staticmethod
    def build(table: Table) -> str:
        """Converte tabela para sintaxe Markdown"""
        if not table.content:
            return ''
            
        md_table = []
        # Cabeçalho
        md_table.append('| ' + ' | '.join(table.content[0]) + ' |')
        # Separador
        md_table.append('| ' + ' | '.join(['---'] * len(table.content[0])) + ' |')
        # Demais linhas
        md_table.extend(
            '| ' + ' | '.join(row) + ' |'
            for row in table.content[1:]
        )
        return '\n'.join(md_table) + '\n'