def test_Bag_is_importable():
    from Scrabble.src.Bag import Bag

def test_draw():
    from Scrabble.src.Bag import Bag
    bag = Bag()
    letters = ''
    letter = bag.draw()[0]
    i = 0
    while letter and i < 200:
        letters += letter
        letter = bag.draw()
        i += 1
    assert len(letters) == 100
