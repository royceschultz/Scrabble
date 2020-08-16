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
        (7,7): 'h',
        (7,8): 'i',
    }
    game.play('P1', move)
    assert game.board[(7,7)] == 'h'
    assert game.board[(7,8)] == 'i'
    assert game.current_player().name == 'P2'

def test_make_2_moves():
    from Scrabble.src.Game import Game
    game = Game()
    game.current_player().rack = {'h':3,'i':4}
    move = {
        (7,7): 'h',
        (7,8): 'i',
    }
    game.play('P1', move)
    assert game.board[(7,7)] == 'h'
    assert game.board[(7,8)] == 'i'
    assert game.current_player().name == 'P2'
    game.current_player().rack = {'p':3,'i':4}
    move = {
        (8,7): 'i',
    }
    game.play('P2', move)
    assert game.board[(7,7)] == 'h'
    assert game.board[(8,7)] == 'i'
    assert game.current_player().name == 'P1'

def test_3_player_turn_rotation():
    from Scrabble.src.Game import Game
    game = Game(players=['1','2','3'])
    assert game.current_player().name == '1'
    game.end_turn()
    assert game.current_player().name == '2'
    game.end_turn()
    assert game.current_player().name == '3'
    game.end_turn()
    assert game.current_player().name == '1'
    game.end_turn()
