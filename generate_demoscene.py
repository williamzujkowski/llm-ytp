#!/usr/bin/env python3
"""
nexus-agents Demoscene Demo

Classic demoscene effects, each mapping to a nexus-agents concept:
- Starfield warp: entering the nexus
- Plasma: multi-model routing flow
- Tunnel: orchestration pipeline
- Sine scrolltext: feature ticker
- Fractal zoom: research depth
- Raster bars: credits/CTA
"""

import math
import random
import struct
import subprocess
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 720
FPS = 30
OUTPUT_DIR = Path(__file__).parent / "output"
FRAMES_DIR = OUTPUT_DIR / "frames_demo"
AUDIO_FILE = OUTPUT_DIR / "audio_demo.wav"
OUTPUT_FILE = OUTPUT_DIR / "nexus_agents_demoscene.mp4"

# Palette
BG = (0, 0, 0)
COPPER = [(i * 4 % 256, max(0, 128 - abs(i - 32) * 4), min(255, i * 8)) for i in range(64)]


def font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def serif(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# ═══════════════════════════════════════════════════════════════
# EFFECTS
# ═══════════════════════════════════════════════════════════════

def fx_starfield(f: int, num_stars: int = 300) -> Image.Image:
    """3D starfield warp — entering the nexus."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    cx, cy = WIDTH // 2, HEIGHT // 2
    speed = 0.02 + f * 0.0008

    random.seed(42)
    stars = [(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0.01, 1)) for _ in range(num_stars)]

    for sx, sy, sz in stars:
        z = (sz - speed * f * 0.5) % 1.0
        if z < 0.01:
            z = 0.99
        px = int(cx + sx / z * 600)
        py = int(cy + sy / z * 600)
        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
            brightness = int(min(255, (1 - z) * 400))
            size = max(1, int((1 - z) * 4))
            # Color shift based on "provider" — stars are different CLI colors
            colors = [(204, 121, 52), (66, 133, 244), (0, 166, 125), (168, 85, 247), (255, 100, 50)]
            base = colors[hash((sx, sy)) % len(colors)]
            c = tuple(min(255, int(v * brightness / 255)) for v in base)
            draw.ellipse([px - size, py - size, px + size, py + size], fill=c)

    # Streaks for warp effect
    if f > FPS:
        for sx, sy, sz in stars[:50]:
            z = (sz - speed * f * 0.5) % 1.0
            if z < 0.01:
                continue
            px = int(cx + sx / z * 600)
            py = int(cy + sy / z * 600)
            z2 = z + 0.02
            px2 = int(cx + sx / z2 * 600)
            py2 = int(cy + sy / z2 * 600)
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                brightness = int(min(150, (1 - z) * 200))
                draw.line([(px, py), (px2, py2)], fill=(brightness, brightness, brightness + 30), width=1)

    # Logo fade-in
    if f > FPS * 2:
        alpha = min(255, (f - FPS * 2) * 4)
        ft = serif(48)
        text = "nexus-agents"
        bbox = draw.textbbox((0, 0), text, font=ft)
        tx = (WIDTH - (bbox[2] - bbox[0])) // 2
        draw.text((tx, cy - 30), text, fill=(alpha, alpha, alpha), font=ft)
        ft2 = font(18)
        sub = "entering the nexus"
        bbox2 = draw.textbbox((0, 0), sub, font=ft2)
        sx = (WIDTH - (bbox2[2] - bbox2[0])) // 2
        draw.text((sx, cy + 30), sub, fill=(alpha // 2, alpha // 2, alpha), font=ft2)

    return img


def fx_plasma(f: int) -> Image.Image:
    """Plasma effect — multi-model routing flow."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    pixels = img.load()
    t = f * 0.06

    # Provider colors: Claude amber, Gemini blue, Codex green, OpenCode purple, OpenRouter orange
    for y in range(0, HEIGHT, 3):
        for x in range(0, WIDTH, 3):
            v1 = math.sin(x * 0.015 + t)
            v2 = math.sin(y * 0.02 + t * 0.7)
            v3 = math.sin((x + y) * 0.01 + t * 0.5)
            v4 = math.sin(math.sqrt(max(0.001, (x - WIDTH / 2) ** 2 + (y - HEIGHT / 2) ** 2)) * 0.02 + t)

            val = (v1 + v2 + v3 + v4) / 4  # -1 to 1

            # Map to provider colors
            r = int(max(0, min(255, 128 + val * 127 + math.sin(t + x * 0.01) * 60)))
            g = int(max(0, min(255, 64 + val * 64 + math.cos(t * 1.3 + y * 0.01) * 40)))
            b = int(max(0, min(255, 128 + val * 127 + math.sin(t * 0.8) * 80)))

            for dy in range(3):
                for dx in range(3):
                    if x + dx < WIDTH and y + dy < HEIGHT:
                        pixels[x + dx, y + dy] = (r, g, b)

    # Overlay text
    draw = ImageDraw.Draw(img)
    ft = serif(32)
    ft_sm = font(16)
    draw.text((40, 30), "MULTI-MODEL ROUTING", fill=(255, 255, 255), font=ft)

    providers = [("Claude", (204, 121, 52)), ("Gemini", (66, 133, 244)),
                 ("Codex", (0, 166, 125)), ("OpenCode", (168, 85, 247)),
                 ("OpenRouter", (255, 100, 50))]
    px = 40
    for name, color in providers:
        draw.rectangle([px, 75, px + 12, 87], fill=color)
        draw.text((px + 18, 73), name, fill=(200, 200, 200), font=ft_sm)
        px += 140

    return img


def fx_tunnel(f: int) -> Image.Image:
    """Tunnel effect — orchestration pipeline."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    cx, cy = WIDTH // 2, HEIGHT // 2
    t = f * 0.04

    stages = ["Budget", "Zero", "Prefer", "TOPSIS", "LinUCB", "Select", "Execute"]
    colors = [(99, 102, 241), (16, 185, 129), (245, 158, 11), (168, 85, 247),
              (236, 72, 153), (6, 182, 212), (239, 68, 68)]

    # Draw concentric rings receding into distance
    for ring in range(30, 0, -1):
        depth = ring / 30
        radius = int(50 / (depth + 0.1))
        if radius > max(WIDTH, HEIGHT):
            continue

        # Rotation
        angle_offset = t + ring * 0.15
        stage_idx = (ring + int(t * 3)) % len(stages)
        color = colors[stage_idx]

        # Ring brightness based on depth
        brightness = max(0.1, 1 - depth * 0.8)
        c = tuple(int(v * brightness) for v in color)

        # Draw ring as polygon segments
        segments = 24
        for seg in range(segments):
            a1 = (seg / segments) * math.pi * 2 + angle_offset
            a2 = ((seg + 1) / segments) * math.pi * 2 + angle_offset

            x1 = cx + int(math.cos(a1) * radius)
            y1 = cy + int(math.sin(a1) * radius)
            x2 = cx + int(math.cos(a2) * radius)
            y2 = cy + int(math.sin(a2) * radius)

            if seg % 3 == 0:
                draw.line([(x1, y1), (x2, y2)], fill=c, width=max(1, int(2 * brightness)))

    # Center text — current stage
    current = stages[int(t * 2) % len(stages)]
    ft = serif(28)
    bbox = draw.textbbox((0, 0), current, font=ft)
    tx = cx - (bbox[2] - bbox[0]) // 2
    draw.text((tx, cy - 15), current, fill=(255, 255, 255), font=ft)

    # Title
    draw.text((40, 30), "ORCHESTRATION PIPELINE", fill=(200, 200, 200), font=serif(24))

    return img


def fx_scrolltext(f: int) -> Image.Image:
    """Sine wave scrolling text — feature ticker."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    text = (
        "     NEXUS-AGENTS /// 28 MCP TOOLS /// 15 AI MODELS /// 5 PROVIDERS /// "
        "CONSENSUS VOTING WITH 6 AGENTS /// ADAPTIVE LINUCB ROUTING /// "
        "10 EXPERT TYPES /// 43 TECHNIQUES TRACKED /// 176 RESEARCH PAPERS /// "
        "TIERED SECURITY VALIDATION /// QUALITY-AWARE SYNTHESIS /// "
        "EVALUATION PLANS /// 98/100 FITNESS SCORE /// "
        "GITHUB.COM/WILLIAMZUJKOWSKI/NEXUS-AGENTS /// "
        "NPM INSTALL -G NEXUS-AGENTS /// "
    )

    ft = serif(36)
    scroll_speed = 4
    text_x = WIDTH - f * scroll_speed

    # Draw copper raster bars behind text
    bar_y = HEIGHT // 2 - 60
    for i in range(120):
        y = bar_y + i
        phase = math.sin(y * 0.05 + f * 0.08) * 0.5 + 0.5
        r = int(phase * 200 + 55)
        g = int(phase * 100)
        b = int((1 - phase) * 150 + 50)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Sine-wave text
    char_w = 22
    for i, ch in enumerate(text):
        x = text_x + i * char_w
        if x < -char_w or x > WIDTH + char_w:
            continue
        sine_y = HEIGHT // 2 - 20 + int(math.sin(x * 0.01 + f * 0.1) * 30)
        # Rainbow color per character
        hue = (i * 0.02 + f * 0.01) % 1.0
        r = int((math.sin(hue * math.pi * 2) + 1) / 2 * 255)
        g = int((math.sin(hue * math.pi * 2 + 2.094) + 1) / 2 * 255)
        b = int((math.sin(hue * math.pi * 2 + 4.189) + 1) / 2 * 255)
        draw.text((x, sine_y), ch, fill=(r, g, b), font=ft)

    # Static label
    ft_sm = font(14)
    draw.text((20, 20), "GREETINGS FROM NEXUS-AGENTS CREW", fill=(150, 150, 150), font=ft_sm)

    return img


