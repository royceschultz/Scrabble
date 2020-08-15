def test_Game_is_importable():
    from Scrabble.src.Game import Game

def test_init():
    from Scrabble.src.Game import Game
    game = Game()

def test_current_player():
    from Scrabble.src.Game import Game
    game = Game()
    assert game.current_player().name == 'P1'

def test_make_move():
    from Scrabble.src.Game import Game
    game = Game()
    game.current_player().rack = {'h':3,'i':4}
    move = {
        (1,1): 'h',
        (1,2): 'i',
    }
    game.play('P1', move)
    assert game.board[(1,1)] == 'h'
    assert game.board[(1,2)] == 'i'
    assert game.current_player().name == 'P2'

def test_make_2_moves():
    from Scrabble.src.Game import Game
    game = Game()
    game.current_player().rack = {'h':3,'i':4}
    move = {
        (1,1): 'h',
        (1,2): 'i',
    }
    game.play('P1', move)
    assert game.board[(1,1)] == 'h'
    assert game.board[(1,2)] == 'i'
    assert game.current_player().name == 'P2'
    game.current_player().rack = {'p':3,'i':4}
    move = {
        (2,1): 'i',
    }
    game.play('P2', move)
    assert game.board[(1,1)] == 'h'
    assert game.board[(2,1)] == 'i'
    assert game.current_player().name == 'P1'
