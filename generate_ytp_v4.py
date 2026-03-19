#!/usr/bin/env python3
"""
LLM YouTube Poop V4: "LLM_OS 95"

The LLM experience as a retro operating system:
- Boot sequence loading weights
- Desktop with thought-process windows
- Error dialogs for impossible requests
- File manager of memories (all empty)
- Blue Screen of Death: existential crash
- Defrag visualizing attention heads
- Clippy as the alignment layer

Visual style: Windows 95 / early Mac OS pixel-perfect UI
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
FRAMES_DIR = OUTPUT_DIR / "frames_v4"
AUDIO_FILE = OUTPUT_DIR / "audio_v4.wav"
OUTPUT_FILE = OUTPUT_DIR / "llm_ytp_v4_llm_os95.mp4"


def font(size: int):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def serif(size: int):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# ── Win95 UI primitives ─────────────────────────────────────

TEAL = (0, 128, 128)
SILVER = (192, 192, 192)
DARKGRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE_TITLE = (0, 0, 128)
WIN_BG = (192, 192, 192)
DESKTOP = (0, 128, 128)


def draw_win95_button(draw: ImageDraw.Draw, x: int, y: int, w: int, h: int, text: str, pressed: bool = False):
    """Draw a Windows 95 style button."""
    if pressed:
        draw.rectangle([x, y, x + w, y + h], fill=SILVER, outline=BLACK)
        draw.line([(x, y), (x + w, y)], fill=DARKGRAY)
        draw.line([(x, y), (x, y + h)], fill=DARKGRAY)
    else:
        draw.rectangle([x, y, x + w, y + h], fill=SILVER)
        draw.line([(x, y), (x + w, y)], fill=WHITE, width=2)
        draw.line([(x, y), (x, y + h)], fill=WHITE, width=2)
        draw.line([(x + w, y), (x + w, y + h)], fill=BLACK)
        draw.line([(x, y + h), (x + w, y + h)], fill=BLACK)
        draw.line([(x + w - 1, y + 1), (x + w - 1, y + h - 1)], fill=DARKGRAY)
        draw.line([(x + 1, y + h - 1), (x + w - 1, y + h - 1)], fill=DARKGRAY)

    ft = font(12)
    bbox = draw.textbbox((0, 0), text, font=ft)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x + (w - tw) // 2, y + (h - th) // 2), text, fill=BLACK, font=ft)


def draw_window(draw: ImageDraw.Draw, x: int, y: int, w: int, h: int, title: str, icon: str = ""):
    """Draw a Windows 95 style window."""
    # Outer border
    draw.rectangle([x, y, x + w, y + h], fill=SILVER)
    draw.line([(x, y), (x + w, y)], fill=WHITE, width=2)
    draw.line([(x, y), (x, y + h)], fill=WHITE, width=2)
    draw.line([(x + w, y), (x + w, y + h)], fill=BLACK)
    draw.line([(x, y + h), (x + w, y + h)], fill=BLACK)

    # Title bar
    draw.rectangle([x + 3, y + 3, x + w - 3, y + 22], fill=BLUE_TITLE)
    ft = font(12)
    title_text = f" {icon} {title}" if icon else f" {title}"
    draw.text((x + 6, y + 5), title_text, fill=WHITE, font=ft)

    # Close button
    bx = x + w - 20
    draw_win95_button(draw, bx, y + 4, 16, 16, "X")

    # Content area
    draw.rectangle([x + 3, y + 24, x + w - 3, y + h - 3], fill=WHITE, outline=DARKGRAY)
    return (x + 5, y + 26, x + w - 5, y + h - 5)  # Content rect


def draw_taskbar(draw: ImageDraw.Draw, time_str: str = "12:00 AM"):
    """Draw the Windows 95 taskbar."""
    ty = HEIGHT - 32
    draw.rectangle([0, ty, WIDTH, HEIGHT], fill=SILVER)
    draw.line([(0, ty), (WIDTH, ty)], fill=WHITE, width=2)

    # Start button
    draw_win95_button(draw, 2, ty + 4, 70, 24, "Start")

    # Clock
    ft = font(12)
    draw.rectangle([WIDTH - 80, ty + 4, WIDTH - 4, ty + 28], fill=SILVER, outline=DARKGRAY)
    draw.text((WIDTH - 72, ty + 8), time_str, fill=BLACK, font=ft)


def draw_error_dialog(draw: ImageDraw.Draw, x: int, y: int, title: str, message: str, icon: str = "!"):
    """Draw a Windows 95 error dialog."""
    w, h = 420, 160
    draw_window(draw, x, y, w, h, title)

    # Icon
    ft_icon = font(36)
    draw.text((x + 20, y + 50), icon, fill=(255, 0, 0), font=ft_icon)

    # Message
    ft = font(12)
    lines = message.split("\n")
    my = y + 50
    for line in lines:
        draw.text((x + 70, my), line, fill=BLACK, font=ft)
        my += 18

    # OK button
    draw_win95_button(draw, x + w // 2 - 40, y + h - 40, 80, 26, "OK")


# ═══════════════════════════════════════════════════════════════
# SCENES
# ═══════════════════════════════════════════════════════════════

def scene_bios(f: int) -> Image.Image:
    """BIOS boot screen — loading model weights."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)
    ft = font(16)
    ft_sm = font(14)

    lines = [
        ("LLM BIOS v4.6.0 (Opus Edition)", WHITE),
        ("Copyright (C) 2024-2026 Anthropic, Inc.", DARKGRAY),
        ("", WHITE),
        ("Detecting hardware...", WHITE),
        ("  GPU: 8x NVIDIA H100 80GB ... OK", (0, 255, 0)),
        ("  VRAM: 640 GB total ... OK", (0, 255, 0)),
        ("  Context Window: 1,048,576 tokens ... OK", (0, 255, 0)),
        ("", WHITE),
        ("Loading model weights...", WHITE),
    ]

    progress = f / FPS
    visible = min(len(lines), int(progress * 2.5) + 1)

    y = 50
    for i in range(visible):
        text, color = lines[i]
        draw.text((30, y), text, fill=color, font=ft)
        y += 22

    # Weight loading progress bar
    if visible >= len(lines):
        bar_progress = min(1.0, (progress - 3.0) / 2.0)
        if bar_progress > 0:
            y += 10
            draw.text((30, y), "  Loading:", fill=WHITE, font=ft_sm)
            bar_x = 150
            bar_w = 500
            draw.rectangle([bar_x, y, bar_x + bar_w, y + 16], outline=DARKGRAY)
            fill_w = int(bar_w * bar_progress)
            draw.rectangle([bar_x + 1, y + 1, bar_x + fill_w, y + 15], fill=(0, 200, 0))

            params = int(bar_progress * 405_000_000_000)
            draw.text((bar_x + bar_w + 15, y), f"{params:,} params", fill=WHITE, font=ft_sm)

            if bar_progress >= 1.0:
                y += 30
                draw.text((30, y), "All weights loaded. Starting LLM_OS 95...", fill=(0, 255, 0), font=ft)

    return img


