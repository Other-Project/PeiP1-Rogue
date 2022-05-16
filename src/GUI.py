import pygame

#button class
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()
		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))
		return action

def printMsg(game):
    msg = game.readMessages()
    if msg is not None and msg != "":
        print(msg)


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
    screen.blit(pygame.transform.scale(pygame.image.load("assets/other/arcade.png"), (infoObject.current_w,infoObject.current_h)), (0, 0))
    start_button = Button((infoObject.current_w/2)-348/2, (infoObject.current_h/2)+149, pygame.image.load("assets/other/startButton.png"), 1)
    while 1:
            for event in pygame.event.get():
                if start_button.draw(screen):
                    screen.fill(black)
                if event.type == pygame.KEYDOWN:
                    game.newTurn(event.key)
                if event.type == pygame.QUIT:
                    sys.exit()
            if start_button.clicked:
                screen.fill(black)
                for y in range(len(game.floor)):
                    for x in range(len(game.floor)):
                        e = game.floor.get(Coord(x, y))
                        if e is None:
                            screen.blit(pygame.transform.scale(pygame.image.load("assets/other/lava.png"), (tileSize, tileSize)), (x*tileSize, y*tileSize))
                        else:
                            screen.blit(pygame.transform.scale(pygame.image.load("assets/other/ground.png"), (tileSize, tileSize)), (x*tileSize, y*tileSize))
                            if e.image is not None:
                                screen.blit(pygame.transform.scale(pygame.image.load(e.image), (tileSize, tileSize)), (x*tileSize, y*tileSize))
                printMsg(game)
                pygame.display.flip()
                if game.hero.hp <= 0:
                    game.addMessage("--- Game Over! ---")
                    printMsg(game)
                    pygame.quit()
                    break
            pygame.display.flip()
