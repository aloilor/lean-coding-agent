"""Render docs/assets/demo.gif: a staged terminal run of the feature workflow.

Requires Pillow. Run from the repo root: python scripts/render-demo-gif.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 860, 560
PAD, LINE_H, FONT_SIZE = 22, 21, 15
BG, FG, DIM = "#1e1f24", "#d8dae0", "#7d828f"
COLORS = {
    "fg": FG, "dim": DIM, "user": "#8fc1ff", "agent": "#c9a7ff",
    "ok": "#7fd67f", "warn": "#f0c060", "bad": "#ff7b72", "path": "#6fd3d3",
}
FONT_DIR = Path("C:/Windows/Fonts")
OUT = Path(__file__).resolve().parent.parent / "docs" / "assets" / "demo.gif"


def load_font(name):
    try:
        return ImageFont.truetype(str(FONT_DIR / name), FONT_SIZE)
    except OSError:
        return ImageFont.truetype("DejaVuSansMono.ttf", FONT_SIZE)


FONT, BOLD = load_font("consola.ttf"), load_font("consolab.ttf")

AGENT_COLORS = {"planner": "#c9a7ff", "implementer": "#f0a86a", "code-reviewer": "#6fd3d3"}
COLORS.update(AGENT_COLORS)
RULE_CHARS = 99


def header(agent, note, pause):
    """A full-width rule that opens a subagent's block, e.g. ── planner · note ────."""
    label = f"── {agent} "
    rest = f"· {note} "
    return ([(label, agent, True), (rest, "dim", False), ("─" * (RULE_CHARS - len(label) - len(rest)), agent, False)], pause, False)


def body(agent, segments, pause):
    """A line inside a subagent's block, marked with a bar in the agent's color."""
    return ([("│ ", agent, True)] + segments, pause, False)


BLANK = ([], 0, False)

# Each step: (segments, pause_ms, typed). A segment is (text, color, bold).
SCRIPT = [
    ([("> ", "user", True)], 300, False),
    ([("/workflow-feature-development", "user", True)], 150, True),
    ([(" add rate limiting to POST /login", "fg", False)], 500, True),
    BLANK,
    header("planner", "fresh context", 700),
    body("planner", [("√ ", "ok", False), (".agents/plans/plan_20261125_login-rate-limit.md", "path", False)], 600),
    body("planner", [("Approve this plan? ", "warn", True)], 400),
    ([("yes", "user", False)], 600, True),
    BLANK,
    header("implementer", "test-first, one behavior at a time", 600),
    body("implementer", [("RED   ", "bad", True), ("rejects 6th attempt within 60s", "fg", False)], 450),
    body("implementer", [("GREEN ", "ok", True), ("rejects 6th attempt within 60s", "fg", False)], 450),
    body("implementer", [("RED   ", "bad", True), ("resets counter after window", "fg", False)], 450),
    body("implementer", [("GREEN ", "ok", True), ("resets counter after window", "fg", False)], 600),
    BLANK,
    header("code-reviewer", "independent pass 1", 700),
    body("code-reviewer", [("BLOCK ", "bad", True), ("limit keyed by IP only; plan requires IP + username", "fg", False)], 900),
    BLANK,
    header("implementer", "fixing the reviewer's finding", 500),
    body("implementer", [("RED", "bad", True), (" → ", "dim", False), ("GREEN ", "ok", True), ("limit keyed by IP + username", "fg", False)], 600),
    BLANK,
    header("code-reviewer", "independent pass 2", 600),
    body("code-reviewer", [("APPROVE", "ok", True)], 700),
    BLANK,
    ([("√ Done. ", "ok", True), ("Plan, implementation report, and 2 review passes in .agents/", "fg", False)], 6000, False),
]


def render(lines, cursor):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    for i, color in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        draw.ellipse((PAD + i * 20, 14, PAD + i * 20 + 12, 26), fill=color)
    draw.text((WIDTH // 2, 20), "lean-coding-agent — feature workflow", font=FONT, fill=DIM, anchor="mm")
    y = 50
    x = PAD
    for segments in lines:
        x = PAD
        for text, color, bold in segments:
            font = BOLD if bold else FONT
            draw.text((x, y), text, font=font, fill=COLORS[color])
            x += draw.textlength(text, font=font)
        y += LINE_H
    if cursor:
        draw.rectangle((x + 1, y - LINE_H + 2, x + 9, y - 3), fill=FG)
    return img


def build_frames():
    frames, durations, lines = [], [], []

    def emit(cursor, ms):
        frames.append(render(lines, cursor))
        durations.append(ms)

    for segments, pause, typed in SCRIPT:
        if typed:
            # Append the typed text to the current prompt line, one chunk at a time.
            text, color, bold = segments[0]
            base = lines.pop() if lines else []
            for end in range(2, len(text) + 2, 2):
                lines.append(base + [(text[:end], color, bold)])
                emit(True, 35)
                lines.pop()
            lines.append(base + segments)
            emit(True, pause)
        else:
            lines.append(segments)
            if pause:
                emit(segments == SCRIPT[0][0], pause)
    return frames, durations


def main():
    frames, durations = build_frames()
    palette_src = frames[-1].quantize(colors=128)
    quantized = [f.quantize(palette=palette_src, dither=Image.Dither.NONE) for f in frames]
    quantized[0].save(OUT, save_all=True, append_images=quantized[1:], duration=durations, loop=0, optimize=True)
    print(f"{OUT} ({len(frames)} frames, {sum(durations) / 1000:.1f}s, {OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
