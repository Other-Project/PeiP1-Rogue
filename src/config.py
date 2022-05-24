from Equipment import Equipment
from Monster import Monster
from Weapon import Weapon
from Ghost import Ghost
from Potion import Potion
from Amulette import Amulette
from Armor import Armor


##################
#     Usages     #
##################

def heal(creature, hpGain=3):
    creature.hp = min(creature.hp + hpGain, creature.healthMax)
    return True


def eat(hero, satietyGain=2):
    hero.satiety = min(hero.satiety + satietyGain, hero.satietyMax)
    return True


def manaPotion(hero, manaGain=2):
    hero.mana = min(hero.mana + manaGain, hero.manaMax)
    return True


def teleport(creature, unique = False):
    from utils import theGame
    floor = theGame().floor
    newC = floor.randEmptyCoord()
    c = floor.pos(creature)
    floor.rm(c)
    floor.put(newC, creature)
    return unique

def FireBall(creature):
    from utils import theGame

    for i in theGame().floor._elem:
        for monster in i:
            if isinstance(monster, Monster) and creature.distance(monster) <= 2:
                creature.attack(monster, 3)



##################
#     Config     #
##################

equipments = {
    0: [
        Equipment("food", "f", lambda item, hero: eat(hero), image="assets/food/chunk.png"),
        Equipment("manaPotion", "!", lambda item, hero: manaPotion(hero), image="assets/other/mana.png")
    ],
    1: [
        Weapon("sword", radius=0, damage=2, image="assets/hero equipment/sword/sword1.png"),
        Amulette("Amulette of strength", image="assets/hero equipment/amulet/strength.png", type="strength"),
        Amulette("Amulette of xp", image="assets/hero equipment/amulet/xp.png", type="xp"),
        Armor("shield", resistance=1, image="assets/hero equipment/shield/shield.png"),
        Potion("potion", "!", lambda item, hero: heal(hero), image="assets/potion/potionHeal.png", price = 1),
        Potion("potion", "!", lambda item, hero: teleport(hero, True), image="assets/potion/potionTeleportation.png", price = 1)
    ],
    2: [
        Weapon("bow", radius=3, image="assets/hero equipment/bow/bow1.0.png"),
        Equipment("chainmail", image="assets/hero equipment/armor/armor1.png")
    ],
    3: [
        Potion("portoloin", "w", lambda item, hero: teleport(hero, False), image="assets/potion/potionPortoloin.png", price = 3),
        Potion("FireBall", "§", lambda item, hero, monster: FireBall(hero), image="assets/potion/potionPortoloin.png", price=4)

    ]
}

monsters = {
    0: [
        Monster("Archer", 1, "A", radius=4, image="assets/monsters/archer.png"),
        Monster("Bat", 2, "W", movingSpeed=2, image="assets/monsters/bat.png"),
        Monster("Goblin", 4, xpGain=2, image="assets/monsters/goblin.png"),
        Ghost("Ghost", 5, xpGain=3)
    ],
    1: [
        Monster("Ork", 6, strength=2, xpGain=3, image="assets/monsters/orc.png"),
        Monster("Blob", 10, xpGain=4, image="assets/monsters/blob.png")
    ],
    5: [
        Monster("Dragon", 20, strength=3, xpGain=10, image="assets/monsters/dragon.png")
    ]
}
