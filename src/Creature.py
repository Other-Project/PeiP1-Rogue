from Element import Element
import pygame


class Creature(Element):
    def __init__(self, name, hp, enemyType, strength=1, image=None, visibility=True):
        """
        :param name: The name of the creature
        :param image: The image of the creature
        :param hp: The health of the creature
        :param enemyType: The type to attack
        :param strength: The strength of the creature
        :param visibility: Is the creature visible
        """
        Element.__init__(self, name, image)
        self.hp = hp
        self.strength = strength
        self.enemyType = enemyType
        self.visibility = visibility
        self.all_projectiles = pygame.sprite.Group()

    def shootProjectile(self, target, onCollide=None):
        from Projectile import Projectile
        self.all_projectiles.add(Projectile(self, target, onCollide))

    def description(self):
        return Element.description(self) + "(" + str(max(self.hp, 0)) + ")"

    def meet(self, attacker) -> bool:
        """Attacked by an enemy"""
        if not isinstance(attacker, self.enemyType):
            return False
        attacker.attack(self)
        return self.hp <= 0

    def attack(self, attacked, damage=None):
        """Attacks an enemy"""
        import utils
        attacked.hp -= damage or self.strength
        utils.theGame().addMessage("The " + self.name + " hits " + ("" if attacked.hp > 0 else "fatally ") + "the " + attacked.name +
                                   (" doing " + str(damage or self.strength) + " hp of damage (remaining hp: " + str(attacked.hp) + ")" if attacked.hp > 0 else ""))

    def doAction(self, floor):
        """A function that is called at each turn"""
        raise NotImplementedError("Abstract method")
