import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_readmath_icon(size=1024):
    # Render at 2x for supersampling (super crisp antialiasing)
    canvas_size = size * 2
    img = Image.new("RGBA", (canvas_size, canvas_size), (8, 12, 20, 255))
    draw = ImageDraw.Draw(img)

    # 1. Subtle radial background glow in center
    cx, cy = canvas_size // 2, canvas_size // 2
    glow_radius = int(canvas_size * 0.45)
    for r in range(glow_radius, 0, -8):
        alpha = int(35 * (1 - r / glow_radius)**1.5)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(79, 70, 229, alpha))

    # 2. Main Squircle Badge
    # Dimensions: 70% of canvas
    badge_size = int(canvas_size * 0.72)
    b_left = (canvas_size - badge_size) // 2
    b_top = (canvas_size - badge_size) // 2
    b_right = b_left + badge_size
    b_bottom = b_top + badge_size
    corner_radius = int(badge_size * 0.24)

    # Create gradient badge mask and texture
    badge = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(badge)
    
    # Rounded rectangle badge
    b_draw.rounded_rectangle(
        [b_left, b_top, b_right, b_bottom],
        radius=corner_radius,
        fill=(15, 23, 42, 255)
    )

    # Gradient inside badge: Electric Indigo (#4F46E5) -> Cyan (#06B6D4) -> Sky Blue (#38BDF8)
    gradient = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gradient)
    for y in range(b_top, b_bottom):
        factor = (y - b_top) / (b_bottom - b_top)
        # Interpolate between deep indigo and vibrant cyan-violet
        r_col = int(79 * (1 - factor) + 6 * factor)
        g_col = int(70 * (1 - factor) + 182 * factor)
        b_col = int(229 * (1 - factor) + 212 * factor)
        g_draw.line([(b_left, y), (b_right, y)], fill=(r_col, g_col, b_col, 255))

    # Inner badge border highlight
    inner_border = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    ib_draw = ImageDraw.Draw(inner_border)
    ib_draw.rounded_rectangle(
        [b_left, b_top, b_right, b_bottom],
        radius=corner_radius,
        outline=(255, 255, 255, 60),
        width=int(canvas_size * 0.006)
    )

    # Composite badge onto main image
    # Use badge alpha as mask for gradient
    badge_mask = badge.split()[3]
    img.paste(gradient, (0, 0), badge_mask)
    img.paste(inner_border, (0, 0), inner_border)

    # 3. Draw the ReadMath Symbol inside the badge:
    # A Harmonious Synthesis of:
    # - "Read" (Open Book of language / deciphering lines)
    # - "Math" (Dynamic Coordinate Curve & Glowing Apex)
    # - Form factor: An iconic open book with coordinate graph
    sym_draw = ImageDraw.Draw(img)

    # Center coordinates of the symbol
    sym_w = int(badge_size * 0.62)
    sym_h = int(badge_size * 0.48)
    sx = cx
    sy = cy - int(canvas_size * 0.015)

    left_x = sx - sym_w // 2
    right_x = sx + sym_w // 2
    top_y = sy - sym_h // 2
    bot_y = sy + sym_h // 2
    spine_x = sx

    # Book Pages Outline (Thick white/silver strokes)
    stroke_w = int(canvas_size * 0.018)
    
    # Left Page Spine to Outer: curves gently
    # Points for left page: (spine_x, bot_y - 20) -> (left_x, bot_y) -> (left_x, top_y + 40) -> (spine_x, top_y)
    p_spine_top = (spine_x, top_y + int(sym_h * 0.12))
    p_spine_bot = (spine_x, bot_y - int(sym_h * 0.08))

    p_left_top = (left_x, top_y + int(sym_h * 0.22))
    p_left_bot = (left_x, bot_y + int(sym_h * 0.04))

    p_right_top = (right_x, top_y + int(sym_h * 0.22))
    p_right_bot = (right_x, bot_y + int(sym_h * 0.04))

    # Center spine
    sym_draw.line([p_spine_top, p_spine_bot], fill=(255, 255, 255, 240), width=stroke_w)

    # Left Page Boundary
    sym_draw.line([p_spine_top, p_left_top], fill=(255, 255, 255, 240), width=stroke_w)
    sym_draw.line([p_left_top, p_left_bot], fill=(255, 255, 255, 240), width=stroke_w)
    sym_draw.line([p_left_bot, p_spine_bot], fill=(255, 255, 255, 240), width=stroke_w)

    # Right Page Boundary
    sym_draw.line([p_spine_top, p_right_top], fill=(255, 255, 255, 240), width=stroke_w)
    sym_draw.line([p_right_top, p_right_bot], fill=(255, 255, 255, 240), width=stroke_w)
    sym_draw.line([p_right_bot, p_spine_bot], fill=(255, 255, 255, 240), width=stroke_w)

    # Inner Content:
    # 1) Left Page: Text / Reading Lines (The "Read" - 수학은 언어다 / 한글 독해)
    line_stroke = int(canvas_size * 0.012)
    lx1 = left_x + int(sym_w * 0.08)
    lx2 = spine_x - int(sym_w * 0.08)
    
    y_l1 = top_y + int(sym_h * 0.38)
    y_l2 = top_y + int(sym_h * 0.54)
    y_l3 = top_y + int(sym_h * 0.70)

    sym_draw.line([(lx1, y_l1), (lx2 - int(sym_w * 0.06), y_l1)], fill=(224, 231, 255, 220), width=line_stroke)
    sym_draw.line([(lx1, y_l2), (lx2, y_l2)], fill=(224, 231, 255, 220), width=line_stroke)
    sym_draw.line([(lx1, y_l3), (lx1 + int(sym_w * 0.22), y_l3)], fill=(224, 231, 255, 220), width=line_stroke)

    # 2) Right Page: Dynamic Math Function Graph (The "Math" - 그래프 시각화)
    rx1 = spine_x + int(sym_w * 0.08)
    rx2 = right_x - int(sym_w * 0.08)
    
    # Coordinate axis (subtle x-axis)
    axis_y = top_y + int(sym_h * 0.74)
    sym_draw.line([(rx1, axis_y), (rx2, axis_y)], fill=(255, 255, 255, 90), width=int(canvas_size * 0.006))

    # Curve points for a parabola / cubic function curve
    curve_points = []
    num_steps = 30
    for i in range(num_steps + 1):
        t = i / num_steps
        # x goes from rx1 to rx2
        cx_pt = rx1 + t * (rx2 - rx1)
        # Parabola opening downwards or smooth S-curve
        # y = vertex at apex
        cy_pt = (axis_y - int(sym_h * 0.06)) - math.sin(t * math.pi * 0.85) * (sym_h * 0.42)
        curve_points.append((cx_pt, cy_pt))

    # Draw curve
    for i in range(len(curve_points) - 1):
        sym_draw.line([curve_points[i], curve_points[i+1]], fill=(254, 240, 138, 255), width=int(canvas_size * 0.014))

    # Glowing Apex Point on the graph
    apex_idx = int(len(curve_points) * 0.6)
    apex_x, apex_y = curve_points[apex_idx]
    apex_r = int(canvas_size * 0.02)
    # Glow circle
    sym_draw.ellipse([apex_x - apex_r * 1.5, apex_y - apex_r * 1.5, apex_x + apex_r * 1.5, apex_y + apex_r * 1.5], fill=(251, 191, 36, 120))
    sym_draw.ellipse([apex_x - apex_r, apex_y - apex_r, apex_x + apex_r, apex_y + apex_r], fill=(255, 255, 255, 255))

    # 4. Text Below Symbol inside badge: "ReadMath"
    # Clean, elegant typographic mark
    # Downsample using Lanczos
    final_img = img.resize((size, size), Image.Resampling.LANCZOS)
    return final_img

