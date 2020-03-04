def format_message(text):
    result_text = ''

    prev_char = ''
    for char in text.strip(' ').strip('\n'):
        if ((char == ' ' and prev_char != ' ' or char != ' ') and
                (char == '\n' and prev_char != '\n' or char != '\n')):
            result_text += char
        prev_char = char

    return result_text
