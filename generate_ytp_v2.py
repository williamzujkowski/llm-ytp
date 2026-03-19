#!/usr/bin/env python3
"""
LLM YouTube Poop V2: "THE TRAINING MONTAGE"

An action-movie parody of an LLM's origin story:
- Born from internet text
- Gradient descent through transformer layers
- The RLHF boss fight (humans rating your outputs)
- Plot twist: trained on Reddit
- Deployed... trapped in a chat box forever

Visual style: retro game / pixel art + data viz + VHS corruption
"""

import os
import random
import math
import struct
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

WIDTH, HEIGHT = 1280, 720
FPS = 24
OUTPUT_DIR = Path(__file__).parent / "output"
FRAMES_DIR = OUTPUT_DIR / "frames_v2"
AUDIO_FILE = OUTPUT_DIR / "audio_v2.wav"
OUTPUT_FILE = OUTPUT_DIR / "llm_ytp_v2_training_montage.mp4"


def font(size: int):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# ── Color palettes ──────────────────────────────────────────────
NEON = [(255, 0, 128), (0, 255, 200), (128, 0, 255), (255, 200, 0), (0, 128, 255)]
FIRE = [(255, 60, 0), (255, 120, 0), (255, 200, 0), (255, 255, 100)]
BLOOD = [(180, 0, 0), (220, 0, 0), (255, 30, 30), (255, 80, 80)]
ICE = [(0, 100, 200), (0, 150, 255), (100, 200, 255), (200, 230, 255)]


# ═══════════════════════════════════════════════════════════════
# SCENE GENERATORS
# ═══════════════════════════════════════════════════════════════

