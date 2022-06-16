import math

import pygame
from GUI import GUI
import utils


# anime le projectile
class Projectile(pygame.sprite.Sprite):
    def __init__(self, hero, gui: GUI):
        super().__init__()
        self.hero = hero
        self.gui = gui
        self.image = pygame.image.load("assets/hero equipment/bow/arrow.png")
        self.rect = self.image.get_rect()
        self.rect.x = gui.getTilePos(utils.theGame().floor.pos(hero).x, utils.theGame().floor.pos(hero).y, hero)[0]
        self.rect.y = gui.getTilePos(utils.theGame().floor.pos(hero).x, utils.theGame().floor.pos(hero).y, hero)[1]
        self.originImage = self.image
        self.angle = 0

    def remove(self):
        self.hero.all_projectiles.remove(self)

    def move(self, other, screen):
        from Coord import Coord
        posHero = utils.theGame().floor.pos(utils.theGame().hero) * self.gui.tileSize + Coord(0.5 * self.gui.tileSize, 0.5 * self.gui.tileSize)
        posOther = utils.theGame().floor.pos(other) * self.gui.tileSize + Coord(0.5 * self.gui.tileSize, 0.5 * self.gui.tileSize)
        distance = posHero.distance(posOther) * self.gui.tileSize + 0.5 * self.gui.tileSize
        distanceX = posOther.x - posHero.x
        distanceY = posOther.y - posHero.y
        if posHero.y < posOther.y and posHero.x < posOther.x:
            self.angle = 180 - math.degrees(math.asin(abs(distanceY / distance)))
        if posHero.y < posOther.y and posHero.x > posOther.x:
            self.angle = math.degrees(math.asin(abs(distanceY / distance)))
        if posHero.y > posOther.y and posHero.x > posOther.x:
            self.angle = -math.degrees(math.asin(abs(distanceY / distance)))
        if posHero.y > posOther.y and posHero.x < posOther.x:
            self.angle = -180 + math.asin(abs(distanceY / distance))
        if posHero.y == posOther.y and posHero.x < posOther.x:
            self.angle = 180
        if posHero.y > posOther.y and posHero.x == posOther.x:
            self.angle = -90
        if posHero.y < posOther.y and posHero.x == posOther.x:
            self.angle = 90
        self.image = pygame.transform.rotate(self.originImage, self.angle)
        nbrEtape = 10
        for i in range(nbrEtape):
            utils.theGame().hero.all_projectiles.draw(screen)
            self.rect.x += distanceX / nbrEtape
            self.rect.y += distanceY / nbrEtape
            pygame.display.flip()
            pygame.time.wait(200)
        self.hero.all_projectiles.remove(self)
