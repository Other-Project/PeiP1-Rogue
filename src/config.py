from Item import Item
from Monster import Monster
from Weapon import Weapon
from Ghost import Ghost
from Amulet import Amulet
from Armor import Armor
from Hero import Hero
from utils import theGame
from Potion import Potion
from Spider import Spider
import utils


##################
#     Usages     #
##################

def heal(hero: Hero, hpGain=3):
    hero.hp = min(hero.hp + hpGain, hero.healthMax)
    theGame().addMessage("The hero cured himself")
    return True


def eat(hero: Hero, satietyGain=2):
    hero.satiety = min(hero.satiety + satietyGain, hero.satietyMax)
    theGame().newTurn()
    return True


def manaPotion(hero: Hero, manaGain=1):
    if hero.mana < hero.manaMax:
        hero.mana = min(hero.mana + manaGain, hero.manaMax)
        return True
    else:
        theGame().addMessage("Your inventory is already full")
        return False


def teleport(hero: Hero):
    floor = theGame().floor
    newC = floor.randEmptyCoord()
    c = floor.pos(hero)
    floor.rm(c)
    floor.put(newC, hero)
    utils.theGame().addMessage(" The hero has been teleported")
    return False


def zap(hero: Hero):
    for monster in theGame().floor.getAllCreaturesInRadius(hero, 3, Monster):
        monster.hp -= 3
        utils.theGame().addMessage("The " + monster.name + " has loss 3 hp")
        utils.theGame().newTurn()


def invincible():
    utils.theGame().hero.invincible=10
    utils.theGame().newTurn()



def invisible():
    utils.theGame().hero.invisible = 10
    utils.theGame().hero.image = "assets/hero/invisibleHero.png"
    utils.theGame().newTurn()


##################
#     Config     #
##################

potions = [
    Potion("invisible", usage=lambda item, hero: invisible(), image="assets/hero/invisibleHero.png", price=5),
    Potion("teleport", usage=lambda item, hero: teleport(hero), image="assets/potions/potionTeleportation.png", price=5),
    Potion("heal", usage=lambda item, hero: heal(hero), image="assets/potions/potionHeal.png", price=6),
    Potion("zap", usage=lambda item, hero: zap(hero), image="assets/potions/zap.png", price=8),
    Potion("invincible", usage=lambda item, hero: invincible(), image="assets/potions/invincible.png", price=9)

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
        Item(name="gold", image="assets/items/gold_dragon_hide.png")
    ],
    3: [
        Weapon("sword", radius=0, damage=4, image="assets/equipments/sword/sword3.png"),
        Weapon("bow", radius=4, damage=0, radiusDamage=4, image="assets/equipments/bow/bow1.0.png"),
        Amulet("amulet of xp", image="assets/equipments/amulet/xp.png", effectType="xp"),
        Item("food", usage=lambda item, hero: eat(hero), image="assets/foods/chunk.png", desc="+2 satiety")
    ]
}

monsters = {
    0: [
        Spider("Spider", 1, movingSpeed=2, xpGain=3, image="assets/monsters/spider.png"),
        Spider("Spider", 1, movingSpeed=2, xpGain=3, image="assets/monsters/spider.png"),
        Spider("Spider", 1, movingSpeed=2, xpGain=3, image="assets/monsters/spider.png"),
        Spider("Spider", 1, movingSpeed=2, xpGain=3, image="assets/monsters/spider.png"),
        Spider("Spider", 1, movingSpeed=2, xpGain=3, image="assets/monsters/spider.png"),
        Spider("Spider", 1, movingSpeed=2, xpGain=3, image="assets/monsters/spider.png"),

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
