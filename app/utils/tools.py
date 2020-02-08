
def format_message(text):
    result_text = ''

    prev_char = ''
    for char in text.strip(' '):
        if (char == ' ' and prev_char != ' ') or char != ' ':
            result_text += char
        prev_char = char

    return result_text

