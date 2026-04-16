def token(s):
    tokens = []
    for ch in s:
        if ch.isspace():
            continue
        if ch in "()+*!":
            tokens.append(ch)
        elif ch.isalpha():
            tokens.append(ch)
        elif ch in "01":
            tokens.append(ch)
        else:
            raise ValueError(f"Invalid character: {ch}")
    return tokens
