import re

def smarten_tex_quotes(text: str) -> str:
    text = re.sub(r'"(.+?)"', r"``\1''", text)
    text = re.sub(r"'(.+?)'", r"`\1'", text)
    return text

def escape_tex(text: str) -> str:
    special = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',  # this will be skipped inside math
        '#': r'\#',
        '_': r'\_',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
    }

    # Pattern to match inline math like $...$
    math_pattern = re.compile(r'\$(.+?)\$')

    # Split text into segments: math and non-math
    parts = []
    last_end = 0

    for match in math_pattern.finditer(text):
        # Text before math → escape
        before = text[last_end:match.start()]
        for char, replacement in special.items():
            if char == '$':
                continue  # don't escape $ outside math yet
            before = before.replace(char, replacement)
        before = before.replace('$', r'\$')  # escape remaining dollar signs outside math

        # Math content → leave as-is
        math = match.group(0)  # includes surrounding $...$

        parts.append(before)
        parts.append(math)
        last_end = match.end()

    # Handle the tail (after last match)
    after = text[last_end:]
    for char, replacement in special.items():
        if char == '$':
            continue
        after = after.replace(char, replacement)
    after = after.replace('$', r'\$')

    parts.append(after)

    return ''.join(parts)
