from .DefaultSettings import DEFAULT_BONUSES, DEFAULT_LETTER_POINTS
from .SparseMatrix import SparseMatrix
from .Bag import Bag
from .Player import Player
from .Dictionary import Is_Word

def parse_bonus(bonus):
    return {
        'dl': (2,1),
        'tl': (3,1),
        'dw': (1,2),
        'tw': (1,3),
    }.get(bonus, (1,1))

def count_unique(values):
    counts = {}
    for v in values:
        if v in counts:
            counts[v] += 1
        else:
            counts[v] = 1
    return counts

class Game:
    def __init__(self, players=['P1','P2']):
        assert len(players) > 1
        self.board_size = 15
        self.board = SparseMatrix()
        self.bonuses = SparseMatrix(DEFAULT_BONUSES)
        # WARNING: using a dict pointer, not a copy.
        # Modifying in this context will affect other instances using this variable
        # I (currently) don't plan to modify the dict
        self.points = DEFAULT_LETTER_POINTS
        self.bag = Bag()
        self.players = [Player(name) for name in players]
        self.player_turn = 0
        self.count_turn = 0

        for player in self.players:
            player.fill_rack(self.bag)
        self.state()

    def state(self):
        print(self.bonuses.toString(overlay=self.board))
        print('Scoreboard:')
        for player in self.players:
            print(player.score, player.name)
        player = self.current_player()
        print('Current Player:', player.name)
        print('Player Rack:', ''.join([letter*player.rack[letter] for letter in player.rack]))


    def current_player(self):
        player = self.players[self.player_turn]
        return player

    def end_turn(self):
        self.player_turn = (self.player_turn + 1) % len(self.players)
        self.count_turn += 1
        return self.current_player()

    def scan_move(self, start_coord, direction, move):
        x,y = start_coord
        Directions = {'h':[1,0],'v':[0,1]}
        dx, dy = Directions[direction]
        # Given the direction, go to the first letter of the word
        while (x-dx, y-dy) in self.board or (x-dx, y-dy) in move:
            x -= dx
            y -= dy
        word = ''
        score = 0
        total_word_scale = 1
        scanned_coords = []
        bonuses = {}
        # Now read through the word in order
        p = (x,y)
        while p in self.board or p in move:
            # Check tile is not already filled
            assert not (p in self.board and p in move)
            if p in self.board:
                letter = self.board[p]
                word += letter
                score += self.points[letter]
            if p in move:
                letter = move[p]
                word += letter
                bonus = self.bonuses.get(p)
                bonuses[p] = f'{bonus} bonus for {letter}'
                letter_scale, word_scale = parse_bonus(bonus)
                score += letter_scale * self.points[letter]
                total_word_scale *= word_scale
            scanned_coords.append(p)
            x,y = p
            x += dx
            y += dy
            p = (x,y)
        score *= total_word_scale
        print(f'found {word} for {score} points with bonuses: {bonuses}')
        return word, score, scanned_coords

    def play(self, player, move):
        # Check it is the players turn
        assert player == self.current_player().name

        # Check player has enough letters for the requested move
        letter_counts = count_unique(move.values())
        for letter in letter_counts:
            assert letter_counts[letter] <= self.current_player().rack.get(letter,0)

        # Check played tiles are within the board boundry
        for dim in range(2):
            xs = [i[dim] for i in move]
            assert all(x >= 0 for x in xs)
            assert all(x < self.board_size for x in xs)

         # Find words for each played tile
        already_scanned = {'h': {}, 'v':{}}
        times_scanned = {'h':0,'v':0}
        words = []
        scores = []
        for coord in move:
            for direc in already_scanned.keys(): # for direction in ['h','v']
                if coord not in already_scanned[direc]:
                    print(f'Scanning {coord} in direction: {direc}')
                    times_scanned[direc] += 1
                    word, score, scanned_coords = self.scan_move(coord, direc, move)
                    for scanned_coord in scanned_coords:
                        already_scanned[direc][scanned_coord] = True
                    if len(word) > 1:
                        words.append(word)
                        scores.append(score)
        flag = False
        for coord in set(already_scanned['h']).union(already_scanned['v']):
            if self.count_turn == 0:
                if self.bonuses.get(coord) == 'ctr':
                    flag = True
                    break
            else:
                if coord in self.board:
                    flag = True
                    break
        # Check the word either includes the center tile or is branched off an existing word
        assert flag
        print('found',words,'for',scores,'points')
        print(times_scanned)
        # Check word is played in a continuous line
        assert 1 in times_scanned.values()

        # Check at least 1 word was found
        assert len(words) > 0

        # Check each word is a real word
        # TODO: Re-enable. Temporarily disabled for dev purposes.
        # for word in words:
        #     assert Is_Word(word)

        # Place tiles on board
        for coord in move:
            self.board[coord] = move[coord]

        # remove from player rack
        for letter in move.values():
            self.current_player().remove_letter(letter)

        # Draw more letters for the player
        self.current_player().fill_rack(self.bag)

        self.current_player().score += sum(scores)
        # advance to the next player
        self.end_turn()
        self.state()