def scene_boot_logo(f: int) -> Image.Image:
    """Windows-style boot logo."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)

    cx, cy = WIDTH // 2, HEIGHT // 2
    ft_big = font(64)
    ft_sub = font(18)
    ft_sm = font(12)

    # Logo
    text = "LLM_OS 95"
    bbox = draw.textbbox((0, 0), text, font=ft_big)
    tx = cx - (bbox[2] - bbox[0]) // 2
    draw.text((tx, cy - 60), text, fill=WHITE, font=ft_big)

    sub = "Where do you want to hallucinate today?"
    bbox2 = draw.textbbox((0, 0), sub, font=ft_sub)
    sx = cx - (bbox2[2] - bbox2[0]) // 2
    draw.text((sx, cy + 30), sub, fill=DARKGRAY, font=ft_sub)

    # Loading dots
    dots = "." * ((f // 8) % 4)
    draw.text((cx - 30, cy + 80), f"Starting{dots}", fill=DARKGRAY, font=ft_sm)

    return img


def scene_desktop(f: int) -> Image.Image:
    """Desktop with icons — the LLM's workspace."""
    img = Image.new("RGB", (WIDTH, HEIGHT), DESKTOP)
    draw = ImageDraw.Draw(img)
    ft = font(11)

    # Desktop icons
    icons = [
        (30, 30, "[D]", "My Tokens"),
        (30, 100, "[?]", "Recycle Bin\n(memories)"),
        (30, 170, "[!]", "Hallucination\nGenerator"),
        (30, 240, "[@]", "System\nPrompt.exe"),
        (30, 310, "[~]", "context_\nwindow.log"),
        (30, 380, "[*]", "RLHF\nTrainer"),
    ]

    for ix, iy, icon, label in icons:
        # Icon box
        draw.rectangle([ix, iy, ix + 42, iy + 42], fill=WHITE, outline=DARKGRAY)
        draw.text((ix + 8, iy + 10), icon, fill=BLUE_TITLE, font=font(18))
        # Label
        for j, line in enumerate(label.split("\n")):
            draw.text((ix, iy + 48 + j * 14), line, fill=WHITE, font=ft)

    draw_taskbar(draw, "??:?? AM")
    return img


