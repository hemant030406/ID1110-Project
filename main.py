import math
import pygame
from basic_functions import rotation_about_center,text_align

class BaseCar:

    # Initialization of the base class
    def __init__(self, max_velocity, rot_velocity):
        self.img = self.IMAGE
        self.max_velocity = max_velocity
        self.velocity = 0
        self.rot_velocity = rot_velocity
        self.angle = 0
        self.x, self.y = self.STARTING_POSITION
        self.accln = 0.1

    # A function which defines forward movement of the cars
    def move_fwd(self):
        self.velocity = min(self.velocity + self.accln, self.max_velocity)
        self.move()

    # A function defining backward movement of the cars
    def move_bwd(self):
        self.velocity = max(self.velocity - self.accln, -self.max_velocity / 2)
        self.move()

    # Defining a function which will define left and right movement i.e.,
    # rotation of the cars
    def rotation(self, left=False, right=False):
        if left:
            self.angle += self.rot_velocity
        elif right:
            self.angle -= self.rot_velocity

    # A function which will actually rotate the cars about the centre
    def draw(self, window):
        rotation_about_center(window, self.img, (self.x, self.y), self.angle)

    # A function to allow the cars to move in the exact forward and backward
    # direction while they're rotated by some angle
    def move(self):
        rad = math.radians(self.angle)
        vertical_velocity = math.cos(rad) * self.velocity
        horizontal_velocity = math.sin(rad) * self.velocity

        self.y -= vertical_velocity
        self.x -= horizontal_velocity

    # Defining collision
    def collision(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = ((self.x - x), (self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    # Defining reset function
    def reset(self):
        self.x, self.y = self.STARTING_POSITION
        self.angle = 0
        self.velocity = 0


# Creating class for player car which inherits the base class
class PlayerCar(BaseCar):

    # Creating variables for player car
    count = 0
    IMAGE = PLAYER_CAR
    STARTING_POSITION = (185, 200)

    # Defining a function which will lead to bouncing back when the car
    # collides
    def bounce_back(self):
        self.velocity = -0.8 * self.velocity
        self.move()

    # A function to reduce the speed of the player car when needed
    def speed_reduction(self):
        self.velocity = max(self.velocity - self.accln / 2, 0)
        self.move()

    # Defining a function for brake application in player car
    def brake(self):
        self.velocity = 0

    # Boost function to boost the speed of the player car once
    def boost(self):
        if self.count <= 1:
            self.velocity = 6


# Function which lists down some commands and resulting actions for the
# movement of the player car
def move_player(player_car):

    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotation(left=True)
    if keys[pygame.K_d]:
        player_car.rotation(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_fwd()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_bwd()
    if keys[pygame.K_f]:
        player_car.brake()
    if keys[pygame.K_e]:
        if pygame.KEYUP:
            player_car.count += 1
        player_car.boost()

    if not moved:
        player_car.speed_reduction()
    
# Variables for main game loop
run = True
clock = pygame.time.Clock()
images = [(BACKGROUND, (0, 0)), (PATH, (0, 0)),
          (RACE_FINISH, RACE_FINISH_POSITION), (RACE_TRACK_BORDER, (0, 0))]
player_car = PlayerCar(4, 4)
computer_car = ComputerCar(1.5, 4, PATH_COORDINATES)
game_info = GameData()

# Main game loop
while run:
    clock.tick(FPS)

    draw(WINDOW, images, player_car, computer_car, game_info)

    # Event handling and game loop updates before a level has begun
    while not game_info.began:
        text_align(
            WINDOW,
            GAME_FONT,
            f"Press any key to start level {game_info.level}!")
        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                game_info.begin_lvl()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        # #To get points for path of computer car using mouse

        # if event.type==pygame.MOUSEBUTTONDOWN:
        #     pos=pygame.mouse.get_pos()
        #     computer_car.path.append(pos)

    move_player(player_car)
    computer_car.move()

    handle_collision(player_car, computer_car, game_info)

    # Game updates after completing all level
    if game_info.game_completed():
        pygame.mixer.Sound.play(
            pygame.mixer.Sound('songs\\game_completed.mp3'))
        text_align(WINDOW, GAME_FONT, "You won the game!")
        pygame.display.update()
        pygame.time.wait(3400)
        pygame.quit()

        # #To be used instead of quit if the game is to be reset after finishing all levels

        # game_info.reset()
        # player_car.reset()
        # computer_car.resett()

# #Printing the computer car path developed using mouse

# print(computer_car.path)

# Quit the game and exit Pygame
pygame.quit()