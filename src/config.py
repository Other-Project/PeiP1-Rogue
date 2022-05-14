from Equipment import Equipment
from Monster import Monster
from Weapon import Weapon
import pygame

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
        Equipment("gold", "o", image=pygame.image.load("assets/other/cursor.png")),
        Weapon("sword", radius=1, damage=2, image=pygame.image.load("assets/hero equipment/sword/sword1.png")),
        Weapon("bow", radius=3, image=pygame.image.load("assets/hero equipment/bow/bow1.0.png")),
        Equipment("potion", "!", lambda item, hero: heal(hero), image=pygame.image.load("assets/potion/potionHeal.png"))
    ],
    1: [
        Equipment("potion", "!", lambda item, hero: teleport(hero, True), image=pygame.image.load("assets/potion/potionTeleportation.png"))
    ],
    2: [
        Equipment("chainmail", image=pygame.image.load("assets/hero equipment/armor/armor1.png"))
    ],
    3: [
        Equipment("portoloin", "w", lambda item, hero: teleport(hero, False), image=pygame.image.load("assets/potion/potionPortoloin.png"))
    ]
}

monsters = {
    0: [Monster("Goblin", 4, image=pygame.image.load("assets/monsters/skeleton/skeleton.png")),
        Monster("Bat", 2, "W", image=pygame.image.load("assets/other/chest.png"))],
    1: [Monster("Ork", 6, strength=2, image=pygame.image.load("assets/other/fontaine.png")),
        Monster("Blob", 10, image=pygame.image.load("assets/other/cursor.png"))],
    5: [Monster("Dragon", 20, strength=3, image=pygame.image.load("assets/other/tile.png"))]
}
