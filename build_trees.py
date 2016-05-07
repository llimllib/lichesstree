from os import mkdir
from os.path import isfile, isdir
from dl import build_tree, filter_games, d3_format
import json

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
    fname = "{dirname}/{user}_games.json".format(**locals())

    if isdir(dirname):
        games = json.load(open(fname))
    else:
        mkdir(dirname)

    games = json.load(open(fname))

    root = build_tree(filter_games(games), user)

    d3tree = d3_format(root)
    d3tree["username"] = user

    treef = "{dirname}/{user}_tree.json".format(**locals())
    json.dump(d3tree, open(treef, 'w'))
