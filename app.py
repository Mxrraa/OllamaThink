import tkinter as tk
from tkinter import ttk, filedialog
import threading
import json
import os
from datetime import datetime

from config.theme import CustomTheme
from ui.components import create_top_frame, create_toolbar
from ui.message_widgets import MessagesManager
from services.ollama_service import process_ollama_message


class OllamaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama AI Chat")
        self.root.geometry("900x700")

        # Set theme
        self.theme = CustomTheme()
        self.apply_theme()

        # Main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Top frame - Model selection and settings
        self.top_frame, self.model_var, self.show_thinking_var, self.status_dot, self.status_label = create_top_frame(
            self.main_frame, self.theme
        )

        # Middle frame - Chat area
        self.chat_frame = ttk.Frame(self.main_frame)
        self.chat_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Chat canvas
        self.chat_canvas = tk.Canvas(
            self.chat_frame, bg=self.theme.bg_color, highlightthickness=0
        )
        self.chat_canvas.pack(side=tk.LEFT, fill="both", expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.chat_frame, orient="vertical", command=self.chat_canvas.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Inner frame - Will hold messages
        self.messages_frame = ttk.Frame(self.chat_canvas)
        self.messages_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")),
        )

        self.canvas_frame = self.chat_canvas.create_window(
            (0, 0), window=self.messages_frame, anchor="nw"
        )
        self.chat_canvas.bind("<Configure>", self.on_canvas_configure)

        # Bottom frame - Input area
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill="x")

        self.input_box = tk.Text(
            self.input_frame,
            height=3,
            wrap=tk.WORD,
            bg=self.theme.ai_msg_bg,
            fg=self.theme.text_color,
            insertbackground=self.theme.text_color,
            font=("Segoe UI", 10),
            padx=10,
            pady=10,
            relief="flat",
        )
        self.input_box.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 10))
        self.input_box.bind("<Return>", self.handle_return)
        self.input_box.bind("<Shift-Return>", lambda e: None)  # Shift+Enter allows newline

        # Send button
        self.send_button = tk.Button(
            self.input_frame,
            text="Gönder",
            bg=self.theme.button_bg,
            fg=self.theme.button_fg,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            command=self.send_message,
        )
        self.send_button.pack(side=tk.RIGHT, padx=(0, 0), pady=(0, 0))

        # Hover effect for send button
        self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg="#78A5EB"))
        self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg=self.theme.button_bg))

        # Toolbar
        self.toolbar_frame, self.toolbar_buttons = create_toolbar(
            self.main_frame, self.theme, self.clear_chat, self.save_conversation, self.change_theme
        )

        # Conversation history
        self.conversation = []

        # Message manager
        self.message_manager = MessagesManager(
            self.messages_frame,
            self.chat_canvas,
            self.theme,
            self.model_var
        )

        # Welcome message
        self.message_manager.add_system_message("Ollama AI Chat'e hoş geldiniz. Seçili model: " + self.model_var.get())

    def apply_theme(self):
        self.root.configure(bg=self.theme.bg_color)

        # Ttk styles
        style = ttk.Style()
        style.configure("TFrame", background=self.theme.bg_color)
        style.configure("TLabel", background=self.theme.bg_color, foreground=self.theme.text_color)
        style.configure("TCheckbutton", background=self.theme.bg_color, foreground=self.theme.text_color)
        style.map("TCheckbutton", background=[("active", self.theme.bg_color)])

        # Scrollbar style
        style.configure(
            "Vertical.TScrollbar",
            background=self.theme.user_msg_bg,
            troughcolor=self.theme.bg_color,
            borderwidth=0,
            arrowsize=14,
        )

    def on_canvas_configure(self, event):
        # Resize window according to canvas width
        self.chat_canvas.itemconfig(self.canvas_frame, width=event.width)

    def handle_return(self, event):
        if not event.state & 0x1:  # Shift key is not pressed
            self.send_message()
            return "break"  # Prevents default behavior

    def send_message(self):
        user_message = self.input_box.get("1.0", tk.END).strip()
        if not user_message:
            return

        # Clear input box
        self.input_box.delete("1.0", tk.END)

        # Add user message to chat
        self.message_manager.add_user_message(user_message)

        # Add to chat history
        self.conversation.append({"role": "user", "content": user_message})

        # Reset for new response
        self.message_manager.reset_response_widgets()

        # Disable interface during processing
        self.send_button.config(state=tk.DISABLED)
        self.status_dot.itemconfig(1, fill="#FFA500")  # Orange = Processing
        self.status_label.config(text="İşleniyor...")

        # Process in background
        threading.Thread(
            target=self.process_message,
            args=(user_message,),
            daemon=True
        ).start()

    def process_message(self, user_message):
        try:
            # Get selected model
            model = self.model_var.get()

            # Process message with Ollama API
            ai_response = process_ollama_message(
                model,
                self.conversation.copy(),
                self.message_manager,
                self.root,
                self.show_thinking_var.get()
            )

            # Add AI response to chat history
            self.conversation.append({"role": "assistant", "content": ai_response})

        except Exception as e:
            error_msg = f"Hata: {str(e)}"
            self.root.after(0, lambda: self.message_manager.add_system_message(error_msg))

        # Re-enable interface
        self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.status_dot.itemconfig(1, fill="#4CAF50"))  # Green = Ready
        self.root.after(0, lambda: self.status_label.config(text="Hazır"))

    def clear_chat(self):
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        self.conversation = []
        self.message_manager.reset_response_widgets()
        self.message_manager.add_system_message("Sohbet temizlendi. Seçili model: " + self.model_var.get())

    def save_conversation(self):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            initialfile=f"ollama_chat_{timestamp}.json",
        )

        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.conversation, f, ensure_ascii=False, indent=2)
            self.message_manager.add_system_message(f"Konuşma başarıyla kaydedildi: {os.path.basename(filename)}")

    def change_theme(self):
        # Toggle between light and dark themes
        if self.theme.bg_color == "#1E1E2E":  # Currently dark theme
            # Switch to light theme
            self.theme.set_light_theme()
        else:
            # Switch to dark theme
            self.theme.set_dark_theme()

        # Apply theme
        self.apply_theme()

        # Update existing widgets
        self.input_box.config(
            bg=self.theme.ai_msg_bg,
            fg=self.theme.text_color,
            insertbackground=self.theme.text_color
        )
        self.chat_canvas.config(bg=self.theme.bg_color)
        self.send_button.config(bg=self.theme.button_bg, fg=self.theme.button_fg)

        for btn in self.toolbar_buttons:
            btn.config(bg=self.theme.user_msg_bg, fg=self.theme.user_msg_fg)

        # Rebuild chat
        self.rebuild_chat()

    def rebuild_chat(self):
        """Rebuild entire chat from message history"""
        # Clear all messages
        for widget in self.messages_frame.winfo_children():
            widget.destroy()

        # Add welcome message
        self.message_manager.add_system_message("Ollama AI Chat'e hoş geldiniz. Seçili model: " + self.model_var.get())

        # Add history messages
        for msg in self.conversation:
            if msg["role"] == "user":
                self.message_manager.add_user_message(msg["content"])
            elif msg["role"] == "assistant":
                # Create new message frame
                frame, msg_frame = self.message_manager.add_new_ai_message_frame()
                self.message_manager.current_ai_message_frame = msg_frame

                # Add message
                self.message_manager.add_ai_response(msg["content"])

                # Cleanup
                self.message_manager.current_ai_message_frame = None