"""CAMPUS_SURVIVE Module 4: Tkinter GUI.

Public screen functions are kept exactly as assigned. The GUI owns presentation
only; question selection, scoring, day progression and persistence belong to
the game engine / other modules.

Start independently with:
    python gui_demo.py

Tkinter is included with most standard Python installations. No external
packages or image/music assets are required.
"""

import tkinter as tk
from tkinter import ttk, messagebox

# Campus palette: forest green, midnight blue, warm paper, and school-bus gold.
BG = "#EEF2EA"
PANEL = "#FFFFFF"
INK = "#192A3A"
MUTED = "#667687"
TEAL = "#287A57"
TEAL_DARK = "#1E5D43"
NAVY = "#172D40"
CORAL = "#D76B4E"
YELLOW = "#E8B84D"
GREEN = "#42805A"
RED = "#B84C49"
BORDER = "#D9E1D8"
FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 25, "bold")
FONT_SUBTITLE = ("Segoe UI", 14, "bold")

_root = None
_content = None
_current_player = None
_stat_labels = {}
_stat_bars = {}
_feedback_label = None
_last_screen = None


def _ensure_root():
    global _root
    if _root is None or not _root.winfo_exists():
        _root = tk.Tk()
        _root.title("Campus Survival")
        _root.geometry("1050x760")
        _root.minsize(760, 620)
        _root.configure(bg=BG)
        _root.option_add("*Font", FONT)
        _root.protocol("WM_DELETE_WINDOW", _root.destroy)
        style = ttk.Style(_root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Campus.Horizontal.TProgressbar",
            troughcolor="#DDE7DD",
            background=TEAL,
            bordercolor="#DDE7DD",
            lightcolor=TEAL,
            darkcolor=TEAL,
            thickness=12,
        )
        style.configure(
            "Campus.Treeview",
            background="#F8FAF6",
            fieldbackground="#F8FAF6",
            foreground=INK,
            rowheight=32,
            borderwidth=0,
            font=FONT,
        )
        style.configure(
            "Campus.Treeview.Heading",
            background=NAVY,
            foreground="#FFFFFF",
            relief="flat",
            font=FONT_BOLD,
        )
        style.map(
            "Campus.Treeview",
            background=[("selected", "#DDECE1")],
            foreground=[("selected", INK)],
        )
    return _root


def _clear_screen():
    global _content, _stat_labels, _stat_bars, _feedback_label
    root = _ensure_root()
    for child in root.winfo_children():
        child.destroy()
    _content = tk.Frame(root, bg=BG)
    _content.pack(fill="both", expand=True)
    _stat_labels = {}
    _stat_bars = {}
    _feedback_label = None
    return _content


