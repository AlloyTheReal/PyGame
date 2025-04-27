import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Couleurs
BLACK = (0, 0, 0)

# Classe pour le vaisseau
class Ship:
    def __init__(self):
        self.image = pygame.image.load("ship.png")  # Chargez votre image de vaisseau
        self.image = pygame.transform.scale(self.image, (50, 30))  # Réduire la taille du vaisseau
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 5
        self.health = 5  # Définir la santé à 5 PV

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Limiter le vaisseau à l'écran
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.rect.y))

# Classe pour les ennemis
class Enemy:
    def __init__(self):
        self.image = pygame.image.load("enemy.png")  # Chargez votre image d'ennemi
        self.image = pygame.transform.scale(self.image, (40, 40))  # Réduire la taille de l'ennemi
        self.rect = self.image.get_rect(center=(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
        self.speed = random.randint(3, 5)  # Augmenter la vitesse des ennemis

    def update(self):
        # Déplacez l'ennemi vers le bas
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, SCREEN_WIDTH)

# Fonction principale
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Galactic Explorer")
    clock = pygame.time.Clock()

    # Chargement de l'arrière-plan
    background = pygame.image.load("background.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Ajuster la taille de l'arrière-plan

    ship = Ship()
    enemies = [Enemy() for _ in range(5)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ship.update()
        for enemy in enemies:
            enemy.update()

        # Vérifiez les collisions
        for enemy in enemies:
            if ship.rect.colliderect(enemy.rect):
                ship.health -= 1
                enemy.rect.y = random.randint(-100, -40)  # Réinitialiser l'ennemi

        # Vérifiez si la santé du vaisseau est à 0
        if ship.health <= 0:
            game_over(screen)

        # Affichage
        screen.blit(background, (0, 0))
        screen.blit(ship.image, ship.rect)
        for enemy in enemies:
            screen.blit(enemy.image, enemy.rect)

        # Affichage de la santé
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {ship.health}", True, (255, 255, 255))
        screen.blit(health_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

def game_over(screen):
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Attendre 2 secondes avant de quitter
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()