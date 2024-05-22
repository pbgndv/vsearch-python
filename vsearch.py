def search4vowels(phrase: str) -> set:
    """Возвращает сет гласных, найденных в фразе"""
    return set('aeiou').intersection(set(phrase))

def search4letters(phrase: str, letters: str='aeiou') -> set:
    """Возвращает сет букв, найденных в фразе"""
    return set(letters).intersection(set(phrase))