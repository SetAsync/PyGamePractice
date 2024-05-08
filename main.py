# 01/05/2024 - Main.py

#// Modules //
import pygame

#// Congif //
config = dict()
config["buttonDefaultColor"] = (128, 128, 128)
config["screenBackgroundColor"] = "#ADD8E6"
config["screenSize"] = (800, 600)

#// Objects //
class App:
    def __init__(self, size = config["screenSize"]):
        self.size = size
        self.screen = pygame.display.set_mode(self.size)
        self.colour = pygame.Color(config["screenBackgroundColor"])
        self.buttons = list()

    def addButton(self, button):
        self.buttons.append(button)

    def draw(self):
        # Ref: https://stackoverflow.com/questions/53253713/
        self.screen.fill(self.colour)

    def update(self, shadowedMouse, mouseDownShadow):
        self.draw()
        for button in self.buttons:
            button.update(self.screen, shadowedMouse, mouseDownShadow)

class Button:
    def __init__(self, text, color = config["buttonDefaultColor"], position = (0,0), size = (200, 100), parent = False):
        assert(parent, "Parent Required")
        self.parent = parent

        self.text = text
        self.position = position
        self.size = size
        self.colour = (128, 128, 128)
        self.hoverColour = (255, 0, 0) if text == "QUIT" else (255, 255, 0)
        self.fontColour = (255, 255, 255)

        # Ref: https://www.pygame.org/docs/ref/rect.html
        print(size, position)
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.hovered = False
        self.activated = False

        self.font = pygame.font.SysFont("Arial", 36)
        self.fontRender = self.font.render(text, True, self.fontColour)
        self.fontRect = self.fontRender.get_rect()
        self.fontRect.center = self.rect.center

    def checkHover(self, mouseObject, mouseDownShadow):
        hovered = not not self.rect.collidepoint(mouseObject)
        self.activated = mouseDownShadow and hovered
        self.hovered = hovered

        if self.activated:
            if self.text == "QUIT":
                exit(200)
            elif self.text == "START":
                self.parent.colour = (1,0,0)
            else:
                # Assume Colour Control
                colourControls = {
                    "RED": "#880808",
                    "GREEN": "#00FF00",
                    "BLUE": "#4169E1"
                }
                colour = colourControls[self.text]
                assert(colour, "Invalid Button Action!")
                self.parent.colour = pygame.Color(colour)

            r, g, b = self.colour # Unpack tuple -> r, g, b
            r = max(0, int(r * .5))
            g = max(0, int(g * .5))
            b = max(0, int(b * .5))
            self.colour = (r, g, b)

    def draw(self, screen):
        targetColour = self.hoverColour if self.hovered else self.colour
        pygame.draw.rect(screen, targetColour, self.rect)
        screen.blit(self.fontRender, self.fontRect)

    def update(self, screen, mouse, mouseDownShadow):
        self.checkHover(mouse, mouseDownShadow)
        self.draw(screen)

##// Initialise PyGame //
print("Loading PyGame..")
pygame.init()
# Setup clock for FPS
clock = pygame.time.Clock()

##// Setup Game //
app = App()
app.addButton(Button(text = "START", position = (app.size[0]/2-100, app.size[1]/2-50), size = (200, 100), parent = app))
app.addButton(Button(text = "QUIT", position = (app.size[0]/2-100, app.size[1]/2-200), size = (200, 100), parent = app))

##// Colour Buttons //
app.addButton(Button(text = "RED", position = (5,5), size = (120, 40), parent = app))
app.addButton(Button(text = "GREEN", position = (5,50), size = (120, 40), parent = app))
app.addButton(Button(text = "BLUE", position = (5,95), size = (120, 40), parent = app))


running = True

#// Game Loop //
while True:
    mouseDown = False
    for event in pygame.event.get(): # Event Listener
        if event == pygame.QUIT:
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True

    mouse = pygame.mouse.get_pos()

    app.update(mouse, mouseDown)
    pygame.display.flip() # Refreshes screen.
    clock.tick(60) # FPS

pygame.quit()
quit()
