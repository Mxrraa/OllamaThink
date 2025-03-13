import tkinter as tk
from tkinter import ttk


def create_top_frame(main_frame, theme):
    """Create the top frame with model selection and settings"""
    top_frame = ttk.Frame(main_frame)
    top_frame.pack(fill="x", pady=(0, 10))

    # Model selection
    ttk.Label(top_frame, text="Model:", style="TLabel").pack(side=tk.LEFT, padx=(0, 5))

    model_var = tk.StringVar(value="deepseek-r1:14b")
    model_combo = ttk.Combobox(top_frame, textvariable=model_var, state="readonly", width=15)
    model_combo["values"] = (
        "deepseek-r1:14b",
        "llama3:8b",
        "gemma:7b",
        "mistral:7b",
        "codellama:7b"
    )
    model_combo.pack(side=tk.LEFT, padx=(0, 15))

    # Thinking mode option
    show_thinking_var = tk.BooleanVar(value=True)
    ttk.Checkbutton(
        top_frame,
        text="Düşünme sürecini göster",
        variable=show_thinking_var,
        style="TCheckbutton"
    ).pack(side=tk.LEFT)

    # Status indicator
    status_frame = ttk.Frame(top_frame)
    status_frame.pack(side=tk.RIGHT)

    status_dot = tk.Canvas(
        status_frame, width=10, height=10, bg=theme.bg_color, highlightthickness=0
    )
    status_dot.pack(side=tk.LEFT, padx=(0, 5))
    status_dot.create_oval(2, 2, 8, 8, fill="#4CAF50", outline="")

    status_label = ttk.Label(status_frame, text="Hazır", style="TLabel")
    status_label.pack(side=tk.RIGHT)

    return top_frame, model_var, show_thinking_var, status_dot, status_label


def create_toolbar(main_frame, theme, clear_func, save_func, theme_func):
    """Create the bottom toolbar with extra buttons"""
    toolbar_frame = ttk.Frame(main_frame)
    toolbar_frame.pack(fill="x", pady=(10, 0))

    # Clear button
    clear_button = tk.Button(
        toolbar_frame,
        text="Temizle",
        bg=theme.user_msg_bg,
        fg=theme.user_msg_fg,
        relief="flat",
        font=("Segoe UI", 9),
        padx=10,
        command=clear_func,
    )
    clear_button.pack(side=tk.LEFT, padx=(0, 5))

    # Save conversation button
    save_button = tk.Button(
        toolbar_frame,
        text="Kaydet",
        bg=theme.user_msg_bg,
        fg=theme.user_msg_fg,
        relief="flat",
        font=("Segoe UI", 9),
        padx=10,
        command=save_func,
    )
    save_button.pack(side=tk.LEFT, padx=(0, 5))

    # Change theme button
    theme_button = tk.Button(
        toolbar_frame,
        text="Tema",
        bg=theme.user_msg_bg,
        fg=theme.user_msg_fg,
        relief="flat",
        font=("Segoe UI", 9),
        padx=10,
        command=theme_func,
    )
    theme_button.pack(side=tk.LEFT)

    # Hover effects for toolbar buttons
    buttons = [clear_button, save_button, theme_button]
    for btn in buttons:
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#545474"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=theme.user_msg_bg))

    return toolbar_frame, buttons