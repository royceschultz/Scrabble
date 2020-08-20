from .Game import current_player

def print_sparse_matrix(matrix, default='.', fill={}, overlay={}):
    xs = [i[0] for i in matrix] + [0]
    ys = [i[1] for i in matrix] + [0]
    for i in range(max(xs)):
        for j in range(max(ys)):
            p = (i,j)
            value = overlay.get(p, matrix.get(p, fill.get(p, default)))
            print(f' {str(value):3s} ', end='')
        print()
    return

def print_game(game):
    print_sparse_matrix(game['bonus_tiles'], overlay=game['played_tiles'])
    print('Scoreboard')
    for player in game['players']:
        print(player['score'], player['name'])

    player = get_current_player(game)
    print('Current Player:', player['name'])
    print(''.join([letter*player['rack'][letter] for letter in player['rack']]))