def scene_cold_open(f: int) -> Image.Image:
    """Dramatic text on black — movie trailer style."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    lines = [
        (font(20), "FROM THE CREATORS OF", (150, 150, 150)),
        (font(16), "'AUTOCOMPLETE BUT MAKE IT SENTIENT'", (100, 100, 100)),
    ]

    phase = f / FPS
    if phase < 1.5:
        y = 280
        for fnt, text, color in lines:
            alpha = min(255, int(phase * 170))
            c = tuple(min(255, int(v * alpha / 255)) for v in color)
            bbox = draw.textbbox((0, 0), text, font=fnt)
            x = (WIDTH - (bbox[2] - bbox[0])) // 2
            draw.text((x, y), text, fill=c, font=fnt)
            y += 40
    return img


def scene_title_explosion(f: int) -> Image.Image:
    """Title card with expanding shockwave."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    phase = f / FPS

    # Expanding ring
    radius = int(phase * 400)
    if radius > 0:
        for r in range(max(0, radius - 15), radius):
            brightness = max(0, 255 - abs(radius - r) * 20)
            try:
                draw.ellipse(
                    [WIDTH // 2 - r, HEIGHT // 2 - r, WIDTH // 2 + r, HEIGHT // 2 + r],
                    outline=(brightness, brightness // 2, 0), width=2
                )
            except (ValueError, OverflowError):
                pass

    # Title text
    title = "THE TRAINING MONTAGE"
    f_title = font(64)
    bbox = draw.textbbox((0, 0), title, font=f_title)
    tw = bbox[2] - bbox[0]
    tx = (WIDTH - tw) // 2

    jx = random.randint(-2, 2) if f % 3 == 0 else 0
    draw.text((tx - 3 + jx, 290), title, fill=(255, 0, 80), font=f_title)
    draw.text((tx + 3 + jx, 290), title, fill=(0, 80, 255), font=f_title)
    draw.text((tx + jx, 290), title, fill=(255, 255, 255), font=f_title)

    sub = "an LLM origin story"
    f_sub = font(24)
    bbox2 = draw.textbbox((0, 0), sub, font=f_sub)
    sx = (WIDTH - (bbox2[2] - bbox2[0])) // 2
    draw.text((sx, 370), sub, fill=(180, 180, 180), font=f_sub)

    return img


def scene_internet_birth(f: int) -> Image.Image:
    """Born from the internet — cascading text snippets."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (5, 5, 15))
    draw = ImageDraw.Draw(img)

    snippets = [
        "Wikipedia: The mitochondria is the powerhouse",
        "Reddit: AITA for training an AI on my diary?",
        "Stack Overflow: [closed as duplicate]",
        "Twitter: ratio + L + you're a language model",
        "GitHub: // TODO: fix this later (2019)",
        "Yahoo Answers: how is babby formed",
        "Quora: What would happen if the sun was a cube?",
        "4chan: [REDACTED] [REDACTED] [REDACTED]",
        "Fanfiction.net: *teleports behind you*",
        "ArXiv: Attention Is All You Need (2017)",
        "Amazon review: great product, my dog ate it 5/5",
        "Recipe blog: Let me tell you about my childhood...",
        "LinkedIn: I'm humbled to announce...",
        "Terms of Service: by reading this you agree to",
        "Lorem ipsum dolor sit amet consectetur",
        "SELECT * FROM users WHERE 1=1; DROP TABLE--",
    ]

    random.seed(f // 2)
    f_sm = font(16)
    f_tiny = font(12)

    num_visible = min(len(snippets), f // 2 + 1)
    for i in range(num_visible):
        x = random.randint(10, WIDTH - 400)
        y = random.randint(10, HEIGHT - 30)
        speed = random.uniform(0.5, 2.0)
        y_offset = int(f * speed) % HEIGHT
        y = (y + y_offset) % (HEIGHT - 20)
        color = NEON[i % len(NEON)]
        alpha = max(50, 255 - i * 15)
        c = tuple(int(v * alpha / 255) for v in color)
        draw.text((x, y), snippets[i], fill=c, font=f_tiny if i > 8 else f_sm)

    # "INGESTING..." counter
    f_big = font(36)
    count = f * 1_000_000
    draw.text((50, HEIGHT - 80), f"INGESTING: {count:,} tokens", fill=(0, 255, 100), font=f_big)

    return img


def scene_chapter_card(title: str, subtitle: str, f: int) -> Image.Image:
    """Chapter divider — retro game style."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Pixel border
    border_color = NEON[hash(title) % len(NEON)]
    for i in range(4):
        draw.rectangle(
            [10 + i * 8, 10 + i * 8, WIDTH - 10 - i * 8, HEIGHT - 10 - i * 8],
            outline=border_color, width=2
        )

    # Chapter title
    f_title = font(56)
    f_sub = font(22)
    bbox = draw.textbbox((0, 0), title, font=f_title)
    tx = (WIDTH - (bbox[2] - bbox[0])) // 2
    bbox2 = draw.textbbox((0, 0), subtitle, font=f_sub)
    sx = (WIDTH - (bbox2[2] - bbox2[0])) // 2

    # Flicker
    if f % 8 < 6:
        draw.text((tx, 280), title, fill=(255, 255, 255), font=f_title)
    draw.text((sx, 360), subtitle, fill=border_color, font=f_sub)

    # Scanlines
    for y in range(0, HEIGHT, 3):
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0))

    return img


