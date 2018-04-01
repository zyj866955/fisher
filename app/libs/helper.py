def is_isbn_or_key(word):
    """
    :param word:
    :return:
    """
    key_or_isbn = 'key'
    if len(word) == 13 and word.isdigit():
        key_or_isbn = 'isbn'
    if '-' in word:
        short_word = word.replace('-', '')
        if len(short_word) == 10 and short_word.isdigit():
            key_or_isbn = 'isbn'
    return key_or_isbn
