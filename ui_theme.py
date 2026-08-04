"""Clean modern light theme tokens and Tk widget helpers for LPHK."""

import tkinter as tk

# Surfaces
BG = "#F4F6F8"
SURFACE = "#FFFFFF"
BORDER = "#D8DEE6"
BORDER_SOFT = "#E6EBF1"

# Text
TEXT = "#1A2332"
TEXT_SECONDARY = "#5A6577"
TEXT_ON_ACCENT = "#FFFFFF"

# Accents
ACCENT = "#0F8A7E"
ACCENT_HOVER = "#0C7369"
ACCENT_SOFT = "#E6F5F3"
DANGER = "#C04545"
DANGER_HOVER = "#A33838"
SUCCESS = "#2F8F5B"
SUCCESS_SOFT = "#E8F5EE"
INACTIVE = "#8A93A3"
INACTIVE_SOFT = "#EEF1F5"

# Pad canvas
PAD_EMPTY = "#E8ECF1"
PAD_EMPTY_BORDER = "#C9D1DB"
PAD_CANVAS_BG = "#FAFBFC"
SELECT = ACCENT

# Spacing
PAD = 12
PAD_LG = 20
GAP = 8
BUTTON_PAD_X = 14
BUTTON_PAD_Y = 8

# Fonts (Windows-friendly)
FONT_UI = ("Bahnschrift", 11)
FONT_UI_BOLD = ("Bahnschrift", 11, "bold")
FONT_BRAND = ("Bahnschrift", 28, "bold")
FONT_SUBTITLE = ("Bahnschrift", 11)
FONT_HINT = ("Bahnschrift", 10)
FONT_PILL = ("Bahnschrift", 10, "bold")
FONT_MODE = ("Bahnschrift", 10, "bold")
FONT_EDITOR = ("Consolas", 11)
FONT_DIALOG_BODY = ("Bahnschrift", 11)
FONT_BUTTON = ("Bahnschrift", 11, "bold")
FONT_CHIP = ("Bahnschrift", 9, "bold")


def apply_window_bg(widget, color=BG):
    try:
        widget.configure(bg=color)
    except tk.TclError:
        pass


def _base_button(btn, bg, fg, active_bg, active_fg, font=FONT_BUTTON):
    btn.configure(
        bg=bg,
        fg=fg,
        activebackground=active_bg,
        activeforeground=active_fg,
        disabledforeground=INACTIVE,
        font=font,
        relief=tk.FLAT,
        borderwidth=0,
        highlightthickness=0,
        padx=BUTTON_PAD_X,
        pady=BUTTON_PAD_Y,
        cursor="hand2",
    )


def style_primary_button(btn):
    _base_button(btn, ACCENT, TEXT_ON_ACCENT, ACCENT_HOVER, TEXT_ON_ACCENT)


def style_danger_button(btn):
    _base_button(btn, DANGER, TEXT_ON_ACCENT, DANGER_HOVER, TEXT_ON_ACCENT)


def style_secondary_button(btn):
    _base_button(btn, SURFACE, TEXT, BORDER_SOFT, TEXT)
    btn.configure(
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=BORDER,
        relief=tk.SOLID,
        borderwidth=1,
        bd=1,
    )


def style_chip_button(btn):
    """Compact secondary button for example / hint chips."""
    _base_button(btn, SURFACE, TEXT_SECONDARY, ACCENT_SOFT, TEXT, FONT_CHIP)
    btn.configure(
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        relief=tk.SOLID,
        borderwidth=1,
        bd=1,
        padx=8,
        pady=4,
    )


def style_mode_button(btn, active=False):
    if active:
        _base_button(btn, ACCENT, TEXT_ON_ACCENT, ACCENT_HOVER, TEXT_ON_ACCENT, FONT_MODE)
        btn.configure(relief=tk.FLAT, borderwidth=0, bd=0, highlightthickness=0)
    else:
        _base_button(btn, SURFACE, TEXT_SECONDARY, BORDER_SOFT, TEXT, FONT_MODE)
        btn.configure(
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=BORDER,
            relief=tk.SOLID,
            borderwidth=1,
            bd=1,
        )


def style_status_pill(label, connected=False):
    if connected:
        label.configure(
            bg=SUCCESS_SOFT,
            fg=SUCCESS,
            font=FONT_PILL,
            padx=12,
            pady=6,
        )
    else:
        label.configure(
            bg=INACTIVE_SOFT,
            fg=TEXT_SECONDARY,
            font=FONT_PILL,
            padx=12,
            pady=6,
        )


def style_scrolled_text(text_widget):
    text_widget.configure(
        bg=SURFACE,
        fg=TEXT,
        insertbackground=TEXT,
        selectbackground=ACCENT_SOFT,
        selectforeground=TEXT,
        font=FONT_EDITOR,
        relief=tk.FLAT,
        borderwidth=1,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        padx=10,
        pady=10,
    )


def display_pad_color(rgb_hex):
    """Map near-black hardware colors to a soft empty-pad fill for the light UI."""
    if not rgb_hex or len(rgb_hex) < 7:
        return PAD_EMPTY
    try:
        r = int(rgb_hex[1:3], 16)
        g = int(rgb_hex[3:5], 16)
        b = int(rgb_hex[5:7], 16)
    except ValueError:
        return PAD_EMPTY
    if r < 4 and g < 4 and b < 4:
        return PAD_EMPTY
    return rgb_hex


def pad_outline_for(fill_hex):
    if fill_hex == PAD_EMPTY:
        return PAD_EMPTY_BORDER
    return ""