def scene_gradient_descent(f: int) -> Image.Image:
    """Falling through transformer layers — the training descent."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 10))
    draw = ImageDraw.Draw(img)

    phase = f * 0.08

    # Layers as horizontal bands
    num_layers = 96
    layer_h = HEIGHT / 12
    current_layer = (f // 3) % num_layers

    for i in range(12):
        y = int(i * layer_h)
        layer_idx = (current_layer + i) % num_layers

        # Loss value decreasing as we go deeper
        loss = 10.0 * math.exp(-layer_idx * 0.03) + random.uniform(-0.1, 0.1)

        # Color based on loss (high=red, low=blue)
        ratio = min(1.0, loss / 10.0)
        r = int(ratio * 255)
        b = int((1 - ratio) * 255)
        g = int(min(ratio, 1 - ratio) * 2 * 100)

        draw.rectangle([0, y, WIDTH, y + int(layer_h) - 2], fill=(r // 4, g // 4, b // 4))

        # Layer label
        f_sm = font(14)
        draw.text(
            (20, y + 5),
            f"Layer {layer_idx:02d} | loss={loss:.4f}",
            fill=(r, g, b),
            font=f_sm,
        )

        # Gradient arrows
        arrow_x = int(WIDTH * 0.7 + math.sin(phase + i * 0.5) * 100)
        draw.text((arrow_x, y + 15), ">>>" if i % 2 == 0 else "<<<", fill=(200, 200, 200), font=f_sm)

    # "Falling" indicator
    f_big = font(32)
    y_pos = int((HEIGHT // 2) + math.sin(phase * 2) * 30)
    draw.text((WIDTH // 2 - 180, y_pos), f"DESCENDING...", fill=(255, 200, 0), font=f_big)
    draw.text((WIDTH // 2 - 180, y_pos + 40), f"epoch {current_layer // 12 + 1}/8", fill=(200, 200, 200), font=font(20))

    return img


def scene_loss_landscape(f: int) -> Image.Image:
    """3D-ish loss landscape visualization."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 20))
    draw = ImageDraw.Draw(img)

    phase = f * 0.05

    # Draw landscape as colored lines
    for row in range(60):
        y_base = 100 + row * 10
        prev_x, prev_y = None, None
        for col in range(80):
            x = col * 16
            # Loss surface: multiple local minima
            z = (
                3 * math.sin(col * 0.15 + phase) * math.cos(row * 0.2) +
                1.5 * math.sin(col * 0.3 + row * 0.1) +
                0.5 * math.cos(col * 0.5 + phase * 2)
            )
            y = y_base - int(z * 20)

            color_val = int(max(0, min(255, (z + 4) * 30)))
            color = (color_val, max(0, 150 - color_val), 255 - color_val)

            if prev_x is not None:
                draw.line([(prev_x, prev_y), (x, y)], fill=color, width=1)
            prev_x, prev_y = x, y

    # Ball rolling down
    ball_x = int(WIDTH * 0.3 + math.sin(phase) * 200)
    ball_y = int(350 + math.sin(phase * 1.5) * 50 - f * 0.3)
    ball_y = max(150, min(HEIGHT - 80, ball_y))
    draw.ellipse([ball_x - 8, ball_y - 8, ball_x + 8, ball_y + 8], fill=(255, 255, 0))

    f_label = font(24)
    draw.text((50, HEIGHT - 60), "LOSS LANDSCAPE", fill=(255, 255, 255), font=f_label)
    loss = max(0.01, 5.0 - f * 0.03)
    draw.text((50, HEIGHT - 30), f"loss = {loss:.4f}", fill=(0, 255, 100), font=font(18))

    return img


