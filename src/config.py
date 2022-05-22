from Equipment import Equipment
from Monster import Monster
from Weapon import Weapon
from Ghost import Ghost


##################
#     Usages     #
##################

def heal(creature):
    creature.hp = min(creature.hp+3, creature.healthMax)
    return True


def eat(hero):
    hero.satiety = min(hero.satiety + 5, hero.satietyMax)
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
        Equipment("food", "f", lambda item, hero: eat(hero), image="assets/food/chunk.png")
    ],
    1: [
        Weapon("sword", radius=0, damage=2, image="assets/hero equipment/sword/sword1.png"),
        Equipment("potion", "!", lambda item, hero: heal(hero), image="assets/potion/potionHeal.png"),
        Equipment("potion", "!", lambda item, hero: teleport(hero, True), image="assets/potion/potionTeleportation.png")
    ],
    2: [
        Weapon("bow", radius=3, image="assets/hero equipment/bow/bow1.0.png"),
        Equipment("chainmail", image="assets/hero equipment/armor/armor1.png")
    ],
    3: [
        Equipment("portoloin", "w", lambda item, hero: teleport(hero, False), image="assets/potion/potionPortoloin.png")
    ]
}

monsters = {
    0: [
        Monster("Goblin", 4, image="assets/monsters/goblin.png"),
        Monster("Bat", 2, "W", image="assets/monsters/bat.png", movingSpeed=2),
        Monster("Archer", 1, "A", radius=4, image="assets/monsters/archer.png"),
        Ghost("Ghost")
    ],
    1: [
        Monster("Ork", 6, strength=2, image="assets/monsters/orc.png"),
        Monster("Blob", 10, image="assets/monsters/blob.png")
    ],
    5: [
        Monster("Dragon", 20, strength=3, image="assets/monsters/dragon.png")
    ]
}
