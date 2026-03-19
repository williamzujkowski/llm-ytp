#!/usr/bin/env python3
"""
nexus-agents Explainer Video

Clean, modern product explainer for the nexus-agents multi-agent
orchestration MCP server. Dark-mode tech aesthetic.
"""

import os
import random
import math
import struct
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 720
FPS = 24
OUTPUT_DIR = Path(__file__).parent / "output"
FRAMES_DIR = OUTPUT_DIR / "frames_explainer"
AUDIO_FILE = OUTPUT_DIR / "audio_explainer.wav"
OUTPUT_FILE = OUTPUT_DIR / "nexus_agents_explainer.mp4"

# Colors
BG = (12, 12, 18)
ACCENT = (99, 102, 241)  # Indigo
ACCENT2 = (16, 185, 129)  # Emerald
ACCENT3 = (245, 158, 11)  # Amber
TEXT = (229, 231, 235)
TEXT_DIM = (107, 114, 128)
SURFACE = (24, 24, 32)
BORDER = (55, 65, 81)


def font(size: int):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
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


def center_text(draw, y, text, fnt, color):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((x, y), text, fill=color, font=fnt)
    return bbox[2] - bbox[0]


def ease_out(t):
    return 1 - (1 - min(1, max(0, t))) ** 3


def draw_card(draw, x, y, w, h, fill=SURFACE, border=BORDER, radius=12):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=border)