def _center_card(parent, width=760):
    outer = tk.Frame(parent, bg=BG)
    outer.pack(fill="both", expand=True, padx=24, pady=22)
    card = tk.Frame(outer, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
    card.pack(fill="both", expand=True, padx=8, pady=8)
    return card


def _campus_illustration(parent, width=172, height=82):
    canvas = tk.Canvas(
        parent, width=width, height=height, bg=NAVY,
        highlightthickness=0, bd=0,
    )
    canvas.pack(side="right", padx=(8, 24), pady=8)
    canvas.create_oval(width - 49, 5, width - 25, 29, fill=YELLOW, outline="")
    canvas.create_rectangle(0, height - 19, width, height, fill="#234D43", outline="")
    canvas.create_polygon(
        0, height - 18, width * .46, height - 18, width * .69, height,
        width * .31, height, fill="#C5A875", outline="",
    )
    canvas.create_rectangle(42, 30, 126, height - 18, fill="#E9E5D8", outline="")
    canvas.create_polygon(35, 31, 84, 9, 133, 31, fill=CORAL, outline="")
    canvas.create_rectangle(76, 43, 92, height - 18, fill=NAVY, outline="")
    for x in (51, 65, 102, 116):
        canvas.create_rectangle(x, 40, x + 7, 50, fill="#8EB8A0", outline="")
    for x, y in ((23, 45), (143, 48)):
        canvas.create_rectangle(x + 5, y + 14, x + 9, height - 17, fill="#806746", outline="")
        canvas.create_oval(x, y, x + 20, y + 23, fill="#4B8A61", outline="")
    canvas.create_text(
        84, height - 5, text="CAMPUS GROUNDS",
        fill="#F7F1DC", font=("Segoe UI", 7, "bold"),
    )
    return canvas


def _header(parent, eyebrow="YOUR CAMPUS, YOUR STORY"):
    frame = tk.Frame(parent, bg=NAVY)
    frame.pack(fill="x", padx=18, pady=(18, 8))
    _campus_illustration(frame)
    copy = tk.Frame(frame, bg=NAVY)
    copy.pack(side="left", fill="both", expand=True, padx=24, pady=14)
    tk.Label(copy, text=eyebrow, bg=NAVY, fg="#E9C66E",
             font=("Segoe UI", 9, "bold")).pack(anchor="w")
    tk.Label(copy, text="Campus Survival", bg=NAVY, fg="#FFFFFF",
             font=FONT_TITLE).pack(anchor="w", pady=(3, 0))
    tk.Label(
        copy, text="Make your mark. Find your balance. Survive the semester.",
        bg=NAVY, fg="#D3DDD9", font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(2, 0))
    return frame


def _button(parent, text, command, kind="primary", width=None):
    palette = {
        "primary": (TEAL, "#FFFFFF", TEAL_DARK),
        "secondary": ("#E8F0E7", TEAL_DARK, "#D8E6D8"),
        "coral": (CORAL, "#FFFFFF", "#BD583F"),
        "plain": (PANEL, INK, "#F0F3EE"),
        "danger": (RED, "#FFFFFF", "#963E3C"),
    }
    bg, fg, active = palette.get(kind, palette["primary"])
    button = tk.Button(
        parent, text=text, command=command, bg=bg, fg=fg,
        activebackground=active, activeforeground=fg,
        relief="flat", bd=0, cursor="hand2", padx=16, pady=11,
        font=FONT_BOLD, width=width,
        highlightthickness=1, highlightbackground=bg,
    )
    button.bind("<Enter>", lambda _event: button.configure(bg=active))
    button.bind("<Leave>", lambda _event: button.configure(bg=bg))
    return button


def _section_title(parent, title, subtitle=None):
    tk.Label(parent, text=title, bg=PANEL, fg=INK, font=FONT_SUBTITLE).pack(anchor="w", padx=26, pady=(12, 2))
    if subtitle:
        tk.Label(parent, text=subtitle, bg=PANEL, fg=MUTED, font=FONT).pack(anchor="w", padx=26, pady=(0, 8))


def _safe_callback(callback, *args):
    if callable(callback):
        return callback(*args)
    return None


def show_login(on_login):
    """Show Student ID/name fields and Login/Create Profile actions.

    Calls on_login(student_id, name) on valid input. Registration/login
    persistence and actual identity validation remain the caller's job.
    """
    root = _ensure_root()
    card = _center_card(_clear_screen())
    _header(card, "WELCOME TO CAMPUS SURVIVAL")

    body = tk.Frame(card, bg=PANEL)
    body.pack(fill="both", expand=True, padx=28, pady=(12, 24))
    body.grid_columnconfigure(0, weight=1, uniform="login")
    body.grid_columnconfigure(1, weight=1, uniform="login")

    welcome = tk.Frame(body, bg="#EAF1E8", highlightbackground=BORDER, highlightthickness=1)
    welcome.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
    tk.Label(welcome, text="YOUR NEXT CHAPTER", bg="#EAF1E8", fg=TEAL,
             font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=22, pady=(24, 8))
    tk.Label(welcome, text="College life is a balancing act.",
             bg="#EAF1E8", fg=INK, font=("Segoe UI", 20, "bold"),
             wraplength=290, justify="left").pack(anchor="w", padx=22)
    tk.Label(
        welcome,
        text="Make thoughtful calls through deadlines, exams, friendships, and the opportunities that shape your future.",
        bg="#EAF1E8", fg=MUTED, font=("Segoe UI", 11),
        wraplength=290, justify="left",
    ).pack(anchor="w", padx=22, pady=(10, 20))
    for symbol, label in (
        ("01", "Stay on top of your studies"),
        ("02", "Look after your well-being"),
        ("03", "Make your opportunities count"),
    ):
        row = tk.Frame(welcome, bg="#EAF1E8")
        row.pack(fill="x", padx=22, pady=5)
        tk.Label(row, text=symbol, bg=TEAL, fg="#FFFFFF",
                 font=("Segoe UI", 8, "bold"), padx=7, pady=4).pack(side="left")
        tk.Label(row, text=label, bg="#EAF1E8", fg=INK,
                 font=FONT_BOLD).pack(side="left", padx=10)
    tk.Label(welcome, text="15 DAYS  ·  YOUR CHOICES  ·  YOUR SEMESTER",
             bg="#EAF1E8", fg=TEAL_DARK, font=("Segoe UI", 8, "bold")
             ).pack(anchor="w", padx=22, pady=(22, 18))

    form = tk.Frame(body, bg=PANEL)
    form.grid(row=0, column=1, sticky="nsew", padx=(12, 0), pady=8)
    tk.Label(form, text="Welcome to campus", bg=PANEL, fg=INK,
             font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(4, 2))
    tk.Label(form, text="Enter your student details to continue.",
             bg=PANEL, fg=MUTED).pack(anchor="w", pady=(0, 22))
    tk.Label(form, text="STUDENT ID", bg=PANEL, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w")
    id_entry = tk.Entry(form, font=("Segoe UI", 12), relief="flat", bd=0,
                        bg="#F6F8F4", fg=INK, insertbackground=TEAL,
                        highlightthickness=1, highlightbackground=BORDER,
                        highlightcolor=TEAL)
    id_entry.pack(fill="x", ipady=10, pady=(6, 16))
    tk.Label(form, text="YOUR NAME", bg=PANEL, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w")
    name_entry = tk.Entry(form, font=("Segoe UI", 12), relief="flat", bd=0,
                          bg="#F6F8F4", fg=INK, insertbackground=TEAL,
                          highlightthickness=1, highlightbackground=BORDER,
                          highlightcolor=TEAL)
    name_entry.pack(fill="x", ipady=10, pady=(6, 8))

    error = tk.Label(form, text="", bg=PANEL, fg=RED, anchor="w", justify="left")
    error.pack(fill="x", pady=(2, 8))

    def submit():
        student_id = id_entry.get().strip()
        name = name_entry.get().strip()
        if not student_id or not name:
            error.config(text="Please enter both Student ID and name.")
            return
        if len(student_id) > 32 or len(name) > 80:
            error.config(text="Student ID must be at most 32 characters and name at most 80.")
            return
        if any(ord(ch) < 32 for ch in student_id + name):
            error.config(text="Please remove unsupported control characters.")
            return
        error.config(text="")
        _safe_callback(on_login, student_id, name)

    buttons = tk.Frame(form, bg=PANEL)
    buttons.pack(fill="x", pady=(12, 0))
    _button(buttons, "Login / Continue", submit, "primary").pack(side="left", padx=(0, 10))
    _button(buttons, "Create Profile", submit, "secondary").pack(side="left")
    tk.Label(form, text="Your progress is saved to your student profile.",
             bg=PANEL, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(18, 0))
    id_entry.bind("<Return>", lambda _event: submit())
    name_entry.bind("<Return>", lambda _event: submit())
    id_entry.focus_set()
    return root


def show_home(player, on_action):
    """Show home menu and dispatch the exact requested action strings."""
    global _current_player
    _current_player = player
    card = _center_card(_clear_screen())
    _header(card, "SEMESTER HUB")

    name = player.get("name", "Student") if isinstance(player, dict) else "Student"
    day = player.get("current_day", 1) if isinstance(player, dict) else 1
    status = tk.Frame(card, bg="#F6F8F4", highlightbackground=BORDER, highlightthickness=1)
    status.pack(fill="x", padx=28, pady=(20, 18))
    status_copy = tk.Frame(status, bg="#F6F8F4")
    status_copy.pack(side="left", fill="both", expand=True, padx=18, pady=16)
    tk.Label(status_copy, text=f"Welcome back, {name}!", bg="#F6F8F4", fg=INK,
             font=("Segoe UI", 19, "bold")).pack(anchor="w")
    tk.Label(status_copy, text=f"Day {day} of 15  ·  Your semester, your story.",
             bg="#F6F8F4", fg=MUTED).pack(anchor="w", pady=(3, 10))
    progress = ttk.Progressbar(
        status_copy, maximum=15, value=max(0, min(15, day - 1)),
        style="Campus.Horizontal.TProgressbar",
    )
    progress.pack(fill="x")
    tk.Label(status, text=f"{max(0, min(15, day - 1))}/15\nDAYS COMPLETE",
             bg="#F6F8F4", fg=TEAL_DARK,
             font=("Segoe UI", 9, "bold"), justify="center"
             ).pack(side="right", padx=20)

    menu = tk.Frame(card, bg=PANEL)
    menu.pack(fill="both", expand=True, padx=28, pady=(0, 12))
    menu.grid_columnconfigure(0, weight=1, uniform="menu")
    menu.grid_columnconfigure(1, weight=1, uniform="menu")
    options = [
        ("CONTINUE YOUR RUN", "▶  Continue Game", "continue", "primary"),
        ("START FRESH", "✦  New Game", "new_game", "coral"),
        ("MAKE IT YOURS", "⚙  Settings", "settings", "secondary"),
        ("STEP AWAY", "↗  Quit", "quit", "plain"),
    ]
    for index, (eyebrow, label, action, kind) in enumerate(options):
        tile = tk.Frame(menu, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        tile.grid(row=index // 2, column=index % 2, sticky="nsew", padx=6, pady=6)
        tk.Label(tile, text=eyebrow, bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=12, pady=(10, 4))
        _button(tile, label, lambda a=action: _safe_callback(on_action, a), kind
                ).pack(fill="x", padx=10, pady=(0, 10))

    tk.Label(card, text="STUDY SMART  ·  TAKE CARE  ·  MAKE YOUR NEXT MOVE",
             bg=PANEL, fg=TEAL, font=("Segoe UI", 9, "bold")
             ).pack(anchor="w", padx=34, pady=(2, 20))
    return _ensure_root()


def _stat_color(stat, value):
    if stat == "stress":
        return CORAL if value >= 70 else YELLOW if value >= 40 else GREEN
    if stat == "money":
        return TEAL
    return RED if value <= 25 else YELLOW if value <= 50 else GREEN if value >= 75 else TEAL


def _add_stats_panel(parent, player):
    panel = tk.Frame(parent, bg="#F6F8F4", highlightbackground=BORDER, highlightthickness=1)
    panel.pack(fill="x", padx=24, pady=(8, 12))
    tk.Label(panel, text="YOUR SEMESTER STATUS", bg="#F6F8F4", fg=INK,
             font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(10, 6))

    stat_info = [
        ("happiness", "😊 Happiness", 100),
        ("attendance", "📅 Attendance", 100),
        ("grades", "📚 Grades", 100),
        ("energy", "⚡ Energy", 100),
        ("stress", "🧠 Stress", 100),
        ("money", "💰 Money", None),
    ]
    for index, (key, label, maximum) in enumerate(stat_info):
        row, col = 1 + index // 2, index % 2
        cell = tk.Frame(panel, bg=PANEL, highlightbackground="#E4EAE2", highlightthickness=1)
        cell.grid(row=row, column=col, sticky="ew", padx=9, pady=4)
        panel.grid_columnconfigure(col, weight=1, uniform="stat")
        value = player.get(key, 0)
        shown = f"₹{value:,}" if key == "money" and isinstance(value, (int, float)) else f"{value}/100"
        top = tk.Frame(cell, bg=PANEL)
        tk.Label(top, text=label, bg=PANEL, fg=INK, font=("Segoe UI", 9, "bold")).pack(side="left")
        value_label = tk.Label(top, text=shown, bg=PANEL, fg=INK, font=("Segoe UI", 9, "bold"))
        value_label.pack(side="right")
        _stat_labels[key] = value_label
        top.pack(fill="x", padx=9, pady=(7, 0))
        if maximum:
            bar = ttk.Progressbar(cell, maximum=100, value=max(0, min(100, value)),
                                  style="Campus.Horizontal.TProgressbar")
            bar.pack(fill="x", padx=9, pady=(5, 8))
            _stat_bars[key] = bar
        else:
            tk.Label(cell, text="Available for campus expenses", bg=PANEL, fg=MUTED,
                     font=("Segoe UI", 8)).pack(anchor="w", padx=9, pady=(4, 8))
    return panel


def show_game_screen(player, question, on_choice):
    """Display one question and stats; choices call on_choice(index).

    If the callback returns a string, it is displayed as feedback. The engine
    can also call show_game_screen again after applying effects to refresh all
    stats and load the next question.
    """
    global _current_player, _feedback_label
    _current_player = player
    card = _center_card(_clear_screen())

    day = player.get("current_day", question.get("day", 1) if isinstance(question, dict) else 1)
    header = tk.Frame(card, bg=PANEL)
    header.pack(fill="x", padx=24, pady=(14, 4))
    day_badge = tk.Frame(header, bg=TEAL_DARK)
    day_badge.pack(side="left")
    tk.Label(day_badge, text="CAMPUS CHALLENGE", bg=TEAL_DARK, fg="#DDEBDC",
             font=("Segoe UI", 8, "bold"), padx=10).pack(anchor="w", pady=(6, 0))
    tk.Label(day_badge, text=f"DAY {day:02d}  /  15", bg=TEAL_DARK, fg="#FFFFFF",
             font=("Segoe UI", 11, "bold"), padx=10).pack(anchor="w", pady=(1, 6))
    _button(header, "Ⅱ  Pause", lambda: _safe_callback(
        player.get("_on_pause", lambda: show_pause_menu(
            player.get("_on_resume", lambda: show_game_screen(player, question, on_choice)),
            player.get("_on_main_menu", lambda: show_home(player, lambda action: None)),
            player.get("_on_restart", lambda: _confirm_restart(lambda: show_game_screen(player, question, on_choice))),
            player.get("_on_quit", lambda: _confirm_quit())
        ))
    ), "plain").pack(side="right")
    ttk.Progressbar(
        card, maximum=15, value=max(0, min(15, day - 1)),
        style="Campus.Horizontal.TProgressbar",
    ).pack(fill="x", padx=24, pady=(4, 5))

    title = question.get("title", "Campus Decision") if isinstance(question, dict) else "Campus Decision"
    scenario = question.get("scenario", "") if isinstance(question, dict) else ""
    prompt = tk.Frame(card, bg="#F6F8F4", highlightbackground=BORDER, highlightthickness=1)
    prompt.pack(fill="x", padx=24, pady=(5, 7))
    tk.Frame(prompt, bg=YELLOW, width=5).pack(side="left", fill="y")
    prompt_copy = tk.Frame(prompt, bg="#F6F8F4")
    prompt_copy.pack(fill="x", expand=True, padx=16, pady=10)
    tk.Label(prompt_copy, text=title, bg="#F6F8F4", fg=INK, font=("Segoe UI", 18, "bold"),
             wraplength=850, justify="left").pack(anchor="w")
    tk.Label(prompt_copy, text=scenario, bg="#F6F8F4", fg=MUTED, font=("Segoe UI", 10),
             wraplength=850, justify="left").pack(anchor="w", pady=(4, 0))

    _add_stats_panel(card, player)
    _section_title(card, "MAKE YOUR MOVE", "Every choice has a trade-off. Choose the path that fits your priorities.")
    choices_frame = tk.Frame(card, bg=PANEL)
    choices_frame.pack(fill="x", padx=26, pady=(0, 8))
    feedback_label = tk.Label(card, text="Your decision debrief will appear here.",
                              bg="#F7F1DE", fg=INK, anchor="w", justify="left",
                              wraplength=900, padx=14, pady=10,
                              highlightbackground="#E9D9A8", highlightthickness=1)
    feedback_label.pack(fill="x", padx=26, pady=(4, 12))
    _feedback_label = feedback_label

    choices = question.get("choices", []) if isinstance(question, dict) else []
    for index, choice in enumerate(choices):
        choice_text = choice.get("text", f"Choice {index + 1}")
        def choose(i=index):
            try:
                result = _safe_callback(on_choice, i)
                if isinstance(result, str) and _feedback_label is not None and _feedback_label.winfo_exists():
                    _feedback_label.config(text=result)
                elif _feedback_label is not None and _feedback_label.winfo_exists():
                    _feedback_label.config(text="Your choice has been recorded.")
            except Exception as exc:
                show_message(f"Could not submit choice: {exc}", "error")
        _button(choices_frame, f"{index + 1}.  {choice_text}", choose,
                "secondary" if index % 2 else "primary").pack(fill="x", pady=4)

    footer = tk.Frame(card, bg=PANEL)
    footer.pack(fill="x", padx=26, pady=(0, 18))
    _button(footer, "Main Menu", lambda: _safe_callback(player.get("_on_main_menu", lambda: show_home(player, lambda action: None))), "plain").pack(side="left")
    return _ensure_root()


def update_stats(player):
    """Refresh currently visible stat labels and progress bars."""
    global _current_player
    _current_player = player
    for key, label in list(_stat_labels.items()):
        if not label.winfo_exists():
            continue
        value = player.get(key, 0)
        if key == "money":
            label.config(text=f"₹{value:,}" if isinstance(value, (int, float)) else str(value))
        else:
            label.config(text=f"{value}/100")
    for key, bar in list(_stat_bars.items()):
        if bar.winfo_exists():
            value = player.get(key, 0)
            bar.configure(value=max(0, min(100, value)) if isinstance(value, (int, float)) else 0)


def show_settings(player, on_resume, on_main_menu, on_restart, on_quit):
    """Show settings; toggles and slider update player['settings'] immediately."""
    settings = player.setdefault("settings", {})
    settings.setdefault("music", True)
    settings.setdefault("sound_effects", True)
    settings.setdefault("volume", 50)
    card = _center_card(_clear_screen())
    _header(card, "PREFERENCES")

    body = tk.Frame(card, bg=PANEL)
    body.pack(fill="both", expand=True, padx=28, pady=(14, 22))
    _section_title(body, "Settings", "Make the campus sound and feel right for you.")

    music_var = tk.BooleanVar(value=bool(settings["music"]))
    sound_var = tk.BooleanVar(value=bool(settings["sound_effects"]))
    tk.Checkbutton(body, text="🎵  Background Music", variable=music_var,
                   command=lambda: settings.__setitem__("music", music_var.get()),
                   bg=PANEL, fg=INK, activebackground=PANEL, selectcolor="#E6EFE5",
                   highlightthickness=0,
                   font=FONT_BOLD).pack(anchor="w", pady=8)
    tk.Checkbutton(body, text="🔔  Sound Effects", variable=sound_var,
                   command=lambda: settings.__setitem__("sound_effects", sound_var.get()),
                   bg=PANEL, fg=INK, activebackground=PANEL, selectcolor="#E6EFE5",
                   highlightthickness=0,
                   font=FONT_BOLD).pack(anchor="w", pady=8)

    volume_row = tk.Frame(body, bg=PANEL)
    volume_row.pack(fill="x", pady=(12, 20))
    volume_value = tk.IntVar(value=max(0, min(100, int(settings.get("volume", 50)))))
    volume_title = tk.Frame(volume_row, bg=PANEL)
    volume_title.pack(fill="x")
    tk.Label(volume_title, text="🔊  Volume", bg=PANEL, fg=INK, font=FONT_BOLD).pack(side="left")
    volume_label = tk.Label(volume_title, text=f"{volume_value.get()}%", bg=PANEL, fg=TEAL, font=FONT_BOLD)
    volume_label.pack(side="right")

    def change_volume(value):
        volume = int(float(value))
        settings["volume"] = volume
        volume_label.config(text=f"{volume}%")

    volume_scale = ttk.Scale(volume_row, from_=0, to=100, orient="horizontal",
                             command=change_volume)
    volume_scale.set(volume_value.get())
    volume_scale.pack(fill="x", pady=(8, 0))
    # Keep player settings authoritative without resetting the saved volume.

    _section_title(body, "Game controls")
    controls = tk.Frame(body, bg=PANEL)
    controls.pack(fill="x", pady=(8, 0))
    _button(controls, "Resume Game", lambda: _safe_callback(on_resume), "primary").pack(fill="x", pady=4)
    _button(controls, "Main Menu", lambda: _safe_callback(on_main_menu), "secondary").pack(fill="x", pady=4)
    _button(controls, "Restart Game", lambda: _confirm_restart(on_restart), "coral").pack(fill="x", pady=4)
    _button(controls, "Quit Game", lambda: _confirm_quit(on_quit), "danger").pack(fill="x", pady=4)
    return _ensure_root()


def show_pause_menu(on_resume, on_main_menu, on_restart, on_quit):
    """Show pause controls. Restart and quit require confirmation."""
    card = _center_card(_clear_screen())
    _header(card, "TAKE FIVE")

    tk.Label(card, text="Game Paused", bg=PANEL, fg=INK,
             font=("Segoe UI", 21, "bold")).pack(anchor="w", padx=28, pady=(30, 4))
    tk.Label(card, text="Take a breath. Your progress is still here.",
             bg=PANEL, fg=MUTED).pack(anchor="w", padx=28, pady=(0, 18))
    controls = tk.Frame(card, bg=PANEL)
    controls.pack(fill="x", padx=28, pady=(0, 28))
    _button(controls, "▶  Resume", lambda: _safe_callback(on_resume), "primary").pack(fill="x", pady=5)
    _button(controls, "Main Menu", lambda: _safe_callback(on_main_menu), "secondary").pack(fill="x", pady=5)
    _button(controls, "Restart Game", lambda: _confirm_restart(on_restart), "coral").pack(fill="x", pady=5)
    _button(controls, "Quit Game", lambda: _confirm_quit(on_quit), "danger").pack(fill="x", pady=5)
    return _ensure_root()


def show_results(player, report, leaderboard):
    """Display final report and leaderboard, with Play Again/Main Menu actions.

    Optional navigation callbacks may be attached by the caller as
    player['_on_play_again'] and player['_on_main_menu'] so this public
    signature remains exactly as assigned.
    """
    card = _center_card(_clear_screen())
    _header(card, "SEMESTER COMPLETE")

    if not isinstance(report, dict):
        report = {}
    score = report.get("final_score", player.get("score", 0))
    rating = report.get("performance_rating", "Not rated")
    result_hero = tk.Frame(card, bg=TEAL_DARK)
    result_hero.pack(fill="x", padx=28, pady=(10, 12))
    score_copy = tk.Frame(result_hero, bg=TEAL_DARK)
    score_copy.pack(side="left", padx=18, pady=12)
    tk.Label(score_copy, text="SEMESTER SCORE", bg=TEAL_DARK, fg="#DDEBDC",
             font=("Segoe UI", 8, "bold")).pack(anchor="w")
    tk.Label(score_copy, text=f"{score}/100", bg=TEAL_DARK, fg="#FFFFFF",
             font=("Segoe UI", 27, "bold")).pack(anchor="w")
    tk.Label(result_hero, text=rating.upper(), bg="#E9C66E", fg=NAVY,
             font=("Segoe UI", 10, "bold"), padx=12, pady=8
             ).pack(side="right", padx=18)
    summary = report.get("summary", "Your semester journey is complete.")
    tk.Label(card, text=summary, bg=PANEL, fg=MUTED, wraplength=900,
             justify="left").pack(anchor="w", padx=28, pady=(0, 12))

    stats = report.get("stats", {})
    stats_text = "   •   ".join(
        f"{label}: {stats.get(key, player.get(key, 0))}"
        for key, label in [
            ("grades", "Grades"), ("attendance", "Attendance"),
            ("happiness", "Happiness"), ("energy", "Energy"),
            ("stress", "Stress"), ("money", "Money (₹)")
        ]
    )
    tk.Label(card, text=stats_text, bg="#F6F8F4", fg=INK, wraplength=900,
             justify="left", padx=12, pady=10,
             highlightbackground=BORDER, highlightthickness=1
             ).pack(fill="x", padx=28, pady=(0, 10))

    badges = report.get("achievements", player.get("achievements", []))
    _section_title(card, "Achievements & badges")
    badge_text = "   •   ".join(str(badge) for badge in badges) if badges else "No badges earned yet. Keep building consistent habits next semester."
    tk.Label(card, text=badge_text, bg=PANEL, fg=TEAL_DARK, wraplength=900,
             justify="left").pack(anchor="w", padx=28, pady=(0, 10))

    _section_title(card, "Leaderboard", "Ties follow the rank values supplied by achievements.py.")
    board_frame = tk.Frame(card, bg=PANEL)
    board_frame.pack(fill="both", expand=True, padx=28, pady=(0, 10))
    columns = ("rank", "student_id", "name", "score")
    tree = ttk.Treeview(board_frame, columns=columns, show="headings", height=5,
                        style="Campus.Treeview")
    for column, heading, width in [
        ("rank", "Rank", 65), ("student_id", "Student ID", 150),
        ("name", "Student", 250), ("score", "Score", 90)
    ]:
        tree.heading(column, text=heading)
        tree.column(column, width=width, anchor="center" if column != "name" else "w")
    for index, entry in enumerate(leaderboard or []):
        tree.insert("", "end", values=(
            entry.get("rank", ""), entry.get("student_id", ""),
            entry.get("name", ""), entry.get("score", "")
        ), tags=("even" if index % 2 == 0 else "odd",))
    tree.tag_configure("even", background="#F8FAF6")
    tree.tag_configure("odd", background="#EDF2EB")
    tree.pack(fill="both", expand=True)

    buttons = tk.Frame(card, bg=PANEL)
    buttons.pack(fill="x", padx=28, pady=(4, 22))
    _button(buttons, "Play Again", lambda: _safe_callback(player.get("_on_play_again")), "primary").pack(side="left", padx=(0, 10))
    _button(buttons, "Main Menu", lambda: _safe_callback(player.get("_on_main_menu")), "secondary").pack(side="left")
    return _ensure_root()


def show_message(message, message_type):
    """Display success/error/warning/confirmation message in a native dialog."""
    root = _ensure_root()
    kind = str(message_type).lower()
    if kind == "success":
        messagebox.showinfo("Success", str(message), parent=root)
    elif kind == "error":
        messagebox.showerror("Error", str(message), parent=root)
    elif kind == "warning":
        messagebox.showwarning("Warning", str(message), parent=root)
    elif kind == "confirmation":
        return messagebox.askyesno("Please confirm", str(message), parent=root)
    else:
        messagebox.showinfo("Campus Survival", str(message), parent=root)
    return None


def _confirm_restart(callback):
    root = _ensure_root()
    if messagebox.askyesno(
        "Restart game?",
        "Restarting may reset the current run. Continue?",
        parent=root,
    ):
        _safe_callback(callback)


def _confirm_quit(callback=None):
    root = _ensure_root()
    if messagebox.askyesno("Quit Campus Survival?", "Are you sure you want to quit?",
                           parent=root):
        if callable(callback):
            _safe_callback(callback)
        else:
            root.destroy()


def run():
    """Start the Tkinter event loop after a screen function has been called."""
    root = _ensure_root()
    root.mainloop()
