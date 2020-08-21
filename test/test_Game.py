def test_Game_is_importable():
    from Scrabble.src import Game

def test_init():
    from Scrabble.src import Game
    game = Game.new_game()

def test_current_player():
    from Scrabble.src import Game
    game = Game.new_game()
    assert Game.get_current_player(game)['name'] == 'P1'


def test_make_move():
    import Scrabble.src.Game as Game
    game = Game.new_game()
    Game.get_current_player(game)['rack'] = {'h':3,'i':4}
    move = {
        '7,7': 'h',
        '7,8': 'i',
    }
    Game.play(game,'P1', move)
    assert game['played_tiles']['7,7'] == 'h'
    assert game['played_tiles']['7,8'] == 'i'
    assert Game.get_current_player(game)['name'] == 'P2'

def test_make_2_moves():
    import Scrabble.src.Game as Game
    game = Game.new_game()
    Game.get_current_player(game)['rack'] = {'h':3,'i':4}
    move = {
        '7,7': 'h',
        '7,8': 'i',
    }
    Game.play(game, 'P1', move)
    assert game['played_tiles']['7,7'] == 'h'
    assert game['played_tiles']['7,8'] == 'i'
    assert Game.get_current_player(game)['name'] == 'P2'
    Game.get_current_player(game)['rack'] = {'p':3,'i':4}
    move = {
        '8,7': 'i',
    }
    Game.play(game,'P2', move)
    assert game['played_tiles']['7,7'] == 'h'
    assert game['played_tiles']['8,7'] == 'i'
    assert Game.get_current_player(game)['name'] == 'P1'

def test_invalid_first_move():
    from Scrabble.src import Game
    game = Game.new_game()
    Game.get_current_player(game)['rack'] = {'h':3,'i':4}
    move = {
        '7,8': 'h',
        '7,9': 'i',
    }
    try:
        Game.play(game,'P1', move)
        assert False
    except:
        assert Game.get_current_player(game)['name'] == 'P1'

def test_invalid_second_move():
    from Scrabble.src import Game
    game = Game.new_game()
    Game.get_current_player(game)['rack'] = {'h':3,'i':4}
    move = {
        '7,7': 'h',
        '7,8': 'i',
    }
    Game.play(game,'P1', move)
    assert game['played_tiles']['7,7'] == 'h'
    assert game['played_tiles']['7,8'] == 'i'
    assert Game.get_current_player(game)['name'] == 'P2'
    Game.get_current_player(game)['rack'] = {'p':3,'i':4}
    move = {
        '7,10': 'i',
    }
    try:
        Game.play(game,'P2', move)
        # Failed to detect invalid move
        assert False
    except:
        print(game)
        assert Game.get_current_player(game)['name'] == 'P2'

def test_3_player_turn_rotation():
    from Scrabble.src import Game
    game = Game.new_game(players=['1','2','3'])
    assert Game.get_current_player(game)['name'] == '1'
    Game.end_turn(game)
    assert Game.get_current_player(game)['name'] == '2'
    Game.end_turn(game)
    assert Game.get_current_player(game)['name'] == '3'
    Game.end_turn(game)
    assert Game.get_current_player(game)['name'] == '1'
    Game.end_turn(game)
