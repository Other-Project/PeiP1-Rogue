import math
from Coord import Coord
import pygame

debug = False  # Debug mode


class Button:
    """Button class"""

    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.clicked = False
        self.rightClicked = False
        self.hover = False

    def update(self, events):
        pos = pygame.mouse.get_pos()  # get mouse position
        if self.rect.collidepoint(pos):  # check mouseover
            self.hover = True
            if events is not None and pygame.MOUSEBUTTONDOWN in events:  # check clicked conditions
                if pygame.mouse.get_pressed()[0] == 1:  # left click
                    self.clicked = True
                if pygame.mouse.get_pressed()[2] == 1:  # right click
                    self.rightClicked = True

    def drawImage(self, surface: pygame.Surface, imagePath, event=None):
        """Draws the button as an image"""
        self.update(event)
        drawImage(surface, imagePath, self.rect.x, self.rect.y, self.rect.w, self.rect.h)

    def drawText(self, surface: pygame.Surface, text, event=None):
        """Draws the button as a text"""
        self.update(event)
        pygame.draw.rect(surface, (75, 75, 75) if self.hover else (64, 64, 64), self.rect)
        drawText(surface, text, self.rect.x, self.rect.y, self.rect.w, self.rect.h, 24)


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


def drawText(screen, text, x, y, w, h, size=14, color=(255, 255, 255), fontName="comicsansms"):
    """Draws a text centered inside the w and h"""
    font = pygame.font.SysFont(fontName, size)
    txt = font.render(text, True, color)
    screen.blit(txt, (x + (w - txt.get_width()) / 2, y + (h - txt.get_height()) / 2))


