OFFLINE = 'Offline'
ONLINE = 'Online'
PLAYING = 'Playing'

PLAYER_STATUS_DEFAULT = OFFLINE
PLAYER_STATUS = (
    (OFFLINE, OFFLINE),
    (ONLINE, ONLINE),
    (PLAYING, PLAYING)
)

UNRANKED = 'UNRANKED'
BRONZE = 'BRONZE'
SILVER = 'SILVER'
GOLD = 'GOLD'
PLATINIUM = 'PLATINIUM'
DIAMOND = 'DIAMOND'
ELITE = 'ELITE'
CHAMPION = 'CHAMPION'
UNREAL = 'UNREAL'

PLAYER_RANKS_DEFAULT = UNRANKED
PLAYER_RANKS = (
    (UNRANKED, UNRANKED),
    (BRONZE, BRONZE),
    (SILVER, SILVER),
    (GOLD, GOLD),
    (PLATINIUM, PLATINIUM),
    (DIAMOND, DIAMOND),
    (ELITE, ELITE),
    (CHAMPION, CHAMPION),
    (UNREAL, UNREAL)
)


def needed_length(input_tuple):
    longest_item = ""
    max_length = 0
    for item in input_tuple:
        if len(str(item)) > max_length:
            longest_item = item
            max_length = len(str(item))
    return max_length