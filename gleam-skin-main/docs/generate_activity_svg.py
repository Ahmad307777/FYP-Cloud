import os

def create_activity_svg():
    width = 1000
    height = 900
    
    # Colors
    c_lane = "#f8f9fa"
    c_lane_border = "#dee2e6"
    c_lane_text = "#495057"
    
    c_action = "#e3f2fd" # Light Blue
    c_action_border = "#1565c0"
    c_action_text = "#0d47a1"
    
    c_decision = "#fff9c4" # Light Yellow
    c_decision_border = "#fbc02d"
    
    c_start = "#4caf50" # Green
    c_end = "#f44336" # Red
    
    c_line = "#455a64"
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <style>
        .lane-title {{ font-family: 'Segoe UI', sans-serif; font-size: 16px; font-weight: bold; fill: {c_lane_text}; text-anchor: middle; }}
        .node-text {{ font-family: 'Segoe UI', sans-serif; font-size: 13px; fill: {c_action_text}; text-anchor: middle; }}
        .lane-rect {{ fill: {c_lane}; stroke: {c_lane_border}; stroke-width: 2; }}
        .action-rect {{ fill: {c_action}; stroke: {c_action_border}; stroke-width: 1.5; rx: 5; ry: 5; }}
        .decision-poly {{ fill: {c_decision}; stroke: {c_decision_border}; stroke-width: 1.5; }}
        .conn {{ stroke: {c_line}; stroke-width: 1.5; fill: none; }}
        .conn-text {{ font-family: 'Consolas', monospace; font-size: 11px; fill: {c_line}; background-color: white; }}
    </style>
    <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="{c_line}" />
        </marker>
    </defs>
    
    <rect width="100%" height="100%" fill="white" />
    <text x="500" y="30" font-family="Segoe UI" font-size="24" font-weight="bold" text-anchor="middle">Survonica Activity Diagram</text>
    '''

    # --- Draw Swimlanes ---
    lane_width = width / 3
    lanes = ["User (Creator)", "System (AI & Backend)", "Respondent"]
    
    for i, lane in enumerate(lanes):
        x = i * lane_width
        svg += f'''
        <rect x="{x}" y="50" width="{lane_width}" height="{height-50}" class="lane-rect"/>
        <text x="{x + lane_width/2}" y="80" class="lane-title">{lane}</text>
        '''

    # Helper Functions
    def draw_action(x, y, text, w=140, h=50):
        cx = x + w/2
        cy = y + h/2
        return f'''
        <rect x="{x}" y="{y}" width="{w}" height="{h}" class="action-rect"/>
        <text x="{cx}" y="{cy+5}" class="node-text">{text}</text>
        ''', {"t": (cx, y), "r": (x+w, cy), "b": (cx, y+h), "l": (x, cy)}

    def draw_decision(cx, cy, text, size=40):
        # Diamond shape
        points = f"{cx},{cy-size} {cx+size*1.2},{cy} {cx},{cy+size} {cx-size*1.2},{cy}"
        return f'''
        <polygon points="{points}" class="decision-poly"/>
        <text x="{cx}" y="{cy+4}" class="node-text" style="font-size: 11px;">{text}</text>
        ''', {"t": (cx, cy-size), "r": (cx+size*1.2, cy), "b": (cx, cy+size), "l": (cx-size*1.2, cy)}

    def draw_start(cx, cy):
        return f'<circle cx="{cx}" cy="{cy}" r="15" fill="{c_start}" stroke="none"/>', {"b": (cx, cy+15)}

    def draw_end(cx, cy):
        return f'''
        <circle cx="{cx}" cy="{cy}" r="15" fill="none" stroke="{c_end}" stroke-width="4"/>
        <circle cx="{cx}" cy="{cy}" r="8" fill="{c_end}" stroke="none"/>
        ''', {"t": (cx, cy-15)}

    def connect(p1, p2, text="", label_offset=0):
        # Orthogonal routing logic simplified
        mid_y = (p1[1] + p2[1]) / 2
        path = f"M {p1[0]} {p1[1]} L {p1[0]} {mid_y} L {p2[0]} {mid_y} L {p2[0]} {p2[1]}"
        # If strictly vertical
        if abs(p1[0] - p2[0]) < 1:
            path = f"M {p1[0]} {p1[1]} L {p2[0]} {p2[1]}"
            
        label = ""
        if text:
            lx = (p1[0] + p2[0]) / 2 + 5
            ly = mid_y - 5
            if abs(p1[0] - p2[0]) < 1:
                ly = (p1[1] + p2[1]) / 2
                lx = p1[0] + 5
            label = f'<text x="{lx}" y="{ly}" class="conn-text">{text}</text>'
            
        return f'<path d="{path}" class="conn" marker-end="url(#arrow)"/>{label}'

    # Coordinates calculation
    l1_c = lane_width * 0.5
    l2_c = lane_width * 1.5
    l3_c = lane_width * 2.5

    # --- Nodes ---
    
    # Lane 1: User
    svg += draw_start(l1_c, 110)[0]
    s_login, p_login = draw_action(l1_c - 70, 150, "Log In")
    svg += s_login
    s_dash, p_dash = draw_action(l1_c - 70, 230, "Dashboard")
    svg += s_dash
    s_create, p_create = draw_action(l1_c - 70, 310, "Create Survey")
    svg += s_create
    s_method, p_method = draw_decision(l1_c, 410, "AI or Manual?")
    svg += s_method
    
    s_prompt, p_prompt = draw_action(l1_c - 120, 500, "Enter Prompt", w=100) # Left side of lane
    svg += s_prompt
    s_manual, p_manual = draw_action(l1_c + 20, 500, "Manual Draft", w=100) # Right side of lane
    svg += s_manual
    
    # Lane 2: System
    s_gen, p_gen = draw_action(l2_c - 70, 500, "AI Generates\nStructure")
    svg += s_gen
    
    # Back to Lane 1
    s_review, p_review = draw_action(l1_c - 70, 600, "Review & Edit")
    svg += s_review
    s_dist, p_dist = draw_action(l1_c - 70, 680, "Distribute Link")
    svg += s_dist
    
    # Lane 3: Respondent
    s_access, p_access = draw_action(l3_c - 70, 680, "Access Link")
    svg += s_access
    s_qual, p_qual = draw_decision(l3_c, 760, "Qualified?")
    svg += s_qual
    s_fill, p_fill = draw_action(l3_c - 70, 850, "Fill Survey")
    svg += s_fill
    
    # Lane 2: System (Audit)
    s_audit, p_audit = draw_action(l2_c - 70, 850, "AI Trust Audit\n(Score)", h=60)
    svg += s_audit
    
    # Lane 1 (Analytics)
    s_analy, p_analy = draw_action(l1_c - 70, 850, "View Analytics")
    svg += s_analy
    
    svg += draw_end(l1_c, 950)[0] # End in User lane

    # --- Connections ---
    svg += connect((l1_c, 125), p_login["t"]) # Start -> Login
    svg += connect(p_login["b"], p_dash["t"])
    svg += connect(p_dash["b"], p_create["t"])
    svg += connect(p_create["b"], p_method["t"])
    
    # Decisions
    svg += connect(p_method["l"], p_prompt["t"], "AI Chat")
    svg += connect(p_method["r"], p_manual["t"], "Manual")
    
    # Cross Lane: User Prompt -> System AI
    svg += f'<path d="M {p_prompt["r"][0]} {p_prompt["r"][1]} L {p_gen["l"][0]} {p_gen["l"][1]}" class="conn" marker-end="url(#arrow)"/>'
    
    # System Gen -> User Review
    svg += f'<path d="M {p_gen["b"][0]} {p_gen["b"][1]} L {p_gen["b"][0]} 580 L {l1_c} 580 L {p_review["t"][0]} {p_review["t"][1]}" class="conn" marker-end="url(#arrow)"/>'
    
    # Manual -> Review
    svg += f'<path d="M {p_manual["b"][0]} {p_manual["b"][1]} L {p_manual["b"][0]} 580 L {l1_c} 580 L {p_review["t"][0]} {p_review["t"][1]}" class="conn" marker-end="url(#arrow)"/>'

    svg += connect(p_review["b"], p_dist["t"])
    
    # User Distribute -> Respondent Access
    svg += f'<path d="M {p_dist["r"][0]} {p_dist["r"][1]} L {p_access["l"][0]} {p_access["l"][1]}" class="conn" marker-end="url(#arrow)"/>'
    
    svg += connect(p_access["b"], p_qual["t"])
    
    # Qual Logic
    svg += connect(p_qual["b"], p_fill["t"], "Yes")
    # No path? End.
    
    # Fill -> Audit
    svg += f'<path d="M {p_fill["l"][0]} {p_fill["l"][1]} L {p_audit["r"][0]} {p_audit["r"][1]}" class="conn" marker-end="url(#arrow)"/>'
    
    # Audit -> Analytics
    svg += f'<path d="M {p_audit["l"][0]} {p_audit["l"][1]} L {p_analy["r"][0]} {p_analy["r"][1]}" class="conn" marker-end="url(#arrow)"/>'
    
    # Analytics -> End
    svg += f'<path d="M {p_analy["b"][0]} {p_analy["b"][1]} L {l1_c} 935" class="conn" marker-end="url(#arrow)"/>'

    svg += "</svg>"
    
    output_path = os.path.join("docs", "images", "activity_diagram.svg")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(svg)
    print(f"Generated SVG at {output_path}")

if __name__ == "__main__":
    create_activity_svg()
