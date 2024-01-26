import pygame
from random import randint
from numpy import floor
from perlin_noise import PerlinNoise
import json
import os


class Cell:
    def __init__(self, coords, type="grass", forest=False, boat=False, building=False):
        self.coords = coords
        self.type = type
        self.forest = forest
        self.boat = boat
        self.building = building
        self.buttons = None

    def draw(self, x, y):
        global screen, board
        if self.type == "grass":
            image = pygame.image.load("data/grass.png")
            image = pygame.transform.scale(image, (100, 100))
            screen.blit(image, (x, y))
            if self.forest:
                image = pygame.image.load("data/tree.png")
                image = pygame.transform.scale(image, (80, 80))
                screen.blit(image, (x + 10, y + 10))
            if self.building:
                image = pygame.image.load(
                    f"data/{self.building.name}{self.building.level if self.building.level is not False else ''}.png")
                image = pygame.transform.scale(image, (80, 80))
                screen.blit(image, (x + 10, y + 10))
            if self.coords == board.player:
                image = pygame.image.load("data/player.png")
                image = pygame.transform.scale(image, (60, 80))
                screen.blit(image, (x + 20, y + 10))
        elif self.type == "water":
            image = pygame.image.load("data/water.jpg")
            image = pygame.transform.scale(image, (100, 100))
            screen.blit(image, (x, y))
            if self.building:
                image = pygame.image.load(
                    f"data/{self.building.name}{self.building.level if self.building.level is not False else ''}.png")
                image = pygame.transform.scale(image, (80, 80))
                screen.blit(image, (x + 10, y + 10))
            if self.boat:
                if self.coords == board.player:
                    image = pygame.image.load("data/player.png")
                    image = pygame.transform.scale(image, (60, 80))
                    screen.blit(image, (x + 20, y + 10))
                image = pygame.image.load("data/boat.png")
                image = pygame.transform.scale(image, (80, 40))
                screen.blit(image, (x + 10, y + 50))
        else:
            image = pygame.image.load("data/grass.png")
            image = pygame.transform.scale(image, (100, 100))
            screen.blit(image, (x, y))
            if self.type == "mountains":
                image = pygame.image.load("data/mountains.png")
                image = pygame.transform.scale(image, (100, 100))
                screen.blit(image, (x, y))
            else:
                image = pygame.image.load("data/gold-mountains.png")
                image = pygame.transform.scale(image, (100, 100))
                screen.blit(image, (x, y))
            if self.building is not False:
                image = pygame.image.load(f"data/{self.building.name}.png")
                image = pygame.transform.scale(image, (80, 80))
                screen.blit(image, (x + 10, y + 10))

    def gen_buttons(self):
        global board
        if not self.building:
            self.buttons = []
            if self.type == "grass" and not self.forest:
                for y1 in range(self.coords[1] - 6, self.coords[1] + 7):
                    a = False
                    for x1 in range(self.coords[0] - 6, self.coords[0] + 7):
                        try:
                            if board.cells[(x1, y1)].building.name == "home":
                                a = True
                                break
                        except Exception:
                            pass
                    if a:
                        break
                if not a:
                    if len(board.town) < 5:
                        self.buttons.append(
                            Button(860, 300, 150, 80, Building("home", 1000 * len(board.town), 10, "w", "f")))
                    else:
                        self.buttons.append(
                            Button(860, 300, 150, 80, Building("home", 1000 * len(board.town), 10, "m", "m")))
            home_ryadom = False
            for y1 in range(self.coords[1] - 3, self.coords[1] + 4):
                for x1 in range(self.coords[0] - 3, self.coords[0] + 4):
                    try:
                        if board.cells[(x1, y1)].building.name == "home":
                            home_ryadom = True
                            break
                    except Exception:
                        pass
                if home_ryadom:
                    break
            if home_ryadom:
                if self.forest:
                    self.buttons.append(Button(720, 300, 150, 100, Building("lesopilka", 10, 1, "f", "w", 1)))
                elif self.type == "water":
                    abc = False
                    for coords in [(self.coords[0] - 1, self.coords[1]), (self.coords[0], self.coords[1] + 1),
                                   (self.coords[0] + 1, self.coords[1]), (self.coords[0], self.coords[1] - 1)]:
                        try:
                            if board.cells[coords].type != self.type:
                                abc = True
                                break
                        except Exception:
                            pass
                    if abc:
                        self.buttons.append(Button(720, 300, 150, 100, Building("port", 50, 1, "w", "f")))
                elif self.type == "grass":
                    for y1 in range(self.coords[1] - 2, self.coords[1] + 3):
                        a = False
                        for x1 in range(self.coords[0] - 2, self.coords[0] + 3):
                            try:
                                if board.cells[(x1, y1)].type == "water":
                                    a = True
                            except Exception:
                                pass
                        if a:
                            break
                    if a:
                        self.buttons.append(Button(720, 300, 150, 100, Building("ferma", 50, 1, "w", "f", 1)))
                elif self.type == "mountains":
                    self.buttons.append(Button(720, 300, 150, 100, Building("mine-stone", 100, 1, "w", "s")))
                elif self.type == "gold-mountains":
                    self.buttons.append(Button(720, 300, 150, 100, Building("mine-gold", 250, 1, "s", "m")))
            if len(self.buttons) == 0:
                self.buttons = None

    def to_build(self, building):
        self.building = building
        if self.building.name == "port":
            self.boat = True
        self.buttons = None


