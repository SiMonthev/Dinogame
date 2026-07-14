import pygame
import random

pygame.init()
pygame.mixer.init()


width, height = 900, 450
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dino Game")

dino_img = pygame.image.load("dino.jpg")
dino_img.set_colorkey((245, 245, 245))

obstacle_img = pygame.image.load("cactus.png")

ground_img = pygame.image.load("ground.jpg")

obstacle2_img = pygame.image.load("cactus2.webp")
obstacle2_img.set_colorkey((255, 255, 255))

dino_img = pygame.transform.scale(dino_img, (60, 60))
obstacle_img = pygame.transform.scale(obstacle_img, (30, 60))
ground_img = pygame.transform.scale(ground_img, (width, 100))
obstacle2_img = pygame.transform.scale(obstacle2_img, (30, 65))


jump_sound = pygame.mixer.Sound("jump sound.wav")
error_sound = pygame.mixer.Sound("error sound.wav")
pygame.mixer.music.load("theme song.wav")

jump_sound.set_volume(1.0)
error_sound.set_volume(1.0)
pygame.mixer.music.set_volume(0.3)

class Dinosaur:
    def __init__(self):
        self.image = dino_img
        self.x = 50
        self.y = height - self.image.get_height() - 50
        self.vel_y = 0
        self.gravity = 1
        self.jump_height = -15
        self.is_jumping = False
        self.rect = pygame.Rect(self.x, self.y,
                                self.image.get_width(), self.image.get_height())

    def update(self):
        if self.is_jumping:
            self.vel_y += self.gravity
            self.y += self.vel_y

            if self.y >= height - self.image.get_height() - 50:
                self.y = height - self.image.get_height() - 50
                self.is_jumping = False

        self.rect.topleft = (self.x, self.y)

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.vel_y = self.jump_height

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, vel):
        self.image = image
        self.x = width
        self.y = height - self.image.get_height() - 60
        self.vel = vel
        self.rect = pygame.Rect(self.x, self.y,
                                self.image.get_width(), self.image.get_height())

    def update(self):
        self.x -= self.vel

        if self.x <= -self.image.get_width():
            self.x = width + random.randint(200, 500)
            return True

        self.rect.topleft = (self.x, self.y)
        return False    

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Ground:
    def __init__(self):
        self.image = ground_img
        self.x = 0
        self.vel = 6
        self.rect = pygame.Rect(self.x, height - 100, width, 50)

    def update(self):
        self.x -= self.vel
        if self.x <= -width:
            self.x = 0
        self.rect.topleft = (self.x, height - 100)

    def draw(self, win):
        win.blit(self.image, (self.x, height - 100))
        win.blit(self.image, (self.x + width, height - 100))


def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font("PressStart2P-Regular.ttf", 30)

    run = True
    game_active = False
    initial_start = True
    music_playing = False

    score = 0
    record = 0
    jump_count = 0

    dino = Dinosaur()
    obstacle = Obstacle(obstacle_img, 12)
    obstacle2 = Obstacle(obstacle2_img, 10)
    obstacle2.x = width + 300 
    ground = Ground()

    while run:
        clock.tick(30)
        win.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump_sound.play()
                    jump_count += 1

                    if not game_active:
                        dino = Dinosaur()
                        obstacle = Obstacle(obstacle_img, 12)
                        obstacle2 = Obstacle(obstacle2_img, 10)
                        obstacle2.x = width + 300
                        ground = Ground()
                        score = 0
                        game_active = True
                        initial_start = False
                    else:
                        dino.jump()

        if game_active:
            if not music_playing:
                pygame.mixer.music.play(-1)
                music_playing = True
                
            dino.update()
            passed1 =obstacle.update()
            passed2 =obstacle2.update()
            ground.update()

            speed = 12 + score // 10
            obstacle.vel = speed
            obstacle2.vel = speed

            if dino.rect.colliderect(obstacle.rect) or dino.rect.colliderect(obstacle2.rect):
                pygame.mixer.music.stop()
                music_playing = False 
                error_sound.play()
                game_active = False
                jump_count = 0

            if passed1:
                score += 1

            if passed2:
                score += 1

            if score > record:
                record = score
                
            if score >= 100:
                win.fill((0, 255, 0))

            ground.draw(win)
            dino.draw(win)
            obstacle.draw(win)
            obstacle2.draw(win)

            score_text = font.render("Score:" + str(score), True, (0, 0, 0))
            record_text = font.render("Record:" + str(record), True, (0, 0, 0))
            jump_count_text = font.render("Jumps:" + str(jump_count), True, (0, 0, 0))

            win.blit(score_text, (10, 10))
            win.blit(record_text, (width - 290, 10))
            win.blit(jump_count_text, (10, 50))

        else:
            if initial_start:
                start_text = font.render("To Start Press Space", True, (0, 0, 0))
                win.blit(start_text,
                         (width // 2 - start_text.get_width() // 2,
                          height // 2 - start_text.get_height() // 2))
            else:
                game_over_text = font.render("Wanna try again?", True, (0, 0, 0))
                game_over_text2 = font.render("Press Space to Start", True, (0, 0, 0))

                win.blit(game_over_text,
                         (width // 2 - game_over_text.get_width() // 2,
                          height // 2 - game_over_text.get_height() // 2))

                win.blit(game_over_text2,
                         (width // 2 - game_over_text2.get_width() // 2,
                          height // 3 - game_over_text2.get_height() // 2))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()