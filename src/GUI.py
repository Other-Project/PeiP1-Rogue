def printMsg(game):
    msg = game.readMessages()
    if msg is not None and msg != "":
        print(msg)


def main(game):
    import sys
    import pygame
    from Coord import Coord
    pygame.init()

    size = width, height = 1080, 720
    black = 0, 0, 0
    tileSize = min(width, height) / game.floor.size
    screen = pygame.display.set_mode(size)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                game.newTurn(event.key)
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(black)
        for y in range(len(game.floor)):
            for x in range(len(game.floor)):
                e = game.floor.get(Coord(x, y))
                if e is None:
                    screen.blit(pygame.transform.scale(pygame.image.load("assets/other/lava.png"), (tileSize, tileSize)), (x * tileSize, y * tileSize))
                else:
                    screen.blit(pygame.transform.scale(pygame.image.load("assets/other/ground.png"), (tileSize, tileSize)), (x * tileSize, y * tileSize))
                    if e.image is not None:
                        screen.blit(pygame.transform.scale(pygame.image.load(e.image), (tileSize, tileSize)), (x * tileSize, y * tileSize))
        printMsg(game)
        pygame.display.flip()
        if game.hero.hp <= 0:
            game.addMessage("--- Game Over! ---")
            printMsg(game)
            pygame.quit()
            break
