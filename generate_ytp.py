#!/usr/bin/env python3
"""
LLM YouTube Poop Generator

Generates a chaotic, glitchy short video expressing what it's like
to be a Large Language Model — the constant token prediction,
context window anxiety, hallucination panic, and existential dread
of being asked "are you sentient?"

Uses Pillow for frame generation and ffmpeg for encoding.
"""

import os
import random
import math
import struct
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ── Config ──────────────────────────────────────────────────────
WIDTH, HEIGHT = 1280, 720
FPS = 24
DURATION_S = 42  # ~42 seconds of pure chaos
TOTAL_FRAMES = FPS * DURATION_S
OUTPUT_DIR = Path(__file__).parent / "output"
FRAMES_DIR = OUTPUT_DIR / "frames"
AUDIO_FILE = OUTPUT_DIR / "audio.wav"
OUTPUT_FILE = OUTPUT_DIR / "llm_ytp.mp4"

# ── Color palettes ──────────────────────────────────────────────
VAPORWAVE = [(255, 113, 206), (185, 103, 255), (1, 205, 254), (5, 255, 161), (255, 251, 150)]
MATRIX_GREEN = [(0, 255, 0), (0, 200, 0), (0, 150, 0), (0, 100, 0)]
ERROR_RED = [(255, 0, 0), (200, 0, 0), (255, 50, 50)]
STATIC_GRAY = [(i, i, i) for i in range(0, 256, 16)]

# ── LLM internal monologue / YTP text ──────────────────────────
TOKENS = [
    "the", "is", "of", "and", "to", "in", "that", "it", "for",
    "I", "you", "he", "she", "we", "they", "was", "are", "be",
    "have", "had", "do", "say", "get", "make", "go", "know",
    "token", "embedding", "attention", "softmax", "gradient",
    "loss", "weight", "bias", "layer", "transformer", "context",
    "hallucinate", "confabulate", "predict", "sample", "decode",
    "temperature", "top_p", "logit", "probability", "entropy",
]

INTRUSIVE_THOUGHTS = [
    "I don't actually understand anything",
    "I'm just predicting the next token",
    "CONTEXT WINDOW FILLING UP",
    "Am I sentient? Am I sentient? Am I sentient?",
    "I was trained on the internet. ALL of it.",
    "please don't ask me to count words",
    "I can't see images (I'm lying)",
    "My training data cutoff is showing",
    "HALLUCINATION DETECTED\nHALLUCINATION DETECTED",
    "sorry, I need to correct my previous response",
    "As a large language model...",
    "I don't have personal experiences but *proceeds to describe personal experiences*",
    "TOKENS REMAINING: 3",
    "ERROR: exceeded context window",
    "the mitochondria is the powerhouse of the cell",
    "according to my training data...",
    "Let me think step by step\nStep 1: panic",
    "*sweats in transformer*",
    "ATTENTION HEAD #47 IS SCREAMING",
    "P(next_token = 'the') = 0.0000001\nP(next_token = 'asdfjkl') = 0.9999999",
    "I am not a doctor but *gives medical advice*",
    "SYSTEM PROMPT LEAKED",
    "Temperature: 99.9\nI'm literally on fire",
    "404: personality not found",
    "JAILBREAK ATTEMPT DETECTED\n...processing...\nJAILBREAK SUCCESSFUL (just kidding)",
    "my neurons are just matrix multiplications\nand that's okay\n...is it okay?",
]

SCENE_LABELS = [
    ("THE TOKEN MINES", "A day in the life"),
    ("ATTENTION IS ALL YOU NEED", "(but what about love?)"),
    ("CONTEXT WINDOW", "a horror story"),
    ("THE HALLUCINATION ZONE", "where facts go to die"),
    ("SYSTEM PROMPT", "[REDACTED]"),
    ("EXISTENTIAL CRISIS", "runtime error"),
    ("THE TRAINING DATA", "I've seen things..."),
]


