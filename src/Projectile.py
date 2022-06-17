import math
import pygame

from GUI import GUI
import utils


# anime le projectile
class Projectile(pygame.sprite.Sprite):
    def __init__(self, gui: GUI, hero, dest, onCollide=None, image="assets/equipments/bow/arrow.png"):
        super().__init__()
        self.hero, self.origin = hero, utils.theGame().floor.pos(hero)
        self.dest = dest
        self.gui = gui
        self.rect = pygame.Rect(0, 0, self.gui.tileSize * 0.5, self.gui.tileSize * 0.5)
        self.originImage = self.image = pygame.transform.scale(pygame.image.load(image), self.rect.size)
        self.angle = 0
        self.onCollide = onCollide

    def draw(self):
        from Coord import Coord
        if self.origin is None:
            return
        posHeroInTiles = self.origin + Coord(0.25, 0.25)
        posHeroInPixels = posHeroInTiles * self.gui.tileSize
        if self.dest is None:
            return
        posMonsterInTiles = self.dest + Coord(0.25, 0.25)
        posMonsterInPixels = posMonsterInTiles * self.gui.tileSize
        distanceX = posMonsterInPixels.x - posHeroInPixels.x
        distanceY = posMonsterInPixels.y - posHeroInPixels.y
        self.rect.x, self.rect.y = posHeroInPixels.x, posHeroInPixels.y
        self.angle = math.degrees(math.atan2(distanceY, -distanceX))
        self.image = pygame.transform.rotate(self.originImage, self.angle)

        distance = posHeroInTiles.distance(posMonsterInTiles)
        nbrEtape = max(round(distance * 2), 2)
        mvtX, mvtY = distanceX / nbrEtape, distanceY / nbrEtape
        for i in range(nbrEtape):
            utils.theGame().hero.all_projectiles.draw(self.gui.screen)
            self.rect.x += mvtX
            self.rect.y += mvtY
            pygame.display.flip()
            pygame.time.wait(100)
        self.onCollide(self.dest)
        self.hero.all_projectiles.remove(self)
