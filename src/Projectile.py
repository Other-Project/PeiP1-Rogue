import math

import pygame

import utils


# anime le projectile
class Projectile(pygame.sprite.Sprite):
    def __init__(self, hero, dest, onCollide=None, image="assets/equipments/bow/arrow.png"):
        super().__init__()
        self.hero = hero
        self.dest = dest
        self.originImage = self.image = pygame.image.load(image)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.angle = 0
        self.onCollide = onCollide

    def draw(self):
        from Coord import Coord
        gui = utils.theGame().gui

        posHeroInTiles = utils.theGame().floor.pos(self.hero) + Coord(0.25, 0.25)
        posHeroInPixels = posHeroInTiles * gui.tileSize
        if self.dest is None:
            return
        posMonsterInTiles = self.dest + Coord(0.25, 0.25)
        posMonsterInPixels = posMonsterInTiles * gui.tileSize
        distanceX = posMonsterInPixels.x - posHeroInPixels.x
        distanceY = posMonsterInPixels.y - posHeroInPixels.y
        self.angle = math.degrees(math.atan2(distanceY, -distanceX))
        self.rect = pygame.Rect(posHeroInPixels.x, posHeroInPixels.y, gui.tileSize * 0.5, gui.tileSize * 0.5)
        self.image = pygame.transform.rotate(pygame.transform.scale(self.originImage, self.rect.size), self.angle)

        distance = posHeroInTiles.distance(posMonsterInTiles)
        nbrEtape = max(round(distance * 2), 2)
        mvtX, mvtY = distanceX / nbrEtape, distanceY / nbrEtape
        for i in range(nbrEtape):
            self.hero.all_projectiles.draw(gui.screen)
            self.rect.x += mvtX
            self.rect.y += mvtY
            pygame.display.flip()
            pygame.time.wait(50)
        if self.onCollide is not None:
            self.onCollide(self.dest)
        self.hero.all_projectiles.remove(self)
