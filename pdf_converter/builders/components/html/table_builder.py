from pdf_converter.core.domain.models import Table


class TableBuilder:
    @staticmethod
    def build(table: Table) -> str:
        """Constrói uma tabela HTML a partir dos dados estruturados"""
        rows = []
        for row in table.content:
            cells = ''.join(f'<td>{cell}</td>' for cell in row)
            rows.append(f'<tr>{cells}</tr>')
        
        return f'''
        <table class="pdf-table" style="left:{table.bbox[0]}px; top:{table.bbox[1]}px">
            {''.join(rows)}
        </table>
        '''