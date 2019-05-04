# @ Reindeer Rain - dodge the reindeers falling from the sky!
# @author Eric Xu
# @date 2018/01/15
# @course ICS3U1

import pygame
import random


# -------- CLASSES -----------

# Makes a Reindeer sprite
# @attr rect.x, rect.y, image
class Reindeer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load image, colour key, make hitbox
        self.image = pygame.image.load('reindeer.png').convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
    
    # Moves reindeer to top to fall again
    # @param height (where on the y axis to be moved)
    def goToTop(self, height):
        self.rect.x = random.randrange(900)
        self.rect.y = height
    
    # Moves reindeer down and reset position if needed
    def update(self):
        self.rect.y += 4 * round(multiplier, 2)

        # Reset position when off screen
        if (self.rect.y > 810):
            self.goToTop(spawnHeight)


# Makes a Heart sprite. Inherits from Reindeer class
# @attr rect.x, rect.y, image
class Heart(Reindeer):
    # Load a different image for heart
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('heart.png').convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()


# Makes a Shield sprite. Inherits from Reindeer class
# @attr rect.x, rect.y, image
class Shield(Reindeer):
    # Load a different image for shield
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('shield.png').convert()
        
        # Colour key is black for this image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()


# Makes Player sprite controlled by mouse
# @attr rect.x, rect.y, image
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('player.png').convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        
    # Moves sprite to where mouse cursor is
    def update(self):
        mousePos = pygame.mouse.get_pos()
        playerPos = mousePos[0] - 11

        # Move sprite only if it's not off screen
        if (playerPos < 960):
            self.rect.x = playerPos
        else:
            self.rect.x = 960


# -------- SUBPROGRAMS -----------

# Sets up the game (only run once, doesn't reset the game)
def initGame():

    # We need to modify these variables
    global BLACK, WHITE, LBLUE, YELLOW, RED
    global screen, clock, background, titleFont, font
    global hitSound, heartSound, shieldSound
    global leaderboard, start
    
    # Colours
    BLACK   = (  0,   0,   0)
    WHITE   = (255, 255, 255)
    LBLUE   = ( 66, 179, 244)
    YELLOW  = (255, 255,   0)
    RED     = (255,   0,   0)

    # Setup screen, background, font
    pygame.init()
    screen = pygame.display.set_mode([1000, 700])
    pygame.display.set_caption("Reindeer Rain")
    clock = pygame.time.Clock()
    background = pygame.image.load('background.png').convert()
    titleFont = pygame.font.Font('PressStart2P.ttf', 60)
    font = pygame.font.Font('PressStart2P.ttf', 40)


    # Background music and sound effects
    pygame.mixer.music.load('music.ogg')
    pygame.mixer.music.play(loops=-1)
    hitSound = pygame.mixer.Sound('hit.wav')
    heartSound = pygame.mixer.Sound('heart.wav')
    shieldSound = pygame.mixer.Sound('shield.wav')
    pygame.mixer.music.set_volume(0.5)
    hitSound.set_volume(0.5)
    heartSound.set_volume(0.5)
    shieldSound.set_volume(0.5)
    
    leaderboard = readLeaderboardFile()
    start = False
    resetGame()


# Get leaderboard from file
# @return leaderboard
def readLeaderboardFile():
    leaderboard = []
    leaderFile = open('leaderboard.txt', 'r')

    # Add each score from the file to leaderboard list
    for line in leaderFile:
            leaderboard.append(int(line))
    leaderFile.close()
    
    return leaderboard


# Write leaderboard to file
def writeLeaderboardFile():
    # Turn each leaderboard score into string
    leaderboardString = []
    lineCounter = 0

    # Add the top 5 scores to the file
    for line in leaderboard:
        if (lineCounter <= 4):
            leaderboardString.append(str(line) + "\n")
        lineCounter += 1

    # Then save the scores in the file
    open('leaderboard.txt', 'w').close()  # First, wipe it
    leaderFile = open('leaderboard.txt', 'a')
    leaderFile.writelines(leaderboardString)
    leaderFile.close()


# Resets game by initializing variables and creating the sprites
def resetGame(): 
    global reindeerList, heartList, shieldList, spriteList
    global player, score, multiplier, lives, shieldEffect
    global addScoreToLeaderboard, highScore, gameOver

    score = 0
    multiplier = 3
    lives = 10
    shieldEffect = 0
    addScoreToLeaderboard = True
    highScore = False
    gameOver = False
    
    # Create/clear sprite groups that contain list of sprites
    reindeerList = pygame.sprite.Group()
    heartList = pygame.sprite.Group()
    shieldList = pygame.sprite.Group()
    spriteList = pygame.sprite.Group()
    
    # Create player
    player = Player()
    player.rect.y = 600
    spriteList.add(player)

    # Create 50 reindeers, hearts and shields
    for counter in range(50):
        # 25th sprite is always a shield
        if (counter == 25):
            sprite = Shield()
            spriteType = 's'
        # Heart every 10 sprites
        elif (counter in [0, 10, 20, 30, 40]):
            sprite = Heart()
            spriteType = 'h'
        # All others are reindeers
        else:
            sprite = Reindeer()
            spriteType = 'r'

        # Spawn on random vertical positions and progressive rows
        sprite.rect.x = random.randrange(900)
        sprite.rect.y = counter * -115

        # Add to lists, depending on type of sprite
        spriteList.add(sprite)
        if (spriteType == 's'):
            shieldList.add(sprite)
        elif (spriteType == 'h'):
            heartList.add(sprite)
        else:
            reindeerList.add(sprite)

