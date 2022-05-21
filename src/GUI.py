import pygame
import time

class Button:
    """Button class"""
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action


messages = None
def printMsg(game):
    global messages
    msg = game.readMessages()
    if msg is not None and msg != "":
        messages = msg
        return msg
    else:
        return messages


def main(game):
    import sys
    import pygame
    from Coord import Coord
    pygame.init()
    black = 0, 0, 0
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
    tileSize = min(infoObject.current_w, infoObject.current_h) / game.floor.size
    screen.fill((255, 255, 255))
    screen.blit(pygame.transform.scale(pygame.image.load("assets/other/arcade.png"), (infoObject.current_w, infoObject.current_h)), (0, 0))
    start_button = Button((infoObject.current_w / 2) - 348 / 2, (infoObject.current_h / 2) + 149, pygame.image.load("assets/other/startButton.png"), 1)
    close_button = Button(infoObject.current_w*(2/3)-75, (infoObject.current_h / 1.3), pygame.image.load("assets/other/exitButton.png"), 2)
    replay_button = Button(infoObject.current_w*(4/5), (infoObject.current_h / 1.3), pygame.image.load("assets/other/restartButton.png"), 2)
    font = pygame.font.SysFont(None, 20)
    img1 = font.render("strength:"+str(game.hero.strength), True, (255, 255, 255))
    img2 = font.render("armor:"+str(game.hero.armor), True, (255, 255, 255))
    img3 = font.render("xp:"+str(game.hero.exp), True, (255, 255, 255))
    #img4 = font.render("level:"+str(game.hero.level), True, (255, 255, 255))
    img5 = font.render("move:", True, (255, 255, 255))
    img6 = font.render("skip one turn:", True, (255, 255, 255))
    img7 = font.render("destroy an object: right click", True, (255, 255, 255))
    img8 = font.render("suicide:", True, (255, 255, 255))
    font1 = pygame.font.SysFont(None, 75)
    img9 = font1.render("---Game Over---", True, (255, 255, 255))


    x=0
    while 1:
        for event in pygame.event.get():
            if start_button.draw(screen):
                screen.fill(black)
            if event.type == pygame.KEYDOWN:
                game.newTurn(event.key)
            if event.type == pygame.QUIT:
                sys.exit()
        if start_button.clicked:
            Startps=time.time()
            screen.fill((75,75,75))
            pygame.draw.rect(screen, (64, 64, 64),pygame.Rect(tileSize * game.floor.size + 20, 20, infoObject.current_w - tileSize * game.floor.size - 40, infoObject.current_h - 40))
            #boite de texte
            img = font.render(str(printMsg(game)), True, (255, 255, 255))
            pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(infoObject.current_w * (3 / 5), infoObject.current_h / 2+80, tileSize*13, tileSize*2))
            screen.blit(img, (infoObject.current_w * (3 / 5)+5, infoObject.current_h / 2+80, tileSize*13, tileSize*2+5))
            #dessine le héro de l'inventaire
            screen.blit(pygame.transform.scale(pygame.image.load("assets/hero/frontHero.png"), (tileSize*5, tileSize*5)), (infoObject.current_w*(4/5), 40))
            #dessine les cases pour armes
            pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(infoObject.current_w*(4.65/5), 75, tileSize, tileSize))
            pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(infoObject.current_w * (4.65 / 5), 125, tileSize, tileSize))
            #dessine les cases pour les armures
            pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(infoObject.current_w * (3.95 / 5), 40, tileSize, tileSize))
            pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(infoObject.current_w * (3.95 / 5), 90, tileSize, tileSize))
            pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(infoObject.current_w * (3.95 / 5), 140, tileSize, tileSize))
            pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(infoObject.current_w * (3.95 / 5), 190, tileSize, tileSize))
            #caractéristiques du héro
            screen.blit(img1, (infoObject.current_w*(4.2/5), 280))
            screen.blit(img2, (infoObject.current_w*(4.2/5), 300))
            screen.blit(img3, (infoObject.current_w*(4.2/5), 260))
            #screen.blit(img4, (infoObject.current_w*(4.2/5), 240))
            #regles du jeu
            screen.blit(img5, (infoObject.current_w * (3 / 5), infoObject.current_h *(8.5/10)))
            screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterZ.png"), (tileSize*0.7, tileSize*0.7)), (infoObject.current_w * (3 / 5)+100, infoObject.current_h *(8.5/10)-40))
            screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterQ.png"), (tileSize * 0.7, tileSize * 0.7)),
                        (infoObject.current_w * (3 / 5) + 60, infoObject.current_h * (8.5 / 10) ))
            screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterS.png"), (tileSize * 0.7, tileSize * 0.71)),
                        (infoObject.current_w * (3 / 5) + 100, infoObject.current_h * (8.5 / 10)))
            screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterD.png"), (tileSize * 0.7, tileSize * 0.7)),
                        (infoObject.current_w * (3 / 5) + 140, infoObject.current_h * (8.5 / 10) ))
            screen.blit(img6, (infoObject.current_w * (4 / 5), infoObject.current_h * (9.3 / 10)))
            screen.blit(pygame.transform.scale(pygame.image.load("assets/other/spaceBar.png"), (tileSize * 3, tileSize * 0.7)),
                        (infoObject.current_w * (4.35 / 5), infoObject.current_h * (9.23 / 10)))
            screen.blit(img7, (infoObject.current_w * (4 / 5), infoObject.current_h *(8.5/10)))
            screen.blit(img8, (infoObject.current_w * (3 / 5), infoObject.current_h * (9.3 / 10)))
            for y in range(len(game.floor)):
                for x in range(len(game.floor)):
                    e = game.floor.get(Coord(x, y))
                    if e is None:
                        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/lava.png"), (tileSize, tileSize)), (x * tileSize, y * tileSize))
                    else:
                        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/ground.png"), (tileSize, tileSize)), (x * tileSize, y * tileSize))
                        if e.image is not None:
                            screen.blit(pygame.transform.scale(pygame.image.load(e.image), (tileSize, tileSize)), (x * tileSize, y * tileSize))
            for nbrElemMax in range(0,12):
                pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(tileSize * game.floor.size + 20 + x, infoObject.current_h/2, tileSize, tileSize))
                x += 50
            x = 0
            for nbrElem in game.hero.inventory:
                screen.blit(pygame.transform.scale(pygame.image.load(nbrElem.image), (tileSize, tileSize)), (tileSize * game.floor.size + 37 + x, infoObject.current_h/2))
                x += 50
            x = 0
            xx = 0
            y=infoObject.current_h / 20
            for nbrHeartMax in range(0, 11):
                if nbrHeartMax<6:
                    screen.blit(pygame.transform.scale(pygame.image.load("assets/other/heartGrey.png"), (tileSize*0.5, tileSize*0.5)), (tileSize * game.floor.size + 37 + x, y))
                    x += 50
                else:
                    y = infoObject.current_h / 20+50
                    screen.blit(pygame.transform.scale(pygame.image.load("assets/other/heartGrey.png"), (tileSize*0.5, tileSize*0.5)), (tileSize * game.floor.size + 37 + xx, y))
                    xx += 50
            x = 0
            y = infoObject.current_h / 20
            xx = 0
            for nbrHeart in range(game.hero.hp):
                if nbrHeart<6:
                    screen.blit(pygame.transform.scale(pygame.image.load("assets/other/heartRed.png"), (tileSize*0.5, tileSize*0.5)), (tileSize * game.floor.size + 37 + x, y))
                    x += 50
                else:
                    x = 0
                    y = infoObject.current_h / 20+50
                    screen.blit(pygame.transform.scale(pygame.image.load("assets/other/heartRed.png"), (tileSize*0.5, tileSize*0.5)), (tileSize * game.floor.size + 37 + xx, y))
            printMsg(game)
            pygame.display.flip()
            if game.hero.hp <= 0:
                game.hero.image= "assets/other/graveHero.png"
                pygame.draw.rect(screen, (0, 0, 0),
                pygame.Rect(tileSize * game.floor.size + 20, 20, infoObject.current_w - tileSize * game.floor.size - 40, infoObject.current_h - 40))
                screen.blit(img9, ((infoObject.current_w*(1.9/3)), (infoObject.current_h/10)))
                close_button.draw(screen)
                replay_button.draw(screen)
                screen.blit(font.render("time:"+str(round(Startps-time.time())), True, (255,255,255)), (infoObject.current_w * (3 / 5), infoObject.current_h * (8.5 / 10)))
                if close_button.clicked:
                    pygame.quit()
                if replay_button.clicked:
                    pass
        pygame.display.flip()
