import os

def create_dfd_svg():
    width = 1200
    height = 900
    
    # Define Colors
    c_creator = "#e3f2fd"
    c_creator_border = "#1565c0"
    c_system = "#fff3e0"
    c_system_border = "#ef6c00"
    c_respondent = "#e8f5e9"
    c_respondent_border = "#2e7d32"
    c_ai = "#f3e5f5"
    c_ai_border = "#7b1fa2"
    c_text = "#000000"
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <style>
        .label {{ font-family: 'Segoe UI', sans-serif; font-size: 13px; font-weight: 500; fill: {c_text}; }}
        .node-label {{ font-family: 'Segoe UI', sans-serif; font-size: 18px; font-weight: bold; fill: {c_text}; text-anchor: middle; }}
        .arrow {{ stroke-width: 2; fill: none; }}
        .arrow-head {{ fill: #333; }}
        .bg {{ fill: white; }}
    </style>
    <defs>
        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" class="arrow-head"/>
        </marker>
    </defs>

    <!-- Background -->
    <rect width="100%" height="100%" fill="white" />
    '''

    # --- Nodes Definition ---
    # Creator (Top Center)
    cx, cy = 600, 100
    cw, ch = 200, 80
    
    # System (Center)
    sx, sy = 600, 450
    sr = 100
    
    # Respondent (Bottom Left)
    rx, ry = 250, 750
    rw, rh = 200, 80
    
    # AI Service (Bottom Right)
    ax, ay = 950, 750
    aw, ah = 220, 80

    # Draw Nodes
    svg += f'''
    <!-- Creator -->
    <rect x="{cx - cw/2}" y="{cy - ch/2}" width="{cw}" height="{ch}" rx="10" fill="{c_creator}" stroke="{c_creator_border}" stroke-width="3"/>
    <text x="{cx}" y="{cy + 5}" class="node-label">Survey Creator</text>

    <!-- System -->
    <circle cx="{sx}" cy="{sy}" r="{sr}" fill="{c_system}" stroke="{c_system_border}" stroke-width="4"/>
    <text x="{sx}" y="{sy - 15}" class="node-label">Survonica</text>
    <text x="{sx}" y="{sy + 10}" class="node-label">System</text>

    <!-- Respondent -->
    <rect x="{rx - rw/2}" y="{ry - rh/2}" width="{rw}" height="{rh}" rx="5" fill="{c_respondent}" stroke="{c_respondent_border}" stroke-width="3"/>
    <text x="{rx}" y="{ry + 5}" class="node-label">Respondent</text>

    <!-- AI -->
    <rect x="{ax - aw/2}" y="{ay - ah/2}" width="{aw}" height="{ah}" fill="{c_ai}" stroke="{c_ai_border}" stroke-dasharray="8,5" stroke-width="3"/>
    <text x="{ax}" y="{ay + 5}" class="node-label">AI Service (Llama)</text>
    '''

    def draw_arrow(x1, y1, x2, y2, label, label_pos_x, label_pos_y, color, c1x=None, c1y=None, c2x=None, c2y=None):
        # Default control points relative to straight line if not provided
        if c1x is None:
            # Simple straight line logic replacement would be here, but we usually want curves
            # Let's enforce passing control points for this specific DFD to ensure shape
            pass
        
        path_d = f"M {x1} {y1} C {c1x} {c1y}, {c2x} {c2y}, {x2} {x2}"
        # Actually use the cubic bezier command
        path_d = f"M {x1} {y1} C {c1x} {c1y} {c2x} {c2y} {x2} {y2}"
        
        # Background for label to make it readable over lines
        lbl_len = len(label) * 7
        bg_rect = f'''<rect x="{label_pos_x - lbl_len/2}" y="{label_pos_y - 10}" width="{lbl_len}" height="14" fill="white" opacity="0.8"/>'''
        
        return f'''
        <path d="{path_d}" stroke="{color}" class="arrow" marker-end="url(#arrowhead)"/>
        {bg_rect}
        <text x="{label_pos_x}" y="{label_pos_y}" class="label" text-anchor="middle" fill="{color}">{label}</text>
        '''

    # --- PORTS ---
    # We distribute points along the bottom of Creator, Top of System, etc.
    
    # Creator Bottom Ports (Left to Right)
    c_p1 = (cx - 60, cy + ch/2) # Login
    c_p2 = (cx - 20, cy + ch/2) # Create
    c_p3 = (cx + 20, cy + ch/2) # Config
    c_p4 = (cx + 60, cy + ch/2) # Define
    
    # Creator Side/Top Ports for returns
    c_r1 = (cx + cw/2, cy)      # Distribute
    c_r2 = (cx + cw/2, cy - 20) # Audit
    c_r3 = (cx + cw/2, cy + 20) # Analytics
    
    # System Ports
    # Top Quadrant (Inputs from Creator)
    s_t1 = (sx - 60, sy - 70) 
    s_t2 = (sx - 20, sy - 85)
    s_t3 = (sx + 20, sy - 85)
    s_t4 = (sx + 60, sy - 70)
    
    # Right Quadrant (Outputs to Creator)
    s_r1 = (sx + 85, sy - 40)
    s_r2 = (sx + 95, sy)
    s_r3 = (sx + 85, sy + 40)
    
    # Left Quadrant (To/From Respondent)
    s_l1 = (sx - 80, sy + 40) # Link
    s_l2 = (sx - 60, sy + 70) # Qual
    s_l3 = (sx - 95, sy)      # Submit (Input)

    # Bottom Quadrant (To/From AI)
    s_b1 = (sx + 40, sy + 80) # To AI
    s_b2 = (sx + 70, sy + 60) # From AI 1
    s_b3 = (sx + 90, sy + 30) # From AI 2
    
    # Respondent Ports
    r_t1 = (rx - 40, ry - rh/2)
    r_t2 = (rx, ry - rh/2)
    r_t3 = (rx + 40, ry - rh/2)
    
    # AI Ports
    a_t1 = (ax - 40, ay - ah/2)
    a_t2 = (ax, ay - ah/2)
    a_t3 = (ax + 40, ay - ah/2)
    
    
    # --- FLOWS ---
    
    # 1. Login (Blue)
    svg += draw_arrow(*c_p1, *s_t1, "1. Login", cx-100, cy+100, "#1565c0", 
                      c1x=cx-60, c1y=cy+150, c2x=sx-60, c2y=sy-150)

    # 2. Create (Blue)
    svg += draw_arrow(*c_p2, *s_t2, "2. Create Survey", cx-30, cy+150, "#1565c0",
                      c1x=cx-20, c1y=cy+100, c2x=sx-20, c2y=sy-120)
                      
    # 3. Config (Blue)
    svg += draw_arrow(*c_p3, *s_t3, "3. Config Visuals", cx+30, cy+150, "#1565c0",
                      c1x=cx+20, c1y=cy+100, c2x=sx+20, c2y=sy-120)

    # 4. Define Test (Blue)
    svg += draw_arrow(*c_p4, *s_t4, "4. Define Test", cx+120, cy+120, "#1565c0",
                      c1x=cx+60, c1y=cy+150, c2x=sx+60, c2y=sy-150)
                      
    # 5. Distribute (Orange)
    svg += draw_arrow(*s_r1, cx+cw/2+20, cy+20, "5. Link", sx+150, sy-60, "#e65100",
                      c1x=sx+180, c1y=sy-80, c2x=cx+200, c2y=cy+50)

    # 6. Quality Audit (Orange)
    svg += draw_arrow(*s_r2, cx+cw/2+20, cy, "6. Audit Flags", sx+180, sy, "#e65100",
                      c1x=sx+220, c1y=sy, c2x=cx+240, c2y=cy)
                      
    # 7. Analytics (Orange)
    svg += draw_arrow(*s_r3, cx+cw/2+20, cy-20, "7. Analytics / 8. Insights", sx+160, sy+60, "#e65100",
                      c1x=sx+200, c1y=sy+80, c2x=cx+220, c2y=cy-50)

    # 9. Survey Link (Green)
    svg += draw_arrow(*s_l1, *r_t1, "9. Survey Link", rx+20, sy+80, "#2e7d32",
                      c1x=sx-120, c1y=sy+80, c2x=rx-40, c2y=ry-150)
                      
    # 10. Qual Test (Green)
    svg += draw_arrow(*s_l2, *r_t2, "10. Qual Test", rx+60, sy+130, "#2e7d32",
                      c1x=sx-80, c1y=sy+120, c2x=rx, c2y=ry-120)
                      
    # 11. Submit (Dark Green)
    svg += draw_arrow(*r_t3, *s_l3, "11. Submit", rx+100, sy+20, "#1b5e20",
                      c1x=rx+40, c1y=ry-100, c2x=sx-150, c2y=sy)


    # 12. Send Prompts (Purple)
    svg += draw_arrow(*s_b1, *a_t1, "12. Prompts", ax-80, sy+100, "#6a1b9a",
                      c1x=sx+60, c1y=sy+120, c2x=ax-100, c2y=ay-150)
                      
    # 13. Generate Qs (Deep Purple)
    svg += draw_arrow(*a_t2, *s_b2, "13. Generate Qs", ax-20, sy+150, "#4a148c",
                      c1x=ax, c1y=ay-120, c2x=sx+100, c2y=sy+100)
                      
    # 14. Visuals (Deep Purple)
    svg += draw_arrow(*a_t3, *s_b3, "14. Visuals / 15. Audit", ax+60, sy+120, "#4a148c",
                      c1x=ax+40, c1y=ay-100, c2x=sx+140, c2y=sy+60)

    svg += "</svg>"
    
    with open("images/dfd_level_0.svg", "w") as f:
        f.write(svg)
    print("Regenerated refined SVG at images/dfd_level_0.svg")

if __name__ == "__main__":
    create_dfd_svg()