class Button:
    def __init__(self, x, y, width, height, move):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.move = move

    def draw(self):
        global screen

        image = pygame.image.load("data/classic-btn.png")
        image = pygame.transform.scale(image, (150, 80))
        screen.blit(image, (self.x, self.y))

        font = pygame.font.Font(None, 20)
        text = font.render(f"{self.move.name}", True, (0, 0, 0))
        text_x = self.x + 30
        text_y = self.y + 10
        screen.blit(text, (text_x, text_y))

        dtype = self.move.dtype
        if dtype == "m":
            image = pygame.image.load("data/money-icon.png")
            image = pygame.transform.scale(image, (20, 20))
            screen.blit(image, (self.x + 30, self.y + 30))
        elif dtype == "f":
            image = pygame.image.load("data/food-icon.png")
            image = pygame.transform.scale(image, (20, 20))
            screen.blit(image, (self.x + 30, self.y + 30))
        elif dtype == "w":
            image = pygame.image.load("data/wood-icon.png")
            image = pygame.transform.scale(image, (20, 20))
            screen.blit(image, (self.x + 30, self.y + 30))
        elif dtype == "s":
            image = pygame.image.load("data/stone-icon.png")
            image = pygame.transform.scale(image, (20, 20))
            screen.blit(image, (self.x + 30, self.y + 30))
        text = font.render(f"+{self.move.dohod}/c", True, (0, 0, 0))
        text_x = self.x + 55
        text_y = self.y + 30
        screen.blit(text, (text_x, text_y))

        ptype = self.move.ptype
        if ptype == "m":
            image = pygame.image.load("data/money-icon.png")
            image = pygame.transform.scale(image, (20, 20))
            screen.blit(image, (self.x + 30, self.y + 50))
        elif ptype == "f":
            image = pygame.image.load("data/food-icon.png")
            image = pygame.transform.scale(image, (20, 20))
            screen.blit(image, (self.x + 30, self.y + 50))
        elif ptype == "w":
            image = pygame.image.load("data/wood-icon.png")
            image = pygame.transform.scale(image, (20, 20))
            screen.blit(image, (self.x + 30, self.y + 50))
        elif ptype == "s":
            image = pygame.image.load("data/stone-icon.png")
            image = pygame.transform.scale(image, (20, 20))
            screen.blit(image, (self.x + 30, self.y + 50))
        text = font.render(f"-{self.move.price}", True, (0, 0, 0))
        text_x = self.x + 55
        text_y = self.y + 50
        screen.blit(text, (text_x, text_y))


class Building:
    def __init__(self, name, price, dohod, ptype="m", dtype="m", level=False):
        self.name = name
        self.price = price
        self.dohod = dohod
        self.ptype = ptype
        self.dtype = dtype
        self.level = level
        self.time = 0

    def update(self, t):
        global money, food, wood, stone
        if self.level is False:
            if self.dtype == "m":
                money += self.dohod * t
            elif self.dtype == "f":
                food += self.dohod * t
            elif self.dtype == "w":
                wood += self.dohod * t
            elif self.dtype == "s":
                stone += self.dohod * t
        else:
            self.time += t
            if self.time >= 1:
                self.level += 1
                self.time -= 1
                if self.level == 4:
                    self.level = 1
                    if self.dtype == "m":
                        money += self.dohod * 3
                    elif self.dtype == "f":
                        food += self.dohod * 3
                    elif self.dtype == "w":
                        wood += self.dohod * 3
                    elif self.dtype == "s":
                        stone += self.dohod * 3


