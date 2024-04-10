import pygame
import sys

# Initialisation de Pygame


# Définition des couleurs
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Classe représentant la balle
class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

# Classe représentant les pads
class Paddle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

# Fonction pour effacer l'écran
def clear_screen(surface):
    surface.fill(black)

# Fonction principale
def main():
    running = True
    clock = pygame.time.Clock()

    ball = Ball(canvas_width // 2, canvas_height // 2, 10, white)
    left_paddle = Paddle(20, canvas_height // 2 - 50, 20, 100, red)
    right_paddle = Paddle(canvas_width - 40, canvas_height // 2 - 50, 20, 100, blue)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clear_screen(canvas)

        # Dessin des éléments
        left_paddle.draw(canvas)
        right_paddle.draw(canvas)
        ball.draw(canvas)

        # Mise à jour de l'affichage
        pygame.display.flip()

        # Limiter le nombre de FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
