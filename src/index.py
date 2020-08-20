from Database import fetchQuery, runQuery, get_connection
import Game
import random
import json

def random_id(length=32):
    symbols = 'abcdefghijklmnopqrstuvwxyz1234567890-'
    return ''.join(random.sample(symbols, k=length))

def get_new_game(user, gameOptions):
    num_players = gameOptions.get('num_players', 2)
    num_bots = gameOptions.get('num_bots', 0)
    num_matchmaking = num_players - 1 - num_bots
    assert num_matchmaking>= 0
    new_game = Game.new_game(players=[user] + num_bots * ['bot'] + num_matchmaking * ['matching'])
    game_id = random_id()

    con = get_connection()
    cur = con.cursor()

    status = 'playing'
    if num_matchmaking > 0:
        status = 'matchmaking'
    query = f"INSERT INTO games (game_id, game_state, status, num_players) VALUES ('{game_id}', '{json.dumps(new_game)}', '{status}', {num_players})"
    cur.execute(query)

    query = f"INSERT INTO sessions (game_id, user_id) VALUES ('{game_id}', '{user}')"
    cur.execute(query)

    con.commit()
    cur.close()
    con.close()
    return {'user': user, 'game': new_game, 'id': game_id}

def get_user_games(user):
    # Return game_ids for logged in user
    query = f'''
    SELECT games.game_id, game_state FROM games
    JOIN sessions ON games.game_id = sessions.game_id
    where sessions.user_id='{user}'
    '''
    rows, cols = fetchQuery(query)
    games = [{'id': x[0],
              'players': [{'name': player['name'], 'score': player['score']} for player in x[1]['players']],
              'current_player_name': Game.get_current_player(x[1])['name'],
    } for x in rows]
    return {'game_ids': [x[0] for x in rows], 'games':games}

def search_game_by_id(game_id, user):
    rows, cols = fetchQuery(f"SELECT game_id, game_state from games WHERE game_id='{game_id}'")
    assert len(rows) > 0
    game_state = rows[0][1]
    game_state['id'] = rows[0][0]
    for player in game_state['players']:
        if player['name'] == user:
            game_state['user'] = player
        else:
            player['rack'] = None

    return {'game_state': game_state}


def handler(event, context):
    path = event['context']['proxy']
    method = event['context']['http-method']
    user = event['context']['user']
    query_str = event['params']['querystring']

    if path == 'new_game':
        if method == 'GET':
            return get_new_game(user, query_str)

    if path == 'game':
        if method == 'GET':
            # GET game by game_id
            if 'game_id' in query_str:
                return search_game_by_id(query_str['game_id'], user)
            else:
                # Return game_ids for logged in user
                return get_user_games(user)
        if method == 'POST':
            post_json = event['body-json']
            game = search_game_by_id(post_json['game_id'])
            try:
                Game.play(game, user, post_json['move'])
                # TODO: Save game to db
                return {'event': event, 'game': game}
            except:
                return {'event': event, 'message': 'INVALID MOVE'}

    if path == 'word':
        # Is word endpoints
        pass

    return {'event': event, 'user': user, 'path': path, 'method': method, 'query_str': query_str}
