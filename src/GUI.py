import pygame


class Button:
    """Button class"""

    def __init__(self, x, y, image, w, h):
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


def drawImage(screen, path, x, y, w, h):
    image = pygame.image.load(path)
    imgW = image.get_width()
    imgH = image.get_height()

    ratio = max(imgW / w, imgH / h)
    width = imgW / ratio
    height = imgH / ratio
    xPos = x + (w - width) / 2
    yPos = y + (h - height) / 2

    image = pygame.transform.scale(image, (width, height))
    screen.blit(image, (xPos, yPos))
    return xPos, yPos, width, height


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
            posHero = self.game.floor.pos(self.game.hero)
            for y in range(len(self.game.floor)):
                for x in range(len(self.game.floor)):
                    e = self.game.floor.get(Coord(x, y))
                    if posHero.distance(Coord(x, y)) <= 6 or Coord(x, y) in self.game.floor.visited:
                        if Coord(x, y) not in self.game.floor.visited:
                            self.game.floor.visited.append(Coord(x, y))
                        if e is None:
                            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/lava.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))
                        else:
                            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/ground.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))

                            if e.image is not None:
                                from Monster import Monster
                                from Item import Item
                                self.screen.blit(pygame.transform.scale(pygame.image.load(e.image), self.getTileSurface(e)), self.getTilePos(x, y, e))
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
                                        self.screen.blit(font4.render(e.description(), True, (255, 255, 255)),
                                                         (self.getTilePos(x, y, e)[0] - self.tileSize * (3 / 5), self.getTilePos(x, y, e)[1] - self.tileSize * (3 / 5)))
                    else:
                        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/cloud.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))

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
        inventoryX = self.game.floor.size * self.tileSize + 20
        inventoryY = 20
        sizeInventory = self.infoObject.current_w - inventoryX - 20  # Window's size - Position of the panel - Margin right of the panel
        inventoryH = self.infoObject.current_h - inventoryY - 20
        pygame.draw.rect(self.screen, (64, 64, 64), pygame.Rect(inventoryX, inventoryY, sizeInventory, inventoryH))  # Draw the panel

        font = pygame.font.SysFont('comicsansms', int(sizeInventory * 0.03))
        screen = self.screen
        tileSize = self.tileSize
        infoObject = self.infoObject

        statsX, statsY = inventoryX + 20, inventoryY + 20
        statsW, statsH = sizeInventory / 2, 300
        equipmentX, equipmentY = statsX + statsW + 20, statsY
        equipmentW, equipmentH = inventoryX + sizeInventory - equipmentX - 20, statsH

        # debug rects
        # pygame.draw.rect(self.screen, (20, 80, 20), pygame.Rect(statsX, statsY, statsW, statsH))
        # pygame.draw.rect(self.screen, (20, 20, 80), pygame.Rect(equipmentX, equipmentY, equipmentW, equipmentH))

        self.drawEquipment(equipmentX, equipmentY, equipmentW, equipmentH)

        # Stats: bars of hp, satiety, etc
        x = 20 * tileSize + sizeInventory * (0.25 / 5)
        y = infoObject.current_h / 20
        self.drawBar(x, y, 10, lambda i: "assets/other/heartRed.png" if i < self.game.hero.hp else "assets/other/heartGrey.png", statsW,
                     padding=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 1.75, sizeImage=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 1.9)
        self.drawBar(x, y + self.tileSize * 2.7, self.game.hero.satietyMax,
                     lambda i: "assets/food/chunk.png" if i < self.game.hero.satiety else "assets/food/chunkBack.png", statsW, nbCol=10,
                     sizeImage=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 1.1)
        self.drawBar(x, y + self.tileSize * 3.7, self.game.hero.manaMax,
                     lambda i: "assets/other/mana.png" if i < self.game.hero.mana else "assets/other/manaBack.png", statsW, nbCol=10,
                     sizeImage=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 1.1)

        # Spells
        self.drawBar(20 * tileSize + sizeInventory * (0.6 / 5), y * 7.5, 4,
                     lambda i: "assets/other/backPotion.png", sizeInventory, nbCol=4, padding=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 7.5,
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

        # Inventory
        self.drawBar(20 * tileSize + sizeInventory * (0.5 / 5), infoObject.current_h / 2, 10,
                     lambda i: "assets/other/backInventory.png", sizeInventory, nbCol=10, padding=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 1.15,
                     sizeImage=((self.infoObject.current_w - 20 * self.tileSize) / 1500) * 1.9)
        size = self.tileSize
        gap = size + size * 0.25
        x = 20 * tileSize + sizeInventory * (0.45 / 5)
        y = infoObject.current_h / 2.01
        columns = 10
        for nbr in range(self.game.hero.inventorySize):
            if nbr < len(self.game.hero.inventory):
                elem = self.game.hero.inventory[nbr]
                elemButton = Button(x + (nbr - int(nbr / columns) * columns) * gap + self.tileSize * (1 / 6), y + int(nbr / columns) * gap + self.tileSize * (1 / 6),
                                    pygame.image.load(elem.image), self.tileSize * 0.75, self.tileSize * 0.75)
                elemButton.draw(self.screen)
                if elemButton.clicked:
                    self.game.hero.use(elem)
                if elemButton.rightClicked:
                    self.game.hero.inventory.remove(elem)

        # Messages
        font2 = pygame.font.SysFont('comicsansms', int(sizeInventory * 0.03))
        pygame.draw.rect(screen, (55, 55, 55),
                         pygame.Rect(20 * tileSize + sizeInventory * (0.25 / 5), self.infoObject.current_h / 2 + 80, sizeInventory * (4.5 / 5),
                                     self.tileSize * 2))
        self.screen.blit(font2.render(str(printMsg(self.game)), True, (255, 255, 255)),
                         (20 * tileSize + sizeInventory * (0.25 / 5), self.infoObject.current_h / 2 + 80, self.tileSize * 13, self.tileSize * 2 + 5))

        # Controls
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

    def drawEquipment(self, x, y, w, h):
        equipmentTileGap = 15
        equipmentTileW, equipmentTileH = self.tileSize, self.tileSize + equipmentTileGap

        equipmentLeftTiles = [self.game.hero.helmet, self.game.hero.chestplate, self.game.hero.legs, self.game.hero.boots]
        equipmentTileLeftW, equipmentTileLeftH = equipmentTileW, equipmentTileH * len(equipmentLeftTiles) - equipmentTileGap
        equipmentTileLeftX, equipmentTileLeftY = x, y + (h - equipmentTileLeftH) / 2
        for equipmentI in range(len(equipmentLeftTiles)):
            self.drawItem(equipmentLeftTiles[equipmentI], equipmentTileLeftX, equipmentTileLeftY + equipmentTileH * equipmentI)

        # Image of the hero
        heroX = equipmentTileLeftX + equipmentTileW + 20
        heroY = y
        heroW = w - (equipmentTileW + 20) * 2
        heroH = h - 50
        heroImgX, heroImgY, heroImgW, heroImgH = drawImage(self.screen, "assets/hero/frontHero.png", heroX, heroY, heroW, heroH)

        # XP bar
        xpH = 15
        xpY = heroImgY - 20
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(heroX, xpY, heroW, xpH))
        pygame.draw.rect(self.screen, (25, 172, 38), pygame.Rect(heroX, xpY, heroW * (self.game.hero.xp / self.game.hero.lvlSup()), xpH))
        font = pygame.font.SysFont('comicsansms', int(xpH * 0.75))
        self.screen.blit(font.render("lvl:" + str(self.game.hero.lvl), True, (255, 255, 255)), (heroX + 5, xpY))
        xpTxt = font.render(str(self.game.hero.xp) + "/" + str(self.game.hero.lvlSup()), True, (255, 255, 255))
        self.screen.blit(xpTxt, (heroX + heroW - xpTxt.get_width() - 5, xpY))

        equipmentRightTiles = [self.game.hero.weapon, self.game.hero.shield, self.game.hero.amulet]
        equipmentTileRightW, equipmentTileRightH = equipmentTileW, equipmentTileH * len(equipmentRightTiles) - equipmentTileGap
        equipmentTileRightX, equipmentTileRightY = heroX + heroW + 20, y + (h - equipmentTileRightH) / 2
        for equipmentI in range(len(equipmentRightTiles)):
            self.drawItem(equipmentRightTiles[equipmentI], equipmentTileRightX, equipmentTileRightY + equipmentTileH * equipmentI)

        # caractéristiques du héros
        statsX, statsY = heroX, heroImgY + heroImgH + 5
        statsW, statsH = heroW / 2 - 20, 30
        statsFont = pygame.font.SysFont('comicsansms', 20)
        drawImage(self.screen, "assets/hero equipment/sword/sword1.png", statsX, statsY, statsW, statsH)
        strengthTxt = statsFont.render(str(self.game.hero.strengthTot()), True, (255, 255, 255))
        self.screen.blit(strengthTxt, (statsX + (statsW - strengthTxt.get_width()) / 2, statsY + statsH))
        drawImage(self.screen, "assets/hero equipment/shield/shield2.png", statsX + statsW + 40, statsY, statsW, statsH)
        resistanceTxt = statsFont.render(str(self.game.hero.resistance()), True, (255, 255, 255))
        self.screen.blit(resistanceTxt, (statsX + statsW + 40 + (statsW - resistanceTxt.get_width()) / 2, statsY + statsH))

    def drawBar(self, x, y, valueMax, image, width, nbCol=5, padding=0.5, sizeImage=None):
        gap = width / nbCol
        if sizeImage is None:
            sizeImage = (self.infoObject.current_w - 20 * self.tileSize) / 1500
        size = min(self.tileSize * sizeImage, gap - padding)
        x += abs(gap - size) / 2  # Center the bar
        for nbr in range(valueMax):
            self.screen.blit(pygame.transform.scale(pygame.image.load(image(nbr)), (size, size)), (x + (nbr - int(nbr / nbCol) * nbCol) * gap, y + int(nbr / nbCol) * gap))

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
