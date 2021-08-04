import pygame
import main
import os

class texture:
    def __init__(self,posx,posy,splashcode):
        self.texture = pygame.image.load(splashcode).convert_alpha()
        self.texture_rect = self.texture.get_rect()
        self.texture_rect.center = (posx+10,posy+10)
        screen.blit(self.texture,self.texture_rect)

bmap,flag_map,bomb_places = main.setup()

for i in bmap:
    print(i)

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#Blue, Green, RED, DARKBLUE, DARK RED, TURKIZ, BLACK,GRAY
BRIGHT_BLUE = (51, 153, 255)
DARK_BLUE = (0, 0, 255)
DARK_RED = (102, 0, 0)
PINK = (255, 51, 255)
TURKIZ = (0, 204, 204)
GRAY = (160, 160, 160)
BRIGHT_GRAY = (224, 224, 224)
YELLOW = (255, 255, 0)
RED_RED = (205,0,0)

color_codes = {
    "0": GRAY,
    "1": BRIGHT_BLUE,
    "2": GREEN,
    "3": RED,
    "4": DARK_BLUE,
    "5": DARK_RED,
    "6": TURKIZ,
    "7": BLACK,
    "8": GRAY,
    "9": PINK,
    "10":BRIGHT_GRAY,
    "11": YELLOW,
    "12": WHITE,
}

splash_codes = {
    "0": "splash/empty.png",
    "1": "splash/num1.png",
    "2": "splash/num2.png",
    "3": "splash/num3.png",
    "4": "splash/num4.png",
    "5": "splash/num5.png",
    "6": "splash/num6.png",
    "7": "splash/num7.png",
    "8": "splash/num8.png",
    "9": "splash/bomb.png",
    "11": "splash/flag.png",
    "12": "splash/num0.png",
    "13": "splash/num0.png",


}
#texture render

def find_around(temp,bmap,grid,flag_map):
    if len(temp) != 0:
        pos_y = temp[0][0]
        pos_x = temp[0][1]
        grid[pos_y][pos_x] = '13'
        bmap[pos_y][pos_x] = '13'
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (((i + j) == 1) or ((i + j) == -1)) and (pos_y +i >=0) and (pos_x + j) >=0:
                    try:
                        if bmap[pos_y + i][pos_x + j] == ' ' and flag_map[pos_y + i][pos_x + j] != 'f':
                            grid[pos_y + i][pos_x + j] = '13'
                            bmap[pos_y][pos_x] = '13'
                            temp.append(tuple([(pos_y + i), (pos_x + j)]))
                        elif int(bmap[pos_y + i][pos_x + j]) <= 8 and int(bmap[pos_y + i][pos_x + j]) >= 1 and flag_map[pos_y + i][pos_x + j] != 'f':
                            grid[pos_y + i][pos_x + j] = bmap[pos_y + i][pos_x + j]
                        else:
                            pass
                    except:
                        pass
        temp.pop(0)
        find_around(temp,bmap,grid,flag_map)
    else:
        return

def reset():
    global grid,lose,timer,flag_counter,bmap,bomb_places
    print('Reset')
    bmap, flag_map, bomb_places = main.setup()
    grid = [[0 for x in range(30)] for y in range(16)]
    lose = False
    timer = 0
    flag_counter = 0
    for i in bmap:
        print(i)

        
pygame.init()
pygame.mixer.init()

#music
background_music = 'audio/background_music.mp3'
music = pygame.mixer.music.load(background_music)

explosion_sound = 'audio/explosion.mp3'
explosion = pygame.mixer.Sound(explosion_sound)
pygame.mixer.Sound.set_volume(explosion, 0.1)
click_sound = 'audio/click.wav'
click = pygame.mixer.Sound(click_sound)

pygame.mixer.music.play(-1)
# Set the width and height of the screen [width, height]
size = (850, 408) # def 765, 408 /// 755, 408 is good
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Minesweeper")

width = 20
height = 20
margin = 5

grid = [[0 for x in range(30)] for y in range(16)]



# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
dt = 0
timer = 0
#win flag
lose = False

#flag counter
flag_counter = 0
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN and 755 <= pos[0] <= 835 and 200 <= pos[1] <= 280:
            pygame.mixer.Sound.play(click)
            reset()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and lose == False:
            pygame.mixer.Sound.play(click)
            column = pos[0] // (width + margin)
            row = pos[1] // (height + margin)
            # Debug prints
            print("Click ", pos, "Grid coordinates: ", row, column)
            try:
                if flag_map[row][column] != 'f':
                    if bmap[row][column] != '9' and bmap[row][column] != ' ' :
                        grid[row][column] = bmap[row][column]
                        #print(f'grid[row][column]: {grid[row][column]} , color {color_codes[grid[row][column]]}')
                    elif bmap[row][column] == '9':
                        for i in bomb_places:
                            grid[i[0]][i[1]] = '9'
                            lose = True
                            pygame.mixer.Sound.play(explosion)
                    else:
                        grid[row][column] = "13"
                        find_around([tuple([row,column])],bmap,grid,flag_map)
            except IndexError:
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and lose == False:
            pygame.mixer.Sound.play(click)
            column = pos[0] // (width + margin)
            row = pos[1] // (height + margin)

            if flag_map[row][column] != 'f' and flag_counter < 99 and grid[row][column] != "13" and grid[row][column] == 0:

                flag_map[row][column] = 'f'
                grid[row][column] = '11'
                flag_counter += 1
            elif flag_map[row][column] == 'f':
                flag_map[row][column] = ' '
                grid[row][column] = '0'
                flag_counter -= 1
            else:
                pass
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.mod & pygame.KMOD_RSHIFT:
                reset()

    # --- Game logic should go here
    pos = pygame.mouse.get_pos()
    x = pos[0]
    y = pos[1]

    # --- Drawing code should go here

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    screen.fill(RED_RED)
    #reset button
    smiley_texture = pygame.image.load("splash/smiley.png").convert_alpha()
    sad_smiley_texture = pygame.image.load("splash/sadsmiley.png").convert_alpha()
    if 755 <= pos[0] <= 835 and 200 <= pos[1] <= 280 or lose == True:
        #pygame.draw.rect(screen, PINK , [755, 200 , 90, 40])
        sad_smiley_texture_rect = sad_smiley_texture.get_rect()
        sad_smiley_texture_rect.center = (795, 240)
        screen.blit(sad_smiley_texture, sad_smiley_texture_rect)
    else:
        #pygame.draw.rect(screen, YELLOW, [755, 200 , 90, 40])

        smiley_texture_rect = smiley_texture.get_rect()
        smiley_texture_rect.center = (795, 240)
        screen.blit(smiley_texture, smiley_texture_rect)
    font = pygame.font.Font(None, 28)
    txt_timer = font.render(("Timer: " + str(int(timer))), True, YELLOW)
    txt_flag_counter = font.render(("Flag: " + str(flag_counter)), True, YELLOW)
    screen.blit(txt_timer, (755, 70))
    screen.blit(txt_flag_counter, (755, 120))
    for row in range(16):
        for column in range(30):
            if int(grid[row][column]) >= 0 and int(grid[row][column]) <= 13:

                splash_code = splash_codes[str(grid[row][column])]
            else:
                splash_code = splash_codes['12']
            #pygame.draw.rect(screen, color,
            #                [margin + (margin + width) * column, margin + (margin + height) * row, width, height])
            texture(margin + (margin + width) * column,margin + (margin + height) * row, splash_code)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    if lose != True:
        timer += dt
    dt = clock.tick(60)/2000

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
