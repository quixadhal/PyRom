import random
import logging

logger = logging.getLogger()

import merc
import interp
import handler_game


# All the posing stuff.
pose_table = {
    'to_ch': {
        'mage': (
            "You sizzle with energy.",
            "You turn into a butterfly, then return to your normal shape.",
            "Blue sparks fly from your fingers.",
            "Little red lights dance in your eyes.",
            "A slimy green monster appears before you and bows.",
            "You turn everybody into a little pink elephant.",
            "A small ball of light dances on your fingertips.",
            "Smoke and fumes leak from your nostrils.",
            "The light flickers as you rap in magical languages.",
            "Your head disappears.",
            "A fire elemental singes your hair.",
            "The sky changes color to match your eyes.",
            "The stones dance to your command.",
            "The heavens and grass change colour as you smile.",
            "Everyone's clothes are transparent, and you are laughing.",
            "A black hole swallows you.",
            "The world shimmers in time with your whistling.",
        ),
        'cleric': (
            "You feel very holy.",
            "You nonchalantly turn wine into water.",
            "A halo appears over your head.",
            "You recite words of wisdom.",
            "Deep in prayer, you levitate.",
            "An angel consults you.",
            "Your body glows with an unearthly light.",
            "A spot light hits you.",
            "Everyone levitates as you pray.",
            "A cool breeze refreshes you.",
            "The sun pierces through the clouds to illuminate you.",
            "The ocean parts before you.",
            "A thunder cloud kneels to you.",
            "The Burning Man speaks to you.",
            "An eye in a pyramid winks at you.",
            "Valentine Michael Smith offers you a glass of water.",
            "The great god Mota gives you a staff.",
        ),
        'thief': (
            "You perform a small card trick.",
            "You wiggle your ears alternately.",
            "You nimbly tie yourself into a knot.",
            "You juggle with daggers, apples, and eyeballs.",
            "You steal the underwear off every person in the room.",
            "The dice roll ... and you win again.",
            "You count the money in everyone's pockets.",
            "You balance a pocket knife on your tongue.",
            "You produce a coin from everyone's ear.",
            "You step behind your shadow.",
            "Your eyes dance with greed.",
            "You deftly steal everyone's weapon.",
            "The Grey Mouser buys you a beer.",
            "Everyone's pocket explodes with your fireworks.",
            "Everyone discovers your dagger a centimeter from their eye.",
            "Where did you go?",
            "Click.",
        ),
        'warrior': (
            "You show your bulging muscles.",
            "You crack nuts between your fingers.",
            "You grizzle your teeth and look mean.",
            "You hit your head, and your eyes roll.",
            "Crunch, crunch -- you munch a bottle.",
            "... 98, 99, 100 ... you do pushups.",
            "Arnold Schwarzenegger admires your physique.",
            "Watch your feet, you are juggling granite boulders.",
            "Oomph!  You squeeze water out of a granite boulder.",
            "You pick your teeth with a spear.",
            "Everyone is swept off their foot by your hug.",
            "Your karate chop splits a tree.",
            "A strap of your armor breaks over your mighty thews.",
            "A boulder cracks at your frown.",
            "Mercenaries arrive to do your bidding.",
            "Four matched Percherons bring in your chariot.",
            "Atlas asks you to relieve him.",
        ),
    },
    'to_others': {
        'mage': (
            "$n sizzles with energy.",
            "$n turns into a butterfly, then returns to $s normal shape.",
            "Blue sparks fly from $n's fingers.",
            "Little red lights dance in $n's eyes.",
            "A slimy green monster appears before $n and bows.",
            "You are turned into a little pink elephant by $n.",
            "A small ball of light dances on $n's fingertips.",
            "Smoke and fumes leak from $n's nostrils.",
            "The light flickers as $n raps in magical languages.",
            "$n's head disappears.",
            "A fire elemental singes $n's hair.",
            "The sky changes color to match $n's eyes.",
            "The stones dance to $n's command.",
            "The heavens and grass change colour as $n smiles.",
            "Your clothes are transparent, and $n is laughing.",
            "A black hole swallows $n.",
            "The world shimmers in time with $n's whistling.",
        ),
        'cleric': (
            "$n looks very holy.",
            "$n nonchalantly turns wine into water.",
            "A halo appears over $n's head.",
            "$n recites words of wisdom.",
            "Deep in prayer, $n levitates.",
            "An angel consults $n.",
            "$n's body glows with an unearthly light.",
            "A spot light hits $n.",
            "You levitate as $n prays.",
            "A cool breeze refreshes $n.",
            "The sun pierces through the clouds to illuminate $n.",
            "The ocean parts before $n.",
            "A thunder cloud kneels to $n.",
            "The Burning Man speaks to $n.",
            "An eye in a pyramid winks at $n.",
            "Valentine Michael Smith offers $n a glass of water.",
            "The great god Mota gives $n a staff.",
        ),
        'thief': (
            "$n performs a small card trick.",
            "$n wiggles $s ears alternately.",
            "$n nimbly ties $mself into a knot.",
            "$n juggles with daggers, apples, and eyeballs.",
            "Your underwear is gone!  $n stole it!",
            "The dice roll ... and $n wins again.",
            "Check your money, $n is counting it.",
            "$n balances a pocket knife on your tongue.",
            "$n produces a coin from your ear.",
            "$n steps behind $s shadow.",
            "$n's eyes dance with greed.",
            "$n deftly steals your weapon.",
            "The Grey Mouser buys $n a beer.",
            "Your pocket explodes with $n's fireworks.",
            "You discover $n's dagger a centimeter from your eye.",
            "Where did $n go?",
            "Click.",
        ),
        'warrior': (
            "$n shows $s bulging muscles.",
            "$n cracks nuts between $s fingers.",
            "$n grizzles $s teeth and looks mean.",
            "$n hits $s head, and $s eyes roll.",
            "Crunch, crunch -- $n munches a bottle.",
            "... 98, 99, 100 ... $n does pushups.",
            "Arnold Schwarzenegger admires $n's physique.",
            "Watch your feet, $n is juggling granite boulders.",
            "Oomph!  $n squeezes water out of a granite boulder.",
            "$n picks $s teeth with a spear.",
            "You are swept off your feet by $n's hug.",
            "$n's karate chop splits a tree.",
            "A strap of $n's armor breaks over $s mighty thews.",
            "A boulder cracks at $n's frown.",
            "Mercenaries arrive to do $n's bidding.",
            "Four matched Percherons bring in $n's chariot.",
            "Atlas asks $n to relieve him.",
        ),
    },
}


def do_pose(ch, argument):
    if ch.is_npc():
        return
    band = merc.LEVEL_HERO // len(pose_table['to_ch'][ch.guild.name])
    level = min(ch.level, merc.LEVEL_HERO) // band
    choice = random.randint(0, level)

    handler_game.act(pose_table['to_ch'][ch.guild.name][choice], ch, None, None, merc.TO_CHAR)
    handler_game.act(pose_table['to_others'][ch.guild.name][choice], ch, None, None, merc.TO_ROOM)
    return


interp.register_command(interp.cmd_type('pose', do_pose, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
