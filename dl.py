from copy import deepcopy
import json
import os.path
import pickle
from pprint import pprint as pp
import sys
import time
import requests

BLACK = "black"
WHITE = "white"

def get_all_games(user):
    games = []
    page = 1
    while 1:
        sys.stdout.write(".")
        url = ("http://en.lichess.org/api/user/{user}/games?"
              "nb=100&with_moves=1&page={page}")

        res = requests.get(url.format(**locals()))
        if res.status_code == 429:
            time.sleep(0.5)
            continue

        try:
            body = res.json()
        except ValueError:
            import ipdb; ipdb.set_trace()
            raise
        games += body["currentPageResults"]

        if body["nextPage"]:
            page += 1
        else:
            break

    return games

def get_color(game, user):
    # Anonymous players don't get userId
    if not "userId" in game["players"][WHITE]:
        return BLACK
    if game["players"][WHITE]["userId"] == user:
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
    user = "llimllib"
    fname = "{user}.json".format(**locals())
    if os.path.isfile(fname):
        games = json.load(open(fname))
    else:
        games = get_all_games(user)
        json.dump(games, open(fname, 'w'))

    root = build_tree(filter_games(games), user)

    d3tree = d3_format(root)
    d3tree["username"] = user

    json.dump(d3tree, open("test_tree.json", 'w'), indent=2)
