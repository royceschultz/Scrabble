def test_Dictionary_is_importable():
    import Scrabble.src.Dictionary

def test_Is_Word():
    from Scrabble.src.Dictionary import Is_Word
    assert Is_Word('test')
    assert Is_Word('hello')
    assert not Is_Word('qwer')
