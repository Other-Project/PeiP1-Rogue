def main(game):
    import sys, pygame

    pygame.init()

    size = width, height = 1080, 720
    black = 0, 0, 0
    tileSize = min(width,height)/game.floor.size
    screen = pygame.display.set_mode(size)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT : sys.exit()
        screen.fill(black)
        for y in range(len(game.floor)):
            for x in range(len(game.floor)):
                e = game.floor._mat[y][x]
                if e is None:
                    screen.blit(pygame.transform.scale(pygame.image.load("assets/other/lave.png"), (tileSize, tileSize)), (x*tileSize, y*tileSize))
                else:
                    screen.blit(pygame.transform.scale(pygame.image.load("assets/other/ground.png"), (tileSize, tileSize)), (x*tileSize, y*tileSize))
                    if e.image is not None:
                        screen.blit(pygame.transform.scale(pygame.image.load(e.image), (tileSize, tileSize)), (x*tileSize, y*tileSize))
        pygame.display.flip()

