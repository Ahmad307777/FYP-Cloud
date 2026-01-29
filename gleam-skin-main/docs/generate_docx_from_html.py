from htmldocx import HtmlToDocx
from docx import Document
import os
import re

def convert_html_to_docx():
    html_file = "Survonica_SRS_Report_Printable.html"
    docx_file = "Survonica_SRS_Report.docx"
    
    if not os.path.exists(html_file):
        print(f"Error: {html_file} not found.")
        return

    # Check/Create output
    document = Document()
    new_parser = HtmlToDocx()
    
    with open(html_file, "r", encoding="utf-8") as f:
        html_string = f.read()
        
    print("Pre-processing HTML to avoid Image errors...")
    
    # Robustly strip images to prevent UnrecognizedImageError with SVGs
    # We replace them with a text note.
    html_safe = re.sub(r'<div class="img-container">.*?</div>', '<p>[<b>Image: DFD Level 0</b> - Please refer to the attached images/dfd_level_0.svg]</p>', html_string, flags=re.DOTALL)
    html_safe = re.sub(r'<img.*?>', '', html_safe) # Safety catch for other images
    
    try:
        new_parser.add_html_to_document(html_safe, document)
        document.save(docx_file)
        print(f"Successfully created {docx_file} (Images replaced with placeholders)")
    except Exception as e:
        print(f"Conversion CRASHED: {e}")

if __name__ == "__main__":
    convert_html_to_docx()
