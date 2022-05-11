from Equipment import Equipment
from Creature import Creature
import Game


##################
#   Utilities    #
##################

def getch():
    """Single char input, only works on Mac/Linux/Windows OS terminals"""
    try:
        import termios
        # POSIX system. Create and return a getch that manipulates the tty.
        import sys
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch().decode('utf-8')


##################
#     Usages     #
##################

def heal(creature):
    creature.hp += 3
    return True


def teleport(creature, unique):
    floor = theGame().floor
    newC = floor.randEmptyCoord()
    c = floor.pos(creature)
    floor.rm(c)
    floor.put(newC, creature)
    return unique


##################
#     Config     #
##################

equipments = {
    0: [
        Equipment("gold", "o"),
        Equipment("potion", "!", lambda item, hero: heal(hero))
    ],
    1: [
        Equipment("sword", usage=lambda item, hero: hero.__setattr__("strength", hero.strength + 1)),
        Equipment("bow"),
        Equipment("potion", "!", lambda item, hero: teleport(hero, True))
    ],
    2: [
        Equipment("chainmail", usage=lambda item, hero: hero.__setattr__("resistance", 2))
    ],
    3: [
        Equipment("portoloin", "w", lambda item, hero: teleport(hero, False))
    ]
}

monsters = {
    0: [Creature("Goblin", 4), Creature("Bat", 2, "W")],
    1: [Creature("Ork", 6, strength=2), Creature("Blob", 10)],
    5: [Creature("Dragon", 20, strength=3)]
}


##################
#     Launch     #
##################

def theGame(game=Game.Game()):
    return game


theGame().play()
