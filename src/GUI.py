import pygame
import math


class Button:
    """Button class"""

    def __init__(self, x, y, image, w, h):
        self.image = pygame.transform.scale(image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.rightClicked = False

    def draw(self, surface):
        """Draws the button"""
        pos = pygame.mouse.get_pos()  # get mouse position
        if self.rect.collidepoint(pos):  # check mouseover and clicked conditions
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
            if pygame.mouse.get_pressed()[2] == 1:
                self.rightClicked = True
        surface.blit(self.image, (self.rect.x, self.rect.y))  # draw button on screen


def drawImage(screen, path, x, y, w, h):
    """Draws an image fitting the w and h"""
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


class GUI:
    from Game import Game

    def __init__(self, game: Game):
        self.game = game
        pygame.init()
        self.updateScreenSize()

    # noinspection PyAttributeOutsideInit
    def updateScreenSize(self, w=0, h=0):
        """Resize the window"""
        self.w, self.h = max(1200, w), max(700, h)
        self.screen = pygame.display.set_mode((self.w, self.h), pygame.RESIZABLE)
        self.tileSize = min(self.w * 0.7, self.w - 400, self.h) / self.game.floor.size

    def main(self):
        """Main loop"""
        import sys

        self.startScreen()
        while self.game.hero.hp > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.game.newTurn(event.key)
                if event.type == pygame.VIDEORESIZE:
                    self.updateScreenSize(event.size[0], event.size[1])
                self.gameMap()
            self.sidePanel()
            pygame.display.flip()

        self.endScreen()

    def getTileSurface(self, e):
        """Returns the screen surface of a map element (i.e. it's width and height)"""
        from Item import Item
        if isinstance(e, Item):
            return self.tileSize * 0.65, self.tileSize * 0.65
        return self.tileSize, self.tileSize

    def getTilePos(self, x, y, e):
        """Returns the screen position of a map element"""
        tileSurface = self.getTileSurface(e)
        tilePos = x * self.tileSize, y * self.tileSize
        return tilePos[0] + (self.tileSize - tileSurface[0]) / 2, tilePos[1] + (self.tileSize - tileSurface[1]) / 2

    def gameMap(self):
        """Draws the map"""
        from Coord import Coord
        self.screen.fill((75, 75, 75))
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
                                                     pygame.Rect(self.getTilePos(x, y, e)[0], self.getTilePos(x, y, e)[1] - self.tileSize * 0.2, self.tileSize, self.tileSize * 0.2))
                                    pygame.draw.rect(self.screen, self.getBarColor(e.hp, e.hpMax),
                                                     pygame.Rect(self.getTilePos(x, y, e)[0], self.getTilePos(x, y, e)[1] - self.tileSize * (0.6 / 5),
                                                                 self.tileSize * (e.hp / e.hpMax), self.tileSize * (0.75 / 5)))
                            if isinstance(e, Item):
                                if pygame.Rect(a, b, self.tileSize, self.tileSize).colliderect(pygame.Rect(self.getTilePos(x, y, e)[0], self.getTilePos(x, y, e)[1], self.tileSize, self.tileSize)):
                                    self.drawInfoBox(self.getTilePos(x, y, e)[0] - self.tileSize * (3 / 5), self.getTilePos(x, y, e)[1] - self.tileSize * 0.75, e)
                else:
                    self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/cloud.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))

    @staticmethod
    def getBarColor(value: float, maxValue: float):
        """The color that the bar should take according to its value"""
        relativeHp = value / maxValue
        if relativeHp > 0.67:  # 2/3 of life remaining
            return 25, 172, 38
        elif relativeHp > 0.34:  # 1/3 of life remaining
            return 255, 216, 0
        return 255, 0, 0

    def startScreen(self):
        """Draws the start screen"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    import sys
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.updateScreenSize(event.size[0], event.size[1])
            self.screen.fill((255, 255, 255))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/back.png"), (self.w, self.h)), (0, 0))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/arcade.png"), (self.w / 2, self.h)),
                             (self.w * (1 / 4), 0))
            start_button = Button((self.w / 2) - 348 / 2, (self.h * (4 / 5)), pygame.image.load("assets/other/startButton.png"), 348, 149)
            start_button.draw(self.screen)
            pygame.display.flip()
            if start_button.clicked:
                break

    def drawInfoBox(self, x, y, e, padding=5):
        """Draws an info box"""
        font = pygame.font.SysFont('comicsansms', int(self.tileSize * (2 / 5)))
        desc = font.render(e.description(), True, (255, 255, 255))
        width = desc.get_width()
        height = desc.get_height()
        x = x - width / 2
        pygame.draw.rect(self.screen, (64, 64, 64), pygame.Rect(x - padding, y - padding, width + padding * 2, height + padding * 2))  # Draw the panel
        self.screen.blit(desc, (x, y))

    def drawItem(self, elem, x, y, action=lambda elem, hero: elem.deEquip(hero), rightAction=lambda elem, hero: None, size=None):
        """Draws a box with an item (or not) inside"""
        size = size or self.tileSize
        pygame.draw.rect(self.screen, (55, 55, 55), pygame.Rect(x, y, size, size))
        if elem is not None:
            elemButton = Button(x + size * 0.125, y + size * 0.125, pygame.image.load(elem.image), size * 0.75, size * 0.75)
            elemButton.draw(self.screen)
            if elemButton.clicked:
                action(elem, self.game.hero)
            if elemButton.rightClicked:
                rightAction(elem, self.game.hero)

    def drawPotion(self, x, y, w, h, i):
        """Draws a potion button"""
        from config import potions
        spellsFont = pygame.font.SysFont('comicsansms', 15)
        spell = potions[i]
        self.drawItem(spell, x, y, action=lambda elem, hero: elem.activate(hero))
        txt = spellsFont.render(spell.name + ": " + str(spell.price) + " mana", True, (255, 255, 255))
        self.screen.blit(txt, (x + (self.tileSize - txt.get_width()) / 2, y + self.tileSize + 5))

    def sidePanel(self, debug=False):
        """Draws the side panel"""
        boxX, boxY = self.game.floor.size * self.tileSize + 20, 20
        boxW, boxH = self.screen.get_width() - boxX - 20, self.screen.get_height() - boxY - 20  # Window's size - Position of the panel - Margin right/bottom of the panel
        pygame.draw.rect(self.screen, (64, 64, 64), pygame.Rect(boxX, boxY, boxW, boxH))  # Draw the panel

        statsX, statsY = boxX + 20, boxY + 20
        equipmentW, equipmentH = max(self.tileSize * 2 + 40 + 100, boxW / 2 - 30), self.tileSize * 4 + 20 * 3
        statsW, statsH = boxX + boxW - statsX - equipmentW - 40, equipmentH
        equipmentX, equipmentY = statsX + statsW + 20, statsY
        if debug:  # debug rects
            pygame.draw.rect(self.screen, (20, 80, 20), pygame.Rect(statsX, statsY, statsW, statsH))
            pygame.draw.rect(self.screen, (20, 20, 80), pygame.Rect(equipmentX, equipmentY, equipmentW, equipmentH))

        self.drawEquipment(equipmentX, equipmentY, equipmentW, equipmentH)

        # Stats: bars of hp, satiety, etc
        self.drawBarImage(statsX, statsY, 10, lambda i: "assets/other/heartRed.png" if i < self.game.hero.hp else "assets/other/heartGrey.png", statsW, sizeImage=self.tileSize * 0.75)
        self.drawBarImage(statsX, statsY + self.tileSize * 2.7, self.game.hero.satietyMax, lambda i: "assets/food/chunk.png" if i < self.game.hero.satiety else "assets/food/chunkBack.png", statsW,
                          nbCol=10)
        self.drawBarImage(statsX, statsY + self.tileSize * 3.7, self.game.hero.manaMax, lambda i: "assets/other/mana.png" if i < self.game.hero.mana else "assets/other/manaBack.png", statsW, nbCol=10)

        # Spells
        from config import potions
        spellsX, spellsY = statsX, statsY + statsH + 20
        spellsW, spellsH = boxW - 40, self.tileSize + 25
        if debug:  # debug rects
            pygame.draw.rect(self.screen, (80, 20, 20), pygame.Rect(spellsX, spellsY, spellsW, spellsH))  # debug rect
        self.drawBar(spellsX, spellsY, len(potions), self.drawPotion, spellsW, spellsH, nbCol=len(potions), sizeImage=self.tileSize)

        # Inventory
        inventoryX, inventoryY = spellsX, spellsY + spellsH + 20
        inventoryW = spellsW
        inventoryColumns = max(min(int(inventoryW / (self.tileSize + 20)), 10), 1)
        inventoryLines = math.ceil(self.game.hero.inventorySize / inventoryColumns)
        inventoryH = self.tileSize * inventoryLines + 20 * (inventoryLines - 1)
        if debug:  # debug rects
            pygame.draw.rect(self.screen, (80, 80, 20), pygame.Rect(inventoryX, inventoryY, inventoryW, inventoryH))
        self.drawBar(inventoryX, inventoryY, self.game.hero.inventorySize,
                     lambda x, y, w, h, i: self.drawItem(self.game.hero.inventory[i] if i < len(self.game.hero.inventory) else None, x, y, size=min(w, h),
                                                         action=lambda elem, hero: hero.use(elem),
                                                         rightAction=lambda elem, hero: hero.inventory.remove(elem)),
                     inventoryW, inventoryH, nbCol=inventoryColumns, sizeImage=self.tileSize)

        # Controls
        controlsW, controlsH = inventoryW, min(150, boxH * 0.15)
        controlsX, controlsY = inventoryX, boxY + boxH + - controlsH - 20
        controls = [
            ("move", "assets/other/zqsd.png", 1.25),
            ("destroy", "assets/other/mouseRight.png", 0.7),
            ("heal", "assets/other/letterR.png", 0.7),
            ("use", "assets/other/mouseLeft.png", 0.7),
            ("suicide", "assets/other/letterK.png", 0.7),
            ("skip", "assets/other/spaceBar.png", 0.7)
        ]
        if debug:  # debug rects
            pygame.draw.rect(self.screen, (20, 80, 80), pygame.Rect(controlsX, controlsY, controlsW, controlsH))
        self.drawBar(controlsX, controlsY, len(controls), lambda x, y, w, h, i: self.drawControl(x, y, w, h, controls[i][0], controls[i][1], controls[i][2]), controlsW, controlsH, nbCol=2)

        # Messages
        messagesX, messagesY = inventoryX, inventoryY + inventoryH + 20
        messagesW, messagesH = inventoryW, controlsY - messagesY - 20
        messagesFont = pygame.font.SysFont('comicsansms', int(max(messagesH / 15, 12)))
        pygame.draw.rect(self.screen, (55, 55, 55), pygame.Rect(messagesX, messagesY, messagesW, messagesH))
        msgs = self.game.readMessages(int(messagesH / messagesFont.get_linesize()))
        for msgI in range(len(msgs)):
            self.screen.blit(messagesFont.render(msgs[msgI], True, (255, 255, 255)), (messagesX, messagesY + messagesFont.get_linesize() * msgI, messagesW, messagesFont.get_linesize()))

    def drawControl(self, x: int, y: int, w: int, h: int, text: str, image: str, scale: float):
        """Draws a control infogram"""
        font = pygame.font.SysFont('comicsansms', 14)
        imgSize = h * 2
        txt = font.render(text, True, (255, 255, 255))
        x += (w - imgSize - txt.get_width()) / 2
        drawImage(self.screen, image, x, y - h * (scale - 1) / 2, imgSize, h * scale)
        self.screen.blit(txt, (x + imgSize + 20, y + (h - txt.get_height()) / 2))

    def drawEquipment(self, x, y, w, h):
        """Draws the equipment area of the side panel"""
        equipmentTileGap = 15
        equipmentTileW, equipmentTileH = self.tileSize, self.tileSize + equipmentTileGap

        # Equipment
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

        # Stats
        statsX, statsY = heroX, heroImgY + heroImgH + 5
        statsW, statsH = heroW / 2 - 20, 30
        statsFont = pygame.font.SysFont('comicsansms', 20)
        drawImage(self.screen, "assets/hero equipment/sword/sword1.png", statsX, statsY, statsW, statsH)
        strengthTxt = statsFont.render(str(self.game.hero.strengthTot()), True, (255, 255, 255))
        self.screen.blit(strengthTxt, (statsX + (statsW - strengthTxt.get_width()) / 2, statsY + statsH))
        drawImage(self.screen, "assets/hero equipment/shield/shield2.png", statsX + statsW + 40, statsY, statsW, statsH)
        resistanceTxt = statsFont.render(str(self.game.hero.resistance()), True, (255, 255, 255))
        self.screen.blit(resistanceTxt, (statsX + statsW + 40 + (statsW - resistanceTxt.get_width()) / 2, statsY + statsH))

    def drawBarImage(self, x, y, valueMax, image, width, height=None, nbCol=5, padding=5, sizeImage=None):
        """Draws a horizontal bar made of images"""
        self.drawBar(x, y, valueMax,
                     lambda _x, _y, w, h, i: self.screen.blit(pygame.transform.scale(pygame.image.load(image(i)), (max(w, 0), max(h, 0))), (_x, _y)),
                     width, height, nbCol, padding, sizeImage)

    # noinspection PyMethodMayBeStatic
    def drawBar(self, x, y, valueMax, drawFct, width, height=None, nbCol=5, padding=5, sizeImage=None):
        """Calculates a horizontal bar and call `drawFct` for each component"""
        gapX = width / nbCol
        gapY = gapX if height is None else height / math.ceil(valueMax / nbCol)
        sizeW = gapX - padding if sizeImage is None else min(sizeImage, gapX - padding)
        sizeH = gapY - padding if sizeImage is None else min(sizeImage, gapY - padding)
        x += abs(gapX - sizeW) / 2  # Center the bar
        for nbr in range(valueMax):
            drawFct(x + (nbr - int(nbr / nbCol) * nbCol) * gapX, y + int(nbr / nbCol) * gapY, sizeW, sizeH, nbr)

    def endScreen(self):
        """Draws the end screen"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    import sys
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.updateScreenSize(event.size[0], event.size[1])
            buttonsY = self.h / 1.3
            close_button = Button(20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.7 / 5), buttonsY, pygame.image.load("assets/other/exitButton.png"),
                                  (self.w - 20 * self.tileSize) * (1.5 / 5), self.h * (1 / 10))
            replay_button = Button(20 * self.tileSize + (self.w - 20 * self.tileSize) * (2.8 / 5), buttonsY, pygame.image.load("assets/other/restartButton.png"),
                                   (self.w - 20 * self.tileSize) * (1.5 / 5), self.h * (1 / 10))
            font = pygame.font.SysFont('comicsansms', int((self.w - 20 * self.tileSize) * 0.05))
            font1 = pygame.font.SysFont('comicsansms', int((self.w - 20 * self.tileSize) * 0.07))
            posHero = self.game.floor.pos(self.game.hero)
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/ground.png"), self.getTileSurface(self.game.hero)),
                             self.getTilePos(posHero.x, posHero.y, self.game.hero))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/graveHero.png"), self.getTileSurface(self.game.hero)),
                             self.getTilePos(posHero.x, posHero.y, self.game.hero))
            self.game.hero.image = "assets/other/graveHero.png"
            pygame.draw.rect(self.screen, (0, 0, 0),
                             pygame.Rect(self.tileSize * self.game.floor.size + 20, 20, self.w - self.tileSize * self.game.floor.size - 40, self.h - 40))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/gameOver.png"),
                                                    (self.w - self.tileSize * self.game.floor.size - 40, self.h * (1 / 3))),
                             (self.tileSize * self.game.floor.size + 20, 20))
            self.screen.blit(font1.render("SCORE:", True, (255, 255, 255)),
                             (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (0.9 / 3)))
            self.screen.blit(font.render("hero level: " + str(self.game.hero.lvl), True, (255, 255, 255)),
                             (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (1.3 / 3)))
            self.screen.blit(font.render("rooms visited: " + str(self.game.level), True, (255, 255, 255)),
                             (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (1.6 / 3)))
            self.screen.blit(font.render("monsters killed: " + str(self.game.hero.monstersKilled), True, (255, 255, 255)),
                             (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (1.9 / 3)))
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
