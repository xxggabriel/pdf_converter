

import pytest
from formatters.markdown_formatter import AdvancedMarkdownFormatter, MarkdownFormatter
from core.domain.models import ListItem, PageData, Table, TextBlock, TextLine, TextSpan
from builders.markdown_builder import MarkdownBuilder
from builders.components.markdown.list_builder import MarkdownListBuilder
from builders.components.markdown.table_builder import MarkdownTableBuilder


# Fixtures
@pytest.fixture
def sample_table():
    return Table(
        content=[
            ["Header 1", "Header 2"],
            ["Row 1 Col 1", "Row 1 Col 2"],
            ["Row 2 Col 1", "Row 2 Col 2"]
        ],
        bbox=(0, 0, 100, 100)
    )

@pytest.fixture
def sample_list_items():
    return [
        ListItem(text="First item", list_type="ul", bbox=(10, 20, 100, 30)),
        ListItem(text="Second item", list_type="ul", bbox=(10, 40, 100, 50))
    ]

@pytest.fixture
def sample_text_block():
    return TextBlock(
        lines=[
            TextLine(
                spans=[
                    TextSpan(
                        text="Hello ",
                        font="Arial",
                        size=12,
                        text_height=.80,
                        color=0,
                        flags=0,
                        origin=(0, 0)
                    ),
                    TextSpan(
                        text="World",
                        font="Arial",
                        size=12,
                        text_height=.80,
                        color=0,
                        flags=2**4,  # Bold
                        origin=(50, 0)
                    )
                ],
                bbox=(0, 0, 100, 10)
            )
        ],
        bbox=(0, 0, 100, 10)
    )

# Tests for MarkdownTableBuilder
def test_table_builder_empty():
    table = Table(content=[], bbox=(0,0,0,0))
    result = MarkdownTableBuilder.build(table)
    assert result == ""

def test_table_builder_with_header(sample_table):
    expected = """
| Header 1 | Header 2 |
| --- | --- |
| Row 1 Col 1 | Row 1 Col 2 |
| Row 2 Col 1 | Row 2 Col 2 |
""".strip()
    result = MarkdownTableBuilder.build(sample_table).strip()
    assert result == expected

# Tests for MarkdownListBuilder
def test_list_builder_empty():
    result = MarkdownListBuilder.build([])
    assert result == ""

def test_unordered_list(sample_list_items):
    expected = """
- First item
- Second item
""".strip()
    result = MarkdownListBuilder.build(sample_list_items).strip()
    assert result == expected

def test_ordered_list():
    items = [ListItem(text="Item 1", list_type="ol", bbox=(0,0,0,0))]
    result = MarkdownListBuilder.build(items).strip()
    assert result == "1. Item 1"

# Tests for MarkdownFormatter
def test_text_formatter_basic(sample_text_block):
    expected = "Hello **World**\n\n"
    result = MarkdownFormatter.format(sample_text_block)
    assert result == expected

def test_text_formatter_italic():
    block = TextBlock(
        lines=[
            TextLine(
                spans=[
                    TextSpan(
                        text="Italic text",
                        flags=2**1,  # Italic
                        font="Arial",
                        size=12,
                        text_height=.80,
                        color=0,
                        origin=(0,0)
                    )
                ],
                bbox=(0,0,0,0)
            )
        ],
        bbox=(0,0,0,0)
    )
    result = MarkdownFormatter.format(block).strip()
    assert result == "*Italic text*"

# Tests for AdvancedMarkdownFormatter
# def test_code_block_detection():
#     block = TextBlock(
#         lines=[
#             TextLine(
#                 spans=[
#                     TextSpan(
#                         text="console.log('Hello');",
#                         font="Courier",
#                         flags=0,
#                         size=12,
#                         text_height=.80,
#                         color=0,
#                         origin=(0,0)
#                     )
#                 ],
#                 bbox=(0,0,0,0)
#             )
#         ],
#         bbox=(0,0,0,0)
#     )
#     expected = "```\nconsole.log('Hello');\n\n```\n"
#     result = AdvancedMarkdownFormatter.format(block)
#     assert result == expected

# def test_blockquote_detection():
#     block = TextBlock(
#         lines=[
#             TextLine(
#                 spans=[TextSpan(text="Quote text", flags=0)],
#                 bbox=(60, 0, 100, 10)  # Margem esquerda > 50
#             )
#         ],
#         bbox=(60,0,100,10)
#     )
#     expected = "> Quote text\n\n"
#     result = AdvancedMarkdownFormatter.format(block)
#     assert result == expected

# Tests for MarkdownBuilder
def test_full_document_build(sample_table, sample_list_items, sample_text_block):
    builder = MarkdownBuilder()
    pages = [
        PageData(
            width=595,
            height=842,
            text_blocks=[sample_text_block],
            tables=[sample_table],
            lists=sample_list_items
        )
    ]
    
    result = builder.build(pages, {"title": "Test Document"}).splitlines()
    
    assert "# Test Document" in result[0]
    assert "Hello **World**" in result[2]
    assert "| Header 1 | Header 2 |" in result[4]
    assert "- First item" in result[8]
    assert "---" in result[-1]  # Page separator

def test_empty_page_handling():
    builder = MarkdownBuilder()
    pages = [PageData(width=595, height=842, text_blocks=[], tables=[], lists=[])]
    result = builder.build(pages, {}).splitlines()
    
    assert len(result) == 3  # Header + separator + empty line
    assert "---" in result[-1]

def test_multiple_pages():
    builder = MarkdownBuilder()
    pages = [
        PageData(
            width=595,
            height=842,
            text_blocks=[TextBlock(lines=[], bbox=(0,0,0,0))],
            tables=[],
            lists=[]
        ),
        PageData(
            width=595,
            height=842,
            text_blocks=[TextBlock(lines=[], bbox=(0,0,0,0))],
            tables=[],
            lists=[]
        )
    ]
    
    result = builder.build(pages, {}).splitlines()
    assert result.count("---") == 2  # Two page separators

def test_special_characters_escaping():
    block = TextBlock(
        lines=[
            TextLine(
                spans=[
                    TextSpan(
                        text="Special | Chars *",
                        flags=0,
                        font="Arial",
                        size=12,
                        color=0,
                        origin=(0,0)
                    )
                ],
                bbox=(0,0,0,0)
            )
        ],
        bbox=(0,0,0,0)
    )
    result = MarkdownFormatter.format(block)
    assert "Special \\| Chars \\*" in result