def create_splash_screen(width=1284, height=2778):
    # Full HD splash screen with center icon and philosophy slogan
    splash = Image.new("RGBA", (width, height), (11, 15, 25, 255))
    s_draw = ImageDraw.Draw(splash)

    # Ambient radial background glow
    cx, cy = width // 2, int(height * 0.42)
    glow_radius = int(width * 0.6)
    for r in range(glow_radius, 0, -10):
        alpha = int(40 * (1 - r / glow_radius)**1.8)
        s_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(79, 70, 229, alpha))

    # Center icon (approx 380x380)
    icon_size = int(width * 0.35)
    icon = create_readmath_icon(icon_size)
    splash.paste(icon, (cx - icon_size // 2, cy - icon_size // 2), icon)

    return splash

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    os.makedirs("public/assets", exist_ok=True)

    print("[Generating ReadMath 1024x1024 Icons...]")
    icon_1024 = create_readmath_icon(1024)
    icon_1024.save("assets/icon.png", format="PNG")
    icon_1024.save("assets/adaptive-icon.png", format="PNG")
    icon_1024.save("public/assets/icon.png", format="PNG")
    icon_1024.save("public/assets/adaptive-icon.png", format="PNG")

    # Favicon 64x64
    fav_64 = icon_1024.resize((64, 64), Image.Resampling.LANCZOS)
    fav_64.save("public/assets/favicon.png", format="PNG")

    print("[Generating ReadMath Splash Screen...]")
    splash = create_splash_screen(1284, 2778)
    splash.save("assets/splash.png", format="PNG")
    splash.save("public/assets/splash.png", format="PNG")

    print("[SUCCESS] All ReadMath icons and splash screens generated without root symbols!")
