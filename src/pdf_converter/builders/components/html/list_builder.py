from typing import List
from pdf_converter.core.domain.models import ListItem


class ListBuilder:
    @staticmethod
    def build(items: List[ListItem]) -> str:
        """Constrói listas HTML ordenadas/não ordenadas"""
        if not items:
            return ''
            
        list_type = items[0].list_type
        items_html = ''.join(
            f'<li style="left:{item.bbox[0]}px; top:{item.bbox[1]}px">'
            f'{item.text}</li>' 
            for item in items
        )
        
        return f'''
        <{list_type} class="pdf-list">
            {items_html}
        </{list_type}>
        '''