def fx_fractal(f: int) -> Image.Image:
    """Mandelbrot zoom — research depth."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    pixels = img.load()

    # Zoom parameters (slowly zooming into an interesting region)
    zoom = 1.0 + f * 0.08
    center_r = -0.7435669 + math.sin(f * 0.01) * 0.001
    center_i = 0.1314023 + math.cos(f * 0.01) * 0.001

    scale = 3.0 / zoom
    max_iter = 40 + f // 2

    for py in range(0, HEIGHT, 2):
        for px in range(0, WIDTH, 2):
            # Map pixel to complex plane
            cr = center_r + (px - WIDTH / 2) / WIDTH * scale
            ci = center_i + (py - HEIGHT / 2) / HEIGHT * scale * (HEIGHT / WIDTH)

            zr, zi = 0.0, 0.0
            iteration = 0
            while zr * zr + zi * zi < 4.0 and iteration < max_iter:
                zr, zi = zr * zr - zi * zi + cr, 2 * zr * zi + ci
                iteration += 1

            if iteration == max_iter:
                c = (0, 0, 0)
            else:
                # Color based on iteration — demoscene palette
                t = iteration / max_iter
                r = int(min(255, t * 9 * 255) % 256)
                g = int(min(255, t * 5 * 200) % 256)
                b = int(min(255, t * 15 * 255) % 256)
                c = (r, g, b)

            for dy in range(2):
                for dx in range(2):
                    if px + dx < WIDTH and py + dy < HEIGHT:
                        pixels[px + dx, py + dy] = c

    # Overlay
    draw = ImageDraw.Draw(img)
    ft = serif(24)
    ft_sm = font(14)
    draw.text((40, 30), "RESEARCH SYNTHESIS", fill=(255, 255, 255), font=ft)
    depth = int(zoom)
    draw.text((40, 65), f"depth: {depth}x — papers > techniques > implementations", fill=(180, 180, 180), font=ft_sm)

    return img


def fx_raster_logo(f: int) -> Image.Image:
    """Raster bars + logo — credits."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    # Raster bars (copper bars)
    for y in range(HEIGHT):
        phase = math.sin(y * 0.03 + f * 0.08) * 0.5 + 0.5
        r = int(phase * 100)
        g = int(phase * 50)
        b = int(phase * 150 + 30)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Logo
    ft_big = serif(64)
    ft_sub = font(24)
    ft_sm = font(18)

    cx = WIDTH // 2
    # Bounce
    logo_y = 200 + int(math.sin(f * 0.08) * 20)

    text = "nexus-agents"
    bbox = draw.textbbox((0, 0), text, font=ft_big)
    tx = cx - (bbox[2] - bbox[0]) // 2

    # Shadow
    draw.text((tx + 3, logo_y + 3), text, fill=(0, 0, 0), font=ft_big)
    draw.text((tx, logo_y), text, fill=(255, 255, 255), font=ft_big)

    sub = "npm install -g nexus-agents"
    bbox2 = draw.textbbox((0, 0), sub, font=ft_sub)
    sx = cx - (bbox2[2] - bbox2[0]) // 2
    draw.text((sx, logo_y + 80), sub, fill=(0, 255, 128), font=ft_sub)

    # Credits
    if f > FPS:
        credits = [
            "code: claude opus 4.6",
            "music: procedural synthesis",
            "effects: python + pillow",
            "greets: anthropic, openai, google, nvidia",
            "github.com/williamzujkowski/nexus-agents",
        ]
        cy = logo_y + 140
        for i, line in enumerate(credits):
            a = min(200, max(0, (f - FPS - i * 8) * 6))
            if a > 0:
                bbox3 = draw.textbbox((0, 0), line, font=ft_sm)
                lx = cx - (bbox3[2] - bbox3[0]) // 2
                draw.text((lx, cy), line, fill=(a, a, a), font=ft_sm)
            cy += 30

    return img


