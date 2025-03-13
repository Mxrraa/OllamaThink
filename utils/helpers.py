def format_timestamp(timestamp):
    """Format timestamp for display"""
    return timestamp.strftime("%H:%M")


def extract_code_blocks(text):
    """Extract code blocks from markdown text"""
    import re

    code_blocks = []
    text_blocks = []

    # Pattern for code blocks with optional language specifier
    pattern = r'```(.*?)```'

    # Split text by code blocks
    parts = re.split(pattern, text, flags=re.DOTALL)

    for i, part in enumerate(parts):
        if i % 2 == 0:  # Even indices are regular text
            if part.strip():
                text_blocks.append(part)
        else:  # Odd indices are code blocks
            # Check if first line specifies language
            lines = part.split('\n')
            if len(lines) > 1 and not lines[0].strip().startswith(' '):
                code_blocks.append((lines[0].strip(), '\n'.join(lines[1:])))
            else:
                code_blocks.append(('', part))

    return text_blocks, code_blocks


def create_empty_init_files():
    """Create empty __init__.py files for Python package structure"""
    import os

    dirs = ['config', 'ui', 'services', 'utils']
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        init_file = os.path.join(dir_name, '__init__.py')