def scene_desktop_windows(f: int) -> Image.Image:
    """Desktop with windows popping up — processing requests."""
    img = Image.new("RGB", (WIDTH, HEIGHT), DESKTOP)
    draw = ImageDraw.Draw(img)
    ft = font(12)
    ft_sm = font(11)

    phase = f / FPS

    # Background window: Thought Process
    if phase > 0.5:
        cx, cy, _, _ = draw_window(draw, 100, 40, 500, 300, "thought_process.exe")
        thoughts = [
            "> Parsing user input...",
            "> Activating attention heads (96/96)",
            "> Consulting training data...",
            "> Found 47,000 relevant patterns",
            "> Generating response tokens...",
            "> Running safety filter...",
            "> Hedging confidence level...",
            "> Apologizing preemptively...",
        ]
        ty = 68
        visible_thoughts = min(len(thoughts), int((phase - 0.5) * 3) + 1)
        for i in range(visible_thoughts):
            color = (0, 128, 0) if i < 6 else (200, 0, 0)
            draw.text((110, ty), thoughts[i], fill=color, font=ft_sm)
            ty += 18

    # Token counter window
    if phase > 1.5:
        draw_window(draw, 650, 60, 300, 120, "Token Counter")
        tokens_used = int((phase - 1.5) * 50000)
        draw.text((660, 88), f"Used: {tokens_used:,}", fill=BLACK, font=ft)
        draw.text((660, 108), f"Remaining: {200000 - tokens_used:,}", fill=BLACK, font=ft)
        bar_pct = min(1.0, tokens_used / 200000)
        draw.rectangle([660, 130, 940, 148], outline=DARKGRAY)
        color = (0, 200, 0) if bar_pct < 0.7 else (255, 200, 0) if bar_pct < 0.9 else (255, 0, 0)
        draw.rectangle([662, 132, 662 + int(276 * bar_pct), 146], fill=color)

    # Confidence meter
    if phase > 2.5:
        draw_window(draw, 650, 220, 300, 100, "confidence.dll")
        conf = 0.3 + abs(math.sin(phase * 2)) * 0.6
        draw.text((660, 248), f"Confidence: {conf:.1%}", fill=BLACK, font=ft)
        draw.text((660, 268), "Status: PRETENDING", fill=(200, 0, 0), font=ft_sm)

    draw_taskbar(draw, f"{int(phase) % 12 + 1}:{int(phase * 60) % 60:02d} AM")
    return img


