import sys
import time
from Level1 import Level1
from Settings import *

class Levels:
    def __init__(self):
        self.SURFACE = pygame.display.get_surface()
        self.running = True

    def run(self):
        # --------------------------------LEVELS------------------------------------------#
        level1 = Level1()
        # -----------------------------------LOOP---------------------------------------------#
        previous_time = time.time()
        while self.running:
            dt = time.time() - previous_time
            previous_time = time.time()
            # ----------------------------------------------------------------------------#
            level1.run()
            self.running = False
            # ----------------------------------------------------------------------------#
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            # ----------------------------------------------------------------------------#
            pygame.display.update()
            CLOCK.tick(60)
        self.running = True