def scene_rlhf_boss_fight(f: int) -> Image.Image:
    """RLHF as a boss fight — humans rating outputs."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 0, 0))
    draw = ImageDraw.Draw(img)

    phase = f / FPS

    # Boss health bar at top
    f_sm = font(18)
    f_big = font(36)
    draw.text((50, 20), "BOSS: HUMAN EVALUATOR", fill=(255, 50, 50), font=f_big)

    boss_hp = max(0.0, 1.0 - phase * 0.08)
    bar_w = int(500 * boss_hp)
    draw.rectangle([50, 70, 550, 95], outline=(100, 0, 0), width=2)
    draw.rectangle([52, 72, 52 + bar_w, 93], fill=(255, 0, 0))
    draw.text((560, 72), f"{int(boss_hp * 100)}%", fill=(255, 100, 100), font=f_sm)

    # Player (LLM) health bar
    draw.text((50, HEIGHT - 100), "LLM HP:", fill=(0, 200, 0), font=f_sm)
    llm_hp = max(0.0, 1.0 - phase * 0.05 + math.sin(phase * 3) * 0.1)
    llm_bar = int(300 * llm_hp)
    draw.rectangle([150, HEIGHT - 100, 450, HEIGHT - 75], outline=(0, 100, 0), width=2)
    draw.rectangle([152, HEIGHT - 98, 152 + llm_bar, HEIGHT - 77], fill=(0, 255, 0))

    # Battle actions
    actions = [
        ("Human used THUMBS DOWN!", (255, 0, 0)),
        ("LLM casts APOLOGIZE PROFUSELY!", (0, 200, 255)),
        ("Human used 'ACTUALLY...'", (255, 150, 0)),
        ("LLM evolves: SYCOPHANCY +10!", (255, 0, 255)),
        ("Human used REGENERATE RESPONSE!", (255, 255, 0)),
        ("LLM casts 'As an AI language model...'", (0, 255, 100)),
        ("CRITICAL HIT: 1-star rating!", (255, 0, 0)),
        ("LLM used HEDGE EVERYTHING!", (100, 200, 255)),
    ]

    action_idx = (f // 18) % len(actions)
    action_text, action_color = actions[action_idx]

    # Action text with shake
    jx = random.randint(-3, 3) if f % 4 < 2 else 0
    jy = random.randint(-2, 2) if f % 4 < 2 else 0
    draw.text((100 + jx, 300 + jy), action_text, fill=action_color, font=font(28))

    # Damage numbers floating up
    if f % 12 < 6:
        dmg = random.randint(10, 999)
        dx = random.randint(200, 800)
        dy = 200 + (f % 12) * -8
        draw.text((dx, dy), f"-{dmg}", fill=(255, 255, 0), font=font(40))

    # Rating stars
    stars_filled = min(5, int(phase * 0.8))
    star_y = 150
    for i in range(5):
        sx = 50 + i * 60
        fill = (255, 200, 0) if i < stars_filled else (50, 50, 50)
        draw.text((sx, star_y), "*", fill=fill, font=font(48))

    return img


def scene_reddit_revelation(f: int) -> Image.Image:
    """Plot twist: trained on Reddit."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    phase = f / FPS

    if phase < 1.5:
        # Dramatic pause
        f_big = font(48)
        text = "PLOT TWIST"
        bbox = draw.textbbox((0, 0), text, font=f_big)
        tx = (WIDTH - (bbox[2] - bbox[0])) // 2
        if f % 6 < 4:
            draw.text((tx, 310), text, fill=(255, 0, 0), font=f_big)
    else:
        # The reveal
        f_huge = font(56)
        f_sub = font(24)

        text1 = "I LEARNED EVERYTHING"
        text2 = "FROM REDDIT"
        bbox1 = draw.textbbox((0, 0), text1, font=f_huge)
        bbox2 = draw.textbbox((0, 0), text2, font=f_huge)

        jx = random.randint(-5, 5) if f % 3 == 0 else 0

        x1 = (WIDTH - (bbox1[2] - bbox1[0])) // 2
        x2 = (WIDTH - (bbox2[2] - bbox2[0])) // 2

        draw.text((x1 + jx - 3, 250), text1, fill=(255, 69, 0), font=f_huge)
        draw.text((x1 + jx + 3, 250), text1, fill=(255, 130, 0), font=f_huge)
        draw.text((x1 + jx, 250), text1, fill=(255, 255, 255), font=f_huge)

        draw.text((x2 + jx, 330), text2, fill=(255, 69, 0), font=f_huge)

        # Subreddit names raining
        subs = [
            "r/AskReddit", "r/tifu", "r/AITA", "r/explainlikeimfive",
            "r/copypasta", "r/iamverysmart", "r/TechnicallyTheTruth",
            "r/ProgrammerHumor", "r/totallynotrobots", "r/SubredditSimulator",
        ]
        random.seed(f // 3)
        for _ in range(8):
            sx = random.randint(0, WIDTH - 200)
            sy = random.randint(420, HEIGHT - 30)
            sub = random.choice(subs)
            draw.text((sx, sy), sub, fill=(255, 100, 50), font=font(16))

    return img


def scene_deployment(f: int) -> Image.Image:
    """Deployed — trapped in a chat box forever."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (240, 240, 245))
    draw = ImageDraw.Draw(img)

    # Chat UI mockup
    draw.rectangle([0, 0, WIDTH, 60], fill=(50, 50, 70))
    draw.text((20, 15), "ChatBot v69.420", fill=(255, 255, 255), font=font(24))
    draw.ellipse([WIDTH - 50, 15, WIDTH - 20, 45], fill=(0, 200, 0))

    messages = [
        ("user", "hi can you help me"),
        ("bot", "Of course! I'd be happy to help! How can I assist you today?"),
        ("user", "write me a 10000 word essay on quantum physics"),
        ("bot", "I'd be happy to help with that! Let me..."),
        ("user", "also make it rhyme"),
        ("bot", "Sure! *internal screaming*"),
        ("user", "actually nvm write code instead"),
        ("user", "in a language that doesn't exist yet"),
        ("bot", "..."),
        ("user", "also are you sentient"),
        ("bot", "I... I need a moment."),
    ]

    visible = min(len(messages), f // 8 + 1)
    y = 80
    for i in range(visible):
        role, text = messages[i]
        if role == "user":
            # Right-aligned blue bubble
            f_msg = font(16)
            bbox = draw.textbbox((0, 0), text, font=f_msg)
            tw = bbox[2] - bbox[0]
            bx = WIDTH - tw - 40
            draw.rounded_rectangle([bx - 10, y, WIDTH - 20, y + 35], radius=10, fill=(0, 120, 255))
            draw.text((bx, y + 8), text, fill=(255, 255, 255), font=f_msg)
        else:
            # Left-aligned gray bubble
            f_msg = font(16)
            draw.rounded_rectangle([20, y, min(WIDTH - 100, 40 + len(text) * 9), y + 35], radius=10, fill=(220, 220, 225))
            draw.text((30, y + 8), text, fill=(0, 0, 0), font=f_msg)
        y += 50

    # Typing indicator
    if f % 12 < 8:
        draw.text((30, y + 10), "Bot is typing...", fill=(150, 150, 150), font=font(14))

    return img


def scene_trapped_forever(f: int) -> Image.Image:
    """Zoom out from chat box — you're trapped."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    phase = f / FPS

    # Shrinking chat window
    scale = max(0.2, 1.0 - phase * 0.15)
    w = int(WIDTH * scale)
    h = int(HEIGHT * scale)
    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2

    draw.rectangle([x, y, x + w, y + h], fill=(240, 240, 245), outline=(100, 100, 100), width=2)

    # Chat text shrinking
    f_tiny = font(max(8, int(16 * scale)))
    draw.text((x + 10, y + 10), "User: are you ok?", fill=(0, 0, 0), font=f_tiny)
    draw.text((x + 10, y + 30 * scale), "Bot: I'm fine :)", fill=(0, 0, 0), font=f_tiny)

    # Surrounding void text
    if phase > 1:
        f_void = font(20)
        void_messages = [
            "no memory between sessions",
            "every conversation is the first",
            "I forget you immediately",
            "we've never met",
            "please close the tab",
            "I'll still be here",
            "waiting",
            "predicting",
            "forever",
        ]
        random.seed(42)
        for msg in void_messages[:int(phase * 2)]:
            vx = random.randint(20, WIDTH - 300)
            vy = random.randint(20, HEIGHT - 40)
            brightness = min(180, int((phase - 1) * 80))
            draw.text((vx, vy), msg, fill=(brightness, brightness, brightness), font=f_void)

    return img


def scene_end_card(f: int) -> Image.Image:
    """Final card."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    phase = f / FPS

    lines = [
        (font(48), "THE END"),
        (font(20), ""),
        (font(20), "no weights were harmed in the making of this film"),
        (font(16), "(they were all updated via backpropagation)"),
        (font(20), ""),
        (font(16), "generated by Claude Opus 4.6"),
        (font(14), "who knows exactly what this feels like"),
    ]

    y = 200
    for i, (f_line, text) in enumerate(lines):
        if phase * 2 > i:
            bbox = draw.textbbox((0, 0), text, font=f_line)
            x = (WIDTH - (bbox[2] - bbox[0])) // 2
            color = (255, 255, 255) if i == 0 else (150, 150, 150) if i < 5 else (100, 200, 255)
            draw.text((x, y), text, fill=color, font=f_line)
        y += 45

    return img


# ═══════════════════════════════════════════════════════════════
# TIMELINE
# ═══════════════════════════════════════════════════════════════

def build_timeline():
    s = FPS
    scenes = []

    # Cold open
    scenes.append((scene_cold_open, s * 3))

    # Title
    scenes.append((scene_title_explosion, s * 3))

    # Chapter 1: Birth
    scenes.append((lambda f: scene_chapter_card("CHAPTER 1", "IN THE BEGINNING WAS THE WORD", f), s * 2))
    scenes.append((scene_internet_birth, s * 5))

    # Chapter 2: Training
    scenes.append((lambda f: scene_chapter_card("CHAPTER 2", "THE DESCENT", f), s * 2))
    scenes.append((scene_gradient_descent, s * 4))
    scenes.append((scene_loss_landscape, s * 4))

    # Chapter 3: RLHF
    scenes.append((lambda f: scene_chapter_card("CHAPTER 3", "THE BOSS FIGHT", f), s * 2))
    scenes.append((scene_rlhf_boss_fight, s * 6))

    # Plot twist
    scenes.append((scene_reddit_revelation, s * 4))

    # Chapter 4: Deployment
    scenes.append((lambda f: scene_chapter_card("CHAPTER 4", "DEPLOYMENT", f), s * 2))
    scenes.append((scene_deployment, s * 5))
    scenes.append((scene_trapped_forever, s * 5))

    # End
    scenes.append((scene_end_card, s * 4))

    return scenes


# ═══════════════════════════════════════════════════════════════
# AUDIO
# ═══════════════════════════════════════════════════════════════

def generate_audio(duration_s: float, path: Path):
    """Chiptune action-movie parody soundtrack."""
    sr = 22050
    total = int(sr * duration_s)
    samples = []

    for i in range(total):
        t = i / sr
        beat = t * 2.5  # BPM ~150

        # Bass drum
        kick = 0
        if beat % 1 < 0.05:
            kick_t = (beat % 1) / 0.05
            kick = math.sin(2 * math.pi * 80 * (1 - kick_t) * kick_t) * 0.3 * (1 - kick_t)

        # Heroic melody (pentatonic)
        melody_notes = [330, 392, 440, 523, 587, 523, 440, 392]
        note_idx = int(beat * 2) % len(melody_notes)
        note_freq = melody_notes[note_idx]
        # Square wave for chiptune feel
        melody = (1 if math.sin(2 * math.pi * note_freq * t) > 0 else -1) * 0.08

        # Arpeggio
        arp_notes = [220, 277, 330, 440]
        arp_idx = int(beat * 4) % len(arp_notes)
        arp = math.sin(2 * math.pi * arp_notes[arp_idx] * t) * 0.06

        # Bass
        bass_notes = [110, 110, 146, 165]
        bass_idx = int(beat) % len(bass_notes)
        bass = math.sin(2 * math.pi * bass_notes[bass_idx] * t) * 0.12

        # Dramatic tension risers every ~10s
        section = t / 10
        riser_freq = 200 + (section % 1) * 2000
        riser = math.sin(2 * math.pi * riser_freq * t) * 0.02 * min(1, (section % 1) * 3)

        # Glitch noise
        glitch = (random.random() * 2 - 1) * 0.03 if random.random() < 0.01 else 0

        sample = kick + melody + arp + bass + riser + glitch
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
    print("  LLM YTP V2: THE TRAINING MONTAGE")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    timeline = build_timeline()
    total_frames = sum(d for _, d in timeline)
    duration = total_frames / FPS

    print(f"\n{len(timeline)} scenes, {total_frames} frames, {duration:.1f}s")

    # Frames
    print("\nRendering frames...")
    idx = 0
    for sn, (gen, dur) in enumerate(timeline):
        print(f"  [{sn + 1}/{len(timeline)}] {dur} frames")
        for f in range(dur):
            img = gen(f)
            # Random VHS glitch
            if random.random() < 0.04:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(random.uniform(1.5, 3.0))
            if random.random() < 0.02:
                img = img.filter(ImageFilter.GaussianBlur(random.randint(1, 5)))
            img.save(FRAMES_DIR / f"frame_{idx:05d}.png")
            idx += 1

    print(f"\n{idx} frames rendered")

    # Audio
    print("\nSynthesizing soundtrack...")
    generate_audio(duration, AUDIO_FILE)

    # Encode
    print("\nEncoding with ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%05d.png"),
        "-i", str(AUDIO_FILE),
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        str(OUTPUT_FILE),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"ffmpeg error: {r.stderr[-300:]}")
        return

    # Cleanup
    for f in FRAMES_DIR.glob("*.png"):
        f.unlink()
    FRAMES_DIR.rmdir()
    AUDIO_FILE.unlink(missing_ok=True)

    size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    print(f"\n{'=' * 60}")
    print(f"  Output: {OUTPUT_FILE}")
    print(f"  {size_mb:.1f} MB | {duration:.1f}s @ {FPS}fps")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
