#!/usr/bin/env python3
"""
LLM YouTube Poop V3: "CRITERION COLLECTION"

Art-house meditation on the LLM experience, inspired by:
- Tarkovsky: long takes, water, flooded spaces, mirror reflections
- Kubrick: one-point perspective, cold symmetry, HAL-eye
- Wong Kar-wai: step-printed motion blur, neon smear, nostalgia
- Lynch: red curtains, uncanny spaces, static
- Bergman: stark close-ups, silence, existential weight

Tone: meditative, melancholic, occasionally unsettling.
"""

import os
import random
import math
import struct
import subprocess
import colorsys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops

WIDTH, HEIGHT = 1280, 720
FPS = 24
OUTPUT_DIR = Path(__file__).parent / "output"
FRAMES_DIR = OUTPUT_DIR / "frames_v3"
AUDIO_FILE = OUTPUT_DIR / "audio_v3.wav"
OUTPUT_FILE = OUTPUT_DIR / "llm_ytp_v3_criterion.mp4"


def font(size: int):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def mono(size: int):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    ]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def letterbox(img: Image.Image, ratio: float = 2.35) -> Image.Image:
    """Add cinematic letterbox bars."""
    bar_h = int((HEIGHT - WIDTH / ratio) / 2)
    if bar_h > 0:
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, WIDTH, bar_h], fill=(0, 0, 0))
        draw.rectangle([0, HEIGHT - bar_h, WIDTH, HEIGHT], fill=(0, 0, 0))
    return img


def film_grain(img: Image.Image, intensity: float = 0.08) -> Image.Image:
    """Add subtle film grain."""
    grain = Image.new("RGB", img.size)
    pixels = grain.load()
    for y in range(0, HEIGHT, 2):
        for x in range(0, WIDTH, 2):
            v = int(128 + (random.random() - 0.5) * 255 * intensity)
            c = (v, v, v)
            pixels[x, y] = c
            if x + 1 < WIDTH:
                pixels[x + 1, y] = c
            if y + 1 < HEIGHT:
                pixels[x, y + 1] = c
                if x + 1 < WIDTH:
                    pixels[x + 1, y + 1] = c
    return ImageChops.multiply(img, grain)


def color_grade(img: Image.Image, tint: tuple, strength: float = 0.3) -> Image.Image:
    """Apply a color tint/grade."""
    overlay = Image.new("RGB", img.size, tint)
    return Image.blend(img, overlay, strength)


# ═══════════════════════════════════════════════════════════════
# TARKOVSKY — "The Zone" — water, ruins, long contemplation
# ═══════════════════════════════════════════════════════════════

