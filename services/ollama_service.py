from ollama import chat, ChatResponse


def process_ollama_message(model, conversation, message_manager, root_widget, show_thinking):
    """Process message with Ollama API and handle response streaming"""
    # Initialize response tracking variables
    ai_response = ""
    thinking_text = ""
    is_thinking = False

    # Send full conversation history
    response: ChatResponse = chat(
        model=model,
        messages=conversation,
        stream=True
    )

    for chunk in response:
        content = chunk.message.content

        # Check for thinking process
        if "<think>" in content and not is_thinking:
            is_thinking = True
            thinking_text = content.replace("<think>", "")
            if show_thinking:
                root_widget.after(0, lambda t=thinking_text: message_manager.add_thinking_message(t))

        elif is_thinking and "</think>" in content:
            # End of thinking process
            think_end = content.split("</think>")
            thinking_text += think_end[0]

            if show_thinking:
                root_widget.after(0, lambda t=thinking_text: message_manager.add_thinking_message(t))

            is_thinking = False

            # Start of normal response
            if len(think_end) > 1:
                ai_response = think_end[1]
                root_widget.after(0, lambda r=ai_response: message_manager.add_ai_response(r))

        elif is_thinking:
            # Thinking continues
            thinking_text += content
            if show_thinking:
                root_widget.after(0, lambda t=thinking_text: message_manager.add_thinking_message(t))

        else:
            # Normal response
            ai_response += content
            root_widget.after(0, lambda r=ai_response: message_manager.add_ai_response(r))

    return ai_response