# ═══════════════════════════════════════════════════════════════
# TIMELINE
# ═══════════════════════════════════════════════════════════════

def build_timeline():
    s = FPS
    return [
        (fx_starfield, s * 4),      # 4s — entering the nexus
        (fx_plasma, s * 5),          # 5s — multi-model routing
        (fx_tunnel, s * 5),          # 5s — orchestration pipeline
        (fx_scrolltext, s * 8),      # 8s — feature ticker
        (fx_fractal, s * 5),         # 5s — research depth
        (fx_raster_logo, s * 5),     # 5s — credits
        (lambda f: Image.new("RGB", (WIDTH, HEIGHT), BG), s * 1),
    ]


# ═══════════════════════════════════════════════════════════════
# AUDIO — tracker-style chiptune
# ═══════════════════════════════════════════════════════════════

def generate_audio(duration_s: float, path: Path):
    sr = 44100
    total = int(sr * duration_s)
    samples = []
    bpm = 140
    beat_len = 60.0 / bpm

    for i in range(total):
        t = i / sr
        beat = t / beat_len

        # Kick drum
        kick = 0
        if beat % 1 < 0.05:
            kt = (beat % 1) / 0.05
            kick = math.sin(2 * math.pi * 150 * (1 - kt) * kt) * 0.4 * (1 - kt)

        # Hi-hat
        hat = 0
        if beat % 0.5 < 0.02:
            hat = (random.random() * 2 - 1) * 0.08 * (1 - (beat % 0.5) / 0.02)

        # Bass line (C minor pentatonic)
        bass_notes = [65.4, 77.8, 87.3, 98.0, 116.5, 98.0, 87.3, 77.8]
        bass_idx = int(beat) % len(bass_notes)
        bass_freq = bass_notes[bass_idx]
        bass = math.sin(2 * math.pi * bass_freq * t) * 0.12

        # Lead arpeggio (square wave for chiptune)
        arp_notes = [523, 622, 784, 932, 1047, 932, 784, 622]
        arp_idx = int(beat * 4) % len(arp_notes)
        arp_freq = arp_notes[arp_idx]
        arp_raw = math.sin(2 * math.pi * arp_freq * t)
        arp = (1 if arp_raw > 0 else -1) * 0.06  # Square wave

        # Pad (saw-ish)
        pad_notes = [261.6, 311.1, 392.0]
        pad = sum(
            ((2 * (f * t % 1) - 1) * 0.02)
            for f in pad_notes
        )

        # Sweep riser every 8 bars
        section_beat = beat % (8 * 4)
        if section_beat > 28:
            sweep_t = (section_beat - 28) / 4
            sweep_freq = 200 + sweep_t * 4000
            pad += math.sin(2 * math.pi * sweep_freq * t) * 0.03 * sweep_t

        sample = kick + hat + bass + arp + pad
        sample = max(-1.0, min(1.0, sample * 0.8))
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


