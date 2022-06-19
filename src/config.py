from Item import Item
from Monster import Monster
from Weapon import Weapon
from Ghost import Ghost
from Amulet import Amulet
from Armor import Armor
from Hero import Hero
from Potion import Potion
from Spider import Spider
from RoomMonster import RoomMonster
from RoomShop import RoomShop
from RoomChest import RoomChest
from RoomBoss import RoomBoss
from RoomTrap import RoomTrap


##################
#     Usages     #
##################

def heal(hero: Hero, hpGain=4):
    from utils import theGame
    hero.hp = min(hero.hp + hpGain, hero.healthMax)
    theGame().addMessage("The hero cured himself")
    return True


def eat(hero: Hero, satietyGain=6):
    from utils import theGame
    hero.satiety = min(hero.satiety + satietyGain, hero.satietyMax)
    theGame().newTurn()
    return True


def manaPotion(hero: Hero, manaGain=1):
    if hero.mana < hero.manaMax:
        hero.mana = min(hero.mana + manaGain, hero.manaMax)
        return True
    else:
        from utils import theGame
        theGame().addMessage("Your inventory is already full")
        return False


def teleport(hero: Hero):
    import utils
    floor = utils.theGame().floor
    newC = floor.randEmptyCoord()
    c = floor.pos(hero)
    floor.rm(c)
    floor.put(newC, hero)
    utils.theGame().addMessage(" The hero has been teleported")
    return False


def zap(hero: Hero):
    import utils
    for monster in utils.theGame().floor.getAllCreaturesInRadius(hero, 3, Monster):
        monster.hp -= 3
        utils.theGame().addMessage("The " + monster.name + " has loss 3 hp")


def invincible(hero: Hero):
    hero.invincible = 10


def invisible(hero: Hero):
    hero.invisible = 6


def superStrength(hero: Hero):
    hero.superStrength = 5


##################
#     Config     #
##################

potions = [
    Potion("invisible", usage=lambda item, hero: invisible(hero), image="assets/potions/invisible.png", price=5),
    Potion("teleport", usage=lambda item, hero: teleport(hero), image="assets/potions/potionTeleportation.png", price=5),
    Potion("heal", usage=lambda item, hero: heal(hero), image="assets/potions/potionHeal.png", price=6),
    Potion("zap", usage=lambda item, hero: zap(hero), image="assets/potions/zap.png", price=8),
    Potion("invincible", usage=lambda item, hero: invincible(hero), image="assets/potions/invincible.png", price=9),
    Potion("stronger", usage=lambda item, hero: superStrength(hero), image="assets/potions/strength.png", price=9)
]

equipments = {
    0: [
        Item("food", usage=lambda item, hero: eat(hero), image="assets/foods/chunk.png", desc="+4 satiety", price=1),
        Item("mana orb", usage=lambda item, hero: manaPotion(hero), image="assets/items/mana.png", desc="+1 mana", price=1),
        Item(name="gold", image="assets/items/gold.png", desc="+1 gold", price=0),
    ],
    1: [
        Weapon("sword", radius=0, damage=5, image="assets/equipments/sword/sword1.png", price=4),
        Weapon("bow", radius=3, damage=0, radiusDamage=10, image="assets/equipments/bow/bow1.0.png", price=4),
        Armor("shield", resistance=1, armorType="shield", image="assets/equipments/shield/shield1.png", price=4),
        Armor("helmet", resistance=1, armorType="helmet", image="assets/equipments/helmet/helmet1.png", price=4),
        Armor("chainmail", resistance=1, armorType="chestplate", image="assets/equipments/armor/armor1.png", price=4),
        Armor("Legs", resistance=1, armorType="legs", image="assets/equipments/leg/leg1.png", price=4),
        Armor("boots", resistance=1, armorType="boots", image="assets/equipments/boot/boot1.png", price=4),
    ],
    4: [
        Armor("shield", resistance=2, armorType="shield", image="assets/equipments/shield/shield2.png", price=8),
        Armor("helmet", resistance=2, armorType="helmet", image="assets/equipments/helmet/helmet3.png", price=8),
        Armor("chainmail", resistance=2, armorType="chestplate", image="assets/equipments/armor/armor3.png", price=8),
        Armor("Legs", resistance=2, armorType="legs", image="assets/equipments/leg/leg2.png", price=8),
        Armor("boots", resistance=2, armorType="boots", image="assets/equipments/boot/boot3.png", price=8),
        Weapon("sword", radius=0, damage=10, image="assets/equipments/sword/sword2.png", price=8),
        Weapon("bow", radius=3, damage=0, radiusDamage=15, image="assets/equipments/bow/bow2.png", price=8),
        Amulet("amulet of strength", image="assets/equipments/amulet/strength.png", effectType="strength", price=8),

    ],
    8: [
        Weapon("sword", radius=0, damage=15, image="assets/equipments/sword/sword3.png", price=12),
        Weapon("bow", radius=4, damage=0, radiusDamage=20, image="assets/equipments/bow/bow3.png", price=12),
        Amulet("amulet of xp", image="assets/equipments/amulet/xp.png", effectType="xp", price=12),
    ]
}

monsters = {
    0: [
        Monster("Archer", 10, strength=1, radius=3, image="assets/monsters/archer.png"),
        Spider("Spider", 15, movingSpeed=2, xpGain=3, image="assets/monsters/spider.png"),
        Monster("Bat", 10, strength=1, movingSpeed=2, image="assets/monsters/bat.png"),
        Monster("Goblin", 20, xpGain=2, image="assets/monsters/goblin.png"),
        Ghost("Ghost", 20, xpGain=3, image="assets/monsters/ghost.png"),
    ],
    3: [
        Monster("Ork", 25, strength=2, xpGain=3, image="assets/monsters/orc.png"),
        Monster("Blob", 50, xpGain=4, image="assets/monsters/blob.png")
    ],
    6: [
        Monster("Dragon", 70, strength=3, xpGain=10, image="assets/monsters/dragon.png")
    ]
}

bosses = [
    Monster("Dragon Boss", 100, strength=5, xpGain=10, image="assets/monsters/boss/boss1.png"),
    Monster("Demon Boss", 200, strength=2, xpGain=10, image="assets/monsters/boss/boss2.png"),
    Monster("Angel Boss", 80, strength=6, xpGain=10, image="assets/monsters/boss/boss3.png")
]

rooms = {
    RoomMonster: 40,
    RoomChest: 5,
    RoomTrap: 5,
    RoomShop: 5,
    RoomBoss: 1
}