# Shows title or death screen w/ button & leaderboard, resets game when button pressed at gameover
# @param showDeathScreen
# @return buttonPressed
def titleScreen(showDeathScreen):
    global gameOver, highScore
    buttonPressed = False
    if showDeathScreen:
        if highScore:
            titleText = " High Score!"
        else:
            titleText = "  Game over"
        buttonText = "Retry"
    else:
        titleText = "Reindeer Rain"
        buttonText = "Start"
    
    # Title text with fancy shadow
    titleTextRender = titleFont.render(titleText, True, WHITE)
    titleTextRenderShadow = titleFont.render(titleText, True, BLACK)
    screen.blit(titleTextRenderShadow, [125, 105])
    screen.blit(titleTextRender, [120, 100])
    
    # Show top 5 scores in leaderboard
    counter = 0
    for eachScore in leaderboard:
        if (counter <= 4) and (eachScore != 0):
            eachScoreText = str(counter + 1) + ". " + str(eachScore)
            # Highlight current score if it's in the leaderboard
            if (score == eachScore):
                textColour = YELLOW
            else:
                textColour = WHITE
            eachScoreTextRender = font.render(eachScoreText, True, textColour)
            screen.blit(eachScoreTextRender, [270, counter * 60 + 240])
        counter += 1
    
    # Button
    pygame.draw.rect(screen, BLACK, [354, 554, 300, 100], 6)
    pygame.draw.rect(screen, WHITE, [350, 550, 300, 100], 6)
    buttonTextRender = font.render(buttonText, True, RED)
    buttonTextRenderShadow = font.render(buttonText, True, BLACK)
    screen.blit(buttonTextRenderShadow, [410, 580])
    screen.blit(buttonTextRender, [406, 576])
    mousePos = pygame.mouse.get_pos()
    mouseButtonState = pygame.mouse.get_pressed()
    
    # Make the button clickable
    if (mousePos[0] > 350 and mousePos[0] < 650) and (mousePos[1] > 550 and mousePos[1] < 650):
        pygame.draw.rect(screen, LBLUE, [350, 550, 300, 100], 6)
        if (mouseButtonState[0]) or (mouseButtonState[2]):
                buttonPressed = True
                if showDeathScreen:  # Also reset game if needed
                    gameOver = False
                    resetGame()
    
    return buttonPressed


# Takes care of sprites
def manageSprites():
    global lives, spawnHeight, shieldEffect
    # Update sprite positions
    spriteList.update()

    # Find place above highest sprite for a fallen sprite to spawn
    spawnHeight = 700
    for sprite in spriteList:
        if (sprite.rect.y < spawnHeight):
            spawnHeight = sprite.rect.y - 115
    
    # Check collisions against reindeers and power-ups
    hitReindeerList = pygame.sprite.spritecollide(player, reindeerList, False)
    if (shieldEffect == 0):  # Only do reindeer collisions if shield is off
        for reindeer in hitReindeerList:
            hitSound.play()
            lives += -1
            # Move reindeer above the highest sprite
            reindeer.goToTop(spawnHeight)
    
    hitHeartList = pygame.sprite.spritecollide(player, heartList, False)
    for heart in hitHeartList:
        heartSound.play()
        lives += 1
        heart.goToTop(spawnHeight)
        
    hitShieldList = pygame.sprite.spritecollide(player, shieldList, False)
    for shield in hitShieldList:
        shieldSound.play()
        # Shield will last for 180 frames (3sec)
        shieldEffect = 180
        shield.goToTop(spawnHeight)

    # Make shield wear off
    if (shieldEffect != 0):
        shieldEffect += -1


# Draws all sprites and shield around player
# @param shieldEffect
def drawSprites(shieldEffect):
    # Draw all sprites
    spriteList.draw(screen)

    # Draw force field around player if shield is not off
    if (shieldEffect != 0):
        shieldColour = (shieldEffect, shieldEffect, 255)
        pygame.draw.circle(screen, shieldColour, [player.rect.x + 21, player.rect.y + 43], 60, 4)  


# Displays score in top left corner
# @param score
def scoreMeter(score):
    scoreText = font.render(str(score), True, WHITE)
    screen.blit(scoreText, [0, 0])


# Graphically displays number of lives left
# @param lives
def healthMeter(lives):
    heartImage = pygame.image.load('heart.png').convert()
    heartImage.set_colorkey(WHITE)

    # Show hearts offset from each other
    for counter in range(lives):
        screen.blit(heartImage, [970 - 35 * counter, 0])


# Makes the game progressively harder each frame
def increaseMultiplier():
    global multiplier, score
    
    # Increase multiplier unless it has reached the limit
    if (multiplier < 7):
        multiplier += 0.001
        
    # Make score increase faster as game gets harder
    score += int(multiplier * 1000)


def endGame():
    global addScoreToLeaderboard, leaderboard, highScore
    
     # Add score to leaderboard, but only once
    if addScoreToLeaderboard:
        leaderboard.append(score)
        
        # Sort by highest to lowest
        leaderboard.sort(reverse=True)
        
        # Checks if the current score is a high score
        if (score == leaderboard[0]):
            highScore = True
        addScoreToLeaderboard = False
        
    # Now show the death screen with updated leaderboard
    titleScreen(True)


# -------- MAIN -----------
initGame()
done = False
while not done:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            done = True
    
    screen.blit(background, [0, 0])

    # Show the title screen if the game hasn't started yet
    if not start:
        start = titleScreen(False)
    else:
        # Show the game over screen and reset game
        if gameOver:
           endGame()
        else:
            # Main game
            manageSprites()
            drawSprites(shieldEffect)
            scoreMeter(score)
            healthMeter(lives)
            increaseMultiplier()

            # Make it game over when the player is dead
            if (lives <= 0):
                gameOver = True
        
    clock.tick(60)
    pygame.display.flip()

writeLeaderboardFile()
pygame.quit()
