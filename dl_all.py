from dl import get_all_games, get_games_until
import json
from os import mkdir
from os.path import isfile, isdir
import sys

def w(s):
    sys.stdout.write(s)
    sys.stdout.flush()

users = [
  "andyquibler", "Pawnprecaution", "Atrophied", "Pitrinu", "Shammies",
  "Matuiss2", "SuperVJ", "cyanfish", "Sonata2", "Sjaart", "crabbypat",
  "Hyzer", "Bloodyfox", "Jyr", "Steiger07", "theino", "ecstaticbroccoli",
  "mhavgar", "sangan", "Toddle", "eamonmont", "Kobol", "resonantpillow",
  "gnarlygoat", "Doganof", "Pasternak", "ventricule", "Toperoco",
  "elwood_", "kimaga", "brwnbr", "somethingpretentious", "Questoguy",
  "DannyKong", "Practicedave", "jughandle10", "ihateRBF", "MorallyGray",
  "Cynosure", "HoxHound", "R-Mena", "CaptNCarter", "dgees", "Knoddel",
  "droodjerky", "Felixnl", "quirked", "Toj", "metalpawn", "JPTriton",
  "Jimmyd7777", "flamehead", "modakshantanu", "super_sanic", "vishysoisse",
  "llimllib", "NonMasterAlex", "jaivl", "AshkanJah", "ForkerofQueens",
  "shetoo", "arlberg", "MrIan15", "krzem", "Revoof", "kingscrusher-fan",
  "jmaltby", "Orgsalsa", "ebb1", "riemannn", "redhoax", "MrLegilimens",
  "Diamanthori", "juldiaz280992", "DurchNachtUndWind", "Unihedron",
  "Philgood84", "Tom_kg", "alexmdaniel", "linail", "iedopadzert", "mkoga",
  "egocrusher", "scarff", "MRSep", "tylerc0816", "scottm91", "ctorh",
  "iebrian", "jagvillspelaschack", "RuizBR", "Anunzio", "EsolcNeveton",
  "sigvei", "bramminator", "explodingllama", "Cheesehead04", "mfink1",
  "infested", "narud", "kirschwasser", "dooje", "Nubas", "nacional100",
  "CarlosMagnussen", "GreyHawk", "n4zgul", "jivey", "shafdanny", "ca7alyst81",
  "BamaBeeblebrox", "djcrisce", "Prune2000", "DiscoverChex", "jshholland",
  "hillrp", "lukhas", "agrav123", "lakinwecker", "jacobhess", "tnan123",
  "daveyjones01", "Seb32", "osskjc", "mbazylisk", "thephobia", "Braffin",
  "darobertson", "Mooserohde", "rwill128", "saschlars", "festivus",
  "greg-butts", "amacy", "stoy", "Immortality", "ghostologist", "JuanSnow",
  "abdelaziz_sayed", "angborxley", "Petruchio", "adamroyd", "eljefe08",
  "Pawnpunter", "Hkivrak", "endrawes0", "OldTom", "Elixr", "Thetasquared",
  "TheKnug", "SirDore", "tworivers", "ChukoDiman", "FradtheImpaler",
  "tothe6thpower", "Dialh", "GMKajrakso", "Frogger", "Thshupe", "Flaneur",
  "sturmwehr_45", "badplayer_cm", "azuaga", "outerheaven92", "Brianmcdonald",
  "mrrobot", "microda", "crafty35a", "outerheaven92", "Eeevk", "soldadofiel",
  "HaakonGM", "likestal", "Machrineith", "WhizNL", "cactus", "harrison2",
  "isaypotato", "Plawo", "AdrianChessNow", "olu_dara", "Boviced", "elbegelbe",
  "solaroar", "hakonj", "saschlars", "Cachaulo", "chad_russell", "nubnub57",
  "ArmasFoster", "Hewkn", "fourtwenty", "ghostult", "pjh2sw", "nik0tine",
  "dojagreen", "eljefe08", "kevinlara", "nitin123",
]

for user in users:
    dirname = "../lichess-user-data/user/{user}".format(**locals())
    if not isdir(dirname):
        mkdir(dirname)

    fname = "{dirname}/{user}_games.json".format(**locals())
    if not isfile(fname):
        w("\ngetting {user}: ".format(**locals()))
        games = get_all_games(user)
        json.dump(games, open(fname, 'w'))
    else:
        with open(fname) as f:
            games = json.load(f)

        t = games[0]["timestamp"]
        w("\nupdating {user}: ".format(**locals()))

        # make sure to prepend so we maintain the games ordered by date
        new_games = get_games_until(user, games[0]["id"], t)
        updated_games = new_games + games

        with open(fname, 'w') as f:
            json.dump(updated_games, f)

    w("\n")
