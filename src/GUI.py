import pygame


class Button:
    """Button class"""

    def __init__(self, x, y, image, w, h):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.rightClicked = False

    def draw(self, surface):
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
            if pygame.mouse.get_pressed()[2] == 1:
                self.rightClicked = True
        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))


messages = None


def printMsg(game):
    global messages
    msg = game.readMessages()
    if msg is not None and msg != "":
        messages = msg
        return msg
    else:
        return messages


class GUI:
    from Game import Game

    def __init__(self, game: Game):
        self.game = game
        pygame.init()
        self.infoObject = pygame.display.Info()
        self.tileSize = min(self.infoObject.current_w, self.infoObject.current_h) / game.floor.size
        self.screen = pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h))
        self.visited = []

    def getTileSurface(self, e):
        from Item import Item
        if isinstance(e, Item):
            return self.tileSize * 0.65, self.tileSize * 0.65
        return self.tileSize, self.tileSize

    def getTilePos(self, x, y, e):
        tileSurface = self.getTileSurface(e)
        tilePos = x * self.tileSize, y * self.tileSize
        return tilePos[0] + (self.tileSize - tileSurface[0]) / 2, tilePos[1] + (self.tileSize - tileSurface[1]) / 2

    def main(self):
        import sys
        from Coord import Coord
        from Armor import Armor

        self.startScreen()
        while self.game.hero.hp > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.game.newTurn(event.key)

            self.screen.fill((75, 75, 75))
            font4 = pygame.font.SysFont('comicsansms', int(self.tileSize * (2 / 5)))
            a, b = pygame.mouse.get_pos()
            for y in range(len(self.game.floor)):
                for x in range(len(self.game.floor)):
                    e = self.game.floor.get(Coord(x, y))
                    if e is None:
                        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/lava.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))
                    else:
                        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/ground.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))

                        if e.image is not None:
                            from Monster import Monster
                            from Item import Item
                            from Weapon import Weapon
                            from Amulet import Amulet

                            distanceX = abs(self.game.floor.pos(self.game.hero).x - self.game.floor.pos(e).x)
                            distanceY = abs(self.game.floor.pos(self.game.hero).y - self.game.floor.pos(e).y)
                            if distanceX <= 8 and distanceY <= 8 or e in self.visited:
                                self.screen.blit(pygame.transform.scale(pygame.image.load(e.image), self.getTileSurface(e)), self.getTilePos(x, y, e))
                                if e not in self.visited:
                                    self.visited.append(e)
                                if isinstance(e, Monster):
                                    if e.visibility:
                                        pygame.draw.rect(self.screen, (0, 0, 0),
                                                         pygame.Rect(self.getTilePos(x, y, e)[0], self.getTilePos(x, y, e)[1] - self.tileSize * (0.6 / 5),
                                                                     self.tileSize, self.tileSize * (0.75 / 5)))
                                        pygame.draw.rect(self.screen, (25, 172, 38),
                                                         pygame.Rect(self.getTilePos(x, y, e)[0], self.getTilePos(x, y, e)[1] - self.tileSize * (0.6 / 5),
                                                                     self.tileSize * (e.hp / e.hpMax), self.tileSize * (0.75 / 5)))
                                if isinstance(e, Item):
                                    if pygame.Rect(a, b, self.tileSize, self.tileSize).colliderect(
                                            pygame.Rect(self.getTilePos(x, y, e)[0], self.getTilePos(x, y, e)[1], self.tileSize, self.tileSize)):
                                        if isinstance(e, Armor):
                                            self.screen.blit(font4.render("resistance: " + str(e.resistance), True, (255, 255, 255)),
                                                             (self.getTilePos(x, y, e)[0]-self.tileSize*(3/5), self.getTilePos(x, y, e)[1] - self.tileSize * (3 / 5)))
                                        if isinstance(e, Weapon):
                                            self.screen.blit(font4.render("damage: " + str(e.damage), True, (255, 255, 255)),
                                                             (self.getTilePos(x, y, e)[0]-self.tileSize*(3/5), self.getTilePos(x, y, e)[1] - self.tileSize * (3 / 5)))
                                        if isinstance(e,Amulet):
                                            if e.type=="strength":
                                                self.screen.blit(font4.render("damage+2", True, (255, 255, 255)),
                                                                 (self.getTilePos(x, y, e)[0] - self.tileSize * (1.9 / 5), self.getTilePos(x, y, e)[1] - self.tileSize * (3 / 5)))
                                            if e.type=="xp":
                                                self.screen.blit(font4.render("xp*1.5", True, (255, 255, 255)),
                                                                 (self.getTilePos(x, y, e)[0] - self.tileSize * (1.5 / 5), self.getTilePos(x, y, e)[1] - self.tileSize * (3 / 5)))

            self.infoBox()
            pygame.display.flip()

        self.endScreen()

    def startScreen(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/back.png"), (self.infoObject.current_w, self.infoObject.current_h)),
                         (0, 0))
        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/arcade.png"), (self.infoObject.current_w / 2, self.infoObject.current_h)),
                         (self.infoObject.current_w * (1 / 4), 0))
        start_button = Button((self.infoObject.current_w / 2) - 348 / 2, (self.infoObject.current_h * (4 / 5)), pygame.image.load("assets/other/startButton.png"), 348, 149)
        while not start_button.clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    import sys
                    sys.exit()
            start_button.draw(self.screen)
            pygame.display.flip()

    def drawItem(self, elem, x, y):
        pygame.draw.rect(self.screen, (55, 55, 55), pygame.Rect(x, y, self.tileSize, self.tileSize))
        if elem is not None:
            elemButton = Button(x + self.tileSize * 0.125, y + self.tileSize * 0.125, pygame.image.load(elem.image), self.tileSize * 0.75, self.tileSize * 0.75)
            elemButton.draw(self.screen)
            if elemButton.clicked:
                elem.deEquip(self.game.hero)


    def drawPotion(self, x, y):
        from Potion import Potion
        from config import heal
        from config import teleport
        from config import fireBall
        size = self.tileSize * ((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 1.9
        gap = size + size * ((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 7.5
        listPotion = [Potion("potion", usage=lambda item, hero: heal(hero), image="assets/potion/potionHeal.png", price=6),
                      Potion("potion", usage=lambda item, hero: teleport(hero, True), image="assets/potion/potionTeleportation.png", price=5),
                      Potion("portoloin", usage=lambda item, hero: teleport(hero, False), image="assets/potion/potionPortoloin.png", price=7),
                      Potion("FireBall", usage=lambda item, hero: fireBall(hero), image="assets/potion/fireball.png", price=9)]
        for potion in range(len(listPotion)):
            potionButton = Button(x + (potion - int(potion / 4) * 4) * gap, y, pygame.image.load(listPotion[potion].image), self.tileSize * 0.7, self.tileSize * 0.7)
            potionButton.draw(self.screen)
            if potionButton.clicked:
                listPotion[potion].activate(self.game.hero)

    def infoBox(self):
        sizeInventory = self.infoObject.current_w - 20 * self.tileSize
        font = pygame.font.SysFont('comicsansms', int(sizeInventory * 0.03))
        screen = self.screen
        tileSize = self.tileSize
        infoObject = self.infoObject

        pygame.draw.rect(screen, (64, 64, 64),
                         pygame.Rect(tileSize * self.game.floor.size + 20, 20, self.infoObject.current_w - self.tileSize * self.game.floor.size - 40,
                                     self.infoObject.current_h - 40))

        # boite de texte
        font2 = pygame.font.SysFont('comicsansms', int(sizeInventory * 0.03))
        pygame.draw.rect(screen, (55, 55, 55),
                         pygame.Rect(20 * tileSize + sizeInventory * (0.25 / 5), self.infoObject.current_h / 2 + 80, sizeInventory * (4.5 / 5),
                                     self.tileSize * 2))
        self.screen.blit(font2.render(str(printMsg(self.game)), True, (255, 255, 255)),
                         (20 * tileSize + sizeInventory * (0.25 / 5), self.infoObject.current_h / 2 + 80, self.tileSize * 13, self.tileSize * 2 + 5))

        # dessine le héros de l'inventaire
        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/hero/frontHero.png"), (sizeInventory * (1.25 / 5), sizeInventory * (1.25 / 5))),
                         (20 * tileSize + sizeInventory * (3 / 5), 40))

        # dessine les cases pour les équipements
        self.drawItem(self.game.hero.weapon, 20 * tileSize + sizeInventory * (4.3 / 5), self.infoObject.current_h * (1.5 / 20))
        self.drawItem(self.game.hero.helmet, 20 * tileSize + sizeInventory * (2.8 / 5), self.infoObject.current_h * (1 / 20))
        self.drawItem(self.game.hero.chestplate, 20 * tileSize + sizeInventory * (2.8 / 5), self.infoObject.current_h * (2.2 / 20))
        self.drawItem(self.game.hero.legs, 20 * tileSize + sizeInventory * (2.8 / 5), self.infoObject.current_h * (3.4 / 20))
        self.drawItem(self.game.hero.boots, 20 * tileSize + sizeInventory * (2.8 / 5), self.infoObject.current_h * (4.6 / 20))
        self.drawItem(self.game.hero.shield, 20 * tileSize + sizeInventory * (4.3 / 5), self.infoObject.current_h * (2.7 / 20))
        self.drawItem(self.game.hero.amulet, 20 * tileSize + sizeInventory * (4.3 / 5), self.infoObject.current_h * (3.9 / 20))

        # caractéristiques du héros
        screen.blit(pygame.transform.scale(pygame.image.load("assets/hero equipment/sword/sword1.png"), (sizeInventory * (1 / 20), sizeInventory * (1 / 20))),
                    (20 * tileSize + sizeInventory * (3.3 / 5), infoObject.current_h * (1.05 / 4)))
        screen.blit(font.render(str(self.game.hero.strength + (self.game.hero.weapon.damage if self.game.hero.weapon is not None else 0)), True, (255, 255, 255)),
                    (20 * tileSize + sizeInventory * (3.4 / 5), infoObject.current_h * (1.15 / 4)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/hero equipment/shield/shield2.png"), (sizeInventory * (1 / 20), sizeInventory * (1 / 20))),
                    (20 * tileSize + sizeInventory * (3.75 / 5), infoObject.current_h * (1.05 / 4)))
        screen.blit(font.render(str(self.game.hero.resistance()), True, (255, 255, 255)),
                    (20 * tileSize + sizeInventory * (3.835 / 5), infoObject.current_h * (1.15 / 4)))

        # barre xp
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect(20 * tileSize + sizeInventory * (3.2 / 5), infoObject.current_h * (0.15 / 4),
                                     sizeInventory * (1 / 5), sizeInventory * (0.05 / 5)))
        pygame.draw.rect(screen, (25, 172, 38),
                         pygame.Rect(20 * tileSize + sizeInventory * (3.2 / 5), infoObject.current_h * (0.15 / 4),
                                     sizeInventory * (1 / 5) * (self.game.hero.xp / self.game.hero.lvlSup()), sizeInventory * (0.05 / 5)))
        font3 = pygame.font.SysFont('comicsansms', int(sizeInventory * 0.02))
        screen.blit(font3.render("lvl:" + str(self.game.hero.lvl), True, (255, 255, 255)), (20 * tileSize + sizeInventory * (3 / 5), infoObject.current_h * (0.12 / 4)))
        screen.blit(font3.render(str(self.game.hero.xp) + "/" + str(self.game.hero.lvlSup()), True, (255, 255, 255)),
                    (20 * tileSize + sizeInventory * (4.25 / 5), infoObject.current_h * (0.12 / 4)))

        # règles du jeu
        screen.blit(font.render("move:", True, (255, 255, 255)), (20 * tileSize + sizeInventory * (0.5 / 5), infoObject.current_h * (7.7 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterZ.png"), (tileSize * 0.7, tileSize * 0.7)),
                    (20 * tileSize + sizeInventory * (1.25 / 5), infoObject.current_h * (7.4 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterQ.png"), (tileSize * 0.7, tileSize * 0.7)),
                    (20 * tileSize + sizeInventory * (1.25 / 5) - tileSize * 0.75, infoObject.current_h * (7.7 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterS.png"), (tileSize * 0.7, tileSize * 0.71)),
                    (20 * tileSize + sizeInventory * (1.25 / 5), infoObject.current_h * (7.7 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterD.png"), (tileSize * 0.7, tileSize * 0.7)),
                    (20 * tileSize + sizeInventory * (1.5 / 5) + tileSize * 0.09, infoObject.current_h * (7.7 / 10)))
        screen.blit(font.render("skip one turn:", True, (255, 255, 255)), (20 * tileSize + sizeInventory * (2.7 / 5), infoObject.current_h * (9.3 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/spaceBar .png"), (tileSize * 2.7, tileSize * 0.9)),
                    (20 * tileSize + sizeInventory * (3.7 / 5), infoObject.current_h * (9.2 / 10)))
        screen.blit(font.render("destroy an object: right click", True, (255, 255, 255)), (20 * tileSize + sizeInventory * (2.7 / 5), infoObject.current_h * (8.8 / 10)))
        screen.blit(font.render("suicide:", True, (255, 255, 255)), (20 * tileSize + sizeInventory * (0.5 / 5), infoObject.current_h * (9.3 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterK.png"), (tileSize * 0.7, tileSize * 0.7)),
                    (20 * tileSize + sizeInventory * (1.25 / 5), infoObject.current_h * (9.25 / 10)))
        screen.blit(font.render("use an object: left click", True, (255, 255, 255)), (20 * tileSize + sizeInventory * (2.7 / 5), infoObject.current_h * (8.3 / 10)))
        screen.blit(font.render("get 5 hp for 10 turns:", True, (255, 255, 255)), (20 * tileSize + sizeInventory * (0.5 / 5), infoObject.current_h * (8.5 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterR.png"), (tileSize * 0.7, tileSize * 0.7)),
                    (infoObject.current_w * (3.75 / 5), infoObject.current_h * (8.5 / 10)))

        y = infoObject.current_h / 20
        self.drawBar(20 * tileSize + sizeInventory * (0.25 / 5), y, 10, lambda i: "assets/other/heartRed.png" if i < self.game.hero.hp else "assets/other/heartGrey.png",
                     padding=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 1.75, sizeImage=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 1.9)
        self.drawBar(20 * tileSize + sizeInventory * (0.25 / 5), y + self.tileSize * 2.7, self.game.hero.satietyMax,
                     lambda i: "assets/food/chunk.png" if i < self.game.hero.satiety else "assets/food/chunkBack.png", nbCol=10,
                     sizeImage=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 1.1)
        self.drawBar(20 * tileSize + sizeInventory * (0.5 / 5), infoObject.current_h / 2, 10,
                     lambda i: "assets/other/backInventory.png", nbCol=10, padding=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 1.15,
                     sizeImage=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 1.9)
        self.drawBar(20 * tileSize + sizeInventory * (0.25 / 5), y + self.tileSize * 3.7, self.game.hero.manaMax,
                     lambda i: "assets/other/mana.png" if i < self.game.hero.mana else "assets/other/manaBack.png", nbCol=10,
                     sizeImage=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 1.1)
        self.drawBar(20 * tileSize + sizeInventory * (0.6 / 5), y * 7.5, 4,
                     lambda i: "assets/other/backPotion.png", nbCol=4, padding=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 7.5,
                     sizeImage=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 1.9)
        self.drawPotion(20 * tileSize + sizeInventory * (0.615 / 5), y * 7.55)
        font1 = pygame.font.SysFont('comicsansms', int(sizeInventory * 0.02))
        self.screen.blit(font1.render("heal: 6 mana", True, (255, 255, 255)),
                         (20 * tileSize + sizeInventory * (0.45 / 5), y * 8.4))
        self.screen.blit(font1.render("teleportation: 5 mana", True, (255, 255, 255)),
                         (20 * tileSize + sizeInventory * (1.45 / 5), y * 8.35))
        self.screen.blit(font1.render("portoloin: 7 mana", True, (255, 255, 255)),
                         (20 * tileSize + sizeInventory * (2.75 / 5), y * 8.35))
        self.screen.blit(font1.render("fireball: 9 mana", True, (255, 255, 255)),
                         (20 * tileSize + sizeInventory * (3.95 / 5), y * 8.35))

        size = self.tileSize
        gap = size + size * 0.25
        x = 20 * tileSize + sizeInventory * (0.45 / 5)
        y = infoObject.current_h / 2.01
        columns = 10
        '''
        font4 = pygame.font.SysFont('comicsansms', int(#taille case*qqc))
        '''
        a, b = pygame.mouse.get_pos()
        for nbr in range(self.game.hero.inventorySize):
            from Item import Item
            from Armor import Armor
            from Weapon import Weapon
            from Amulet import Amulet

            if nbr < len(self.game.hero.inventory):
                elem = self.game.hero.inventory[nbr]
                elemButton = Button(x + (nbr - int(nbr / columns) * columns) * gap + self.tileSize * (1 / 6), y + int(nbr / columns) * gap + self.tileSize * (1 / 6),
                                    pygame.image.load(elem.image), self.tileSize * 0.75, self.tileSize * 0.75)
                elemButton.draw(self.screen)
                if elemButton.clicked:
                    self.game.hero.use(elem)
                if elemButton.rightClicked:
                    self.game.hero.inventory.remove(elem)
                '''
                if isinstance(elem, Item):
                    if pygame.Rect(a, b, self.tileSize, self.tileSize).colliderect(
                            pygame.Rect(elem.x, elem.y, #taille de la case, #taille de la case)):
                        if isinstance(elem, Armor):
                            self.screen.blit(font4.render("resistance: " + str(elem.resistance), True, (255, 255, 255)),
                                             (elem.x, elem.y- #taille cases * qqc))
                        if isinstance(elem, Weapon):
                            self.screen.blit(font4.render("damage: " + str(elem.damage), True, (255, 255, 255)),
                                             (elem.x #- taille case*qqc, elem.y# - taille case *qqc ))
                        if isinstance(elem, Amulet):
                            if elem.type == "strength":
                                self.screen.blit(font4.render("damage+2", True, (255, 255, 255)),
                                                 (elem.x# - taille case*qqc, elem.y# - self.tileSize * (3 / 5)))
                            if elem.type == "xp":
                                self.screen.blit(font4.render("xp*1.5", True, (255, 255, 255)),
                                                 (elem.x# - taille case*qqc, elem.y#- taille case*qqc))
                '''

    def drawBar(self, x, y, valueMax, image, nbCol=5, padding=0.5, sizeImage=None):
        if sizeImage is None:
            sizeImage = (self.infoObject.current_w - 20 * self.tileSize) / 1500
        size = self.tileSize * sizeImage
        gap = size + size * padding
        for nbr in range(valueMax):
            self.screen.blit(pygame.transform.scale(pygame.image.load(image(nbr)), (size, size)),
                             (x + (nbr - int(nbr / nbCol) * nbCol) * gap, y + int(nbr / nbCol) * gap))

    def endScreen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    import sys
                    sys.exit()
            buttonsY = self.infoObject.current_h / 1.3
            close_button = Button(20 * self.tileSize + (self.infoObject.current_w - 20 * self.tileSize) * (0.7 / 5), buttonsY, pygame.image.load("assets/other/exitButton.png"),
                                  (self.infoObject.current_w - 20 * self.tileSize) * (1.5 / 5), self.infoObject.current_h * (1 / 10))
            replay_button = Button(20 * self.tileSize + (self.infoObject.current_w - 20 * self.tileSize) * (2.8 / 5), buttonsY, pygame.image.load("assets/other/restartButton.png"),
                                   (self.infoObject.current_w - 20 * self.tileSize) * (1.5 / 5), self.infoObject.current_h * (1 / 10))
            font = pygame.font.SysFont('comicsansms', int((self.infoObject.current_w - 20 * self.tileSize) * 0.05))
            font1 = pygame.font.SysFont('comicsansms', int((self.infoObject.current_w - 20 * self.tileSize) * 0.07))
            posHero = self.game.floor.pos(self.game.hero)
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/ground.png"), self.getTileSurface(self.game.hero)),
                             self.getTilePos(posHero.x, posHero.y, self.game.hero))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/graveHero.png"), self.getTileSurface(self.game.hero)),
                             self.getTilePos(posHero.x, posHero.y, self.game.hero))
            self.game.hero.image = "assets/other/graveHero.png"
            pygame.draw.rect(self.screen, (0, 0, 0),
                             pygame.Rect(self.tileSize * self.game.floor.size + 20, 20, self.infoObject.current_w - self.tileSize * self.game.floor.size - 40,
                                         self.infoObject.current_h - 40))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/gameOver.png"),
                                                    (self.infoObject.current_w - self.tileSize * self.game.floor.size - 40, self.infoObject.current_h * (1 / 3))),
                             (self.tileSize * self.game.floor.size + 20, 20))
            self.screen.blit(font1.render("SCORE:", True, (255, 255, 255)),
                             (20 * self.tileSize + (self.infoObject.current_w - 20 * self.tileSize) * (0.5 / 5), self.infoObject.current_h * (0.9 / 3)))
            self.screen.blit(font.render("hero level: " + str(self.game.hero.lvl), True, (255, 255, 255)),
                             (20 * self.tileSize + (self.infoObject.current_w - 20 * self.tileSize) * (0.5 / 5), self.infoObject.current_h * (1.3 / 3)))
            self.screen.blit(font.render("rooms visited: " + str(self.game.level), True, (255, 255, 255)),
                             (20 * self.tileSize + (self.infoObject.current_w - 20 * self.tileSize) * (0.5 / 5), self.infoObject.current_h * (1.6 / 3)))
            self.screen.blit(font.render("monsters killed: " + str(self.game.hero.monstersKilled), True, (255, 255, 255)),
                             (20 * self.tileSize + (self.infoObject.current_w - 20 * self.tileSize) * (0.5 / 5), self.infoObject.current_h * (1.9 / 3)))
            close_button.draw(self.screen)
            replay_button.draw(self.screen)
            pygame.display.flip()

            if close_button.clicked:
                pygame.quit()
                import sys
                sys.exit()
            if replay_button.clicked:
                self.game.__init__()
                self.game.buildFloor()
                self.main()
                break
