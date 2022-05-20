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
        Weapon("sword", radius=0, damage=2, image="assets/hero equipment/sword/sword1.png"),
        Weapon("bow", radius=3, image="assets/hero equipment/bow/bow1.0.png"),
        Equipment("potion", "!", lambda item, hero: heal(hero), image="assets/potion/potionHeal.png")
    ],
    1: [
        Equipment("potion", "!", lambda item, hero: teleport(hero, True), image="assets/potion/potionTeleportation.png")
    ],
    2: [
        Equipment("chainmail", image="assets/hero equipment/armor/armor1.png")
    ],
    3: [
        Equipment("portoloin", "w", lambda item, hero: teleport(hero, False), image="assets/potion/potionPortoloin.png")
    ]
}

monsters = {
    0: [
        Monster("Goblin", 4, image="assets/monsters/skeleton/skeleton.png"),
        Monster("Bat", 2, "W", image="assets/other/chest.png"),
        Monster("Archer", 1, "A", range=4, image="assets/hero equipment/bow/bow1.0.png")
    ],
    1: [
        Monster("Ork", 6, strength=2, image="assets/other/fountain.png"),
        Monster("Blob", 10, image="assets/other/cursor.png")
    ],
    5: [
        Monster("Dragon", 20, strength=3, image="assets/other/tile.png")
    ]
}
