"""Starter LPHKscript examples shown in the Edit Button window."""

# Each entry: short button label, one-line tip, script body (loaded into the editor).
EXAMPLES = [
    {
        "label": "Type text",
        "tip": "Types text, then presses Enter.",
        "script": """- Type text and press Enter
STRING Hello world!
TAP enter
""",
    },
    {
        "label": "Simple key",
        "tip": "Hold a key while the pad is pressed (@SIMPLE).",
        "script": """@SIMPLE space
- @SIMPLE maps the pad to one key while held.
- Only comments/blank lines are allowed with @SIMPLE.
""",
    },
    {
        "label": "Hotkey",
        "tip": "Keyboard shortcut (Ctrl+Shift+J).",
        "script": """- Modifier combo: press modifiers, tap key, release modifiers
PRESS ctrl
PRESS shift
TAP j
RELEASE shift
RELEASE ctrl
""",
    },
    {
        "label": "Hold key",
        "tip": "Hold a key until you release the pad (@ASYNC).",
        "script": """@ASYNC
- Runs in the background; tap the pad again to kill it.
PRESS y
WAIT_UNPRESSED
RELEASE y
""",
    },
    {
        "label": "Website",
        "tip": "Open a URL in your default browser.",
        "script": """- Open a website
WEB https://github.com/nimaid/LPHK
""",
    },
    {
        "label": "Play sound",
        "tip": "Play a file from user_sounds/ (wav/flac/ogg).",
        "script": """- Put a .wav / .flac / .ogg file in user_sounds/
- Then uncomment the next line (path is relative to that folder)
- SOUND my_sound.wav 80
- Optional: stop all sounds (fade out ms)
SOUND_STOP
""",
    },
    {
        "label": "Media",
        "tip": "Media keys: play/pause, mute, tracks, volume.",
        "script": """- Other media keys: mute, next_track, prev_track, vol_up, vol_down
TAP play_pause
""",
    },
    {
        "label": "Delay",
        "tip": "Wait between actions (seconds).",
        "script": """STRING Wait for it...
DELAY 1.5
STRING done!
TAP enter
""",
    },
    {
        "label": "Mouse",
        "tip": "Store position, move, click, then return.",
        "script": """@ASYNC
- Save cursor, move, click, restore
M_STORE
M_MOVE 100 50
TAP mouse_left
M_RECALL
""",
    },
    {
        "label": "Loop",
        "tip": "Repeat a label a fixed number of times.",
        "script": """- LABEL + REPEAT_LABEL for loops
LABEL tap_a
TAP a
DELAY 0.2
REPEAT_LABEL tap_a 5
""",
    },
    {
        "label": "Open file",
        "tip": "Open a file or folder with the OS.",
        "script": """- Use a full path, or something your OS can resolve
OPEN C:\\
""",
    },
    {
        "label": "Template",
        "tip": "Type a code snippet with Enter and Tab.",
        "script": """STRING for x in range():
TAP enter
TAP tab
""",
    },
]
