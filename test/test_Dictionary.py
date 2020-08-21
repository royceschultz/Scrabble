def test_Dictionary_is_importable():
    import Scrabble.src.Dictionary

def test_is_word():
    from Scrabble.src.Dictionary import is_word
    assert is_word('test')
    assert is_word('hello')
    assert not is_word('qwer')
