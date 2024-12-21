import re
import os
from typing import List, Optional

def read_file(file_path: str) -> Optional[str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

def write_file(file_path: str, content: str) -> bool:
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except IOError as e:
        print(f"Error writing file: {e}")
        return False

def format_row(cells: List[str]) -> str:
    formatted_cells = '\n            '.join(cells)
    return f"        <tr>\n            {formatted_cells}\n        </tr>"

def extract_table_cells(table: str) -> List[str]:
    td_pattern = r'<td[^>]*>(?:(?!</?td>).)*</td>'
    return re.findall(td_pattern, table, re.DOTALL)

def create_updated_table(rows: List[str]) -> str:
    return (
        "<table>\n"
        "    <tbody>\n"
        f"{os.linesep.join(rows)}\n"
        "    </tbody>\n"
        "</table>"
    )

def update_readme(file_path: str) -> None:
    content = read_file(file_path)
    if content is None:
        return

    table_pattern = r'<table>.*?</table>'
    table_match = re.search(table_pattern, content, re.DOTALL)
    
    if not table_match:
        print("Table not found in README.md")
        return

    table = table_match.group(0)
    table_cells = extract_table_cells(table)
    
    rows = [format_row(table_cells[i:i+3]) for i in range(0, len(table_cells), 3)]
    updated_table = create_updated_table(rows)
    
    updated_content = content.replace(table_match.group(0), updated_table)
    
    if write_file(file_path, updated_content):
        print(f"README.md updated successfully. Total rows: {len(rows)}")
    else:
        print("Failed to update README.md")

if __name__ == "__main__":
    readme_path = os.path.join(os.path.dirname(__file__), '..', '..', 'README.md')
    update_readme(readme_path)