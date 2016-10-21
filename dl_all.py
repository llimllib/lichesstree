from dl import get_all_games, get_games_until, get_timestamp
import json
from os import mkdir
from os.path import isfile, isdir
import sys

def w(s):
    return
    sys.stdout.write(s)
    sys.stdout.flush()

users = {'prune2000', 'ChemicalMagician', 'endrawes0', 'spotless_mind',
        'jshholland', 'dojagreen', 'Hyzer', 'mfink1', 'dose7781', 'Boviced',
        'Lake', 'theino', 'shafdanny', 'ghostult', 'JPTriton', 'jaivl',
        'Orgsalsa', 'super_sanic', 'Mooserohde', 'brianmcdonald', 'GnarlyGoat',
        'jacobhess', 'Aliquantus', 'mrrobot', 'Jimmyd7777', 'Jaivl',
        'Shammies', 'juldiaz280992', 'sturmwehr_45', 'chesswithamir',
        'Prune2000', 'shetoo', 'Sonata2', 'Krzem', 'narud', 'brainkim',
        'Seb32', 'explodingllama', 'Jivey', 'cactus', 'LaurentiuI', 'cyanfish',
        'nubnub57', 'infested', 'n4zgul', 'gandalf013', 'Ambite',
        'foulmouthmatt', 'sigvei', 'revoof', 'king_me_wing', 'JuanSnow',
        'Cynosure', 'NonMasterAlex', 'crabbypat', 'stoy', 'Tephra', 'Revoof',
        'Pasternak', 'greg-butts', 'aeilnrst', 'Immortality', 'Practicedave',
        'Linail', 'festivus', 'Ghostologist', 'Greg-butts', 'egocrusher',
        'adamroyd', 'somethingpretentious', 'jagvillspelaschack', 'eljefe08',
        'redhoax', 'OldTom', 'johnhammer1456', 'crackhorse', 'heidman',
        'amacy', 'ecstaticbroccoli', 'mooserohde', 'SirDore', 'Unihedron',
        'kirschwasser', 'Deerack', 'carbon752', 'modakshantanu',
        'daveyjones01', 'CarlosMagnussen', 'ImRealBadAtChess', 'kevban',
        'mhavgar', 'beeeeck', 'Freefal', 'happy0', 'VinMyStBorn', 'krischan',
        'tylerc0816', 'Knoddel', 'dakillian', 'fradtheimpaler', 'harrison2',
        'Methyl_Diammine', 'Toddle', 'Questoguy', 'DiscoverChex', 'dkillian',
        'tnan123', 'TheKnug', 'canofcoolhwip', 'plasmacat', 'Elbegelbe',
        'ForkerofQueens', 'mkoga', 'EsolcNeveton', 'RuizBR', 'droodjerky',
        'elwood_', 'chill5555', 'AdrianChessNow', 'HoxHound', 'nik0tine',
        'Hkivrak', 'ebb1', 'hillrp', 'Arensma', 'darksquaregames', 'steiger07',
        'soldadofiel', 'Thetasquared', 'CarbyPls', 'sangan', 'Buaco',
        'Transit', 'joecupojoe', 'GreyHawk', 'MRSep', 'Forhavu', 'arlberg',
        'scottm91', 'jughandle10', 'Frogger', 'Plawo', 'Cheesehead04',
        'BamaBeeblebrox', 'fourtwenty', 'saschlars', 'oldtom', 'djcrisce',
        'DurchNachtUndWind', 'dmitri31', 'kevinlara', 'VicCoren',
        'Soldadofiel', 'krzem', 'osskjc', 'andyquibler', 'Nubas', 'agrav123',
        'R-Mena', 'elixr', 'outerheaven92', 'Braffin', 'hakonj', 'Steiger07',
        'bloodyfox', 'badplayer_cm', 'gnarlygoat', 'MrIan15', 'MorallyGray',
        'alexmdaniel', 'GMKajrakso', 'thephobia', 'Nebulas', 'FradtheImpaler',
        'quirked', 'Lord_Karamat', 'Sigvei', 'BButch', 'jivey', 'Toperoco',
        'jmcampbell', 'dctrip13', 'Atrophied', 'Chennis', 'green_bat',
        'ghostologist', 'kjfoster17', 'lukhas', 'Pawnprecaution', 'Shetoo',
        'likestal', 'jmaltby', 'flamehead', 'darobertson', 'hetraie',
        'metalpawn', 'crafty35a', 'AngBorxley', 'pawnsac101', 'isaypotato',
        'FelixNL', 'Kimaga', 'ArmasFoster', 'WhizNL', 'Toj', 'Anunzio',
        'MiZero', 'chesspastamasta', 'chad_russell', 'x_0', 'hairbeRt',
        'eamonmont', 'x73ar', 'Derked', 'llimllib', 'mbazylisk', 'HaakonGM',
        'mightydogg', 'barry_stipplebanger', 'Diamanthori', 'Domg', 'Flaneur',
        'grinnifwin', 'ChukoDiman', 'wpruitt14', 'Pitrinu', 'ohorla',
        'PancakeMistakes', 'OuterHeaven92', 'josbri', 'bramminator',
        'jdpeters', 'Cachaulo', 'freefal', 'Tom_kg', 'tworivers',
        'MrLegilimens', 's2004k1993', 'Philgood84', 'carc', 'GM1224',
        'rwill128', 'Dialh', 'Doganof', 'iedopadzert', 'DannyKong', 'Eeevk',
        'gambytes', 'microda', 'cynosure', 'Hewkn', 'Matuiss2',
        'abdelaziz_sayed', 'azuaga', 'jakobks', 'TingelTangel10', 'Mamba1988',
        'solaroar', 'bpgbcg', 'nubas', 'Thshupe', 'Pawnpunter', 'iebrian',
        'highphive', 'pjh2sw', 'CaptNCarter', 'angborxley', 'nitin123', 'OrgSalsa',
        'neo_yahtzee', 'vishysoisse', 'scarff', 'resonantpillow', 'jimmyd7777',
        'ImBadGoEasy', 'eljello', 'linail', 'Jyr', 'dooje', 'tothe6thpower',
        'dangerously_average', 'nacional100', 'Elixr', 'AshkanJah', 'kingscrusher-fan',
        'Bloodyfox', 'Felixnl', 'Brianmcdonald', 'Josh789', 'ctorh', 'Aprentice1',
        'Kobol', 'Festivus', 'Notvassil', 'dearprudence', 'riemannn', 'ihateRBF',
        'kimaga', 'r-mena', 'DefinitelyNotAlekhsi', 'ca7alyst81', 'olu_dara',
        'Machrineith', 'brwnbr', 'elbegelbe', 'Icendoan', 'lakinwecker', 'seende',
        'Sjaart', 'p_implies_q', 'RookMassacre1851', 'Narud', 'Microda', 'dgees',
        'Cactus', 'SuperVJ', 'Petruchio', 'ventricule'}

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
