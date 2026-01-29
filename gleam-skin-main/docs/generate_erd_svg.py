import os

def create_erd_svg():
    width = 1200
    height = 800
    
    # Pastel Color Palette mimicking the reference image
    styles = {
        "blue":   {"header": "#b3e5fc", "body": "#e1f5fe", "stroke": "#81d4fa"}, # Products/Survey
        "green":  {"header": "#c8e6c9", "body": "#e8f5e9", "stroke": "#a5d6a7"}, # Categories/QualTest
        "yellow": {"header": "#fff9c4", "body": "#fffde7", "stroke": "#fff59d"}, # Orders/Response
        "pink":   {"header": "#f8bbd0", "body": "#fce4ec", "stroke": "#f48fb1"}, # Options/RespQual
        "brown":  {"header": "#d7ccc8", "body": "#efebe9", "stroke": "#bcaaa4"}, # Customers/User
    }
    
    c_text_header = "#37474f"
    c_text_body = "#455a64"
    c_line = "#78909c"
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <style>
        .entity-title {{ font-family: 'Segoe UI', sans-serif; font-size: 14px; font-weight: bold; fill: {c_text_header}; text-anchor: middle; }}
        .field-text {{ font-family: 'Consolas', monospace; font-size: 12px; fill: {c_text_body}; }}
        .header-rect {{ stroke-width: 1; }}
        .body-rect {{ stroke-width: 1; }}
        .conn {{ stroke: {c_line}; stroke-width: 1.5; fill: none; }}
    </style>
    <defs>
        <marker id="one" markerWidth="12" markerHeight="12" refX="0" refY="6" orient="auto">
            <path d="M0,6 L12,6 M6,0 L6,12" stroke="{c_line}" stroke-width="1.5" fill="none"/>
        </marker>
        <marker id="many" markerWidth="12" markerHeight="12" refX="0" refY="6" orient="auto">
            <path d="M0,6 L12,6 M12,0 L6,6 L12,12" stroke="{c_line}" stroke-width="1.5" fill="none"/>
        </marker>
    </defs>
    
    <rect width="100%" height="100%" fill="white" />
    <text x="{width/2}" y="40" font-family="Segoe UI" font-size="24" font-weight="bold" fill="#333" text-anchor="middle">Survonica Database Schema</text>
    '''

    def draw_entity(x, y, name, fields, style_key="blue"):
        s = styles.get(style_key, styles["blue"])
        box_width = 200
        header_height = 30
        field_height = 20
        body_height = len(fields) * field_height + 10
        total_height = header_height + body_height
        
        svg_chunk = f'''
        <g transform="translate({x}, {y})">
            <rect x="0" y="0" width="{box_width}" height="{header_height}" fill="{s['header']}" stroke="{s['stroke']}" class="header-rect"/>
            <text x="{box_width/2}" y="20" class="entity-title">{name}</text>
            <rect x="0" y="{header_height}" width="{box_width}" height="{body_height}" fill="{s['body']}" stroke="{s['stroke']}" class="body-rect"/>
        '''
        
        for i, f in enumerate(fields):
            fy = header_height + 18 + (i * field_height)
            parts = f.split(" ", 1)
            if len(parts) == 2 and parts[0] in ["PK", "FK"]:
                chunk = f'<tspan font-weight="bold">{parts[0]}</tspan> {parts[1]}'
            else:
                chunk = f
            svg_chunk += f'<text x="10" y="{fy}" class="field-text">{chunk}</text>'
            
        svg_chunk += '</g>'
        
        return svg_chunk, {
            "x": x, "y": y, "w": box_width, "h": total_height,
            "t": (x + box_width/2, y),
            "r": (x + box_width, y + total_height/2),
            "b": (x + box_width/2, y + total_height),
            "l": (x, y + total_height/2)
        }

    # Entities
    svg += draw_entity(100, 100, "User", ["PK id", "username", "email", "password_hash"], "brown")[0]
    p_user = {"r": (300, 100 + (30+90)/2)} # Approx center right
    
    svg += draw_entity(450, 80, "Survey", ["PK id", "FK user_id", "title", "questions (JSON)", "is_active"], "blue")[0]
    p_survey = {"l": (450, 80 + (30+110)/2), "r": (650, 80 + (30+110)/2), "b": (550, 80 + 30 + 110)}
    
    svg += draw_entity(800, 100, "QualificationTest", ["PK id", "FK survey_id", "topic", "time_limit"], "green")[0]
    p_qual = {"l": (800, 100 + (30+90)/2)}
    
    svg += draw_entity(450, 400, "SurveyResponse", ["PK id", "FK survey_id", "email", "responses (JSON)", "score"], "yellow")[0]
    p_resp = {"t": (550, 400), "r": (650, 400 + (30+110)/2)}

    svg += draw_entity(800, 400, "RespondentQual", ["PK id", "FK survey_id", "email", "passed"], "pink")[0]
    p_rq = {"l": (800, 400 + (30+90)/2)}

    # Connectors (Orthogonal-ish)
    def connect_ortho(p1, p2):
        # p1 is (x,y), p2 is (x,y)
        mid_x = (p1[0] + p2[0]) / 2
        return f'<path d="M {p1[0]},{p1[1]} L {mid_x},{p1[1]} L {mid_x},{p2[1]} L {p2[0]},{p2[1]}" class="conn" marker-start="url(#one)" marker-end="url(#many)"/>'

    # User -> Survey
    svg += connect_ortho(p_user["r"], p_survey["l"])
    
    # Survey -> QualTest
    svg += connect_ortho(p_survey["r"], p_qual["l"])
    
    # Survey -> Response
    # Vertical connector
    svg += f'<path d="M {p_survey["b"][0]},{p_survey["b"][1]} L {p_resp["t"][0]},{p_resp["t"][1]}" class="conn" marker-start="url(#one)" marker-end="url(#many)"/>'

    # Survey -> RespQual (Diagonal/Orthogonal)
    # Route from Survey Right to RespQual Left via a path
    p_start = (650, 150) # Approx Survey Right
    p_end = p_rq["l"]
    svg += f'<path d="M {p_start[0]},{p_start[1]} L {725},{p_start[1]} L {725},{p_end[1]} L {p_end[0]},{p_end[1]}" class="conn" marker-start="url(#one)" marker-end="url(#many)"/>'

    svg += "</svg>"
    
    output_path = os.path.join("docs", "images", "entity_relationship_diagram.svg")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(svg)
    print(f"Generated Pastel ERD SVG at {output_path}")

if __name__ == "__main__":
    create_erd_svg()
