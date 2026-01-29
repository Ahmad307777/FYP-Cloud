import os

def create_use_case_svg():
    width = 1200
    height = 1000
    
    # Colors
    c_actor = "#e3f2fd"
    c_actor_border = "#1565c0"
    c_usecase = "#ffffff"
    c_usecase_border = "#1565c0"
    c_system_bg = "#f5f5f5"
    c_text = "#000000"
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <style>
        .actor-label {{ font-family: 'Segoe UI', sans-serif; font-size: 16px; font-weight: bold; fill: {c_text}; text-anchor: middle; }}
        .uc-label {{ font-family: 'Segoe UI', sans-serif; font-size: 14px; fill: {c_text}; text-anchor: middle; }}
        .sys-label {{ font-family: 'Segoe UI', sans-serif; font-size: 20px; font-weight: bold; fill: #333; }}
        .arrow {{ stroke: #333; stroke-width: 2; fill: none; }}
        .dashed {{ stroke-dasharray: 5,5; }}
    </style>
    <defs>
        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
        </marker>
    </defs>
    
    <rect width="100%" height="100%" fill="white" />
    
    <!-- System Boundary -->
    <rect x="300" y="50" width="600" height="900" fill="{c_system_bg}" stroke="#999" stroke-width="2" rx="10" />
    <text x="600" y="90" class="sys-label" text-anchor="middle">Survonica System</text>
    '''

    # Helper function for Actor Stick Figure
    def draw_actor(x, y, label):
        return f'''
        <circle cx="{x}" cy="{y}" r="20" fill="{c_actor}" stroke="{c_actor_border}" stroke-width="2"/>
        <line x1="{x}" y1="{y+20}" x2="{x}" y2="{y+70}" stroke="{c_actor_border}" stroke-width="2"/>
        <line x1="{x-20}" y1="{y+30}" x2="{x+20}" y2="{y+30}" stroke="{c_actor_border}" stroke-width="2"/>
        <line x1="{x}" y1="{y+70}" x2="{x-20}" y2="{y+110}" stroke="{c_actor_border}" stroke-width="2"/>
        <line x1="{x}" y1="{y+70}" x2="{x+20}" y2="{y+110}" stroke="{c_actor_border}" stroke-width="2"/>
        <text x="{x}" y="{y+130}" class="actor-label">{label}</text>
        '''

    # Actors
    svg += draw_actor(150, 200, "Survey Creator")
    svg += draw_actor(1050, 400, "Respondent")
    
    # External Service (Box instead of stick figure for AI)
    svg += f'''
    <rect x="1000" y="700" width="100" height="60" fill="{c_actor}" stroke="{c_actor_border}" stroke-width="2" rx="5"/>
    <text x="1050" y="735" class="actor-label">AI Service</text>
    '''

    # Use Cases
    use_cases = [
        {"id": "uc1", "y": 150, "label": "Login / Register"},
        {"id": "uc2", "y": 250, "label": "Create Survey (AI)"},
        {"id": "uc3", "y": 350, "label": "Generate Questions"},
        {"id": "uc4", "y": 450, "label": "Detect Redundancy"},
        {"id": "uc5", "y": 550, "label": "Edit Survey (Manual)"},
        {"id": "uc6", "y": 650, "label": "Distribute link"},
        {"id": "uc7", "y": 750, "label": "View Analytics"},
        {"id": "uc8", "y": 850, "label": "Take Survey"},
    ]
    
    cx = 600
    cw = 220
    ch = 60
    
    for uc in use_cases:
        svg += f'''
        <ellipse cx="{cx}" cy="{uc['y']}" rx="{cw/2}" ry="{ch/2}" fill="{c_usecase}" stroke="{c_usecase_border}" stroke-width="2"/>
        <text x="{cx}" y="{uc['y']+5}" class="uc-label">{uc['label']}</text>
        '''

    # Connections (Creator)
    # To Login
    svg += f'<line x1="170" y1="230" x2="{cx-cw/2}" y2="150" class="arrow" />'
    # To AI Create
    svg += f'<line x1="170" y1="230" x2="{cx-cw/2}" y2="250" class="arrow" />'
    # To Edit
    svg += f'<line x1="170" y1="230" x2="{cx-cw/2}" y2="550" class="arrow" />'
    # To Distribute
    svg += f'<line x1="170" y1="230" x2="{cx-cw/2}" y2="650" class="arrow" />'
    # To Analytics
    svg += f'<line x1="170" y1="230" x2="{cx-cw/2}" y2="750" class="arrow" />'

    # Connections (Respondent)
    # To Take Survey
    svg += f'<line x1="1030" y1="430" x2="{cx+cw/2}" y2="850" class="arrow" />'

    # Connections (AI)
    # Cloud interactions (dashed)
    # AI Create includes Generate Qs
    svg += f'<path d="M 600 280 L 600 320" class="arrow dashed" marker-end="url(#arrowhead)"/>'
    svg += f'<text x="610" y="300" font-size="12" fill="#555">&lt;&lt;include&gt;&gt;</text>'
    
    # AI Create includes Detect Redundancy
    svg += f'<path d="M 600 280 L 600 420" class="arrow dashed" marker-end="url(#arrowhead)"/>'
    
    # AI Service linked to Generate Questions
    svg += f'<line x1="1000" y1="730" x2="{cx+cw/2}" y2="350" class="arrow" />'
    
    svg += "</svg>"
    
    output_path = os.path.join("docs", "images", "use_case_diagram.svg")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(svg)
    print(f"Generated SVG at {output_path}")

if __name__ == "__main__":
    create_use_case_svg()
