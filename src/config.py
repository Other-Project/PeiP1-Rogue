from Item import Item
from Monster import Monster
from Weapon import Weapon
from Ghost import Ghost
from Amulet import Amulet
from Armor import Armor
from Hero import Hero
from utils import theGame
from Potion import Potion


##################
#     Usages     #
##################

def heal(creature, hpGain=3):
    creature.hp = min(creature.hp + hpGain, creature.healthMax)
    return True


def eat(hero, satietyGain=2):
    hero.satiety = min(hero.satiety + satietyGain, hero.satietyMax)
    theGame().newTurn()
    return True


def manaPotion(hero, manaGain=1):
    if hero.mana < hero.manaMax:
        hero.mana = min(hero.mana + manaGain, hero.manaMax)
        return True
    else:
        theGame().addMessage("Your inventory is already full")
        return False


def teleport(creature):
    floor = theGame().floor
    newC = floor.randEmptyCoord()
    c = floor.pos(creature)
    floor.rm(c)
    floor.put(newC, creature)
    return False


def fireBall(creature: Hero):
    import utils
    for monster in theGame().floor.getAllCreaturesInRadius(creature, 3, Monster):
        theGame().floor.rm(theGame().floor.pos(monster))
        utils.theGame().addMessage("The " + monster.name + " has been fatally wounded by the spell.")


##################
#     Config     #
##################

potions = [
    Potion("teleport", usage=lambda item, hero: teleport(hero), image="assets/potions/potionTeleportation.png", price=5),
    Potion("heal", usage=lambda item, hero: heal(hero), image="assets/potions/potionHeal.png", price=6),
    Potion("range attack", usage=lambda item, hero: fireBall(hero), image="assets/potions/fireball.png", price=9)
]

equipments = {
    0: [
        Item("food", usage=lambda item, hero: eat(hero), image="assets/foods/chunk.png", desc="+2 satiety"),
        Item("mana orb", usage=lambda item, hero: manaPotion(hero), image="assets/items/mana.png", desc="+1 mana"),
        Weapon("bow", radius=3, damage=2, image="assets/equipments/bow/bow1.0.png"),
    ],
    1: [
        Weapon("sword", radius=0, damage=2, image="assets/equipments/sword/sword1.png"),
        Weapon("bow", radius=3, damage=2, image="assets/equipments/bow/bow1.0.png"),
        Armor("shield", resistance=1, armorType="shield", image="assets/equipments/shield/shield1.png"),
        Armor("helmet", resistance=1, armorType="helmet", image="assets/equipments/helmet/helmet1.png"),
        Armor("chainmail", resistance=1, armorType="chestplate", image="assets/equipments/armor/armor1.png"),
        Armor("Legs", resistance=1, armorType="legs", image="assets/equipments/leg/leg1.png"),
        Armor("boots", resistance=1, armorType="boots", image="assets/equipments/boot/boot1.png"),
    ],
    2: [
        Armor("shield", resistance=2, armorType="shield", image="assets/equipments/shield/shield2.png"),
        Armor("helmet", resistance=2, armorType="helmet", image="assets/equipments/helmet/helmet3.png"),
        Armor("chainmail", resistance=2, armorType="chestplate", image="assets/equipments/armor/armor3.png"),
        Armor("Legs", resistance=2, armorType="legs", image="assets/equipments/leg/leg2.png"),
        Armor("boots", resistance=2, armorType="boots", image="assets/equipments/boot/boot3.png"),
        Weapon("sword", radius=0, damage=3, image="assets/equipments/sword/sword2.png"),
        Weapon("bow", radius=3, damage=3, image="assets/equipments/bow/bow1.0.png"),
        Amulet("amulet of strength", image="assets/equipments/amulet/strength.png", effectType="strength"),
    ],
    3: [
        Weapon("sword", radius=0, damage=4, image="assets/equipments/sword/sword3.png"),
        Weapon("bow", radius=4, damage=4, image="assets/equipments/bow/bow1.0.png"),
        Amulet("amulet of xp", image="assets/equipments/amulet/xp.png", effectType="xp"),
        Item("food", usage=lambda item, hero: eat(hero), image="assets/foods/chunk.png", desc="+2 satiety")
    ]
}

monsters = {
    0: [
        Monster("Archer", 1, radius=2, image="assets/monsters/archer.png"),
        Monster("Bat", 2, movingSpeed=2, image="assets/monsters/bat.png"),
        Monster("Goblin", 4, xpGain=2, image="assets/monsters/goblin.png"),
        Ghost("Ghost", 5, xpGain=3, image="assets/monsters/ghost.png")
    ],
    1: [
        Monster("Ork", 6, strength=2, xpGain=3, image="assets/monsters/orc.png"),
        Monster("Blob", 10, xpGain=4, image="assets/monsters/blob.png")
    ],
    5: [
        Monster("Dragon", 20, strength=3, xpGain=10, image="assets/monsters/dragon.png")
    ]
}
