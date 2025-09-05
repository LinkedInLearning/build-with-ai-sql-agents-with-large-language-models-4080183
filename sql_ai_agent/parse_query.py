import re


def is_markdown_code_chunk(text):
    """
    Checks if the given text is in Markdown code chunk format.

    Args:
        text (str): The text to check.

    Returns:
        bool: True if the text is in Markdown code chunk format, False otherwise.
    """
    pattern = r"```[^`]*```"
    return bool(re.search(pattern, text, re.DOTALL))


def extract_code_from_markdown(markdown_text):
    """
    Extracts code from a Markdown code chunk.

    Args:
        markdown_text (str): The Markdown text containing the code chunk.

    Returns:
        str: The extracted code.
    """
    pattern = r"```(.*?)\n(?P<code>.*?)\n```"
    match = re.search(pattern, markdown_text, re.DOTALL)
    if match:
        return match.group("code")
    else:
        return None