class Board:
    def __init__(self, width, height, a):
        self.width = width
        self.height = height
        self.a = a
        self.town = None
        self.player = (1, 1)
        self.moves_player = None
        self.cell_choosed = None
        self.sdvig = [0, 0]
        self.buttons = None

    def new_board(self):
        noise = PerlinNoise(octaves=1, seed=randint(-10000, 10000))
        amp = 6
        period = 24
        terrain_width = self.width

        landscale = [[0 for i in range(terrain_width)] for i in range(terrain_width)]

        for position in range(terrain_width ** 2):
            x = floor(position / terrain_width)
            z = floor(position % terrain_width)
            y = floor(noise([x / period, z / period]) * amp)
            landscale[int(x)][int(z)] = int(y)

        self.cells = dict()
        for y in range(self.height):
            for x in range(self.width):
                if landscale[y][x] > 0:
                    if randint(0, 9):
                        self.cells[(x, y)] = Cell((x, y), "grass")
                        if randint(0, 3) == 0:
                            self.cells[(x, y)].forest = True
                    else:
                        if randint(0, 2):
                            self.cells[(x, y)] = Cell((x, y), "mountains")
                        else:
                            self.cells[(x, y)] = Cell((x, y), "gold-mountains")
                else:
                    self.cells[(x, y)] = Cell((x, y), "water")
        while True:
            x, y = randint(9, 240), randint(9, 240)
            if self.cells[(x, y)].type == "grass":
                if not self.cells[(x, y)].forest:
                    self.cells[(x, y)].building = Building("home", 0, 2, "m", "f")
                    self.town = [(x, y)]
                    self.player = (x, y)
                    break

        self.sdvig = [self.player[0] - 3, self.player[1] - 3]
        if self.sdvig[0] < 0:
            self.sdvig[0] = 0
        elif self.sdvig[0] > 243:
            self.sdvig[0] = 243
        if self.sdvig[1] < 0:
            self.sdvig[1] = 0
        elif self.sdvig[1] > 243:
            self.sdvig[1] = 243
        self.draw_board()

    def take_dohod(self, t):
        for y in range(self.width):
            for x in range(self.height):
                if self.cells[(x, y)].building is not False:
                    self.cells[(x, y)].building.update(t)

    def draw_board(self):
        global screen, money, food, wood, stone
        screen.fill((177, 220, 252))
        up = 10
        left = 10
        for y in range(self.sdvig[1], self.sdvig[1] + 7):
            for x in range(self.sdvig[0], self.sdvig[0] + 7):
                self.cells[(x, y)].draw(left, up)
                pygame.draw.rect(screen, (0, 0, 0), (left, up, self.a, self.a), 1)
                left += self.a
            left = 10
            up += self.a
        if self.cell_choosed is not None:
            pygame.draw.rect(screen, (255, 0, 0),
                             ((self.cell_choosed[0] - self.sdvig[0]) * self.a + 10,
                              (self.cell_choosed[1] - self.sdvig[1]) * self.a + 10, self.a, self.a),
                             2)
        if self.moves_player is not None:
            for i in range(len(self.moves_player)):
                pos = list(self.moves_player[i])
                if self.player[0] > 246:
                    pos[0] = pos[0] - self.player[0] + (self.player[0] - 243)
                elif self.player[0] != 4:
                    if pos[0] > 3:
                        pos[0] = pos[0] - self.player[0] + 3
                else:
                    pos[0] -= 1
                if self.player[1] > 246:
                    pos[1] = pos[1] - self.player[1] + (self.player[1] - 243)
                elif self.player[1] != 4:
                    if pos[1] > 3:
                        pos[1] = pos[1] - self.player[1] + 3
                else:
                    pos[1] -= 1
                pygame.draw.circle(screen, (255, 255, 255),
                                   (pos[0] * self.a + self.a // 2 + 10, pos[1] * self.a + self.a // 2 + 10),
                                   self.a // 3, 1)
                pygame.draw.circle(screen, (255, 255, 255),
                                   (pos[0] * self.a + self.a // 2 + 11, pos[1] * self.a + self.a // 2 + 10),
                                   self.a // 3, 1)
                pygame.draw.circle(screen, (255, 255, 255),
                                   (pos[0] * self.a + self.a // 2 + 10, pos[1] * self.a + self.a // 2 + 11),
                                   self.a // 3, 1)
                pygame.draw.circle(screen, (255, 255, 255),
                                   (pos[0] * self.a + self.a // 2 + 11, pos[1] * self.a + self.a // 2 + 11),
                                   self.a // 3, 1)

        for town in self.town:
            pygame.draw.rect(screen, (255, 0, 0),
                             (self.a * (town[0] - self.sdvig[0] - 3) + 10, self.a * (town[1] - self.sdvig[1] - 3) + 10,
                              700, 700), 2)

        pygame.draw.rect(screen, (177, 220, 252), (710, 0, 390, 720))
        pygame.draw.rect(screen, (177, 220, 252), (0, 0, 720, 720), 10)

        font = pygame.font.Font(None, 30)
        text = font.render(f"coords: {self.player}", True, (0, 0, 0))
        text_x = 730
        text_y = 270
        screen.blit(text, (text_x, text_y))

        text = font.render(str(int(money)), True, (0, 0, 0))
        text_x = 1025
        text_y = 10
        screen.blit(text, (text_x, text_y))
        image = pygame.image.load("data/money-icon.png")
        image = pygame.transform.scale(image, (20, 20))
        screen.blit(image, (1000, 10))

        text = font.render(str(int(food)), True, (0, 0, 0))
        text_x = 1025
        text_y = 40
        screen.blit(text, (text_x, text_y))
        image = pygame.image.load("data/food-icon.png")
        image = pygame.transform.scale(image, (20, 20))
        screen.blit(image, (1000, 40))

        text = font.render(str(int(wood)), True, (0, 0, 0))
        text_x = 1025
        text_y = 70
        screen.blit(text, (text_x, text_y))
        image = pygame.image.load("data/wood-icon.png")
        image = pygame.transform.scale(image, (20, 20))
        screen.blit(image, (1000, 70))

        text = font.render(str(int(stone)), True, (0, 0, 0))
        text_x = 1025
        text_y = 100
        screen.blit(text, (text_x, text_y))
        image = pygame.image.load("data/stone-icon.png")
        image = pygame.transform.scale(image, (20, 20))
        screen.blit(image, (1000, 100))

        if self.buttons is not None:
            for button in self.buttons:
                button.draw()

        self.minicard()

    def minicard(self):
        global screen
        left = 730
        up = 10
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[(x, y)].type == "grass":
                    pygame.draw.rect(screen, (0, 255, 0), (left, up, 1, 1))
                elif self.cells[(x, y)].type == "water":
                    pygame.draw.rect(screen, (0, 0, 255), (left, up, 1, 1))
                elif self.cells[(x, y)].type == "mountains":
                    pygame.draw.rect(screen, (125, 125, 125), (left, up, 1, 1))
                elif self.cells[(x, y)].type == "gold-mountains":
                    pygame.draw.rect(screen, (255, 255, 0), (left, up, 1, 1))
                left += 1
            left = 730
            up += 1
        for town in self.town:
            pygame.draw.rect(screen, (0, 0, 0), (town[0] + 728, town[1] + 8, 5, 5))
            pygame.draw.rect(screen, (255, 0, 0), (self.player[0] + 728, self.player[1] + 8, 5, 5))

    def clicked(self, coords):
        global money
        x, y = coords[0], coords[1]
        if 10 <= x <= 710 and 10 <= y <= 710:
            x -= 10
            y -= 10
            x = x // self.a + self.sdvig[0]
            y = y // self.a + self.sdvig[1]
            if 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1:
                if self.player == (x, y):
                    if self.moves_player is not None:
                        if self.cell_choosed is None:
                            self.cell_choosed = (x, y)
                        else:
                            if self.cell_choosed == (x, y):
                                self.cell_choosed = None
                            else:
                                self.cell_choosed = (x, y)
                        self.moves_player = None
                    else:
                        if self.cell_choosed == (x, y):
                            self.cell_choosed = None
                        elif self.cell_choosed != (x, y) or self.cell_choosed is None:
                            self.cell_choosed = None
                            self.moves_player = list()
                            for y1 in range(y - 1, y + 2):
                                for x1 in range(x - 1, x + 2):
                                    if 0 <= x1 <= self.width - 1 and 0 <= y1 <= self.height - 1:
                                        if (x1, y1) != (x, y):
                                            if self.cells[self.player].type == "grass":
                                                if self.cells[(x1, y1)].type == "grass":
                                                    self.moves_player.append((x1, y1))
                                                elif self.cells[(x1, y1)].type == "water":
                                                    if self.cells[(x1, y1)].boat:
                                                        self.moves_player.append((x1, y1))
                                            else:
                                                self.moves_player.append((x1, y1))

                elif self.moves_player is not None:
                    if (x, y) in self.moves_player:
                        if self.cells[self.player].type == "water" and self.cells[(x, y)].type == "water":
                            if not self.cells[(x, y)].boat:
                                self.cells[self.player].boat = False
                                self.cells[(x, y)].boat = True
                        self.player = (x, y)
                        self.moves_player = None
                    else:
                        self.cell_choosed = (x, y)
                        self.moves_player = None

                else:
                    if self.cell_choosed is None:
                        self.cell_choosed = (x, y)
                    else:
                        if self.cell_choosed == (x, y):
                            self.cell_choosed = None
                        else:
                            self.cell_choosed = (x, y)

                if self.cell_choosed is not None:
                    self.cells[self.cell_choosed].gen_buttons()
                    self.buttons = self.cells[self.cell_choosed].buttons
                else:
                    self.buttons = None

                self.sdvig = [self.player[0] - 3, self.player[1] - 3]
                if self.sdvig[0] < 0:
                    self.sdvig[0] = 0
                elif self.sdvig[0] > 243:
                    self.sdvig[0] = 243
                if self.sdvig[1] < 0:
                    self.sdvig[1] = 0
                elif self.sdvig[1] > 243:
                    self.sdvig[1] = 243

        elif self.buttons is not None:
            for button in self.buttons:
                if button.x <= x <= button.x + button.width and button.y <= y <= button.y + button.height:
                    global money, food, wood, stone
                    ptype = button.move.ptype
                    if ptype == "m":
                        if money >= button.move.price:
                            money -= button.move.price
                            if button.move.name == "home":
                                self.town.append(self.cell_choosed)
                            self.cells[self.cell_choosed].to_build(button.move)
                            self.buttons = None
                            break
                    elif ptype == "f":
                        if food >= button.move.price:
                            food -= button.move.price
                            if button.move.name == "home":
                                self.town.append(self.cell_choosed)
                            self.cells[self.cell_choosed].to_build(button.move)
                            self.buttons = None
                            break
                    elif ptype == "w":
                        if wood >= button.move.price:
                            wood -= button.move.price
                            if button.move.name == "home":
                                self.town.append(self.cell_choosed)
                            self.cells[self.cell_choosed].to_build(button.move)
                            self.buttons = None
                            break
                    elif ptype == "s":
                        if stone >= button.move.price:
                            stone -= button.move.price
                            if button.move.name == "home":
                                self.town.append(self.cell_choosed)
                            self.cells[self.cell_choosed].to_build(button.move)
                            self.buttons = None
                            break

    def move(self, moves):
        if self.cell_choosed is not None and len(moves) > 0:
            coords = list(self.cell_choosed)
            for move in moves:
                if move == "left":
                    if coords[0] != 0 and coords[0] != self.player[0] - 3:
                        coords[0] -= 1
                elif move == "right":
                    if coords[0] != self.width - 1 and coords[0] != self.player[0] + 3:
                        coords[0] += 1
                elif move == "up":
                    if coords[1] != 0 and coords[1] != self.player[1] - 3:
                        coords[1] -= 1
                elif move == "down":
                    if coords[1] != self.height - 1 and coords[1] != self.player[1] + 3:
                        coords[1] += 1
            self.cell_choosed = tuple(coords)
            self.cells[self.cell_choosed].gen_buttons()
            self.buttons = self.cells[self.cell_choosed].buttons

    def save(self):
        global money, food, wood, stone
        cells_json = dict()

        for x, y in self.cells.keys():
            coords = f"{x} {y}"
            cells_json[coords] = dict()
            cells_json[coords]["type"] = self.cells[(x, y)].type
            cells_json[coords]["forest"] = self.cells[(x, y)].forest
            cells_json[coords]["boat"] = self.cells[(x, y)].boat
            cells_json[coords]["building"] = self.cells[(x, y)].building
            if cells_json[coords]["building"]:
                cells_json[coords]["building"] = dict()
                cells_json[coords]["building"]["name"] = self.cells[(x, y)].building.name
                cells_json[coords]["building"]["price"] = self.cells[(x, y)].building.price
                cells_json[coords]["building"]["dohod"] = self.cells[(x, y)].building.dohod
                cells_json[coords]["building"]["ptype"] = self.cells[(x, y)].building.ptype
                cells_json[coords]["building"]["dtype"] = self.cells[(x, y)].building.dtype
                cells_json[coords]["building"]["level"] = self.cells[(x, y)].building.level
                cells_json[coords]["building"]["time"] = self.cells[(x, y)].building.time

        cells_json["towns"] = self.town
        cells_json["player"] = self.player
        cells_json["sdvig"] = self.sdvig

        cells_json["money"] = money
        cells_json["food"] = food
        cells_json["wood"] = wood
        cells_json["stone"] = stone

        with open("data/save.json", "w") as file:
            json.dump(cells_json, file)

    def load(self):
        global money, food, wood, stone

        with open('data/save.json') as file:
            data = json.load(file)

        self.cells = dict()
        for x in range(250):
            for y in range(250):
                coords = f"{x} {y}"
                bldg = data[coords]["building"]
                if bldg is not False:
                    bldg = Building(data[coords]["building"]["name"], data[coords]["building"]["price"],
                                    data[coords]["building"]["dohod"],
                                    data[coords]["building"]["ptype"], data[coords]["building"]["dtype"],
                                    data[coords]["building"]["level"])
                    bldg.time = data[coords]["building"]["time"]
                self.cells[(x, y)] = Cell((x, y), data[coords]["type"], data[coords]["forest"], data[coords]["boat"],
                                          bldg)

        self.town = tuple(data["towns"])
        self.player = tuple(data["player"])
        self.sdvig = tuple(data["sdvig"])

        money = data["money"]
        food = data["food"]
        wood = data["wood"]
        stone = data["stone"]

        self.draw_board()


def menu():
    global stop, screen
    stop = True
    screen.fill((56, 245, 56))

    image = pygame.image.load("data/title.png")
    image = pygame.transform.scale(image, (700, 200))
    screen.blit(image, (200, 30))

    image = pygame.image.load("data/button-new-game.png")
    image = pygame.transform.scale(image, (500, 200))
    screen.blit(image, (300, 260))

    if os.path.isfile("data/save.json"):
        image = pygame.image.load("data/button-old-game.png")
        image = pygame.transform.scale(image, (500, 200))
        screen.blit(image, (300, 490))


if __name__ == '__main__':
    pygame.init()
    size = 1100, 720
    screen = pygame.display.set_mode(size)

    pygame.mixer.music.load('data/sound.mp3')
    pygame.mixer.music.play(-1)

    stop = True
    money = 0
    food = 15
    wood = 0
    stone = 0
    menu()
    pygame.display.flip()

    clock = pygame.time.Clock()
    running = True
    while running:
        tick = clock.tick() / 1000
        if not stop:
            board.take_dohod(tick)
        moves = list()
        for event in pygame.event.get():
            if not stop:
                if event.type == pygame.MOUSEBUTTONUP:
                    board.clicked(event.pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        moves.append("left")
                    elif event.key == pygame.K_RIGHT:
                        moves.append("right")
                    elif event.key == pygame.K_UP:
                        moves.append("up")
                    elif event.key == pygame.K_DOWN:
                        moves.append("down")
                    elif event.key == pygame.K_ESCAPE:
                        board.save()
                        menu()
                if event.type == pygame.QUIT:
                    board.save()
                    running = False
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    coords = event.pos
                    if 300 <= coords[0] <= 800 and 260 <= coords[1] <= 460:
                        screen.fill((255, 255, 255))
                        image = pygame.image.load("data/loading.jpg")
                        image = pygame.transform.scale(image, (640, 360))
                        screen.blit(image, (230, 180))
                        pygame.display.flip()

                        money = 0
                        food = 15
                        wood = 0
                        stone = 0
                        board = Board(250, 250, 100)
                        board.new_board()
                        stop = False
                    elif 300 <= coords[0] <= 800 and 490 <= coords[1] <= 690 and os.path.isfile("data/save.json"):
                        screen.fill((255, 255, 255))
                        image = pygame.image.load("data/loading.jpg")
                        image = pygame.transform.scale(image, (640, 360))
                        screen.blit(image, (230, 180))
                        pygame.display.flip()

                        board = Board(250, 250, 100)
                        board.load()

                        stop = False

                if event.type == pygame.QUIT:
                    running = False
        if not stop:
            board.move(moves)
            board.draw_board()
        pygame.display.flip()
    pygame.quit()