class GUI:
    from Game import Game

    def __init__(self, game: Game):
        self.game = game
        self.difficulty = 1
        pygame.init()
        pygame.display.set_caption('Roguelike')
        try:
            pygame.display.set_icon(pygame.image.load('assets/hero/hero.png'))
        except FileNotFoundError as e:
            print(e)
        self.updateScreenSize()

    # noinspection PyAttributeOutsideInit
    def updateScreenSize(self, w=0, h=0):
        """Resize the window"""
        self.w, self.h = max(1300, w), max(700, h)
        self.screen = pygame.display.set_mode((self.w, self.h), pygame.RESIZABLE)
        if self.game.floor is not None:
            self.tileSize = min(self.w * 0.7, self.w - 500, self.h) / self.game.floor.size

    def getEvents(self, additionalEvents=None):
        events = []
        additionalEvents = additionalEvents or {}
        for event in pygame.event.get(eventtype=[pygame.QUIT, pygame.KEYDOWN, pygame.VIDEORESIZE, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION] + list(additionalEvents.keys())):
            if event.type in events:
                continue
            events.append(event.type)
            if event.type == pygame.QUIT:
                import sys
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self.updateScreenSize(event.size[0], event.size[1])
            elif event.type in additionalEvents:
                additionalEvents[event.type](event)
            if debug:
                print("Received event:", pygame.event.event_name(event.type))
        return events

    # region Draw utils

    def drawStatComponent(self, x, y, w, h, data):
        statsFont = pygame.font.SysFont('comicsansms', 20)
        drawImage(self.screen, data[0], x, y, w, h)
        strengthTxt = statsFont.render(data[1], True, (255, 255, 255))
        self.screen.blit(strengthTxt, (x + (w - strengthTxt.get_width()) / 2, y + h))

    def drawBarImage(self, x, y, valueMax, image, width, height=None, nbCol=5, padding=5, sizeImage=None):
        """Draws a horizontal bar made of images"""
        self.drawBar(x, y, valueMax,
                     lambda _x, _y, w, h, i: drawImage(self.screen, image(i), _x, _y, max(w, 0), max(h, 0)),
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

    def drawItem(self, elem, x, y, event, action=lambda elem, hero: elem.deEquip(hero), rightAction=lambda elem, hero: elem.deEquip(hero, True), size=None):
        """Draws a box with an item (or not) inside"""
        size = size or self.tileSize
        pygame.draw.rect(self.screen, (55, 55, 55), pygame.Rect(x, y, size, size))
        if elem is None:
            return
        elemButton = Button(x + size * 0.125, y + size * 0.125, size * 0.75, size * 0.75)
        elemButton.drawImage(self.screen, elem.image, event)
        if elemButton.clicked:
            action(elem, self.game.hero)
        if elemButton.rightClicked:
            rightAction(elem, self.game.hero)

        from Equipment import Equipment
        if isinstance(elem, Equipment):
            self.drawProgressBar(x + size * 0.125, y + size * 0.8125, size * 0.75, size * 0.125, elem.solidity / elem.solidityMax, self.getBarColor(elem.solidity, elem.solidityMax))

    def drawProgressBar(self, x, y, w, h, val, color, r=None):
        r = r or int(h // 2)
        pygame.draw.rect(self.screen, (32, 32, 32), pygame.Rect(x, y, w, h), border_radius=r)
        pygame.draw.rect(self.screen, color, pygame.Rect(x + 1, y + 1, (w - 2) * max(min(val, 1), 0), h - 2), border_radius=r)

    @staticmethod
    def getBarColor(value: float, maxValue: float):
        """The color that the bar should take according to its value"""
        relativeHp = value / maxValue
        if relativeHp > 0.67:  # 2/3 of life remaining
            return 25, 172, 38
        elif relativeHp > 0.34:  # 1/3 of life remaining
            return 255, 216, 0
        return 255, 0, 0

    # endregion

    def main(self, w=0, h=0):
        """Main loop"""
        self.updateScreenSize(w, h)
        self.startScreen()

        events = None
        while self.game.hero.hp > 0:
            if events is not None:
                events = self.getEvents({pygame.KEYDOWN: lambda event: self.game.keyPressed(event.key)})
            if events is None or len(events) > 0:
                self.screen.fill((75, 75, 75))
                self.sidePanel(events)
                self.gameMap(events)
                # Updates the display but don't pass event, so it doesn't count a click twice
                self.sidePanel(None)
                self.gameMap(None)
                pygame.display.flip()
                if debug:
                    print("Game screen updated")
                events = []

        self.endScreen()

    # region Game map

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

    def gameMap(self, event):
        """Draws the map"""
        from Coord import Coord
        a, b = pygame.mouse.get_pos()
        posHero = self.game.floor.pos(self.game.hero)
        for y in range(len(self.game.floor)):
            for x in range(len(self.game.floor)):
                e = self.game.floor.get(Coord(x, y))
                if self.difficulty > 1 and posHero.distance(Coord(x, y)) > 6 and (self.difficulty > 2 or Coord(x, y) not in self.game.floor.visited):
                    self.screen.blit(pygame.transform.scale(pygame.image.load("assets/grounds/cloud.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))
                    continue
                if Coord(x, y) not in self.game.floor.visited:
                    self.game.floor.visited.append(Coord(x, y))
                if e is None:
                    self.screen.blit(pygame.transform.scale(pygame.image.load("assets/grounds/lava.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))
                    continue

                self.screen.blit(pygame.transform.scale(pygame.image.load("assets/grounds/ground.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))
                if e.image is not None:
                    from Monster import Monster
                    from Hero import Hero
                    from Item import Item
                    element1_button = Button(self.getTilePos(x, y, None)[0], self.getTilePos(x, y, None)[1], self.tileSize, self.tileSize)
                    element1_button.drawImage(self.screen, e.getImage() if isinstance(e, Hero) else e.image, event)
                    if isinstance(e, Monster):
                        if element1_button.clicked:
                            if self.game.hero.weapon is not None:
                                if posHero.distance(Coord(x, y)) <= self.game.floor.hero.weapon.radius:
                                    self.game.hero.shootProjectile(Coord(x, y), lambda coord: self.game.hero.weapon.rangedAttack(self.game.floor.get(coord)))
                        if e.visibility:
                            hpBarX, hpBarY = self.getTilePos(x, y, e)
                            hpBarW, hpBarH = self.tileSize, self.tileSize * 0.175
                            hpBarY += -hpBarH if hpBarY >= self.tileSize else self.tileSize
                            self.drawProgressBar(hpBarX, hpBarY, hpBarW, hpBarH, e.hp / e.hpMax, self.getBarColor(e.hp, e.hpMax))
                    if isinstance(e, Item):
                        if pygame.Rect(a, b, self.tileSize, self.tileSize).colliderect(pygame.Rect(self.getTilePos(x, y, e)[0], self.getTilePos(x, y, e)[1], self.tileSize, self.tileSize)):
                            self.drawInfoBox(self.getTilePos(x, y, None), e)
        for elem in self.game.floor._elem.copy():
            from Creature import Creature
            if isinstance(elem, Creature) and elem.hp > 0:
                for projectile in elem.all_projectiles:
                    projectile.draw()

    def drawInfoBox(self, pos, e, padding=5):
        """Draws an info box"""
        font = pygame.font.SysFont('comicsansms', int(self.tileSize * (2 / 5)))
        desc = font.render(e.description(), True, (255, 255, 255))
        width = desc.get_width()
        height = desc.get_height()
        x = pos[0] + (self.tileSize - width) / 2
        y = pos[1] - height
        pygame.draw.rect(self.screen, (80, 80, 80), pygame.Rect(x - padding, y - padding, width + padding * 2, height + padding * 2))  # Draw the panel
        self.screen.blit(desc, (x, y))

    def heroTrapped(self, coord: Coord, image="assets/hero/heroTrapped.png"):
        self.gameMap(None)
        self.screen.blit(pygame.transform.scale(pygame.image.load(image), self.getTileSurface(None)), self.getTilePos(coord.x, coord.y, None))
        pygame.display.flip()

    # endregion

    # region Side Bar

    def sidePanel(self, event):
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

        self.drawEquipment(equipmentX, equipmentY, equipmentW, equipmentH, event)

        # Stats: bars of hp, satiety, etc
        statsHpCol, statsSatietyCol, statsManaCol = math.ceil(self.game.hero.healthMax / 2), 10, 10
        statsHpR, statsSatietyR, statsManaR = 2, math.ceil(self.game.hero.satietyMax / statsSatietyCol), math.ceil(self.game.hero.manaMax / statsManaCol)
        statsHpH = self.tileSize * 0.75 * statsHpR + 20 * (statsHpR - 1)
        statsSatietyH = self.tileSize * 0.75 * statsSatietyR + 20 * (statsHpR - 1)
        statsManaH = self.tileSize * 0.75 * statsManaR + 20 * (statsHpR - 1)
        statsGap = (statsH - statsHpH - statsSatietyH - statsManaH) / 2
        self.drawBarImage(statsX, statsY, self.game.hero.healthMax, lambda i: "assets/gui/sidebar/heart_fg.png" if i < self.game.hero.hp else "assets/gui/sidebar/heart_bg.png",
                          statsW, statsHpH, sizeImage=self.tileSize * 0.75, nbCol=statsHpCol)
        self.drawBarImage(statsX, statsY + statsHpH + statsGap, self.game.hero.satietyMax, lambda i: "assets/foods/chunk.png" if i < self.game.hero.satiety else "assets/gui/sidebar/food_bg.png",
                          statsW, statsSatietyH, sizeImage=self.tileSize * 0.75, nbCol=10)
        self.drawBarImage(statsX, statsY + statsHpH + statsSatietyH + statsGap * 2, self.game.hero.manaMax,
                          lambda i: "assets/items/mana.png" if i < self.game.hero.mana else "assets/gui/sidebar/mana_bg.png",
                          statsW, statsManaH, sizeImage=self.tileSize * 0.75, nbCol=10)

        # Spells
        from config import potions
        spellsX, spellsY = statsX, statsY + statsH + 20
        spellsW, spellsH = boxW - 40, self.tileSize + 50
        if debug:  # debug rects
            pygame.draw.rect(self.screen, (80, 20, 20), pygame.Rect(spellsX, spellsY, spellsW, spellsH))  # debug rect
        self.drawBar(spellsX, spellsY, len(potions), lambda x, y, w, h, i: self.drawPotion(x, y, i, event), spellsW, spellsH, nbCol=len(potions), sizeImage=self.tileSize)

        # Inventory
        inventoryX, inventoryY = spellsX, spellsY + spellsH + 20
        inventoryW = spellsW
        inventoryColumns = max(min(int(inventoryW / (self.tileSize + 20)), 10), 1)
        inventoryLines = math.ceil(self.game.hero.inventorySize / inventoryColumns)
        inventoryH = self.tileSize * inventoryLines + 20 * (inventoryLines - 1)
        if debug:  # debug rects
            pygame.draw.rect(self.screen, (80, 80, 20), pygame.Rect(inventoryX, inventoryY, inventoryW, inventoryH))
        self.drawBar(inventoryX, inventoryY, self.game.hero.inventorySize,
                     lambda x, y, w, h, i: self.drawItem(self.game.hero.inventory[i] if i < len(self.game.hero.inventory) else None, x, y, event, size=min(w, h),
                                                         action=lambda elem, hero: hero.use(elem),
                                                         rightAction=lambda elem, hero: hero.inventory.remove(elem)),
                     inventoryW, inventoryH, nbCol=inventoryColumns, sizeImage=self.tileSize)

        # Controls
        controlsW, controlsH = inventoryW, min(150, boxH * 0.15)
        controlsX, controlsY = inventoryX, boxY + boxH + - controlsH - 20
        controls = [
            ("move", "assets/gui/sidebar/zqsd.png", 1.25),
            ("destroy", "assets/gui/sidebar/mouseRight.png", 0.7),
            ("rest", "assets/gui/sidebar/letterR.png", 0.7),
            ("use", "assets/gui/sidebar/mouseLeft.png", 0.7),
            ("suicide", "assets/gui/sidebar/letterK.png", 0.7),
            ("skip", "assets/gui/sidebar/spaceBar.png", 0.7)
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

    def drawPotion(self, x, y, i, event):
        """Draws a potion button"""
        from config import potions
        spellsFont = pygame.font.SysFont('comicsansms', 15)
        spell = potions[i]

        self.drawItem(spell, x, y, event, action=lambda elem, hero: elem.activate(hero), rightAction=lambda elem, hero: None)

        name = spellsFont.render(spell.name, True, (255, 255, 255))
        self.screen.blit(name, (x + (self.tileSize - name.get_width()) / 2, y + self.tileSize + 5))

        price = spellsFont.render("x" + str(spell.price), True, (255, 255, 255))
        priceY = y + self.tileSize + name.get_height() + 10
        priceSize = max(price.get_width(), price.get_height())
        drawImage(self.screen, "assets/items/mana.png", x + (self.tileSize - priceSize) / 2, priceY, priceSize, priceSize)
        self.screen.blit(price, (x + (self.tileSize - priceSize) / 2, priceY))

    def drawControl(self, x: int, y: int, w: int, h: int, text: str, image: str, scale: float):
        """Draws a control infogram"""
        font = pygame.font.SysFont('comicsansms', 14)
        imgSize = h * 2
        txt = font.render(text, True, (255, 255, 255))
        x += (w - imgSize - txt.get_width()) / 2
        drawImage(self.screen, image, x, y - h * (scale - 1) / 2, imgSize, h * scale)
        self.screen.blit(txt, (x + imgSize + 20, y + (h - txt.get_height()) / 2))

    def drawEquipment(self, x, y, w, h, event):
        """Draws the equipment area of the side panel"""
        equipmentTileGap = 15
        equipmentTileW, equipmentTileH = self.tileSize, self.tileSize + equipmentTileGap

        # Equipment
        equipmentLeftTiles = [self.game.hero.helmet, self.game.hero.chestplate, self.game.hero.legs, self.game.hero.boots]
        equipmentTileLeftW, equipmentTileLeftH = equipmentTileW, equipmentTileH * len(equipmentLeftTiles) - equipmentTileGap
        equipmentTileLeftX, equipmentTileLeftY = x, y + (h - equipmentTileLeftH) / 2
        for equipmentI in range(len(equipmentLeftTiles)):
            self.drawItem(equipmentLeftTiles[equipmentI], equipmentTileLeftX, equipmentTileLeftY + equipmentTileH * equipmentI, event)

        # Image of the hero
        heroX = equipmentTileLeftX + equipmentTileW + 20
        heroY = y + 20
        heroW = w - (equipmentTileW + 20) * 2
        heroH = h - 80
        heroImgX, heroImgY, heroImgW, heroImgH = drawImage(self.screen, "assets/hero/hero.png", heroX, heroY, heroW, heroH)

        # XP bar
        xpH = 15
        xpY = heroImgY - 20
        self.drawProgressBar(heroX, xpY, heroW, xpH, self.game.hero.xp / self.game.hero.lvlSup(), (25, 172, 38))
        font = pygame.font.SysFont('comicsansms', int(xpH * 0.75))
        self.screen.blit(font.render("lvl:" + str(self.game.hero.lvl), True, (255, 255, 255)), (heroX + 8, xpY - 2))
        xpTxt = font.render(str(self.game.hero.xp) + "/" + str(self.game.hero.lvlSup()), True, (255, 255, 255))
        self.screen.blit(xpTxt, (heroX + heroW - xpTxt.get_width() - 8, xpY - 2))

        equipmentRightTiles = [self.game.hero.weapon, self.game.hero.shield, self.game.hero.amulet]
        equipmentTileRightW, equipmentTileRightH = equipmentTileW, equipmentTileH * len(equipmentRightTiles) - equipmentTileGap
        equipmentTileRightX, equipmentTileRightY = heroX + heroW + 20, y + (h - equipmentTileRightH) / 2
        for equipmentI in range(len(equipmentRightTiles)):
            self.drawItem(equipmentRightTiles[equipmentI], equipmentTileRightX, equipmentTileRightY + equipmentTileH * equipmentI, event)

        # Stats
        statsX, statsY = heroX, heroImgY + heroImgH + 5
        statsW, statsH = heroW / 3 - 40, 30
        stats = [
            ("assets/equipments/sword/sword1.png", str(self.game.hero.strengthTot())),
            ("assets/equipments/bow/bow1.0.png", str(self.game.hero.rangeStrengthTot())),
            ("assets/equipments/shield/shield2.png", str(self.game.hero.resistance())),
            ("assets/items/gold.png", str(self.game.hero.gold))
        ]
        self.drawBar(statsX, statsY, len(stats), lambda x, y, w, h, i: self.drawStatComponent(x, y, w, h, stats[i]), heroW, statsH, nbCol=len(stats))

    # endregion

    # region Start and End screens

    def startScreen(self):
        """Draws the start screen"""
        self.screen.fill((255, 255, 255))
        events = [pygame.event.Event(pygame.NOEVENT)]
        while True:
            if len(events) > 0:
                self.screen.blit(pygame.transform.scale(pygame.image.load("assets/gui/start_screen/back.png"), (self.w, self.h)), (0, 0))
                self.screen.blit(pygame.transform.scale(pygame.image.load("assets/gui/start_screen/arcade.png"), (self.w / 2, self.h)), (self.w * (1 / 4), 0))

                difficultyBtnY = self.h * 4 / 5
                difficultyBtnW, difficultyBtnH = self.w / 6, self.h / 10
                easy = Button(self.w / 6 - difficultyBtnW / 2, difficultyBtnY, difficultyBtnW, difficultyBtnH)
                easy.drawText(self.screen, "Easy", events)
                if easy.clicked:
                    self.difficulty = 1
                    break
                medium = Button(self.w / 2 - difficultyBtnW / 2, difficultyBtnY, difficultyBtnW, difficultyBtnH)
                medium.drawText(self.screen, "Medium", events)
                if medium.clicked:
                    self.difficulty = 2
                    break
                hard = Button(5 * self.w / 6 - difficultyBtnW / 2, difficultyBtnY, difficultyBtnW, difficultyBtnH)
                hard.drawText(self.screen, "Hard", events)
                if hard.clicked:
                    self.difficulty = 3
                    break
                pygame.display.flip()
                if debug:
                    print("Start screen updated")
            events = self.getEvents()

    def endScreen(self):
        """Draws the end screen"""
        buttonsY = self.h / 1.3
        close_button = Button(20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.7 / 5), buttonsY, (self.w - 20 * self.tileSize) * (1.5 / 5), self.h * (1 / 10))
        replay_button = Button(20 * self.tileSize + (self.w - 20 * self.tileSize) * (2.8 / 5), buttonsY, (self.w - 20 * self.tileSize) * (1.5 / 5), self.h * (1 / 10))
        font = pygame.font.SysFont('comicsansms', int((self.w - 20 * self.tileSize) * 0.05))
        font1 = pygame.font.SysFont('comicsansms', int((self.w - 20 * self.tileSize) * 0.07))

        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/gui/end_screen/endBACK.png"), (self.w - self.tileSize * self.game.floor.size - 40, self.h - 40)),
                         (self.tileSize * self.game.floor.size + 20, 20))
        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/gui/end_screen/gameOver.png"), (self.w - self.tileSize * self.game.floor.size - 40, self.h * (1 / 3))),
                         (self.tileSize * self.game.floor.size + 20, 20))
        self.screen.blit(font1.render("SCORE:", True, (160, 0, 0)), (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (0.9 / 3)))
        self.screen.blit(font.render("hero level: " + str(self.game.hero.lvl), True, (160, 0, 0)), (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (1.3 / 3)))
        self.screen.blit(font.render("rooms visited: " + str(self.game.level), True, (160, 0, 0)), (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (1.6 / 3)))
        self.screen.blit(font.render("monsters killed: " + str(self.game.hero.monstersKilled), True, (160, 0, 0)),
                         (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (1.9 / 3)))

        self.gameMap(None)

        events = None
        while True:
            if events is not None:
                events = self.getEvents()
            if events is None or len(events) > 0:
                close_button.drawText(self.screen, "Exit", events)
                if close_button.clicked:
                    pygame.quit()
                    import sys
                    sys.exit()
                replay_button.drawText(self.screen, "Restart", events)
                if replay_button.clicked:
                    self.game.newGame()
                    self.game.buildFloor()
                    self.main(self.w, self.h)
                    break
                pygame.display.flip()
                events = []
                if debug:
                    print("End screen updated")

    # endregion

    # region Chest and merchant interaction

    from Chest import Chest

    def chestPopup(self, chest: Chest, sell):
        popupW, popupH = self.tileSize * 10, self.tileSize * 5
        popupX, popupY = (self.tileSize * self.game.floor.size - popupW) / 2, (self.tileSize * self.game.floor.size - popupH) / 2

        y = popupY + 2 * self.tileSize
        Y = popupY + 3 * self.tileSize
        events = None
        while True:
            if events is not None:
                events = self.getEvents()
            pygame.draw.rect(self.screen, (70, 70, 70), pygame.Rect(popupX, popupY, popupW, popupH))
            pygame.draw.rect(self.screen, (64, 64, 64), pygame.Rect(popupX + 0.5 * self.tileSize, popupY + 0.5 * self.tileSize, popupW - self.tileSize, popupH - self.tileSize))

            closeButton = Button(popupX + 8.5 * self.tileSize, popupY + 0.5 * self.tileSize, self.tileSize, self.tileSize)
            closeButton.drawImage(self.screen, "assets/other/cross.png", events)
            if closeButton.clicked:
                break

            x = popupX + self.tileSize
            if events is None or len(events) > 0:
                for i in range(chest.size):
                    if i < len(chest.items):
                        element = chest.items[i]
                        self.drawItem(element, x, y, events, lambda e, h: self.takeItemFromChest(chest, e))
                        if sell:  # Display the price
                            drawText(self.screen, str(element.price), x, Y, self.tileSize, self.tileSize, size=14, color=(255, 255, 255), fontName="comicsansms")
                    else:
                        self.drawItem(None, x, y, events, lambda e, h: None)
                    x += self.tileSize * 3.5
                    events = []
                pygame.display.flip()

    def takeItemFromChest(self, chest, element):
        chest.takeItem(self.game.hero, element)
        self.sidePanel(None)

    # endregion
