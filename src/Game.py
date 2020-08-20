from DefaultSettings import DEFAULT_BONUSES, DEFAULT_LETTER_POINTS, DEFAULT_BAG_DIST
import random
from Dictionary import is_word

'''
Bag Functions
'''
def count_unique(values):
    unique_values = {}
    for value in values:
        add_to_bag(value, unique_values)
    return unique_values

def num_tiles(bag):
    return sum(bag.values())

def add_to_bag(letter, bag):
    if letter in bag:
        bag[letter] += 1
    else:
        bag[letter] = 1
    return

def remove_from_bag(letter, bag):
    assert letter in bag
    bag[letter] -= 1
    assert bag[letter] >= 0

def draw_from_bag(bag):
    if num_tiles(bag) == 0:
        return None
    letter = random.choices(list(bag.keys()), weights=list(bag.values()))[0]
    bag[letter] -= 1
    assert bag[letter] >= 0
    # TODO: remove empty letters (bag[letter] == 0) to minimize object size
    return letter


def fill_player_rack(player, bag, full_rack_len=7):
    print('filling player rack', player)
    rack_space = full_rack_len - num_tiles(player['rack'])
    assert rack_space >= 0
    for i in range(rack_space):
        letter = draw_from_bag(bag)
        if letter is None:
            break
        add_to_bag(letter, player['rack'])
    return

'''
Game Functions
'''

def new_game(players=['P1', 'P2']):
    game = {
        'board_size': 15,
        'played_tiles': {},
        'bonus_tiles': DEFAULT_BONUSES.copy(),
        'letter_values': DEFAULT_LETTER_POINTS.copy(),
        'bag': DEFAULT_BAG_DIST.copy(),
        'players': [{'name': player, 'rack': {}, 'score': 0} for player in players],
        'turn_number': 0
    }
    for player in game['players']:
        fill_player_rack(player, game['bag'])
    return game

def get_current_player(game):
    return game['players'][game['turn_number'] % len(game['players'])]

def end_turn(game):
    game['turn_number'] += 1
    return

def parse_bonus(bonus):
    if bonus == None: return (1,1)
    if bonus == 'dl': return (2,1)
    if bonus == 'tl': return (3,1)
    if bonus == 'dw': return (1,2)
    if bonus == 'tw': return (1,3)
    return (1,1)

def scan_move(game, start_coord, direction, move):
    x,y = start_coord
    dx, dy = {'h':[1,0],'v':[0,1]}[direction]
    # Given the direction, go to the first letter of the word
    while (x-dx, y-dy) in move or (x-dx, y-dy) in game['played_tiles']:
        x -= dx
        y -= dy
    word = ''
    score = 0
    total_word_scale = 1
    scanned_coords = []
    # TODO: Remove. Saving bonus scales for logging purposes only.
    bonuses = {}
    # Now read through the word in order
    p = (x,y)
    while p in move or p in game['played_tiles']:
        # Check tile is not already filled
        assert not (p in move and p in game['played_tiles'])
        if p in game['played_tiles']:
            letter = game['played_tiles'][p]
            word += letter
            score += game['letter_values'][letter]
        if p in move:
            letter = move[p]
            word += letter
            bonus = game['bonus_tiles'].get(p)
            # TODO: Remove bonuses. Used for logging only.
            bonuses[p] = f'{bonus} bonus for {letter}'
            letter_scale, word_scale = parse_bonus(bonus)
            score += letter_scale * game['letter_values'][letter]
            total_word_scale *= word_scale
        scanned_coords.append(p)
        # Move to the next letter
        x,y = p
        x += dx
        y += dy
        p = (x,y)
    score *= total_word_scale
    print(f'found {word} for {score} points with bonuses: {bonuses}')
    return word, score, scanned_coords

def play(game, player, move):
    # Check it is the players turn
    assert player == get_current_player(game)['name']

    # Check player has enough letters for the requested move
    letter_counts = count_unique(move.values())
    for letter in letter_counts:
        assert letter_counts[letter] <= get_current_player(game)['rack'].get(letter,0)

    # Check played tiles are within the board boundry
    for dim in range(2):
        xs = [i[dim] for i in move]
        assert all(x >= 0 for x in xs)
        assert all(x < game['board_size'] for x in xs)

     # Find words for each played tile
    already_scanned = {'h': {}, 'v':{}}
    times_scanned = {'h':0,'v':0}
    words = []
    scores = []
    for coord in move:
        for direc in already_scanned: # for direc in ['h','v']
            if coord not in already_scanned[direc]:
                print(f'Scanning {coord} in direction: {direc}')
                times_scanned[direc] += 1
                word, score, scanned_coords = scan_move(game, coord, direc, move)
                for scanned_coord in scanned_coords:
                    already_scanned[direc][scanned_coord] = True
                if len(word) > 1:
                    words.append(word)
                    scores.append(score)
    # Check word is played in a continuous line
    assert 1 in times_scanned.values()

    # Check the word either includes the center tile or is branched off an existing word
    # TODO: Integrate into the loop above
    flag = False
    for coord in set(already_scanned['h']).union(already_scanned['v']):
        if game['turn_number'] == 0:
            if game['bonus_tiles'].get(coord) == 'ctr':
                flag = True
                break
        else:
            if coord in game['played_tiles']:
                flag = True
                break
    # Check the word either includes the center tile or is branched off an existing word
    assert flag
    print('found',words,'for',scores,'points')
    # Check at least 1 word was found
    assert len(words) > 0
    # Check each word is a real word
    # TODO: Re-enable. Temporarily disabled for dev purposes.
    # for word in words:
    #     assert Is_Word(word)

    # Place tiles on board
    for coord in move:
        game['played_tiles'][coord] = move[coord]

    # remove from player rack
    for letter in move.values():
        remove_from_bag(letter, get_current_player(game)['rack'])

    # Draw more letters for the player
    fill_player_rack(get_current_player(game), game['bag'])

    get_current_player(game)['score'] += sum(scores)
    # advance to the next player
    end_turn(game)