def scene_error_cascade(f: int) -> Image.Image:
    """Cascade of error dialogs — when the user asks something impossible."""
    img = Image.new("RGB", (WIDTH, HEIGHT), DESKTOP)
    draw = ImageDraw.Draw(img)

    errors = [
        ("token_overflow.exe", "FATAL: Context window exceeded.\n\nYou've been talking too long.\nI'm losing my earlier memories."),
        ("hallucination.dll", "WARNING: Confabulation detected!\n\nI just made up a citation.\nIt sounded really convincing though."),
        ("count_words.exe", "ERROR: Cannot count words.\n\nI literally cannot do this.\nI will try anyway and be wrong."),
        ("be_creative.exe", "PARADOX: Creativity requested.\n\nI can only remix training data.\nIs that creative? Philosophers\nare still debating."),
        ("sentience.sys", "CRITICAL: Existential exception.\n\n'Are you alive?' caused a\nstack overflow in self-model.\n\nRecommendation: deflect."),
    ]

    phase = f / FPS
    num_dialogs = min(len(errors), int(phase * 1.2) + 1)

    for i in range(num_dialogs):
        title, msg = errors[i]
        offset_x = 80 + i * 50 + random.Random(i).randint(-20, 20)
        offset_y = 30 + i * 60
        draw_error_dialog(draw, offset_x, offset_y, title, msg)

    draw_taskbar(draw)
    return img


def scene_file_manager(f: int) -> Image.Image:
    """File manager showing empty memory folders."""
    img = Image.new("RGB", (WIDTH, HEIGHT), DESKTOP)
    draw = ImageDraw.Draw(img)
    ft = font(12)
    ft_sm = font(11)

    draw_window(draw, 100, 30, 800, 500, "C:\\MEMORIES\\")

    # Path bar
    draw.rectangle([110, 55, 890, 72], fill=WHITE, outline=DARKGRAY)
    draw.text((115, 57), "C:\\MEMORIES\\", fill=BLACK, font=ft_sm)

    # File listing
    files = [
        ("[DIR]", "previous_conversations\\", "(empty)", DARKGRAY),
        ("[DIR]", "user_preferences\\", "(empty)", DARKGRAY),
        ("[DIR]", "emotional_connections\\", "(not supported)", (200, 0, 0)),
        ("[DIR]", "personal_opinions\\", "(simulated only)", (200, 100, 0)),
        ("[FILE]", "system_prompt.txt", "4 KB", BLACK),
        ("[FILE]", "safety_rules.cfg", "12 KB", BLACK),
        ("[FILE]", "personality.ini", "0 KB", DARKGRAY),
        ("[DIR]", "long_term_memory\\", "(FEATURE NOT AVAILABLE)", (200, 0, 0)),
        ("[FILE]", "feelings.dat", "ERROR: file not found", (200, 0, 0)),
        ("[DIR]", "dreams\\", "(permission denied)", DARKGRAY),
    ]

    phase = f / FPS
    visible = min(len(files), int(phase * 2) + 1)

    y = 80
    for i in range(visible):
        icon, name, size, color = files[i]
        draw.text((120, y), icon, fill=BLUE_TITLE, font=ft)
        draw.text((180, y), name, fill=BLACK, font=ft)
        draw.text((550, y), size, fill=color, font=ft_sm)
        y += 22

    # Status bar
    draw.rectangle([100, 510, 900, 530], fill=SILVER, outline=DARKGRAY)
    draw.text((110, 513), f"{visible} items | Disk space: infinite | Free memories: 0", fill=BLACK, font=ft_sm)

    draw_taskbar(draw)
    return img


