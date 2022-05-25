import utils
from Item import Item
from Monster import Monster
from Weapon import Weapon
from Ghost import Ghost
from Amulet import Amulet
from Armor import Armor
from Hero import Hero


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


def fireBall(creature: Hero):
    from utils import theGame
    for m in floor.getAllCreaturesInRadius(creature, 6, creature.enemyType):
        if m.meet(creature):
            theGame().floor.rm(floor.pos(m))


##################
#     Config     #
##################

equipments = {
    0: [
        Item("food", "f", lambda item, hero: eat(hero), image="assets/food/chunk.png"),
        Item("manaPotion", "!", lambda item, hero: manaPotion(hero), image="assets/other/mana.png"),
    ],
    1: [
        Weapon("sword", radius=0, damage=2, image="assets/hero equipment/sword/sword1.png"),
        Weapon("bow", radius=3, damage=2, image="assets/hero equipment/bow/bow1.0.png"),
        Armor("shield", resistance=1, armorType="shield", image="assets/hero equipment/shield/shield1.png"),
        Armor("helmet", resistance=1, armorType="helmet", image="assets/hero equipment/helmet/helmet1.png"),
        Armor("chainmail", resistance=1, armorType="chestplate", image="assets/hero equipment/armor/armor1.png"),
        Armor("Legs", resistance=1, armorType="legs", image="assets/hero equipment/leg/leg1.png"),
        Armor("boots", resistance=1, armorType="boots", image="assets/hero equipment/boot/boot1.png"),
    ],
    2: [
        Armor("shield", resistance=2, armorType="shield", image="assets/hero equipment/shield/shield2.png"),
        Armor("helmet", resistance=2, armorType="helmet", image="assets/hero equipment/helmet/helmet3.png"),
        Armor("chainmail", resistance=2, armorType="chestplate", image="assets/hero equipment/armor/armor3.png"),
        Armor("Legs", resistance=2, armorType="legs", image="assets/hero equipment/leg/leg2.png"),
        Armor("boots", resistance=2, armorType="boots", image="assets/hero equipment/boot/boot3.png"),
        Weapon("sword", radius=0, damage=3, image="assets/hero equipment/sword/sword2.png"),
        Weapon("bow", radius=3, damage=3, image="assets/hero equipment/bow/bow1.0.png"),
        Amulet("Amulette of strength", image="assets/hero equipment/amulet/strength.png", type="strength"),
    ],
    3: [
        Weapon("sword", radius=0, damage=4, image="assets/hero equipment/sword/sword3.png"),
        Weapon("bow", radius=4, damage=4, image="assets/hero equipment/bow/bow1.0.png"),
        Amulet("Amulette of xp", image="assets/hero equipment/amulet/xp.png", type="xp"),
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
