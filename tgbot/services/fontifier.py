ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя1234567890,\"()?!#@$%"


def fontify(text: str, font: str) -> str:
    dct = zip(ALPHABET, font)
    for orig, font_char in dct:
        text = text.replace(orig, font_char)

    return text
