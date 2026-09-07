from unidecode import unidecode

def normalizar(texto):
    texto = str(texto)
    texto = unidecode(texto)
    texto = texto.lower().strip()

    while "  " in texto:
        texto = texto.replace("  ", " ")

    return texto