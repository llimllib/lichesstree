from os import mkdir
from os.path import isfile, isdir
from dl import build_tree, filter_games, d3_format
import json

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
