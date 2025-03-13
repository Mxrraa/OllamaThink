import tkinter as tk
from tkinter import ttk
import re
from datetime import datetime


class MessagesManager:
    def __init__(self, messages_frame, chat_canvas, theme, model_var):
        self.messages_frame = messages_frame
        self.chat_canvas = chat_canvas
        self.theme = theme
        self.model_var = model_var

        # Current active response widgets
        self.current_ai_message_frame = None
        self.current_thinking_frame = None
        self.is_thinking_active = False

    def add_system_message(self, message):
        """Add a gray system message"""
        frame = ttk.Frame(self.messages_frame, style="TFrame")
        frame.pack(fill="x", padx=10, pady=5)

        msg_label = tk.Label(
            frame,
            text=message,
            wraplength=800,
            justify="center",
            bg=self.theme.ai_msg_bg,
            fg=self.theme.think_fg,
            padx=10,
            pady=5,
            font=("Segoe UI", 9, "italic"),
        )
        msg_label.pack(fill="x")

        self.scroll_to_bottom()

    def add_user_message(self, message):
        """Add a blue user message"""
        frame = ttk.Frame(self.messages_frame, style="TFrame")
        frame.pack(fill="x", padx=10, pady=5)

        # Right aligned
        msg_frame = ttk.Frame(frame, style="TFrame")
        msg_frame.pack(side=tk.RIGHT)

        timestamp = datetime.now().strftime("%H:%M")
        time_label = tk.Label(
            msg_frame,
            text=timestamp,
            bg=self.theme.bg_color,
            fg=self.theme.think_fg,
            font=("Segoe UI", 8),
        )
        time_label.pack(anchor="e", padx=(0, 5), pady=(0, 2))

        msg_label = tk.Label(
            msg_frame,
            text=message,
            wraplength=600,
            justify="left",
            bg=self.theme.user_msg_bg,
            fg=self.theme.user_msg_fg,
            padx=15,
            pady=10,
            font=("Segoe UI", 10),
        )
        msg_label.pack(anchor="e")

        self.scroll_to_bottom()

    def add_new_ai_message_frame(self):
        """Create a new AI message frame"""
        frame = ttk.Frame(self.messages_frame, style="TFrame")
        frame.pack(fill="x", padx=10, pady=5)

        # Left aligned
        msg_frame = ttk.Frame(frame, style="TFrame")
        msg_frame.pack(side=tk.LEFT)

        # Model and time info
        header_frame = ttk.Frame(msg_frame, style="TFrame")
        header_frame.pack(anchor="w", fill="x", pady=(0, 2))

        model_label = tk.Label(
            header_frame,
            text=self.model_var.get(),
            bg=self.theme.bg_color,
            fg=self.theme.accent_color,
            font=("Segoe UI", 8, "bold"),
        )
        model_label.pack(side=tk.LEFT, padx=(5, 10))

        timestamp = datetime.now().strftime("%H:%M")
        time_label = tk.Label(
            header_frame,
            text=timestamp,
            bg=self.theme.bg_color,
            fg=self.theme.think_fg,
            font=("Segoe UI", 8),
        )
        time_label.pack(side=tk.LEFT)

        return frame, msg_frame

    def add_thinking_message(self, message):
        """Add or update thinking message"""
        # Indicate that Deepseek is thinking
        message = "Deepseek düşünüyor...\n\n" + message

        if self.current_thinking_frame:
            # Update existing thinking frame
            for widget in self.current_thinking_frame.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget("font")[2] == "italic":
                    widget.config(text=message)
                    break
        else:
            # Create new thinking frame
            frame, msg_frame = self.add_new_ai_message_frame()

            # Custom style for thinking mode
            think_label = tk.Label(
                msg_frame,
                text=message,
                wraplength=600,
                justify="left",
                bg=self.theme.think_bg,
                fg=self.theme.think_fg,
                padx=15,
                pady=10,
                font=("Segoe UI", 10, "italic"),
            )
            think_label.pack(anchor="w", fill="x")

            self.current_thinking_frame = msg_frame

        self.scroll_to_bottom()

    def add_ai_response(self, message):
        """Add or update AI response"""
        # Remove thinking frame
        if self.current_thinking_frame:
            parent = self.current_thinking_frame.master
            parent.destroy()
            self.current_thinking_frame = None

        if self.current_ai_message_frame:
            # Clear existing message widgets
            for widget in self.current_ai_message_frame.winfo_children():
                if not isinstance(widget, ttk.Frame):  # Preserve header frame
                    widget.destroy()
        else:
            # Create new AI message frame
            frame, msg_frame = self.add_new_ai_message_frame()
            self.current_ai_message_frame = msg_frame

        # Format code blocks
        message_parts = []
        current_pos = 0

        # Detect code blocks (like ```python)
        code_pattern = re.compile(r'```(.*?)```', re.DOTALL)
        for match in code_pattern.finditer(message):
            # Add text before code block
            if match.start() > current_pos:
                message_parts.append(("text", message[current_pos:match.start()]))

            # Add code block
            code_block = match.group(1)
            # If language is specified (like ```python), remove first line
            if "\n" in code_block and not code_block.startswith("\n"):
                # Remove first line (language specifier)
                code_lines = code_block.split("\n")
                code_block = "\n".join(code_lines[1:])

            message_parts.append(("code", code_block))
            current_pos = match.end()

        # Add remaining text
        if current_pos < len(message):
            message_parts.append(("text", message[current_pos:]))

        # If no code blocks found, add entire message
        if not message_parts:
            message_parts.append(("text", message))

        for part_type, part_content in message_parts:
            if part_type == "text":
                msg_label = tk.Label(
                    self.current_ai_message_frame,
                    text=part_content,
                    wraplength=600,
                    justify="left",
                    bg=self.theme.ai_msg_bg,
                    fg=self.theme.ai_msg_fg,
                    padx=15,
                    pady=10,
                    font=("Segoe UI", 10),
                )
                msg_label.pack(anchor="w", fill="x")
            elif part_type == "code":
                code_frame = tk.Frame(self.current_ai_message_frame, bg="#1a1b26", padx=5, pady=5)
                code_frame.pack(anchor="w", fill="x", pady=2)

                code_text = tk.Text(
                    code_frame,
                    wrap=tk.WORD,
                    width=70,
                    height=min(15, part_content.count('\n') + 3),
                    bg="#1a1b26",
                    fg="#7dcfff",
                    font=("Cascadia Code", 9),
                    padx=10,
                    pady=10,
                    relief="flat",
                )
                code_text.insert("1.0", part_content)
                code_text.config(state="disabled")
                code_text.pack(fill="both")

        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        """Scroll chat canvas to bottom"""
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

    def reset_response_widgets(self):
        """Reset current response widgets"""
        self.current_ai_message_frame = None
        self.current_thinking_frame = None
        self.is_thinking_active = False