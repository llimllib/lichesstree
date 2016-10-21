# -*- coding: utf8 -*-
from copy import deepcopy
import json
import logging
import os.path
from os import mkdir
import pickle
from pprint import pprint as pp
import sys
import time

import requests

BLACK = "black"
WHITE = "white"

# personal communication with lukhas suggests that for now this is the best
# UA to use, may help prevent 404s
UA = "Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0"

def w(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def get_timestamp(game):
    if 'timestamp' in game: return game['timestamp']
    if 'createdAt' in game: return game['createdAt']
    raise KeyError(game)

def get_page(user, page, failures=0):
    # this endpoint is currently dead, therefore so is lichess opening tree
    # see https://github.com/s-ted/liPGN/issues/4 ; there doesn't seem to
    # be a corresponding issue in the lichess repo
    url = ("https://en.lichess.org/api/user/{user}/games?"
          "nb=100&with_moves=1&page={page}")

    print(url.format(**locals()))
    res = requests.get(url.format(**locals()),
            headers={'User-Agent': UA})

    # Seems like now there are 404s as well as 429s
    if res.status_code in [404, 429]:
        print("Failure status code {}".format(res.status_code))
        if failures < 3:
            w("💩")
            # 60, 240, 960
            print("sleep {}".format(60 * 4 ** failures))
            time.sleep(60 * 4 ** failures)
            # live dangerously
            return get_page(user, page, failures+1)
        else:
            import ipdb; ipdb.set_trace()

    try:
        return res.json()
    except ValueError:
        import ipdb; ipdb.set_trace()
        raise

def get_all_games(user):
    games = []
    page = 1
    while 1:
        w(".")

        body = get_page(user, page)

        games += body["currentPageResults"]

        if body["nextPage"] and int(page) < 5:
            page += 1
        else:
            break

        time.sleep(3)

    w("\n")
    return games

def get_games_until(user, game_id, timestamp):
    games = []
    page = 1
    while 1:
        w('.')

        body = get_page(user, page)

        for game in body["currentPageResults"]:
            try:
                if game["id"] == game_id:
                    w('💥')
                    time.sleep(3)
                    return games
                if timestamp > get_timestamp(game):
                    w('👎')

                games.append(game)
            except KeyError:
                import ipdb; ipdb.set_trace()

        if body["nextPage"] and int(page) < 5:
            page += 1
        else:
            break

        time.sleep(3)

    return games

def get_color(game, user):
    # Anonymous players don't get userId
    if not "userId" in game["players"][WHITE]:
        return BLACK
    if game["players"][WHITE]["userId"] == user.lower():
        return WHITE
    return "black"

def build_tree(games, user):
    root = {
        WHITE: {},
        BLACK: {},
        "games": games,
    }

    for (i, game) in enumerate(games[:300]):
        color = get_color(game, user)
        moves = game["moves"].split(" ")
        leaf = root[color]

        win = lose = draw = 0
        if "winner" in game:
            win = 1 if game["winner"] == color else 0
            lose = 1 - win
        elif game["status"] in ["draw", "stalemate", "outoftime", "timeout"]:
            # note that we can only do this on 'outoftime' statuses here
            # because we've eliminated cases where there's a winner
            draw = 1
        else:
            print(game)
            raise Exception("wtf mate")

        for move in moves:
            if move in leaf:
                leaf[move]["count"] += 1
                leaf[move]["win"] += win
                leaf[move]["lose"] += lose
                leaf[move]["draw"] += draw
                leaf[move]["games"].add(i)
            else:
                leaf[move] = {
                    "count": 1,
                    "win": win,
                    "draw": draw,
                    "lose": lose,
                    "games": { i }
                }

            leaf = leaf[move]

    return root

# XXX: just here for debugging purposes
def print_node(node):
    c = deepcopy(node)
    if 'children' in c:
        del(c['children'])
    pp(c)

def d3_branch(root, move=None, depth=0):
    newroot = {"children": []}

    if move:
        newroot["move"] = move

    for key, val in root.items():
        if key in ["count", "win", "draw", "lose"]:
            newroot[key] = val
        elif key == "games":
            newroot["games"] = list(val)
        else:
            # recurse
            if depth < 11:
                newroot["children"].append(d3_branch(val, key, depth+1))

    return newroot

# return a tree in d3 format, like http://bl.ocks.org/mbostock/raw/4063550/flare.json
# so that I can just re-use mbostock's code
def d3_format(tree):
    d3_tree = {
        WHITE: {},
        BLACK: {},
        "games": tree["games"],
    }

    d3_tree[WHITE] = d3_branch(tree[WHITE])
    d3_tree[BLACK] = d3_branch(tree[BLACK])
    return d3_tree

def filter_games(games):
    return [
        game for game in games
        if game["variant"] == "standard" and
           game["moves"] and
           game["rated"] == True and
           game["perf"] in ['classical', 'blitz'] #exclude bullet
    ]

if __name__=="__main__":
    user = sys.argv[1]
    dirname = "../lichess-user-data/user/{user}".format(**locals())
    fname = "{dirname}/{user}_games.json".format(**locals())
    if not os.path.isdir(dirname):
        mkdir(dirname)

    if os.path.isfile(fname):
        with open(fname) as f:
            games = json.load(f)

        try:
            t = get_timestamp(games[0])
        except KeyError:
            import ipdb; ipdb.set_trace()
        w("\nupdating {user}: ".format(**locals()))

        # make sure to prepend so we maintain the games ordered by date
        new_games = get_games_until(user, games[0]["id"], t)
        updated_games = new_games + games

        with open(fname, 'w') as f:
            json.dump(updated_games, f)

        w("\n")
    else:
        games = get_all_games(user)
        json.dump(games, open(fname, 'w'))
