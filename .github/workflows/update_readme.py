import re

def update_readme():
    def format_row(cells):
        formatted_cells = '\n                '.join(cells)  
        return f"        <tr>\n            {formatted_cells}\n        </tr>"

    with open('../../README.md', 'r', encoding='utf-8') as file:
        content = file.read()

    # Find the table in the README
    table_pattern = r'<table>.*?</table>'
    table_match = re.search(table_pattern, content, re.DOTALL)
    
    if table_match:
        table = table_match.group(0)
        
        # Count the number of contributor entries
        td_pattern = r'<td[^>]*>(?:(?!</?td>).)*<td[^>]*>.*?</td>.*?</td>'
        # td_pattern = r'<td.*?>.*?</td>'
        table_cells = re.findall(td_pattern, table, re.DOTALL)
        
        # Create rows with exactly 3 cells each
        rows = []
        for i in range(0, len(table_cells), 3):
            row_cells = table_cells[i:i + 3]
            # row = '<tr>' + ''.join(row_cells) + '</tr>'
            rows.append(format_row(row_cells))

        # Join rows and wrap with table and tbody tags
        updated_table = (
            "<table>\n"
            "    <tbody>\n"
            f"{'\n'.join(rows)}\n"
            "    </tbody>\n"
            "</table>"
        )
        
        # Replace the old table with the updated one
        updated_content = content.replace(table_match.group(0), updated_table)
        
        with open('../../README.md', 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print(f"README.md updated successfully. Total rows: {len(rows)}")
    else:
        print("Table not found in README.md")

if __name__ == "__main__":
    update_readme()
