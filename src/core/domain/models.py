from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class TextSpan:
    text: str
    font: str
    text_height: float
    size: float
    color: int
    flags: int
    origin: Tuple[float, float]

@dataclass
class TextLine:
    spans: List[TextSpan]
    bbox: Tuple[float, float, float, float]

@dataclass
class TextBlock:
    # text: str
    lines: List[TextLine]
    bbox: Tuple[float, float, float, float]
    font_size: float

@dataclass
class Table:
    content: List[List[str]]
    bbox: Tuple[float, float, float, float]

@dataclass
class ListItem:
    text: str
    bbox: Tuple[float, float, float, float]
    list_type: str
    
@dataclass
class PageData:
    width: float
    height: float
    text_blocks: List[TextBlock]
    tables: List[Table]
    lists: List[ListItem]