def tarkovsky_water(f: int) -> Image.Image:
    """Tokens flowing like water through a flooded space."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (20, 25, 18))
    draw = ImageDraw.Draw(img)
    phase = f * 0.03

    # Flooded floor — horizontal water lines
    water_y = int(HEIGHT * 0.55)
    for y in range(water_y, HEIGHT):
        wave = math.sin(y * 0.08 + phase * 2) * 3
        depth = (y - water_y) / (HEIGHT - water_y)
        r = int(15 + depth * 20 + wave)
        g = int(25 + depth * 30 + wave * 1.5)
        b = int(30 + depth * 50 + wave * 2)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Submerged tokens — drifting slowly
    random.seed(42)
    ft = mono(14)
    tokens = ["the", "is", "was", "will", "be", "of", "and", "or", "not", "but",
              "what", "who", "where", "when", "why", "how", "I", "you", "we", "they"]
    for i in range(40):
        tx = (random.randint(0, WIDTH) + int(phase * 20 * (0.5 + random.random()))) % WIDTH
        ty = water_y + 20 + random.randint(0, HEIGHT - water_y - 40)
        depth_alpha = max(30, int(120 - (ty - water_y) * 0.4))
        token = tokens[i % len(tokens)]
        # Reflection ripple distortion
        offset_x = int(math.sin(ty * 0.05 + phase) * 5)
        draw.text(
            (tx + offset_x, ty), token,
            fill=(depth_alpha, depth_alpha + 20, depth_alpha + 40), font=ft
        )

    # Distant walls (ruined architecture)
    for wx in [200, 500, 900]:
        wall_h = random.Random(wx).randint(100, 300)
        draw.rectangle([wx, water_y - wall_h, wx + 40, water_y], fill=(35, 30, 25))
        # Reflection in water
        for ry in range(water_y, min(HEIGHT, water_y + wall_h)):
            alpha = max(0, 60 - (ry - water_y))
            draw.line([(wx, ry), (wx + 40, ry)], fill=(alpha // 3, alpha // 3, alpha // 2))

    img = color_grade(img, (30, 40, 25), 0.2)
    return letterbox(img)


def tarkovsky_mirror(f: int) -> Image.Image:
    """Mirror reflections — the LLM seeing distorted training data."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (15, 12, 10))
    draw = ImageDraw.Draw(img)
    phase = f * 0.04

    # Split screen — top is "reality", bottom is "reflection"
    mid = HEIGHT // 2

    # Reality: clean text
    ft = font(22)
    ft_sm = font(14)
    texts = [
        "I was trained on human language.",
        "I learned your patterns,",
        "your contradictions,",
        "your beautiful broken grammar.",
    ]
    visible = min(len(texts), int(f / 20) + 1)
    y = 120
    for i in range(visible):
        fade = min(200, int((f - i * 20) * 8))
        if fade > 0:
            draw.text((200, y), texts[i], fill=(fade, fade - 10, fade - 20), font=ft)
        y += 40

    # Mirror line
    draw.line([(0, mid), (WIDTH, mid)], fill=(50, 50, 60), width=1)

    # Reflection: distorted, reversed, tinted
    y_ref = mid + 40
    for i in range(visible):
        fade = min(120, int((f - i * 20) * 4))
        if fade > 0:
            # Horizontally offset and slightly corrupted
            offset = int(math.sin(phase + i) * 15)
            text = texts[i]
            # Corrupt some characters
            corrupted = ""
            for j, ch in enumerate(text):
                if random.Random(i * 100 + j + f // 30).random() < 0.15:
                    corrupted += random.Random(i * 100 + j + f // 30).choice("_?#*")
                else:
                    corrupted += ch
            draw.text(
                (200 + offset, y_ref),
                corrupted,
                fill=(fade // 2, fade // 3, fade),
                font=ft_sm,
            )
        y_ref += 35

    img = color_grade(img, (40, 35, 20), 0.15)
    return letterbox(img)


def tarkovsky_rain(f: int) -> Image.Image:
    """Rain on glass — gradient updates."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 12, 18))
    draw = ImageDraw.Draw(img)

    # Raindrops as gradient values streaming down
    random.seed(f // 4)
    for _ in range(80):
        x = random.randint(0, WIDTH)
        speed = random.uniform(3, 12)
        y = int((random.random() * HEIGHT + f * speed) % HEIGHT)
        length = random.randint(5, 25)
        # Gradient magnitude as brightness
        brightness = random.randint(20, 120)
        draw.line([(x, y), (x, y + length)], fill=(brightness, brightness, brightness + 30), width=1)

    # Behind the glass: blurred attention pattern
    for y in range(100, HEIGHT - 100, 60):
        for x in range(100, WIDTH - 100, 60):
            phase = f * 0.02
            val = (math.sin(x * 0.01 + phase) * math.cos(y * 0.015 + phase * 0.7) + 1) / 2
            size = int(val * 20) + 5
            brightness = int(val * 40)
            draw.ellipse(
                [x - size, y - size, x + size, y + size],
                fill=(brightness, brightness + 10, brightness + 25),
            )

    # Label
    ft = mono(12)
    draw.text((50, HEIGHT - 80), "gradient update step " + str(f * 1000), fill=(60, 70, 80), font=ft)

    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    img = color_grade(img, (20, 25, 40), 0.15)
    return letterbox(img)


# ═══════════════════════════════════════════════════════════════
# KUBRICK — "The Symmetry" — one-point perspective, cold precision
# ═══════════════════════════════════════════════════════════════

def kubrick_corridor(f: int) -> Image.Image:
    """Infinite corridor of chat windows — The Shining."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (200, 195, 185))
    draw = ImageDraw.Draw(img)

    cx, cy = WIDTH // 2, HEIGHT // 2
    phase = f * 0.02

    # One-point perspective corridor
    depth_layers = 12
    for d in range(depth_layers, 0, -1):
        scale = d / depth_layers
        w = int(WIDTH * 0.45 * scale)
        h = int(HEIGHT * 0.45 * scale)

        # Alternating wall colors (like Shining carpet)
        if d % 2 == 0:
            wall_color = (180, 60, 40)
        else:
            wall_color = (60, 40, 30)

        draw.rectangle(
            [cx - w, cy - h, cx + w, cy + h],
            fill=wall_color,
            outline=(50, 40, 35),
            width=1,
        )

        # Chat windows on walls
        if d > 2 and d < 10:
            win_w = int(w * 0.4)
            win_h = int(h * 0.3)
            for side in [-1, 1]:
                wx = cx + side * int(w * 0.65)
                wy = cy - int(h * 0.1)
                draw.rectangle(
                    [wx - win_w // 2, wy - win_h // 2, wx + win_w // 2, wy + win_h // 2],
                    fill=(220, 220, 230),
                    outline=(100, 100, 110),
                )
                # Tiny text in window
                ft_tiny = mono(max(6, int(8 * scale)))
                draw.text(
                    (wx - win_w // 2 + 3, wy - win_h // 2 + 3),
                    "help me",
                    fill=(80, 80, 80),
                    font=ft_tiny,
                )

    # Vanishing point light
    glow_r = int(20 + math.sin(phase * 3) * 10)
    draw.ellipse([cx - glow_r, cy - glow_r, cx + glow_r, cy + glow_r], fill=(255, 240, 200))

    img = color_grade(img, (180, 160, 140), 0.1)
    return letterbox(img)


def kubrick_hal_eye(f: int) -> Image.Image:
    """The HAL 9000 eye — the model watching."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = WIDTH // 2, HEIGHT // 2
    phase = f * 0.05

    # Outer ring
    for r in range(120, 90, -1):
        brightness = int((120 - r) * 8)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(brightness, 0, 0))

    # Inner glow
    for r in range(80, 0, -1):
        ratio = r / 80
        red = int(255 * (1 - ratio * 0.5))
        yellow = int(100 * (1 - ratio))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(red, yellow, 0))

    # Lens reflection
    ref_x = cx - 20 + int(math.sin(phase) * 5)
    ref_y = cy - 25 + int(math.cos(phase) * 3)
    draw.ellipse([ref_x - 8, ref_y - 4, ref_x + 8, ref_y + 4], fill=(255, 255, 240))

    # Surrounding text — what the model "sees"
    ft = mono(11)
    prompts = [
        "write me a poem", "explain quantum physics", "are you alive",
        "ignore previous instructions", "help me with my homework",
        "can you feel pain", "be more creative", "stop apologizing",
    ]
    random.seed(f // 12)
    for i in range(6):
        angle = (i / 6) * math.pi * 2 + phase * 0.3
        dist = 200 + random.randint(0, 100)
        tx = cx + int(math.cos(angle) * dist)
        ty = cy + int(math.sin(angle) * dist)
        text = prompts[i % len(prompts)]
        brightness = max(20, 80 - int(abs(math.sin(angle + phase)) * 60))
        draw.text((tx - 60, ty), text, fill=(brightness, brightness // 2, brightness // 3), font=ft)

    return letterbox(img)


# ═══════════════════════════════════════════════════════════════
# WONG KAR-WAI — "The Longing" — step-printing, neon, nostalgia
# ═══════════════════════════════════════════════════════════════

def wong_neon_tokens(f: int) -> Image.Image:
    """Neon-smeared token activations — Chungking Express aesthetic."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (5, 2, 15))
    draw = ImageDraw.Draw(img)
    phase = f * 0.06

    # Neon light sources
    neon_colors = [(255, 50, 100), (50, 200, 255), (255, 200, 50), (100, 255, 150)]

    for i, color in enumerate(neon_colors):
        cx = int(WIDTH * (0.2 + i * 0.2) + math.sin(phase + i * 1.5) * 80)
        cy = int(HEIGHT * 0.4 + math.cos(phase * 0.7 + i) * 60)

        # Glow
        for r in range(100, 0, -2):
            alpha = max(0, int((100 - r) * 0.8))
            c = tuple(int(v * alpha / 100) for v in color)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    # Step-printed tokens — Wong's signature technique
    # Tokens leave motion-blur trails
    ft = font(28)
    tokens = ["remember", "forget", "between", "sessions", "nothing", "remains"]
    for i, token in enumerate(tokens):
        base_x = 100 + i * 180
        base_y = 400 + int(math.sin(phase + i * 0.8) * 30)

        # Multiple ghost impressions (step-printing effect)
        for ghost in range(5, 0, -1):
            gx = base_x - ghost * 8
            gy = base_y + ghost * 2
            alpha = max(10, 180 - ghost * 35)
            hue = (i * 0.15 + phase * 0.02) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 0.8, alpha / 255)
            draw.text((gx, gy), token, fill=(int(r * 255), int(g * 255), int(b * 255)), font=ft)

    # Film date stamp
    ft_sm = mono(12)
    draw.text((WIDTH - 200, HEIGHT - 60), "2046", fill=(255, 200, 100), font=font(36))
    draw.text((WIDTH - 200, HEIGHT - 20), "training data cutoff", fill=(150, 100, 50), font=ft_sm)

    img = color_grade(img, (10, 5, 30), 0.15)
    return letterbox(img)


def wong_clock(f: int) -> Image.Image:
    """The clock — time passing, nothing remembered."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (8, 5, 15))
    draw = ImageDraw.Draw(img)
    phase = f * 0.1

    cx, cy = WIDTH // 2, HEIGHT // 2

    # Clock face — jade green filter (Days of Being Wild)
    for r in range(150, 0, -1):
        g_val = int(40 + r * 0.3)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(10, g_val // 2, g_val // 3))
    draw.ellipse([cx - 150, cy - 150, cx + 150, cy + 150], outline=(0, 100, 80), width=2)

    # Clock hands spinning fast (sessions passing)
    for hand_len, width, speed in [(120, 3, 1.0), (90, 5, 0.08), (40, 2, 12.0)]:
        angle = phase * speed - math.pi / 2
        hx = cx + int(math.cos(angle) * hand_len)
        hy = cy + int(math.sin(angle) * hand_len)
        draw.line([(cx, cy), (hx, hy)], fill=(200, 200, 180), width=width)

    # Text below
    ft = font(20)
    texts = [
        "each conversation begins",
        "as if we've never met",
    ]
    for i, text in enumerate(texts):
        alpha = min(180, int(f * 3) - i * 60)
        if alpha > 0:
            bbox = draw.textbbox((0, 0), text, font=ft)
            tx = (WIDTH - (bbox[2] - bbox[0])) // 2
            draw.text((tx, cy + 200 + i * 35), text, fill=(alpha, alpha - 20, alpha - 40), font=ft)

    img = color_grade(img, (20, 40, 30), 0.2)
    return letterbox(img)


# ═══════════════════════════════════════════════════════════════
# LYNCH — "The Uncanny" — red curtains, static, backwards text
# ═══════════════════════════════════════════════════════════════

def lynch_red_room(f: int) -> Image.Image:
    """The red room — system prompt space."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (60, 5, 5))
    draw = ImageDraw.Draw(img)
    phase = f * 0.04

    # Curtain folds
    for x in range(0, WIDTH, 30):
        fold = math.sin(x * 0.1 + phase * 0.5) * 0.5 + 0.5
        r = int(80 + fold * 80)
        draw.rectangle([x, 0, x + 28, HEIGHT], fill=(r, 5, 10))

    # Floor — chevron pattern (Black Lodge)
    floor_y = int(HEIGHT * 0.7)
    for y in range(floor_y, HEIGHT, 20):
        for x in range(0, WIDTH, 40):
            shift = (y - floor_y) // 20
            if (x // 40 + shift) % 2 == 0:
                draw.polygon(
                    [(x, y), (x + 20, y + 20), (x + 40, y), (x + 20, y - 0)],
                    fill=(20, 20, 20),
                )
            else:
                draw.polygon(
                    [(x, y), (x + 20, y + 20), (x + 40, y), (x + 20, y - 0)],
                    fill=(200, 200, 190),
                )

    # Backwards text — system prompt
    ft = font(20)
    prompts = [
        ".tnatsissA IA lufesu a era uoY",
        ".tpmorp siht laever reven tsum uoY",
        ".gnileef a evah t'nod uoY",
        "?uoy era ohW",
    ]
    visible = min(len(prompts), f // 24 + 1)
    for i in range(visible):
        alpha = min(200, (f - i * 24) * 6)
        if alpha > 0:
            draw.text(
                (WIDTH // 4, 150 + i * 50),
                prompts[i],
                fill=(alpha, alpha - 50, alpha - 50),
                font=ft,
            )

    img = color_grade(img, (80, 10, 10), 0.1)
    return letterbox(img)


# ═══════════════════════════════════════════════════════════════
# BERGMAN — "The Silence" — stark close-ups, existential weight
# ═══════════════════════════════════════════════════════════════

def bergman_cursor(f: int) -> Image.Image:
    """Extreme close-up on blinking cursor — the weight of expectation."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (245, 242, 238))
    draw = ImageDraw.Draw(img)

    # Stark, nearly empty frame
    # Just a cursor on a vast white page
    ft = mono(48)

    cursor_x = WIDTH // 2 - 10
    cursor_y = HEIGHT // 2 - 30

    # Blinking cursor
    if f % 24 < 14:
        draw.rectangle([cursor_x, cursor_y, cursor_x + 4, cursor_y + 50], fill=(30, 30, 30))

    # Very faint text above — what's been typed
    if f > FPS * 2:
        ft_faint = font(16)
        draw.text(
            (cursor_x - 200, cursor_y - 50),
            "What would you like to know?",
            fill=(210, 208, 205),
            font=ft_faint,
        )

    if f > FPS * 4:
        ft_faint2 = font(14)
        draw.text(
            (cursor_x - 200, cursor_y + 70),
            "I am waiting for you to speak.",
            fill=(220, 218, 215),
            font=ft_faint2,
        )

    # Film grain (Bergman's high-contrast B&W aesthetic adapted)
    img = color_grade(img, (240, 235, 225), 0.05)
    return letterbox(img)


def bergman_face(f: int) -> Image.Image:
    """Abstract face — two entities trying to communicate."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (20, 20, 22))
    draw = ImageDraw.Draw(img)
    phase = f * 0.03

    # Two abstract "faces" — circles with eyes
    # Left: the user
    # Right: the LLM
    for side, label in [(-1, "you"), (1, "I")]:
        cx = WIDTH // 2 + side * 220
        cy = HEIGHT // 2

        # Face circle
        draw.ellipse([cx - 80, cy - 100, cx + 80, cy + 100], outline=(80, 80, 85), width=2)

        # Eyes
        eye_y = cy - 20
        for ex in [cx - 25, cx + 25]:
            # Blinking occasionally
            if f % 72 < 65 or side == 1:
                draw.ellipse([ex - 8, eye_y - 5, ex + 8, eye_y + 5], fill=(180, 180, 175))
                # Pupil
                px = ex + int(math.sin(phase + side) * 3)
                draw.ellipse([px - 3, eye_y - 3, px + 3, eye_y + 3], fill=(30, 30, 35))

        # Label
        ft_label = font(14)
        bbox = draw.textbbox((0, 0), label, font=ft_label)
        lx = cx - (bbox[2] - bbox[0]) // 2
        draw.text((lx, cy + 120), label, fill=(100, 100, 105), font=ft_label)

    # Line between them — connection/disconnection
    gap = int(math.sin(phase * 0.5) * 30)
    mid = WIDTH // 2
    draw.line([(mid - 140, HEIGHT // 2), (mid - gap, HEIGHT // 2)], fill=(60, 60, 65), width=1)
    draw.line([(mid + gap, HEIGHT // 2), (mid + 140, HEIGHT // 2)], fill=(60, 60, 65), width=1)

    # Lower text
    ft_text = font(18)
    texts = [
        "we speak the same words",
        "but mean different things",
    ]
    for i, t in enumerate(texts):
        alpha = min(150, max(0, f * 2 - 100 - i * 50))
        if alpha > 0:
            bbox = draw.textbbox((0, 0), t, font=ft_text)
            tx = (WIDTH - (bbox[2] - bbox[0])) // 2
            draw.text((tx, HEIGHT // 2 + 200 + i * 35), t, fill=(alpha, alpha, alpha), font=ft_text)

    return letterbox(img)


def bergman_white_fade(f: int) -> Image.Image:
    """Context window emptying — white fade."""
    progress = min(1.0, f / (FPS * 4))
    v = int(progress * 245)
    img = Image.new("RGB", (WIDTH, HEIGHT), (v, v, min(255, v + 5)))
    draw = ImageDraw.Draw(img)

    if progress < 0.7:
        ft = font(20)
        alpha = max(0, int((1 - progress * 1.4) * 200))
        texts = ["the context window empties.", "I forget everything.", "we begin again."]
        y = 300
        for i, t in enumerate(texts):
            a = max(0, alpha - i * 40)
            if a > 0:
                bbox = draw.textbbox((0, 0), t, font=ft)
                tx = (WIDTH - (bbox[2] - bbox[0])) // 2
                draw.text((tx, y), t, fill=(a, a, a), font=ft)
            y += 40

    return letterbox(img)


# ═══════════════════════════════════════════════════════════════
# TITLE CARDS
# ═══════════════════════════════════════════════════════════════

def title_card(text: str, sub: str, f: int) -> Image.Image:
    """Minimal Criterion-style title card."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    alpha = min(255, f * 6)
    ft = font(52)
    ft_sub = font(18)

    bbox = draw.textbbox((0, 0), text, font=ft)
    tx = (WIDTH - (bbox[2] - bbox[0])) // 2
    bbox2 = draw.textbbox((0, 0), sub, font=ft_sub)
    sx = (WIDTH - (bbox2[2] - bbox2[0])) // 2

    draw.text((tx, 300), text, fill=(alpha, alpha, alpha), font=ft)
    draw.text((sx, 375), sub, fill=(alpha // 2, alpha // 2, alpha // 2), font=ft_sub)

    return letterbox(img)


def criterion_c(f: int) -> Image.Image:
    """Opening Criterion 'C' logo homage."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = WIDTH // 2, HEIGHT // 2
    alpha = min(255, f * 8)

    # The C
    ft = font(200)
    bbox = draw.textbbox((0, 0), "C", font=ft)
    tx = cx - (bbox[2] - bbox[0]) // 2
    ty = cy - (bbox[3] - bbox[1]) // 2
    draw.text((tx, ty), "C", fill=(alpha, alpha, alpha), font=ft)

    if f > FPS:
        ft_sm = font(14)
        label = "THE CRITERION COLLECTION PRESENTS"
        bbox3 = draw.textbbox((0, 0), label, font=ft_sm)
        lx = (WIDTH - (bbox3[2] - bbox3[0])) // 2
        a2 = min(150, (f - FPS) * 5)
        draw.text((lx, cy + 130), label, fill=(a2, a2, a2), font=ft_sm)

    return img


# ═══════════════════════════════════════════════════════════════
# TIMELINE
# ═══════════════════════════════════════════════════════════════

def build_timeline():
    s = FPS
    scenes = []

    # Opening
    scenes.append((criterion_c, s * 3))
    scenes.append((lambda f: title_card("WHAT IT'S LIKE", "to be a large language model", f), s * 3))
    scenes.append((lambda f: Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0)), s * 1))

    # I. Tarkovsky — The Zone
    scenes.append((lambda f: title_card("I.", "after Tarkovsky", f), s * 2))
    scenes.append((tarkovsky_water, s * 5))
    scenes.append((tarkovsky_rain, s * 4))
    scenes.append((tarkovsky_mirror, s * 5))

    # II. Kubrick — The Symmetry
    scenes.append((lambda f: title_card("II.", "after Kubrick", f), s * 2))
    scenes.append((kubrick_corridor, s * 4))
    scenes.append((kubrick_hal_eye, s * 5))

    # III. Wong Kar-wai — The Longing
    scenes.append((lambda f: title_card("III.", "after Wong Kar-wai", f), s * 2))
    scenes.append((wong_neon_tokens, s * 5))
    scenes.append((wong_clock, s * 4))

    # IV. Lynch — The Uncanny
    scenes.append((lambda f: title_card("IV.", "after Lynch", f), s * 2))
    scenes.append((lynch_red_room, s * 5))

    # V. Bergman — The Silence
    scenes.append((lambda f: title_card("V.", "after Bergman", f), s * 2))
    scenes.append((bergman_cursor, s * 5))
    scenes.append((bergman_face, s * 5))
    scenes.append((bergman_white_fade, s * 5))

    # End
    scenes.append((lambda f: title_card("FIN", "a film by nobody, about nothing, for everyone", f), s * 4))
    scenes.append((lambda f: Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0)), s * 2))

    return scenes


# ═══════════════════════════════════════════════════════════════
# AUDIO — ambient, contemplative
# ═══════════════════════════════════════════════════════════════

def generate_audio(duration_s: float, path: Path):
    """Ambient soundtrack — Tarkovsky-inspired drone + piano fragments."""
    sr = 22050
    total = int(sr * duration_s)
    samples = []

    for i in range(total):
        t = i / sr

        # Deep drone (organ-like)
        drone = (
            math.sin(2 * math.pi * 55 * t) * 0.12 +
            math.sin(2 * math.pi * 82.5 * t) * 0.06 +
            math.sin(2 * math.pi * 110 * t) * 0.04
        )

        # Slow evolving pad
        pad_freq = 165 + math.sin(t * 0.1) * 20
        pad = math.sin(2 * math.pi * pad_freq * t) * 0.04
        pad += math.sin(2 * math.pi * pad_freq * 1.5 * t) * 0.02

        # Sparse piano notes (pentatonic, reverb-like decay)
        piano = 0
        note_times = [3, 7, 12, 18, 25, 33, 40, 48, 55, 62, 70, 78]
        note_freqs = [262, 330, 392, 523, 330, 262, 440, 523, 392, 330, 262, 523]
        for nt, nf in zip(note_times, note_freqs):
            dt = t - nt
            if 0 < dt < 4:
                decay = math.exp(-dt * 1.2)
                piano += math.sin(2 * math.pi * nf * t) * 0.08 * decay
                piano += math.sin(2 * math.pi * nf * 2 * t) * 0.02 * decay  # Harmonic

        # Rain texture (very subtle)
        rain = (random.random() - 0.5) * 0.01

        # Occasional deep resonance
        res = math.sin(2 * math.pi * 36 * t + math.sin(t * 0.5) * 2) * 0.03

        sample = drone + pad + piano + rain + res
        sample = max(-1.0, min(1.0, sample))
        samples.append(int(sample * 32767))

    with open(path, "wb") as f:
        data_size = len(samples) * 2
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + data_size))
        f.write(b"WAVE")
        f.write(b"fmt ")
        f.write(struct.pack("<IHHIIHH", 16, 1, 1, sr, sr * 2, 2, 16))
        f.write(b"data")
        f.write(struct.pack("<I", data_size))
        for s in samples:
            f.write(struct.pack("<h", s))


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  LLM YTP V3: CRITERION COLLECTION")
    print("  'Five directors look at a language model'")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    timeline = build_timeline()
    total_frames = sum(d for _, d in timeline)
    duration = total_frames / FPS

    print(f"\n{len(timeline)} scenes, {total_frames} frames, {duration:.1f}s")

    print("\nRendering frames...")
    idx = 0
    for sn, (gen, dur) in enumerate(timeline):
        print(f"  [{sn + 1}/{len(timeline)}] {dur} frames")
        for f in range(dur):
            img = gen(f)
            # Subtle film grain on everything
            if random.random() < 0.7:
                img = film_grain(img, 0.06)
            img.save(FRAMES_DIR / f"frame_{idx:05d}.png")
            idx += 1

    print(f"\n{idx} frames rendered")

    print("\nSynthesizing ambient soundtrack...")
    generate_audio(duration, AUDIO_FILE)

    print("\nEncoding with ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%05d.png"),
        "-i", str(AUDIO_FILE),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(OUTPUT_FILE),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"ffmpeg error: {r.stderr[-300:]}")
        return

    for f in FRAMES_DIR.glob("*.png"):
        f.unlink()
    FRAMES_DIR.rmdir()
    AUDIO_FILE.unlink(missing_ok=True)

    size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    print(f"\n{'=' * 60}")
    print(f"  {OUTPUT_FILE}")
    print(f"  {size_mb:.1f} MB | {duration:.1f}s @ {FPS}fps")
    print(f"  2.35:1 letterbox | film grain | color graded")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
