import pygame
import math
from tkinter import *

debug = False  # Debug mode


class Button:
    """Button class"""

    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.clicked = False
        self.rightClicked = False
        self.hover = False

    def update(self, event=pygame.event.Event(pygame.NOEVENT)):
        pos = pygame.mouse.get_pos()  # get mouse position
        if self.rect.collidepoint(pos):  # check mouseover
            self.hover = True
            if event.type == pygame.MOUSEBUTTONDOWN:  # check clicked conditions
                if pygame.mouse.get_pressed()[0] == 1:  # left click
                    self.clicked = True
                if pygame.mouse.get_pressed()[2] == 1:  # right click
                    self.rightClicked = True

    def drawImage(self, surface: pygame.Surface, imagePath, event=pygame.event.Event(pygame.NOEVENT)):
        """Draws the button as an image"""
        self.update(event)
        drawImage(surface, imagePath, self.rect.x, self.rect.y, self.rect.w, self.rect.h)

    def drawText(self, surface: pygame.Surface, text, event=pygame.event.Event(pygame.NOEVENT)):
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
        pygame.display.set_icon(pygame.image.load('assets/hero/hero.png'))
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
        self.screen.fill((75, 75, 75))
        while self.game.hero.hp > 0:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.game.keyPressed(event.key)
            elif event.type == pygame.VIDEORESIZE:
                self.updateScreenSize(event.size[0], event.size[1])
            elif event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                continue
            self.gameMap(event)
            self.sidePanel(event)
            pygame.display.flip()
            if debug:
                print("Game screen updated:", pygame.event.event_name(event.type))

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

    def gameMap(self, event):
        """Draws the map"""
        from Coord import Coord
        a, b = pygame.mouse.get_pos()
        posHero = self.game.floor.pos(self.game.hero)
        for y in range(len(self.game.floor)):
            for x in range(len(self.game.floor)):
                e = self.game.floor.get(Coord(x, y))
                if self.difficulty <= 1 or posHero.distance(Coord(x, y)) <= 6 or (self.difficulty <= 2 and Coord(x, y) in self.game.floor.visited):
                    if Coord(x, y) not in self.game.floor.visited:
                        self.game.floor.visited.append(Coord(x, y))
                    if e is None:
                        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/grounds/lava.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))
                    else:
                        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/grounds/ground.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))
                        if e.image is not None:
                            from Monster import Monster
                            from Item import Item
                            from Weapon import Weapon
                            element1_button = Button(self.getTilePos(x, y, None)[0], self.getTilePos(x, y, None)[1], self.tileSize, self.tileSize)
                            element1_button.drawImage(self.screen, e.image, event)
                            if isinstance(e, Monster):
                                if element1_button.clicked:
                                    if self.game.hero.weapon is not None:
                                        if posHero.distance(self.game.floor.pos(e)) <= self.game.floor.hero.weapon.radius:
                                            self.game.hero.shootProjectile(self)
                                            for projectile in self.game.hero.all_projectiles:
                                                projectile.move(e, self.screen)
                                            if e.meet(self.game.hero):
                                                self.game.floor.rm(self.game.floor.pos(e))
                                            pygame.display.flip()

                                if e.visibility:
                                    hpBarX, hpBarY = self.getTilePos(x, y, e)
                                    hpBarW, hpBarH = self.tileSize, self.tileSize * 0.175
                                    hpBarY -= hpBarH
                                    hpBarRadius = int(hpBarH // 2)
                                    pygame.draw.rect(self.screen, (32, 32, 32), pygame.Rect(hpBarX, hpBarY, hpBarW, hpBarH), border_radius=hpBarRadius)
                                    pygame.draw.rect(self.screen, self.getBarColor(e.hp, e.hpMax), pygame.Rect(hpBarX + 1, hpBarY + 1, (hpBarW - 2) * (e.hp / e.hpMax), hpBarH - 2),
                                                     border_radius=hpBarRadius)
                            if isinstance(e, Item):
                                if pygame.Rect(a, b, self.tileSize, self.tileSize).colliderect(pygame.Rect(self.getTilePos(x, y, e)[0], self.getTilePos(x, y, e)[1], self.tileSize, self.tileSize)):
                                    self.drawInfoBox(self.getTilePos(x, y, e)[0] - self.tileSize * (3 / 5), self.getTilePos(x, y, e)[1] - self.tileSize * 0.75, e)
                else:
                    self.screen.blit(pygame.transform.scale(pygame.image.load("assets/grounds/cloud.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))

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
        self.screen.fill((255, 255, 255))

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                import sys
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self.updateScreenSize(event.size[0], event.size[1])
            elif event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                continue

            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/gui/start_screen/back.png"), (self.w, self.h)), (0, 0))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/gui/start_screen/arcade.png"), (self.w / 2, self.h)), (self.w * (1 / 4), 0))

            difficultyBtnY = self.h * 4 / 5
            difficultyBtnW, difficultyBtnH = self.w / 6, self.h / 10
            easy = Button(self.w / 6 - difficultyBtnW / 2, difficultyBtnY, difficultyBtnW, difficultyBtnH)
            easy.drawText(self.screen, "Easy", event)
            if easy.clicked:
                self.difficulty = 1
                break
            medium = Button(self.w / 2 - difficultyBtnW / 2, difficultyBtnY, difficultyBtnW, difficultyBtnH)
            medium.drawText(self.screen, "Medium", event)
            if medium.clicked:
                self.difficulty = 2
                break
            hard = Button(5 * self.w / 6 - difficultyBtnW / 2, difficultyBtnY, difficultyBtnW, difficultyBtnH)
            hard.drawText(self.screen, "Hard", event)
            if hard.clicked:
                self.difficulty = 3
                break
            pygame.display.flip()
            if debug:
                print("Start screen updated:", pygame.event.event_name(event.type))

    def drawInfoBox(self, x, y, e, padding=5):
        """Draws an info box"""
        font = pygame.font.SysFont('comicsansms', int(self.tileSize * (2 / 5)))
        desc = font.render(e.description(), True, (255, 255, 255))
        width = desc.get_width()
        height = desc.get_height()
        x = x - width / 2
        pygame.draw.rect(self.screen, (64, 64, 64), pygame.Rect(x - padding, y - padding, width + padding * 2, height + padding * 2))  # Draw the panel
        self.screen.blit(desc, (x, y))

    def drawItem(self, elem, x, y, event, action=lambda elem, hero: elem.deEquip(hero), rightAction=lambda elem, hero: None, size=None):
        """Draws a box with an item (or not) inside"""
        size = size or self.tileSize
        pygame.draw.rect(self.screen, (55, 55, 55), pygame.Rect(x, y, size, size))
        if elem is not None:
            elemButton = Button(x + size * 0.125, y + size * 0.125, size * 0.75, size * 0.75)
            elemButton.drawImage(self.screen, elem.image, event)
            if elemButton.clicked:
                action(elem, self.game.hero)
            if elemButton.rightClicked:
                rightAction(elem, self.game.hero)

    def drawPotion(self, x, y, i, event):
        """Draws a potion button"""
        from config import potions
        spellsFont = pygame.font.SysFont('comicsansms', 15)
        spell = potions[i]
        self.drawItem(spell, x, y, event, action=lambda elem, hero: elem.activate(hero))
        txt = spellsFont.render(spell.name + ": " + str(spell.price) + " mana", True, (255, 255, 255))
        self.screen.blit(txt, (x + (self.tileSize - txt.get_width()) / 2, y + self.tileSize + 5))

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
        self.drawBarImage(statsX, statsY, 10, lambda i: "assets/gui/sidebar/heart_fg.png" if i < self.game.hero.hp else "assets/gui/sidebar/heart_bg.png", statsW, sizeImage=self.tileSize * 0.75)
        self.drawBarImage(statsX, statsY + self.tileSize * 2.7, self.game.hero.satietyMax, lambda i: "assets/foods/chunk.png" if i < self.game.hero.satiety else "assets/gui/sidebar/food_bg.png", statsW,
                          nbCol=10)
        self.drawBarImage(statsX, statsY + self.tileSize * 3.7, self.game.hero.manaMax, lambda i: "assets/items/mana.png" if i < self.game.hero.mana else "assets/gui/sidebar/mana_bg.png", statsW, nbCol=10)

        # Spells
        from config import potions
        spellsX, spellsY = statsX, statsY + statsH + 20
        spellsW, spellsH = boxW - 40, self.tileSize + 25
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
            ("heal", "assets/gui/sidebar/letterR.png", 0.7),
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
        heroY = y
        heroW = w - (equipmentTileW + 20) * 2
        heroH = h - 50
        heroImgX, heroImgY, heroImgW, heroImgH = drawImage(self.screen, "assets/hero/hero.png", heroX, heroY, heroW, heroH)

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
            self.drawItem(equipmentRightTiles[equipmentI], equipmentTileRightX, equipmentTileRightY + equipmentTileH * equipmentI, event)

        # Stats
        statsX, statsY = heroX, heroImgY + heroImgH + 5
        statsW, statsH = heroW / 2 - 20, 30
        statsFont = pygame.font.SysFont('comicsansms', 20)
        drawImage(self.screen, "assets/equipments/sword/sword1.png", statsX, statsY, statsW, statsH)
        strengthTxt = statsFont.render(str(self.game.hero.strengthTot()), True, (255, 255, 255))
        self.screen.blit(strengthTxt, (statsX + (statsW - strengthTxt.get_width()) / 2, statsY + statsH))
        drawImage(self.screen, "assets/equipments/shield/shield2.png", statsX + statsW + 40, statsY, statsW, statsH)
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
        buttonsY = self.h / 1.3
        close_button = Button(20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.7 / 5), buttonsY, (self.w - 20 * self.tileSize) * (1.5 / 5), self.h * (1 / 10))
        replay_button = Button(20 * self.tileSize + (self.w - 20 * self.tileSize) * (2.8 / 5), buttonsY, (self.w - 20 * self.tileSize) * (1.5 / 5), self.h * (1 / 10))
        font = pygame.font.SysFont('comicsansms', int((self.w - 20 * self.tileSize) * 0.05))
        font1 = pygame.font.SysFont('comicsansms', int((self.w - 20 * self.tileSize) * 0.07))
        posHero = self.game.floor.pos(self.game.hero)
        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/grounds/ground.png"), self.getTileSurface(self.game.hero)), self.getTilePos(posHero.x, posHero.y, self.game.hero))
        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/hero/grave.png"), self.getTileSurface(self.game.hero)), self.getTilePos(posHero.x, posHero.y, self.game.hero))
        self.game.hero.image = "assets/hero/grave.png"
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.tileSize * self.game.floor.size + 20, 20, self.w - self.tileSize * self.game.floor.size - 40, self.h - 40))
        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/gui/end_screen/gameOver.png"), (self.w - self.tileSize * self.game.floor.size - 40, self.h * (1 / 3))),
                         (self.tileSize * self.game.floor.size + 20, 20))
        self.screen.blit(font1.render("SCORE:", True, (255, 255, 255)), (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (0.9 / 3)))
        self.screen.blit(font.render("hero level: " + str(self.game.hero.lvl), True, (255, 255, 255)), (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (1.3 / 3)))
        self.screen.blit(font.render("rooms visited: " + str(self.game.level), True, (255, 255, 255)), (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (1.6 / 3)))
        self.screen.blit(font.render("monsters killed: " + str(self.game.hero.monstersKilled), True, (255, 255, 255)),
                         (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (1.9 / 3)))

        close_button.drawImage(self.screen, "assets/gui/end_screen/exitButton.png")
        replay_button.drawImage(self.screen, "assets/gui/end_screen/restartButton.png")
        self.gameMap(pygame.event.Event(pygame.NOEVENT))
        pygame.display.flip()

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                import sys
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self.updateScreenSize(event.size[0], event.size[1])
            elif event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
                continue

            close_button.drawImage(self.screen, "assets/gui/end_screen/exitButton.png", event)
            if close_button.clicked:
                pygame.quit()
                import sys
                sys.exit()
            replay_button.drawImage(self.screen, "assets/gui/end_screen/restartButton.png", event)
            if replay_button.clicked:
                self.game.__init__()
                self.game.buildFloor()
                self.main()
                break
            pygame.display.flip()
            if debug:
                print("End screen updated:", pygame.event.event_name(event.type))