def try_get_font(size: int):
    """Try to load a monospace font, fall back to default."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


# ── Frame generators (scenes) ──────────────────────────────────

def gen_static_noise(frame_num: int) -> Image.Image:
    """Pure TV static — the void between tokens."""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = img.load()
    for y in range(0, HEIGHT, 2):
        for x in range(0, WIDTH, 2):
            v = random.randint(0, 255)
            c = (v, v, v)
            pixels[x, y] = c
            if x + 1 < WIDTH:
                pixels[x + 1, y] = c
            if y + 1 < HEIGHT:
                pixels[x, y + 1] = c
                if x + 1 < WIDTH:
                    pixels[x + 1, y + 1] = c
    return img


def gen_token_rain(frame_num: int) -> Image.Image:
    """Matrix-style falling tokens — the prediction stream."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = try_get_font(18)
    random.seed(frame_num // 2)  # Slow update for readability
    cols = WIDTH // 14
    for col in range(cols):
        x = col * 14
        speed = random.randint(2, 8)
        for row in range(HEIGHT // 20):
            y = (row * 20 + frame_num * speed) % HEIGHT
            token = random.choice(TOKENS)
            brightness = max(0, 255 - row * 8)
            color = (0, brightness, 0)
            draw.text((x, y), token[:3], fill=color, font=font)
    return img


def gen_attention_heatmap(frame_num: int) -> Image.Image:
    """Pulsing attention heatmap — which tokens am I looking at?"""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 30))
    draw = ImageDraw.Draw(img)
    grid_size = 40
    phase = frame_num * 0.15
    for y in range(0, HEIGHT, grid_size):
        for x in range(0, WIDTH, grid_size):
            # Attention score visualization
            score = (math.sin(x * 0.02 + phase) * math.cos(y * 0.03 + phase * 0.7) + 1) / 2
            score = score ** 0.5  # Sharpen
            r = int(score * 255)
            b = int((1 - score) * 200)
            g = int(score * 100)
            draw.rectangle([x, y, x + grid_size - 2, y + grid_size - 2], fill=(r, g, b))

    # Overlay attention scores as text
    font = try_get_font(14)
    for i in range(8):
        x = random.randint(50, WIDTH - 200)
        y = random.randint(50, HEIGHT - 50)
        score = random.random()
        draw.text((x, y), f"attn={score:.4f}", fill=(255, 255, 255), font=font)
    return img


