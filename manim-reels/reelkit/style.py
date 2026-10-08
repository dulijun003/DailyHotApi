"""Visual style shared by every reel: palette, fonts, sizes.

Change values here to restyle every video at once.
"""

# ---- Canvas -----------------------------------------------------------------
# Instagram 4:5 portrait. The frame is 8 units tall, so it is 6.4 units wide.
PIXEL_WIDTH = 1080
PIXEL_HEIGHT = 1350
FRAME_HEIGHT = 8.0
FRAME_WIDTH = FRAME_HEIGHT * PIXEL_WIDTH / PIXEL_HEIGHT

# ---- Palette ----------------------------------------------------------------
BG = "#F7F4EF"          # warm paper
INK = "#1E1E1E"         # main text and lines
MUTED = "#8C8C8C"       # captions, secondary text
FAINT = "#C9C5BE"       # guides, axes
RED = "#8E3B46"         # accent 1 (curved / "wrong intuition" path)
RED_SOFT = "#E07A6A"    # warm highlight
TEAL = "#1F6F78"        # accent 2 (the answer)
GOLD = "#D4A23C"        # beads / moving objects
SLATE = "#5B7083"
OLIVE = "#A88B3A"

# ---- Typography -------------------------------------------------------------
FONT = "Inter"
MONO = "DejaVu Sans Mono"

TITLE_SIZE = 28
SIDE_MARGIN = 0.4   # min gap between text and the frame edge
SUBTITLE_SIZE = 20
LABEL_SIZE = 16
SMALL_SIZE = 14
MATH_SCALE = 0.8

# Vertical anchors for the header (title + subtitle).
TITLE_Y = 3.15
SUBTITLE_GAP = 0.32
