from Equipment import Equipment
from Monster import Monster
from Weapon import Weapon


##################
#     Usages     #
##################

def heal(creature):
    creature.hp += 3
    return True


def teleport(creature, unique):
    from utils import theGame
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
        Weapon("sword", radius=1, damage=2),
        Weapon("bow", radius=3),
        Equipment("potion", "!", lambda item, hero: heal(hero))
    ],
    1: [
        Equipment("potion", "!", lambda item, hero: teleport(hero, True))
    ],
    2: [
        Equipment("chainmail")
    ],
    3: [
        Equipment("portoloin", "w", lambda item, hero: teleport(hero, False))
    ]
}

monsters = {
    0: [Monster("Goblin", 4), Monster("Bat", 2, "W")],
    1: [Monster("Ork", 6, strength=2), Monster("Blob", 10)],
    5: [Monster("Dragon", 20, strength=3)]
}
