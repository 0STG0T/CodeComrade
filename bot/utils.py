def clean_code(code: str):
    if '/' in code:
        code = code.replace('/', ' ')
    