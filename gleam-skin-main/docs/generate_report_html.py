import re
import os
import datetime

def convert_md_to_html(md_content):
    html = ""
    toc = []
    lines = md_content.split('\n')
    
    in_list = False
    in_table = False
    
    for line in lines:
        line = line.strip()
        
        # Headers & TOC
        header_match = re.match(r'^(#+)\s+(.*)', line)
        if header_match:
            level = len(header_match.group(1))
            title = header_match.group(2)
            anchor = re.sub(r'[^a-zA-Z0-9]', '-', title.lower())
            toc.append((level, title, anchor))
            
            # Page break before H1 (Chapters), but not the very first one
            page_break = 'style="page-break-before: always;"' if level == 1 and len(toc) > 1 else ''
            html += f'<h{level} id="{anchor}" {page_break}>{title}</h{level}>\n'
            continue
            
        # Images
        img_match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
        if img_match:
            alt = img_match.group(1)
            src = img_match.group(2)
            html += f'<div class="img-container"><img src="{src}" alt="{alt}"><p class="caption">{alt}</p></div>\n'
            continue
            
        # Tables (Simple pipe tables)
        if line.startswith('|'):
            if not in_table:
                html += '<table>\n'
                in_table = True
            
            row = line.strip('|').split('|')
            html += '<tr>'
            for cell in row:
                if '---' in cell: continue # Skip separator lines
                html += f'<td>{cell.strip()}</td>'
            html += '</tr>\n'
            continue
        elif in_table:
            html += '</table>\n'
            in_table = False
            
        # Lists
        if line.startswith('* ') or line.startswith('- '):
            if not in_list:
                html += '<ul>\n'
                in_list = True
            content = line[2:]
            # Bold/Italic parsing
            content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)
            content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', content)
            html += f'<li>{content}</li>\n'
            continue
        elif in_list:
            html += '</ul>\n'
            in_list = False
            
        # Paragraphs
        if line:
            # Formatting
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line)
            line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
            html += f'<p>{line}</p>\n'
            
    return html, toc

def generate_html_report():
    input_file = "Survonica_SRS_Report.md"
    output_file = "Survonica_SRS_Report_Printable.html"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        md_content = f.read()
        
    body_html, toc_data = convert_md_to_html(md_content)
    
    # Generate TOC HTML
    toc_html = '<div class="toc"><h2>Table of Contents</h2><ul>'
    for level, title, anchor in toc_data:
        indent = (level - 1) * 20
        toc_html += f'<li style="margin-left: {indent}px"><a href="#{anchor}">{title}</a></li>'
    toc_html += '</ul></div>'
    
    full_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Survonica SRS Report</title>
        <style>
            body {{
                font-family: "Times New Roman", Times, serif;
                font-size: 12pt;
                line-height: 1.5;
                margin: 0;
                padding: 0;
                background: #f0f0f0;
            }}
            .page {{
                width: 8.5in;
                min-height: 11in;
                margin: 1cm auto;
                padding: 1in;
                background: white;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            @media print {{
                body {{ background: none; }}
                .page {{ margin: 0; box-shadow: none; width: auto; }}
            }}
            h1 {{ font-size: 24pt; text-align: center; margin-top: 2em; margin-bottom: 1em; }}
            h2 {{ font-size: 18pt; margin-top: 1.5em; border-bottom: 1px solid #ccc; }}
            h3 {{ font-size: 14pt; margin-top: 1.2em; }}
            p {{ text-align: justify; margin-bottom: 1em; }}
            ul {{ margin-bottom: 1em; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 1em; }}
            td, th {{ border: 1px solid black; padding: 5px; }}
            .img-container {{ text-align: center; margin: 2em 0; }}
            img {{ max-width: 100%; height: auto; }}
            .caption {{ font-style: italic; font-size: 10pt; color: #555; }}
            .title-page {{ text-align: center; margin-top: 3in; page-break-after: always; }}
            .toc {{ page-break-after: always; }}
            a {{ color: black; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="page">
            <div class="title-page">
                <h1>Survonica: The Intelligent Way to Create and Distribute Surveys</h1>
                <p><strong>Software Requirements Specification</strong></p>
                <p>Generated: {datetime.date.today()}</p>
                <br><br>
                <p><strong>Team Members:</strong> Ahmad Mustafa, Abdul Qadeer</p>
                <p><strong>Supervisor:</strong> Dr. Ali Shahid</p>
                <p><strong>Namal University, Mianwali</strong></p>
            </div>
            
            {toc_html}
            
            {body_html}
        </div>
    </body>
    </html>
    '''
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_html)
    
    print(f"Report generated: {output_file}")

if __name__ == "__main__":
    generate_html_report()