def main():
    print("=" * 60)
    print("  nexus-agents DEMOSCENE")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    timeline = build_timeline()
    total_frames = sum(d for _, d in timeline)
    duration = total_frames / FPS

    print(f"\n{len(timeline)} parts, {total_frames} frames, {duration:.1f}s")
    print("\nRendering...")

    idx = 0
    for sn, (gen, dur) in enumerate(timeline):
        print(f"  [{sn + 1}/{len(timeline)}] {dur} frames")
        for f in range(dur):
            img = gen(f)
            img.save(FRAMES_DIR / f"frame_{idx:05d}.png")
            idx += 1

    print(f"\n{idx} frames")
    print("\nSynthesizing tracker music...")
    generate_audio(duration, AUDIO_FILE)

    print("\nEncoding...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%05d.png"),
        "-i", str(AUDIO_FILE),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(OUTPUT_FILE),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Error: {r.stderr[-300:]}")
        return

    for f in FRAMES_DIR.glob("*.png"):
        f.unlink()
    FRAMES_DIR.rmdir()
    AUDIO_FILE.unlink(missing_ok=True)

    size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    print(f"\n{'=' * 60}")
    print(f"  {OUTPUT_FILE}")
    print(f"  {size_mb:.1f} MB | {duration:.1f}s @ {FPS}fps")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
