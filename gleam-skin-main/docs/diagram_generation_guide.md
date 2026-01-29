# Diagram Generation Guide

This guide explains how to create, view, and export diagrams for the Survonica project.

## 1. Mermaid Diagrams (Recommended)
We use [Mermaid](https://mermaid.js.org/) for diagrams because it is text-based and easy to version control.

### How to Create
1. Open any `.md` file in the `docs/` folder.
2. Add a code block with the `mermaid` language identifier:
   ```
   ```mermaid
   graph TD
       A[Start] --> B[End]
   ```
   ```

### Supported Diagram Types
- **Flowcharts**: `graph TD` or `graph LR`
- **Sequence Diagrams**: `sequenceDiagram`
- **Class Diagrams**: `classDiagram`
- **Entity Relationship**: `erDiagram`
- **Use Case**: `usecaseDiagram` (Note: use lowercase `usecase`)

### How to View
- **VS Code**: Install the "Markdown Preview Mermaid Support" extension.
- **Online**: Copy your code to the [Mermaid Live Editor](https://mermaid.live/).

---

## 2. Generating High-Quality Images (Python)
Since AI image generation has quotas, we have Python scripts to generate vector graphics (SVG) programmatically.

### Available Scripts
| Script | Diagram | Output |
| :--- | :--- | :--- |
| `docs/generate_use_case_svg.py` | Use Case Diagram | `docs/images/use_case_diagram.svg` |
| `docs/generate_erd_svg.py` | Entity Relationship | `docs/images/entity_relationship_diagram.svg` |
| `docs/generate_dfd_svg.py` | DFD Level 0 | `docs/images/dfd_level_0.svg` |

### How to Run
1. Open your terminal in VS Code.
2. Navigate to the project root.
3. Run the python script:
   ```powershell
   python docs/generate_use_case_svg.py
   ```
4. The image will be saved in `docs/images/`.

### Customizing the Python Scripts
If you want to change colors or layout:
1. Open the `.py` script.
2. Look for the `Colors` section at the top of the function.
3. Edit the `svg += ...` lines to add new shapes or change text.