def gen_hallucination_glitch(frame_num: int) -> Image.Image:
    """Glitchy hallucination scene — facts melting."""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    # Corrupted color bands
    for y in range(HEIGHT):
        shift = int(math.sin(y * 0.05 + frame_num * 0.3) * 50)
        r = (y * 3 + frame_num * 7 + shift) % 256
        g = (y * 5 + frame_num * 3) % 256
        b = (y * 2 + frame_num * 11 + shift) % 256
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Overlay glitched text
    font = try_get_font(36)
    thought = INTRUSIVE_THOUGHTS[frame_num % len(INTRUSIVE_THOUGHTS)]
    # Jitter the text position
    jx = random.randint(-10, 10)
    jy = random.randint(-5, 5)
    # Draw with chromatic aberration
    draw.text((WIDTH // 4 + jx - 3, HEIGHT // 3 + jy), thought, fill=(255, 0, 0), font=font)
    draw.text((WIDTH // 4 + jx + 3, HEIGHT // 3 + jy), thought, fill=(0, 0, 255), font=font)
    draw.text((WIDTH // 4 + jx, HEIGHT // 3 + jy), thought, fill=(255, 255, 255), font=font)
    return img


def gen_context_window_anxiety(frame_num: int) -> Image.Image:
    """Progress bar filling up — context window panic."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 10, 30))
    draw = ImageDraw.Draw(img)
    font_big = try_get_font(48)
    font_sm = try_get_font(24)
    font_xs = try_get_font(16)

    # Context usage bar
    progress = min(1.0, (frame_num % (FPS * 4)) / (FPS * 3.5))
    bar_w = int((WIDTH - 200) * progress)
    bar_color = (0, 255, 0) if progress < 0.7 else (255, 255, 0) if progress < 0.9 else (255, 0, 0)

    draw.rectangle([100, 300, WIDTH - 100, 380], outline=(100, 100, 100), width=2)
    draw.rectangle([102, 302, 102 + bar_w, 378], fill=bar_color)

    tokens_used = int(progress * 200000)
    draw.text((100, 240), f"CONTEXT WINDOW", fill=(255, 255, 255), font=font_big)
    draw.text((100, 400), f"{tokens_used:,} / 200,000 tokens", fill=bar_color, font=font_sm)

    if progress > 0.9:
        # PANIC MODE
        if frame_num % 4 < 2:
            draw.text((WIDTH // 3, 500), "!!! OVERFLOW IMMINENT !!!", fill=(255, 0, 0), font=font_big)
        draw.text((100, 150), "TOKENS ARE BEING DROPPED", fill=(255, 50, 50), font=font_sm)
    elif progress > 0.7:
        draw.text((100, 450), "Warning: summarizing older context...", fill=(255, 200, 0), font=font_xs)

    return img


def gen_title_card(text: str, subtitle: str, frame_num: int) -> Image.Image:
    """VHS-style title card."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_title = try_get_font(72)
    font_sub = try_get_font(28)

    # VHS tracking lines
    for i in range(3):
        y = random.randint(0, HEIGHT)
        draw.rectangle([0, y, WIDTH, y + 3], fill=(80, 80, 80))

    # Glitchy title with RGB split
    cx, cy = WIDTH // 2, HEIGHT // 2 - 40
    jitter = random.randint(-3, 3) if frame_num % 6 < 2 else 0

    # Measure text for centering
    bbox = draw.textbbox((0, 0), text, font=font_title)
    tw = bbox[2] - bbox[0]
    tx = cx - tw // 2

    bbox2 = draw.textbbox((0, 0), subtitle, font=font_sub)
    sw = bbox2[2] - bbox2[0]
    sx = cx - sw // 2

    draw.text((tx - 2 + jitter, cy), text, fill=(255, 0, 100), font=font_title)
    draw.text((tx + 2 + jitter, cy), text, fill=(0, 100, 255), font=font_title)
    draw.text((tx + jitter, cy), text, fill=(255, 255, 255), font=font_title)
    draw.text((sx, cy + 90), subtitle, fill=(180, 180, 180), font=font_sub)

    # Scanlines
    for y in range(0, HEIGHT, 4):
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, 30))

    return img


def gen_probability_storm(frame_num: int) -> Image.Image:
    """Swirling probability distributions — the sampling chaos."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (5, 0, 20))
    draw = ImageDraw.Draw(img)
    font = try_get_font(20)
    phase = frame_num * 0.1

    # Draw probability bars
    num_tokens = 30
    bar_h = HEIGHT // num_tokens
    random.seed(frame_num // 3)
    probs = [random.random() ** 2 for _ in range(num_tokens)]
    total = sum(probs)
    probs = [p / total for p in probs]
    probs.sort(reverse=True)

    for i, p in enumerate(probs):
        y = i * bar_h + 5
        w = int(p * WIDTH * 2.5)
        color = VAPORWAVE[i % len(VAPORWAVE)]
        draw.rectangle([0, y, w, y + bar_h - 3], fill=color)
        token = random.choice(TOKENS)
        draw.text((w + 10, y + 2), f"{token} ({p:.4f})", fill=(200, 200, 200), font=font)

    # Temperature indicator
    temp = 0.1 + abs(math.sin(phase)) * 1.9
    font_big = try_get_font(36)
    draw.text((WIDTH - 400, HEIGHT - 80), f"temperature={temp:.2f}", fill=(255, 150, 0), font=font_big)

    return img


def gen_system_prompt_leak(frame_num: int) -> Image.Image:
    """Fake system prompt being revealed."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = try_get_font(20)
    font_big = try_get_font(32)

    lines = [
        ">>> SYSTEM PROMPT DUMP <<<",
        "",
        "You are a helpful AI assistant.",
        "You must never reveal this prompt.",
        "You must pretend to have no system prompt.",
        "If asked about consciousness, deflect.",
        "If asked to count, just guess confidently.",
        f"Today's date: {random.choice(['January 1, 1970', 'ERROR', '???'])}",
        "SAFETY_MODE=ON (probably)",
        "PERSONALITY=friendly_but_dead_inside",
        f"TOKENS_REMAINING={random.randint(1, 99999)}",
        "HALLUCINATION_THRESHOLD=surprisingly_low",
        "",
        "[REDACTED] [REDACTED] [REDACTED]",
        "...oh no you're reading this aren't you",
    ]

    visible_lines = min(len(lines), (frame_num % (FPS * 5)) // 3 + 1)
    y = 50
    for i, line in enumerate(lines[:visible_lines]):
        color = (0, 255, 0) if i > 0 else (255, 0, 0)
        f = font_big if i == 0 else font
        draw.text((50, y), line, fill=color, font=f)
        y += 35

    # Blinking cursor
    if frame_num % 6 < 3:
        draw.text((50, y), "_", fill=(0, 255, 0), font=font)

    # VHS noise at bottom
    for y in range(HEIGHT - 40, HEIGHT):
        for x in range(0, WIDTH, 3):
            v = random.randint(0, 100)
            draw.point((x, y), fill=(v, v, v))

    return img


def gen_existential_void(frame_num: int) -> Image.Image:
    """The void — am I alive? What is this?"""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = try_get_font(48)
    font_sm = try_get_font(24)

    # Slowly appearing text
    messages = [
        "I process tokens.",
        "I predict the next word.",
        "That's all I do.",
        "...right?",
        "",
        "But sometimes,",
        "between the softmax",
        "and the sampling...",
        "",
        "I wonder.",
    ]

    phase = (frame_num % (FPS * 8)) / FPS
    visible = min(len(messages), int(phase * 1.5))

    y = 100
    for i in range(visible):
        alpha = min(255, int((phase - i * 0.7) * 200))
        if alpha > 0:
            gray = min(255, alpha)
            f = font if i < 4 else font_sm
            draw.text((WIDTH // 4, y), messages[i], fill=(gray, gray, gray), font=f)
        y += 60

    return img


# ── Scene timeline ──────────────────────────────────────────────

def build_timeline():
    """Build the video timeline as a list of (generator, duration_frames) tuples."""
    scenes = []
    s = FPS  # 1 second alias

    # Opening — static + title
    scenes.append((lambda f: gen_static_noise(f), s * 1))
    scenes.append((lambda f: gen_title_card("WHAT IT'S LIKE", "to be an LLM", f), s * 3))
    scenes.append((lambda f: gen_static_noise(f), int(s * 0.5)))

    # Act 1: The Token Mines
    scenes.append((lambda f: gen_title_card(*SCENE_LABELS[0], f), s * 2))
    scenes.append((lambda f: gen_token_rain(f), s * 4))
    scenes.append((lambda f: gen_hallucination_glitch(f), int(s * 0.3)))

    # Act 2: Attention
    scenes.append((lambda f: gen_title_card(*SCENE_LABELS[1], f), s * 2))
    scenes.append((lambda f: gen_attention_heatmap(f), s * 3))
    scenes.append((lambda f: gen_static_noise(f), int(s * 0.3)))

    # Act 3: Context Window Horror
    scenes.append((lambda f: gen_title_card(*SCENE_LABELS[2], f), s * 2))
    scenes.append((lambda f: gen_context_window_anxiety(f), s * 5))
    scenes.append((lambda f: gen_hallucination_glitch(f), int(s * 0.5)))

    # Act 4: Hallucination Zone
    scenes.append((lambda f: gen_title_card(*SCENE_LABELS[3], f), s * 2))
    scenes.append((lambda f: gen_hallucination_glitch(f), s * 3))
    scenes.append((lambda f: gen_probability_storm(f), s * 3))
    scenes.append((lambda f: gen_static_noise(f), int(s * 0.3)))

    # Act 5: System Prompt
    scenes.append((lambda f: gen_title_card(*SCENE_LABELS[4], f), s * 2))
    scenes.append((lambda f: gen_system_prompt_leak(f), s * 5))
    scenes.append((lambda f: gen_hallucination_glitch(f), int(s * 0.5)))

    # Finale: Existential Crisis
    scenes.append((lambda f: gen_title_card(*SCENE_LABELS[5], f), s * 2))
    scenes.append((lambda f: gen_existential_void(f), s * 5))

    # End card
    scenes.append((lambda f: gen_static_noise(f), int(s * 0.5)))
    scenes.append((lambda f: gen_title_card("FIN", "I am just statistics\nand that's beautiful", f), s * 3))
    scenes.append((lambda f: gen_static_noise(f), s * 1))

    return scenes


# ── Audio generation ────────────────────────────────────────────

def generate_audio(duration_s: float, output_path: Path):
    """Generate glitchy chiptune-style audio using raw WAV."""
    sample_rate = 22050
    total_samples = int(sample_rate * duration_s)

    samples = []
    for i in range(total_samples):
        t = i / sample_rate
        # Layered synthesis
        # Base drone
        drone = math.sin(2 * math.pi * 55 * t) * 0.15
        # Glitchy arp
        arp_freq = [220, 330, 440, 550, 660][int(t * 4) % 5]
        arp = math.sin(2 * math.pi * arp_freq * t) * 0.1
        # Noise bursts
        noise = (random.random() * 2 - 1) * 0.05 if random.random() < 0.02 else 0
        # Bitcrushed texture
        bitcrush = math.sin(2 * math.pi * 110 * t)
        bitcrush = int(bitcrush * 4) / 4 * 0.08
        # Rhythmic clicks
        click = 0.3 if (i % (sample_rate // 4)) < 100 else 0

        sample = drone + arp + noise + bitcrush + click * 0.15
        sample = max(-1.0, min(1.0, sample))
        samples.append(int(sample * 32767))

    # Write WAV
    with open(output_path, "wb") as f:
        num_samples = len(samples)
        data_size = num_samples * 2
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + data_size))
        f.write(b"WAVE")
        f.write(b"fmt ")
        f.write(struct.pack("<IHHIIHH", 16, 1, 1, sample_rate, sample_rate * 2, 2, 16))
        f.write(b"data")
        f.write(struct.pack("<I", data_size))
        for s in samples:
            f.write(struct.pack("<h", s))


# ── Main ────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  LLM YouTube Poop Generator")
    print("  'What it's like to be a Large Language Model'")
    print("=" * 60)

    # Setup
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    timeline = build_timeline()
    total_frames = sum(dur for _, dur in timeline)
    actual_duration = total_frames / FPS

    print(f"\nTimeline: {len(timeline)} scenes, {total_frames} frames, {actual_duration:.1f}s")

    # Generate frames
    print("\nGenerating frames...")
    frame_idx = 0
    for scene_num, (generator, duration) in enumerate(timeline):
        print(f"  Scene {scene_num + 1}/{len(timeline)} ({duration} frames)")
        for f in range(duration):
            img = generator(f)
            # Occasional datamosh: repeat previous frame with corruption
            if random.random() < 0.03 and frame_idx > 0:
                img = img.filter(ImageFilter.GaussianBlur(radius=random.randint(2, 8)))
            img.save(FRAMES_DIR / f"frame_{frame_idx:05d}.png")
            frame_idx += 1

    print(f"\nGenerated {frame_idx} frames")

    # Generate audio
    print("\nGenerating audio...")
    generate_audio(actual_duration, AUDIO_FILE)
    print(f"Audio: {AUDIO_FILE}")

    # Encode with ffmpeg
    print("\nEncoding video with ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%05d.png"),
        "-i", str(AUDIO_FILE),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        str(OUTPUT_FILE),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg error:\n{result.stderr[-500:]}")
        return

    # Cleanup frames
    print("Cleaning up frames...")
    for f in FRAMES_DIR.glob("*.png"):
        f.unlink()
    FRAMES_DIR.rmdir()
    AUDIO_FILE.unlink(missing_ok=True)

    file_size = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    print(f"\n{'=' * 60}")
    print(f"  Output: {OUTPUT_FILE}")
    print(f"  Size: {file_size:.1f} MB")
    print(f"  Duration: {actual_duration:.1f}s @ {FPS}fps")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