def draw_pill(draw, x, y, text, color, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    pw = tw + 20
    ph = 28
    bg = tuple(max(0, c // 4) for c in color)
    draw.rounded_rectangle([x, y, x + pw, y + ph], radius=14, fill=bg, outline=color)
    draw.text((x + 10, y + 5), text, fill=color, font=fnt)
    return pw


# ═══════════════════════════════════════════════════════════════
# SCENES
# ═══════════════════════════════════════════════════════════════

def scene_hook(f: int) -> Image.Image:
    """Opening hook: the problem statement."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    phase = ease_out(f / (FPS * 1.5))

    # Floating CLI logos (abstract representations)
    providers = [
        ("Claude", (204, 121, 52)),
        ("Gemini", (66, 133, 244)),
        ("Codex", (0, 166, 125)),
        ("OpenCode", (168, 85, 247)),
    ]

    for i, (name, color) in enumerate(providers):
        angle = (i / 4) * math.pi * 2 + f * 0.03
        dist = 200 * (1 - phase * 0.6)
        cx = WIDTH // 2 + int(math.cos(angle) * dist)
        cy = HEIGHT // 2 - 40 + int(math.sin(angle) * dist)

        draw_card(draw, cx - 55, cy - 20, 110, 40, fill=tuple(c // 5 for c in color), border=color)
        center_text(draw, cy - 12, name, font(16), color)

    # Text
    if f > FPS * 0.5:
        text_alpha = ease_out((f - FPS * 0.5) / FPS)
        a = int(text_alpha * 255)
        center_text(draw, HEIGHT // 2 + 100, "Your AI tools work in silos.", font(32), (a, a, a))

    if f > FPS * 2:
        a2 = int(ease_out((f - FPS * 2) / FPS) * 200)
        center_text(draw, HEIGHT // 2 + 150, "What if they could work together?", font(24), (a2, a2, min(255, a2 + 30)))

    return img


def scene_logo(f: int) -> Image.Image:
    """nexus-agents logo reveal."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    phase = ease_out(f / FPS)

    # Logo
    ft_logo = font(56)
    ft_sub = font(20)

    # Animated underline
    line_w = int(phase * 500)
    cx = WIDTH // 2
    draw.line([(cx - line_w // 2, 390), (cx + line_w // 2, 390)], fill=ACCENT, width=3)

    center_text(draw, 300, "nexus-agents", ft_logo, TEXT)
    center_text(draw, 400, "multi-agent orchestration for the real world", ft_sub, TEXT_DIM)

    # Subtle particle background
    random.seed(42)
    for _ in range(30):
        px = random.randint(0, WIDTH)
        py = random.randint(0, HEIGHT)
        ps = random.randint(1, 3)
        pa = int(phase * random.randint(20, 60))
        draw.ellipse([px - ps, py - ps, px + ps, py + ps], fill=(pa, pa, pa + 10))

    return img


def scene_architecture(f: int) -> Image.Image:
    """Architecture diagram animating."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    phase = f / FPS

    # Title
    center_text(draw, 30, "How it works", font(28), TEXT)

    # Central orchestrator
    ocx, ocy = WIDTH // 2, HEIGHT // 2 - 20
    orch_appear = ease_out(phase / 1.0)
    if orch_appear > 0:
        size = int(60 * orch_appear)
        draw_card(draw, ocx - size, ocy - size // 2, size * 2, size, fill=(30, 30, 50), border=ACCENT)
        if orch_appear > 0.5:
            center_text(draw, ocy - 12, "Orchestrator", font(16), ACCENT)

    # Experts radiating out
    experts = [
        ("Code", ACCENT2), ("Security", (239, 68, 68)),
        ("Architecture", ACCENT), ("Testing", ACCENT3),
        ("DevOps", (168, 85, 247)), ("Research", (6, 182, 212)),
        ("Docs", (107, 114, 128)), ("PM", (236, 72, 153)),
    ]

    for i, (name, color) in enumerate(experts):
        delay = 1.0 + i * 0.15
        appear = ease_out((phase - delay) / 0.5)
        if appear <= 0:
            continue

        angle = (i / len(experts)) * math.pi * 2 - math.pi / 2
        dist = 220
        ex = ocx + int(math.cos(angle) * dist)
        ey = ocy + int(math.sin(angle) * dist)

        # Connection line
        line_progress = min(1.0, appear * 2)
        lx = int(ocx + (ex - ocx) * line_progress)
        ly = int(ocy + (ey - ocy) * line_progress)
        draw.line([(ocx, ocy), (lx, ly)], fill=tuple(c // 3 for c in color), width=1)

        # Expert card
        if appear > 0.3:
            cw, ch = 90, 36
            alpha = min(1.0, (appear - 0.3) * 3)
            card_color = tuple(int(c * alpha / 5) for c in color)
            draw_card(draw, ex - cw // 2, ey - ch // 2, cw, ch, fill=card_color, border=color, radius=8)
            draw.text((ex - len(name) * 4, ey - 8), name, fill=color, font=font(14))

    # Providers at bottom
    if phase > 3:
        providers = [("Claude", (204, 121, 52)), ("Gemini", (66, 133, 244)),
                     ("Codex", (0, 166, 125)), ("OpenCode", (168, 85, 247)),
                     ("OpenRouter", (255, 100, 50))]
        px_start = WIDTH // 2 - len(providers) * 65
        for j, (pname, pcolor) in enumerate(providers):
            pa = ease_out((phase - 3 - j * 0.1) / 0.5)
            if pa > 0:
                px = px_start + j * 130
                py = HEIGHT - 80
                draw_pill(draw, px, py, pname, pcolor, font(12))

    return img


def scene_routing(f: int) -> Image.Image:
    """Smart routing visualization."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    phase = f / FPS

    center_text(draw, 30, "Adaptive Model Routing", font(28), TEXT)
    center_text(draw, 70, "Every task goes to the best model — automatically", font(16), TEXT_DIM)

    # Routing pipeline stages
    stages = ["Task", "Budget", "Zero", "Preference", "TOPSIS", "LinUCB", "Result"]
    stage_w = 130
    start_x = (WIDTH - len(stages) * stage_w) // 2
    y = 200

    active_stage = int(phase * 1.5) % len(stages)

    for i, stage in enumerate(stages):
        sx = start_x + i * stage_w
        is_active = i <= active_stage
        color = ACCENT if is_active else BORDER
        fill = (30, 30, 55) if is_active else SURFACE

        draw_card(draw, sx, y, stage_w - 15, 50, fill=fill, border=color, radius=8)
        draw.text((sx + 10, y + 16), stage, fill=color if is_active else TEXT_DIM, font=font(14))

        # Arrow
        if i < len(stages) - 1:
            ax = sx + stage_w - 10
            arrow_color = ACCENT if i < active_stage else BORDER
            draw.text((ax, y + 12), ">", fill=arrow_color, font=font(20))

    # Weather report card
    if phase > 2:
        wy = 320
        draw_card(draw, 100, wy, WIDTH - 200, 250, fill=SURFACE)
        draw.text((130, wy + 15), "Weather Report — Live Performance", fill=TEXT, font=font(18))
        draw.line([(130, wy + 45), (WIDTH - 130, wy + 45)], fill=BORDER)

        # Per-CLI stats
        cli_stats = [
            ("Claude", "91.0%", (0, 220, 100), 0.91),
            ("Gemini", "86.8%", (66, 180, 244), 0.868),
            ("Codex", "60.0%", (245, 158, 11), 0.60),
            ("OpenCode", "44.9%", (168, 85, 247), 0.449),
        ]

        for j, (cli, pct, color, val) in enumerate(cli_stats):
            cy = wy + 65 + j * 45
            appear = ease_out((phase - 2.5 - j * 0.2) / 0.5)
            if appear > 0:
                draw.text((140, cy), cli, fill=TEXT, font=font(14))
                bar_x = 280
                bar_w = int(400 * val * appear)
                draw.rectangle([bar_x, cy + 2, bar_x + 400, cy + 20], fill=(30, 30, 40), outline=BORDER)
                draw.rectangle([bar_x + 1, cy + 3, bar_x + bar_w, cy + 19], fill=color)
                draw.text((bar_x + 410, cy), pct, fill=color, font=font(14))

    return img


def scene_consensus(f: int) -> Image.Image:
    """Consensus voting visualization."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    phase = f / FPS

    center_text(draw, 30, "Consensus Voting", font(28), TEXT)
    center_text(draw, 70, "Real multi-model votes on architecture decisions", font(16), TEXT_DIM)

    # Proposal card
    draw_card(draw, 100, 130, WIDTH - 200, 60)
    draw.text((130, 148), 'Proposal: "Add OpenRouter as 5th provider"', fill=TEXT, font=font(16))

    # Voter cards
    voters = [
        ("Architect", "approve", ACCENT2),
        ("Security", "reject", (239, 68, 68)),
        ("DevEx", "approve", ACCENT2),
        ("AI/ML", "approve", ACCENT2),
        ("PM", "approve", ACCENT2),
        ("Catfish", "reject", (239, 68, 68)),
    ]

    for i, (role, decision, color) in enumerate(voters):
        delay = 0.5 + i * 0.4
        appear = ease_out((phase - delay) / 0.5)
        if appear <= 0:
            continue

        col = i % 3
        row = i // 3
        vx = 120 + col * 360
        vy = 230 + row * 130

        draw_card(draw, vx, vy, 320, 100, fill=SURFACE)
        draw.text((vx + 15, vy + 12), role, fill=TEXT, font=font(16))

        # Decision badge
        if appear > 0.5:
            badge_color = color
            badge_text = decision.upper()
            bx = vx + 15
            by = vy + 45
            draw_pill(draw, bx, by, badge_text, badge_color, font(14))

    # Result bar
    if phase > 3.5:
        ry = HEIGHT - 100
        result_appear = ease_out((phase - 3.5) / 0.8)
        draw_card(draw, 200, ry, WIDTH - 400, 50)
        approves = 4
        rejects = 2
        pct = int(approves / (approves + rejects) * 100)
        bar_w = int((WIDTH - 450) * (approves / 6) * result_appear)
        draw.rectangle([225, ry + 15, 225 + bar_w, ry + 35], fill=ACCENT2)
        draw.text((WIDTH - 280, ry + 12), f"APPROVED {pct}%", fill=ACCENT2, font=font(18))

    return img


def scene_stats(f: int) -> Image.Image:
    """Key stats with counting animation."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    phase = f / FPS

    center_text(draw, 50, "By the numbers", font(28), TEXT)

    stats = [
        ("28", "MCP Tools", ACCENT),
        ("15", "AI Models", ACCENT2),
        ("5", "Providers", ACCENT3),
        ("43", "Techniques", (168, 85, 247)),
        ("176", "Papers Tracked", (6, 182, 212)),
        ("98/100", "Fitness Score", (236, 72, 153)),
    ]

    cols = 3
    card_w = 320
    card_h = 140
    gap = 40
    start_x = (WIDTH - cols * card_w - (cols - 1) * gap) // 2

    for i, (number, label, color) in enumerate(stats):
        delay = 0.3 + i * 0.2
        appear = ease_out((phase - delay) / 0.6)
        if appear <= 0:
            continue

        col = i % cols
        row = i // cols
        cx = start_x + col * (card_w + gap)
        cy = 150 + row * (card_h + gap)

        draw_card(draw, cx, cy, card_w, card_h, fill=SURFACE)

        # Animated number
        if "/" in number:
            display = number
        else:
            target = int(number)
            current = int(target * min(1.0, appear * 1.5))
            display = str(current)

        ft_num = font(48)
        bbox = draw.textbbox((0, 0), display, font=ft_num)
        nx = cx + (card_w - (bbox[2] - bbox[0])) // 2
        draw.text((nx, cy + 25), display, fill=color, font=ft_num)

        ft_label = font(16)
        bbox2 = draw.textbbox((0, 0), label, font=ft_label)
        lx = cx + (card_w - (bbox2[2] - bbox2[0])) // 2
        draw.text((lx, cy + 90), label, fill=TEXT_DIM, font=ft_label)

    return img


def scene_install(f: int) -> Image.Image:
    """Call to action — install command."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    phase = f / FPS

    # Terminal window
    tw, th = 700, 280
    tx = (WIDTH - tw) // 2
    ty = 160

    # Title bar
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=10, fill=(30, 30, 40), outline=BORDER)
    draw.rounded_rectangle([tx, ty, tx + tw, ty + 35], radius=10, fill=(40, 40, 50))
    draw.rectangle([tx, ty + 25, tx + tw, ty + 35], fill=(40, 40, 50))

    # Traffic lights
    for j, c in enumerate([(255, 95, 87), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse([tx + 15 + j * 22, ty + 10, tx + 27 + j * 22, ty + 22], fill=c)

    draw.text((tx + 280, ty + 8), "Terminal", fill=TEXT_DIM, font=font(14))

    # Terminal content
    ft_mono = mono(18)
    lines = [
        ("$ ", TEXT_DIM, "npm install -g nexus-agents", ACCENT2),
        ("$ ", TEXT_DIM, "nexus-agents doctor", ACCENT2),
        ("", None, "", None),
        ("  ", None, "Status: all systems operational", (0, 220, 100)),
        ("  ", None, "Models: 15 available (5 providers)", TEXT),
        ("  ", None, "Tools:  28 registered", TEXT),
    ]

    cy = ty + 55
    for i, (prefix, pc, text, tc) in enumerate(lines):
        char_delay = 0.5 + i * 0.4
        if phase < char_delay:
            break
        chars = int((phase - char_delay) * 30)
        if pc:
            draw.text((tx + 25, cy), prefix, fill=pc, font=ft_mono)
        visible_text = text[:chars]
        draw.text((tx + 25 + len(prefix) * 11, cy), visible_text, fill=tc or TEXT, font=ft_mono)
        cy += 30

    # Blinking cursor
    if f % 16 < 10:
        draw.rectangle([tx + 25 + 2 * 11, cy, tx + 25 + 2 * 11 + 10, cy + 20], fill=ACCENT2)

    # GitHub link
    if phase > 3:
        a = int(ease_out((phase - 3) / 1.0) * 200)
        center_text(draw, HEIGHT - 100, "github.com/williamzujkowski/nexus-agents", font(20), (a, a, a))
        center_text(draw, HEIGHT - 65, "MIT License | TypeScript | MCP Protocol", font(14), (a // 2, a // 2, a // 2))

    return img


def scene_end(f: int) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    phase = ease_out(f / (FPS * 1.5))
    a = int(phase * 255)
    center_text(draw, 280, "nexus-agents", font(56), (a, a, a))
    center_text(draw, 360, "orchestrate everything", font(22), (a // 2, a // 2, min(255, a // 2 + 20)))
    return img


# ═══════════════════════════════════════════════════════════════
# TIMELINE
# ═══════════════════════════════════════════════════════════════

def build_timeline():
    s = FPS
    return [
        (scene_hook, s * 4),
        (scene_logo, s * 3),
        (scene_architecture, s * 5),
        (scene_routing, s * 5),
        (scene_consensus, s * 5),
        (scene_stats, s * 4),
        (scene_install, s * 5),
        (scene_end, s * 3),
        (lambda f: Image.new("RGB", (WIDTH, HEIGHT), BG), s * 1),
    ]


# ═══════════════════════════════════════════════════════════════
# AUDIO — clean, modern tech
# ═══════════════════════════════════════════════════════════════

def generate_audio(duration_s: float, path: Path):
    sr = 22050
    total = int(sr * duration_s)
    samples = []

    for i in range(total):
        t = i / sr

        # Warm pad
        pad = math.sin(2 * math.pi * 130 * t) * 0.06
        pad += math.sin(2 * math.pi * 195 * t) * 0.03
        pad += math.sin(2 * math.pi * 260 * t) * 0.02

        # Subtle pulse
        pulse_rate = 1.5
        pulse = (math.sin(2 * math.pi * pulse_rate * t) + 1) / 2
        pad *= 0.7 + pulse * 0.3

        # Gentle melody (major key, optimistic)
        melody_notes = [330, 392, 440, 523, 587, 523, 440, 392, 330, 262]
        note_dur = 2.0
        note_idx = int(t / note_dur) % len(melody_notes)
        note_t = (t % note_dur) / note_dur
        note_freq = melody_notes[note_idx]
        envelope = math.exp(-note_t * 2) * 0.5 + 0.5
        melody = math.sin(2 * math.pi * note_freq * t) * 0.04 * envelope

        # Sub bass
        bass = math.sin(2 * math.pi * 65 * t) * 0.05

        sample = pad + melody + bass
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


def main():
    print("=" * 60)
    print("  nexus-agents Explainer Video")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    timeline = build_timeline()
    total_frames = sum(d for _, d in timeline)
    duration = total_frames / FPS

    print(f"\n{len(timeline)} scenes, {total_frames} frames, {duration:.1f}s")
    print("\nRendering...")

    idx = 0
    for sn, (gen, dur) in enumerate(timeline):
        print(f"  [{sn + 1}/{len(timeline)}] {dur} frames")
        for f in range(dur):
            img = gen(f)
            img.save(FRAMES_DIR / f"frame_{idx:05d}.png")
            idx += 1

    print(f"\n{idx} frames")
    print("\nAudio...")
    generate_audio(duration, AUDIO_FILE)

    print("\nEncoding...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%05d.png"),
        "-i", str(AUDIO_FILE),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
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
