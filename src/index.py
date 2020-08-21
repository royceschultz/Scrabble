from Database import fetchQuery, runQuery, get_connection
import Game
import random
import json
import re

def prepare_game_for_user(game, user):
    game_cleaned = game.copy()
    for player in game_cleaned['players']:
        if player['name'] != user:
            player['rack'] = None
        else:
            game_cleaned['user'] = player
    game_cleaned['bag'] = None
    game_cleaned['current_player'] = Game.get_current_player(game_cleaned)
    return game_cleaned

def summarize_game(game):
    summary = {}
    copy_fields = ['id', 'players']
    game['id'] = game.get('id', '1234')
    for field in copy_fields:
        summary[field] = game[field]
    return summary


def random_id(length=32):
    symbols = 'abcdefghijklmnopqrstuvwxyz1234567890-'
    return ''.join(random.sample(symbols, k=length))


def get_new_game(user, gameOptions):
    num_players = gameOptions.get('num_players', 2)
    num_bots = gameOptions.get('num_bots', 0)
    num_matchmaking = num_players - 1 - num_bots
    assert num_matchmaking >= 0

    game_id = random_id()
    new_game = Game.new_game(players=[user] + num_bots * ['bot'] + num_matchmaking * ['matching'])
    new_game['id'] = game_id

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
    SELECT game_state FROM games
    JOIN sessions ON games.game_id = sessions.game_id
    where sessions.user_id='{user}'
    '''
    rows, cols = fetchQuery(query)
    games = [summarize_game(prepare_game_for_user(row[0], user)) for row in rows]
    return {'games': games}


def search_game_by_id(game_id):
    rows, cols = fetchQuery(f"SELECT game_state from games WHERE game_id='{game_id}'")
    assert len(rows) > 0
    game_state = rows[0][0]
    return game_state


def handler(event, context):
    path = event['context']['proxy']
    method = event['context']['http-method']
    user = event['context']['user']
    query_str = event['params']['querystring']

    if re.search('^new_game', path):
        if method == 'GET':
            return get_new_game(user, query_str)

    if re.search('^games', path):
        if method == 'GET':
            # GET game by game_id
            if re.search('^games/game_id', path):
                # TODO: Add error handling
                assert 'game_id' in query_str
                return {'game_state': prepare_game_for_user(search_game_by_id(query_str['game_id']), user)}
            else:
                # Return a list of summaries for games matching the logged in user
                return get_user_games(user)
    if re.search('^play', path):
        if method == 'POST':
            post_json = event['body-json']
            assert 'game_id' in post_json
            assert 'move' in post_json
            game = search_game_by_id(post_json['game_id'])
            try:
                Game.play(game, user, post_json['move'])
                con = get_connection()
                cur = con.cursor()
                query = f"UPDATE games SET game_state={json.dumps(game)} WHERE game_id={post_json['game_id']}"
                cur.execute(query)
                query = f"INSERT INTO sessions (game_id, user_id) VALUES ('{game_id}', '{user}')"
                cur.execute(query)
                con.commit()
                cur.close()
                con.close()

                # TODO: Handle AI move

                return {'event': event, 'game': game}
            except:
                return {'event': event, 'message': 'INVALID MOVE'}

    if re.search('^dictionary', path):
        # Is word endpoints
        pass

    return {'event': event, 'user': user, 'path': path, 'method': method, 'query_str': query_str}
