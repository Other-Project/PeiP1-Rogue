import pygame


class Button:
    """Button class"""

    def __init__(self, x, y, image, w ,h):
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

    def getTileSurface(self, e):
        from Equipment import Equipment
        if isinstance(e, Equipment):
            return self.tileSize * 0.65, self.tileSize * 0.65
        return self.tileSize, self.tileSize

    def getTilePos(self, x, y):
        return x * self.tileSize, y * self.tileSize

    def main(self):
        import sys
        from Coord import Coord

        self.startScreen()

        while self.game.hero.hp > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.game.newTurn(event.key)

            self.screen.fill((75, 75, 75))

            for y in range(len(self.game.floor)):
                for x in range(len(self.game.floor)):
                    e = self.game.floor.get(Coord(x, y))
                    if e is None:
                        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/lava.png"), self.getTileSurface(None)), self.getTilePos(x, y))
                    else:
                        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/ground.png"), self.getTileSurface(None)), self.getTilePos(x, y))
                        if e.image is not None:
                            self.screen.blit(pygame.transform.scale(pygame.image.load(e.image), self.getTileSurface(e)), self.getTilePos(x, y))
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

    def infoBox(self):
        font = pygame.font.SysFont('comicsansms', 20)
        screen = self.screen
        tileSize = self.tileSize
        infoObject = self.infoObject

        pygame.draw.rect(screen, (64, 64, 64),
                         pygame.Rect(tileSize * self.game.floor.size + 20, 20, self.infoObject.current_w - self.tileSize * self.game.floor.size - 40,
                                     self.infoObject.current_h - 40))

        # boite de texte
        font2 = pygame.font.SysFont('comicsansms', 20)
        pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(self.infoObject.current_w * (3 / 5), self.infoObject.current_h / 2 + 80, self.tileSize * 13, self.tileSize * 2))
        self.screen.blit(font2.render(str(printMsg(self.game)), True, (255, 255, 255)),
                         (self.infoObject.current_w * (3 / 5) + 5, self.infoObject.current_h / 2 + 80, self.tileSize * 13, self.tileSize * 2 + 5))

        # dessine le héros de l'inventaire
        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/hero/frontHero.png"), (tileSize * 5, tileSize * 5)), (infoObject.current_w * (4 / 5), 40))

        # dessine les cases pour armes
        pygame.draw.rect(self.screen, (55, 55, 55), pygame.Rect(self.infoObject.current_w * (4.65 / 5), self.infoObject.current_h * (2 / 20), tileSize, tileSize))
        pygame.draw.rect(self.screen, (55, 55, 55), pygame.Rect(self.infoObject.current_w * (4.65 / 5), self.infoObject.current_h * (3.2 / 20), tileSize, tileSize))
        if self.game.hero.weapon is not None:
            screen.blit(pygame.transform.scale(pygame.image.load(self.game.hero.weapon.image), (self.tileSize, self.tileSize)),
                        (self.infoObject.current_w * (4.65 / 5), self.infoObject.current_h * (2 / 20)))

        # dessine les cases pour les armures
        pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(infoObject.current_w * (3.95 / 5), self.infoObject.current_h * (1 / 20), tileSize, tileSize))
        pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(infoObject.current_w * (3.95 / 5), self.infoObject.current_h * (2.2 / 20), tileSize, tileSize))
        pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(infoObject.current_w * (3.95 / 5), self.infoObject.current_h * (3.4 / 20), tileSize, tileSize))
        pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(infoObject.current_w * (3.95 / 5), self.infoObject.current_h * (4.6 / 20), tileSize, tileSize))

        # caractéristiques du héros
        screen.blit(font.render("strength:" + str(self.game.hero.strength), True, (255, 255, 255)), (infoObject.current_w * (4.2 / 5), infoObject.current_h * (1 / 4)))
        screen.blit(font.render("armor:" + str(self.game.hero.armor), True, (255, 255, 255)), (infoObject.current_w * (4.2 / 5), infoObject.current_h * (1.1 / 4)))
        screen.blit(font.render("xp:" + str(self.game.hero.xp), True, (255, 255, 255)), (infoObject.current_w * (4.2 / 5), infoObject.current_h * (1.2 / 4)))
        screen.blit(font.render("level:" + str(self.game.hero.lvl), True, (255, 255, 255)), (infoObject.current_w * (4.2 / 5), infoObject.current_h * (1.3 / 4)))
        screen.blit(font.render("mana:" + str(self.game.hero.mana) + "/" + str(self.game.hero.manaMax), True, (255, 255, 255)), (infoObject.current_w * (4.2 / 5), infoObject.current_h * (1.4 / 4)))

        # règles du jeu
        screen.blit(font.render("move:", True, (255, 255, 255)), (infoObject.current_w * (3 / 5), infoObject.current_h * (8.5 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterZ.png"), (tileSize * 0.7, tileSize * 0.7)),
                    (infoObject.current_w * (3 / 5) + 100, infoObject.current_h * (8.5 / 10) - 30))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterQ.png"), (tileSize * 0.7, tileSize * 0.7)),
                    (infoObject.current_w * (3 / 5) + 60, infoObject.current_h * (8.5 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterS.png"), (tileSize * 0.7, tileSize * 0.71)),
                    (infoObject.current_w * (3 / 5) + 100, infoObject.current_h * (8.5 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterD.png"), (tileSize * 0.7, tileSize * 0.7)),
                    (infoObject.current_w * (3 / 5) + 140, infoObject.current_h * (8.5 / 10)))
        screen.blit(font.render("skip one turn:", True, (255, 255, 255)), (infoObject.current_w * (4 / 5), infoObject.current_h * (9.3 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/spaceBar .png"), (tileSize * 2.7, tileSize * 0.9)),
                    (infoObject.current_w * (4.45 / 5), infoObject.current_h * (9.2 / 10)))
        screen.blit(font.render("destroy an object: right click", True, (255, 255, 255)), (infoObject.current_w * (4 / 5), infoObject.current_h * (8.8 / 10)))
        screen.blit(font.render("suicide:", True, (255, 255, 255)), (infoObject.current_w * (3 / 5), infoObject.current_h * (9.3 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterK.png"), (tileSize * 0.7, tileSize * 0.7)),
                    (infoObject.current_w * (3 / 5) + 100, infoObject.current_h * (9.3 / 10)))
        screen.blit(font.render("use an object: left click", True, (255, 255, 255)), (infoObject.current_w * (4 / 5), infoObject.current_h * (8.3 / 10)))

        x = tileSize * self.game.floor.size + 37
        y = infoObject.current_h / 20
        self.drawBar(x, y, 10, lambda i: "assets/other/heartRed.png" if i < self.game.hero.hp else "assets/other/heartGrey.png", sizeImage=0.75, padding=0.75)
        self.drawBar(x - 10, y + self.tileSize * 2.5, self.game.hero.satietyMax,
                     lambda i: "assets/food/chunk.png" if i < self.game.hero.satiety else "assets/food/chunkBack.png", nbCol=10)
        self.drawBar(infoObject.current_w * (3 / 5) + tileSize * self.game.floor.size * (1 / 55), infoObject.current_h / 2, 10,
                     lambda i: "assets/other/backInventory.png", nbCol=10, sizeImage=1, padding=0.25)

        size = self.tileSize
        gap = size + size * 0.25
        x = infoObject.current_w * (3 / 5) + tileSize * self.game.floor.size * (1 / 55)
        y = infoObject.current_h / 2
        columns = 10
        for nbr in range(self.game.hero.inventorySize):
            if nbr < len(self.game.hero.inventory):
                elem = self.game.hero.inventory[nbr]
                elemButton = Button(x - 2 + (nbr - int(nbr / columns) * columns) * gap, y + int(nbr / columns) * gap, pygame.image.load(elem.image), self.tileSize, self.tileSize)
                elemButton.draw(self.screen)
                if elemButton.clicked:
                    self.game.hero.use(elem)
                if elemButton.rightClicked:
                    self.game.hero.inventory.remove(elem)

    def drawBar(self, x, y, valueMax, image, nbCol=5, padding=0.5, sizeImage=0.5):
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
            close_button = Button(self.infoObject.current_w * (2 / 3) - 75, buttonsY, pygame.image.load("assets/other/exitButton.png"), 200, 84)
            replay_button = Button(self.infoObject.current_w * (4 / 5), buttonsY, pygame.image.load("assets/other/restartButton.png"), 200, 84)
            font = pygame.font.SysFont('comicsansms', 35)
            font1 = pygame.font.SysFont('comicsansms', 65)
            posHero= self.game.floor.pos(self.game.hero)
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/ground.png"), self.getTileSurface(self.game.hero)), self.getTilePos(posHero.x, posHero.y))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/graveHero.png"), self.getTileSurface(self.game.hero)), self.getTilePos(posHero.x, posHero.y))
            self.game.hero.image = "assets/other/graveHero.png"
            pygame.draw.rect(self.screen, (0, 0, 0),
                             pygame.Rect(self.tileSize * self.game.floor.size + 20, 20, self.infoObject.current_w - self.tileSize * self.game.floor.size - 40,
                                         self.infoObject.current_h - 40))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/gameOver.png"),
                                                    (self.infoObject.current_w - self.tileSize * self.game.floor.size - 40, self.infoObject.current_h * (1 / 3))),
                             (self.tileSize * self.game.floor.size + 20, 20))
            self.screen.blit(font1.render("SCORE:", True, (255, 255, 255)),
                             (self.infoObject.current_w * (3 / 5) + self.tileSize * self.game.floor.size * (1 / 55), self.infoObject.current_h * (0.9 / 3)))
            self.screen.blit(font.render("hero level: " + str(self.game.hero.lvl), True, (255, 255, 255)),
                             (self.infoObject.current_w * (3 / 5) + self.tileSize * self.game.floor.size * (1 / 55), self.infoObject.current_h * (1.3 / 3)))
            self.screen.blit(font.render("rooms visited: " + str(self.game.level), True, (255, 255, 255)),
                             (self.infoObject.current_w * (3 / 5) + self.tileSize * self.game.floor.size * (1 / 55), self.infoObject.current_h * (1.6 / 3)))
            self.screen.blit(font.render("monsters killed: " + str(self.game.hero.monstersKilled), True, (255, 255, 255)),
                             (self.infoObject.current_w * (3 / 5) + self.tileSize * self.game.floor.size * (1 / 55), self.infoObject.current_h * (1.9 / 3)))
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
