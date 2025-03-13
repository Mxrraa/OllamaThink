class CustomTheme:
    def __init__(self):
        # Default to dark theme
        self.bg_color = "#1E1E2E"  # Dark background
        self.text_color = "#CDD6F4"  # Light text
        self.accent_color = "#89B4FA"  # Accent color
        self.user_msg_bg = "#45475A"  # User message background
        self.user_msg_fg = "#FFFFFF"  # User message text
        self.ai_msg_bg = "#313244"  # AI message background
        self.ai_msg_fg = "#CDD6F4"  # AI message text
        self.think_bg = "#2A2A3C"  # Thinking background
        self.think_fg = "#A6ADC8"  # Thinking text
        self.button_bg = "#89B4FA"  # Button background
        self.button_fg = "#1E1E2E"  # Button text

    def set_light_theme(self):
        """Switch to light theme"""
        self.bg_color = "#F5F5F5"
        self.text_color = "#333333"
        self.accent_color = "#1E88E5"
        self.user_msg_bg = "#1E88E5"
        self.user_msg_fg = "#FFFFFF"
        self.ai_msg_bg = "#EEEEEE"
        self.ai_msg_fg = "#333333"
        self.think_bg = "#E1E1E1"
        self.think_fg = "#666666"
        self.button_bg = "#1E88E5"
        self.button_fg = "#FFFFFF"

    def set_dark_theme(self):
        """Switch to dark theme"""
        self.bg_color = "#1E1E2E"
        self.text_color = "#CDD6F4"
        self.accent_color = "#89B4FA"
        self.user_msg_bg = "#45475A"
        self.user_msg_fg = "#FFFFFF"
        self.ai_msg_bg = "#313244"
        self.ai_msg_fg = "#CDD6F4"
        self.think_bg = "#2A2A3C"
        self.think_fg = "#A6ADC8"
        self.button_bg = "#89B4FA"
        self.button_fg = "#1E1E2E"