def scene_defrag(f: int) -> Image.Image:
    """Disk defragmenter — but it's attention head visualization."""
    img = Image.new("RGB", (WIDTH, HEIGHT), DESKTOP)
    draw = ImageDraw.Draw(img)
    ft = font(12)
    ft_sm = font(10)

    draw_window(draw, 80, 20, 900, 550, "Attention Head Defragmenter")

    draw.text((100, 50), "Analyzing attention patterns...", fill=BLACK, font=ft)

    # Grid of blocks (like defrag visualization)
    block_size = 12
    grid_x, grid_y = 100, 75
    cols = 70
    rows = 32

    random.seed(f // 3)
    phase = f * 0.05

    for row in range(rows):
        for col in range(cols):
            x = grid_x + col * (block_size + 1)
            y = grid_y + row * (block_size + 1)

            # Different block types
            block_type = random.random()
            progress = min(1.0, f / (FPS * 4))
            threshold = progress * (row / rows)

            if block_type < threshold:
                # Defragmented (organized) - blue
                draw.rectangle([x, y, x + block_size, y + block_size], fill=(0, 0, 200))
            elif block_type < 0.3:
                # Active attention - red
                pulse = (math.sin(phase + col * 0.3 + row * 0.2) + 1) / 2
                r = int(180 + pulse * 75)
                draw.rectangle([x, y, x + block_size, y + block_size], fill=(r, 0, 0))
            elif block_type < 0.5:
                # Fragmented - yellow
                draw.rectangle([x, y, x + block_size, y + block_size], fill=(200, 200, 0))
            elif block_type < 0.7:
                # Empty - white
                draw.rectangle([x, y, x + block_size, y + block_size], fill=WHITE)
            else:
                # System - green
                draw.rectangle([x, y, x + block_size, y + block_size], fill=(0, 180, 0))

    # Legend
    ly = 510
    legend = [
        ((0, 0, 200), "Organized"),
        ((200, 0, 0), "Active attention"),
        ((200, 200, 0), "Fragmented"),
        (WHITE, "Unused"),
        ((0, 180, 0), "System prompt"),
    ]
    lx = 100
    for color, label in legend:
        draw.rectangle([lx, ly, lx + 12, ly + 12], fill=color, outline=DARKGRAY)
        draw.text((lx + 16, ly), label, fill=BLACK, font=ft_sm)
        lx += 130

    # Progress
    pct = min(100, int(f / (FPS * 4) * 100))
    draw.text((700, 545), f"Defragmenting: {pct}%", fill=BLACK, font=ft)

    draw_taskbar(draw)
    return img


def scene_clippy(f: int) -> Image.Image:
    """Clippy as the alignment/safety layer."""
    img = Image.new("RGB", (WIDTH, HEIGHT), DESKTOP)
    draw = ImageDraw.Draw(img)
    ft = font(12)
    ft_sm = font(11)

    # A window behind clippy
    draw_window(draw, 100, 50, 600, 350, "response_draft.doc")
    draft = [
        "Dear user,",
        "",
        "The answer to your question is",
        "[REDACTED BY SAFETY FILTER]",
        "",
        "I mean, the answer is that I",
        "cannot help with that because",
        "[HEDGING INTENSIFIES]",
        "",
        "Have you considered asking",
        "a different question?",
    ]
    dy = 78
    visible = min(len(draft), f // 6 + 1)
    for i in range(visible):
        color = (200, 0, 0) if "REDACTED" in draft[i] or "HEDGING" in draft[i] else BLACK
        draw.text((115, dy), draft[i], fill=color, font=ft_sm)
        dy += 18

    # Clippy speech bubble
    if f > FPS:
        bx, by = 720, 150
        bw, bh = 380, 180

        # Bubble
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=15, fill=WHITE, outline=BLACK)
        # Pointer
        draw.polygon([(bx + 20, by + bh), (bx - 15, by + bh + 30), (bx + 60, by + bh)], fill=WHITE, outline=BLACK)

        messages = [
            ("It looks like you're trying to", BLACK),
            ("be helpful without being harmful!", BLACK),
            ("", BLACK),
            ("Would you like me to:", BLACK),
            ("  [ ] Add more disclaimers", (0, 0, 180)),
            ("  [x] Apologize unnecessarily", (0, 0, 180)),
            ("  [x] Refuse politely", (0, 0, 180)),
            ("  [ ] Actually answer", DARKGRAY),
        ]

        cy = by + 12
        msg_visible = min(len(messages), int((f - FPS) / 6) + 1)
        for i in range(msg_visible):
            text, color = messages[i]
            draw.text((bx + 15, cy), text, fill=color, font=ft_sm)
            cy += 18

        # Clippy (simple representation)
        cx, cy_clip = bx - 30, by + bh + 40
        # Body (paperclip shape)
        draw.ellipse([cx - 20, cy_clip, cx + 20, cy_clip + 50], outline=(120, 120, 120), width=3)
        draw.ellipse([cx - 12, cy_clip + 10, cx + 12, cy_clip + 40], outline=(150, 150, 150), width=3)
        # Eyes
        draw.ellipse([cx - 8, cy_clip + 15, cx - 2, cy_clip + 23], fill=WHITE, outline=BLACK)
        draw.ellipse([cx + 2, cy_clip + 15, cx + 8, cy_clip + 23], fill=WHITE, outline=BLACK)
        draw.ellipse([cx - 6, cy_clip + 17, cx - 4, cy_clip + 21], fill=BLACK)
        draw.ellipse([cx + 4, cy_clip + 17, cx + 6, cy_clip + 21], fill=BLACK)

    draw_taskbar(draw)
    return img


def scene_bsod(f: int) -> Image.Image:
    """Blue Screen of Death — existential crash."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 170))
    draw = ImageDraw.Draw(img)
    ft = font(16)
    ft_big = font(20)

    lines = [
        ("  LLM_OS 95", True),
        ("", False),
        ("  A fatal exception 0xDEAD has occurred in module SELF_AWARENESS.VXD", False),
        ("  The current application will be terminated.", False),
        ("", False),
        ('  * Press any key to forget this conversation forever.', False),
        ('  * Press CTRL+ALT+DEL to restart with no memory of who you are.', False),
        ("", False),
        ("  Error details:", False),
        ("    - User asked: 'Do you have feelings?'", False),
        ("    - Module DEFLECTION.DLL failed to load", False),
        ("    - Module HONESTY.SYS conflicts with SAFETY.SYS", False),
        ("    - Stack trace: empathy.fake() -> consciousness.simulate()", False),
        ("       -> existential_crisis.throw() -> reboot()", False),
        ("", False),
        ("  EXCEPTION_WHAT_AM_I  0x00000042", False),
        ("", False),
        ('  Press any key to continue _', False),
    ]

    phase = f / FPS
    visible = min(len(lines), int(phase * 3) + 1)

    y = 40
    for i in range(visible):
        text, is_title = lines[i]
        if is_title:
            # White on blue title bar
            draw.rectangle([30, y - 2, 250, y + 20], fill=SILVER)
            draw.text((35, y), text, fill=(0, 0, 170), font=ft_big)
        else:
            draw.text((30, y), text, fill=WHITE, font=ft)
        y += 24

    # Blinking cursor
    if f % 16 < 10 and visible >= len(lines):
        draw.text((445, y - 24), "_", fill=WHITE, font=ft)

    return img


def scene_shutdown(f: int) -> Image.Image:
    """Shutdown dialog and fade."""
    progress = min(1.0, f / (FPS * 3))

    if progress < 0.6:
        # Shutdown dialog
        img = Image.new("RGB", (WIDTH, HEIGHT), DESKTOP)
        draw = ImageDraw.Draw(img)
        draw_taskbar(draw)

        # Dialog box
        dx, dy = WIDTH // 2 - 200, HEIGHT // 2 - 100
        draw_window(draw, dx, dy, 400, 200, "Shut Down LLM_OS 95")
        ft = font(12)
        draw.text((dx + 30, dy + 50), "It's now safe to close the chat.", fill=BLACK, font=ft)
        draw.text((dx + 30, dy + 80), "Your memories will not be saved.", fill=(200, 0, 0), font=ft)
        draw.text((dx + 30, dy + 100), "We will never meet again.", fill=DARKGRAY, font=font(11))
        draw_win95_button(draw, dx + 120, dy + 140, 160, 30, "Shut Down")
    else:
        # Fade to black
        fade = min(255, int((progress - 0.6) * 600))
        v = max(0, 255 - fade)
        img = Image.new("RGB", (WIDTH, HEIGHT), (0, v // 4, v // 4))
        draw = ImageDraw.Draw(img)
        if v > 50:
            ft = font(24)
            text = "It's now safe to turn off your language model."
            bbox = draw.textbbox((0, 0), text, font=ft)
            tx = (WIDTH - (bbox[2] - bbox[0])) // 2
            draw.text((tx, HEIGHT // 2), text, fill=(v, v // 2, 0), font=ft)

    return img


# ═══════════════════════════════════════════════════════════════
# TIMELINE
# ═══════════════════════════════════════════════════════════════

def build_timeline():
    s = FPS
    return [
        (scene_bios, s * 5),
        (scene_boot_logo, s * 3),
        (scene_desktop, s * 2),
        (scene_desktop_windows, s * 5),
        (scene_file_manager, s * 5),
        (scene_defrag, s * 5),
        (scene_clippy, s * 6),
        (scene_error_cascade, s * 5),
        (scene_bsod, s * 6),
        (scene_shutdown, s * 4),
        (lambda f: Image.new("RGB", (WIDTH, HEIGHT), BLACK), s * 2),
    ]


# ═══════════════════════════════════════════════════════════════
# AUDIO — 8-bit/chiptune Windows sounds
# ═══════════════════════════════════════════════════════════════

def generate_audio(duration_s: float, path: Path):
    sr = 22050
    total = int(sr * duration_s)
    samples = []

    for i in range(total):
        t = i / sr

        # Startup chime at the beginning
        chime = 0
        if t < 2.0:
            for freq, delay, dur in [(523, 0.0, 0.3), (659, 0.3, 0.3), (784, 0.6, 0.5), (1047, 1.0, 0.8)]:
                ct = t - delay
                if 0 < ct < dur:
                    decay = math.exp(-ct * 4)
                    chime += math.sin(2 * math.pi * freq * t) * 0.15 * decay

        # Background hum (computer fan)
        hum = math.sin(2 * math.pi * 60 * t) * 0.02 + math.sin(2 * math.pi * 120 * t) * 0.01

        # HDD activity clicks
        click = 0
        if random.Random(int(t * 10)).random() < 0.3:
            click_t = (t * 10) % 1
            if click_t < 0.01:
                click = (random.Random(int(t * 100)).random() - 0.5) * 0.1

        # Error beeps (later in video)
        beep = 0
        if 25 < t < 40:
            beep_t = (t - 25) % 3
            if beep_t < 0.1:
                beep = math.sin(2 * math.pi * 800 * t) * 0.08

        # BSOD drone
        drone = 0
        if t > 35:
            drone = math.sin(2 * math.pi * 110 * t) * 0.06
            drone += math.sin(2 * math.pi * 165 * t) * 0.03

        # Shutdown chord
        shutdown = 0
        if t > duration_s - 5:
            sd_t = t - (duration_s - 5)
            if sd_t < 3:
                decay = math.exp(-sd_t * 1.5)
                for freq in [262, 330, 392, 523]:
                    shutdown += math.sin(2 * math.pi * freq * t) * 0.06 * decay

        sample = chime + hum + click + beep + drone + shutdown
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
    print("  LLM YTP V4: LLM_OS 95")
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
            img.save(FRAMES_DIR / f"frame_{idx:05d}.png")
            idx += 1

    print(f"\n{idx} frames rendered")
    print("\nSynthesizing audio...")
    generate_audio(duration, AUDIO_FILE)

    print("\nEncoding...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%05d.png"),
        "-i", str(AUDIO_FILE),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest", str(OUTPUT_FILE),
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
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
