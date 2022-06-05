import pygame #imports pygame so we can use its commands (ie. pygame.something)
import os
pygame.font.init() #for fonts 
pygame.mixer.init() #for music 

width, height = 1150, 670 #window title + window size
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("catz <3")

#colours !! + other defined variables 
catgame = (255,255,255)
pink = (255, 128, 214)
purple = (177, 156, 217)
org = (251, 163, 26)

cat1wins = 0
cat2wins = 0

border = pygame.Rect(0, height/2 - 5, width, 5)
fps = 80
cat1width = 80
cat1length = 80
velocity  = 12
maxhits = 5 
vel = 15

#hits and health is registered 
cat1_hit = pygame.USEREVENT + 1
cat2_hit = pygame.USEREVENT + 2

#font, size, bold
font = pygame.font.SysFont("baskerville", 50, bold = True)
#meow sound from mp3
meow = pygame.mixer.Sound(os.path.join("cat-meow-14536.mp3"))

#cat1and cat2 pngs are taken from another folder and scaled to my png size variables
cat1image = pygame.image.load(os.path.join("cat1.png"))
cat1image = pygame.transform.scale(cat1image, (cat1width, cat1length))
cat2image = pygame.image.load(os.path.join("cat2.png"))
cat2image = pygame.transform.scale(cat2image, (cat1width, cat1length))
#background is opened from another folder and scaled to the window
hearts = pygame.transform.scale(pygame.image.load(os.path.join("hearts.jpeg")), (width, height))

def gamewindow(cat1, cat2, cat2_attacks, cat1_attacks, cat1HP, cat2HP):
    #background png is displayed in the window and the border is created in the middle
    window.blit(hearts, (0, 0))
    pygame.draw.rect(window, pink, border)

    #health is displayed and updated  
    cat1healthtext = font.render("cat1 lives: " + str(cat1HP), 1, catgame)
    cat2healthtext = font.render("cat2 lives: " + str(cat2HP), 1, catgame)
    window.blit(cat2healthtext, (width - cat2healthtext.get_width()-15, 15))
    window.blit(cat1healthtext, (15, height - cat1healthtext.get_height()-15))

    #cat1and cat2 are placed in the window 
    window.blit(cat1image, (cat1.x, cat1.y))
    window.blit(cat2image, (cat2.x, cat2.y))

    #makes a rectangle for each shot 
    for attacks in cat1_attacks:
        pygame.draw.rect(window, purple, attacks)
    for attacks in cat2_attacks:
        pygame.draw.rect(window, org, attacks)
        
    pygame.display.update()

#cat2's controls and limits to where he can move is here
def cat2move(KeysPressed, cat2):
    if KeysPressed[pygame.K_a] and cat2.x - vel > 0:
        cat2.x -= vel
    if KeysPressed[pygame.K_d] and cat2.x + vel + cat2.width < width:
        cat2.x += vel
    if KeysPressed[pygame.K_w] and cat2.y - vel > 0:
        cat2.y -= vel
    if KeysPressed[pygame.K_s] and cat2.y + vel + cat2.height < height / 2:
        cat2.y += vel

#cat1's controls and limits to where he can move is here
def cat1move(KeysPressed, cat1):
    if KeysPressed[pygame.K_LEFT] and cat1.x - vel > 0:
        cat1.x -= vel
    if KeysPressed[pygame.K_RIGHT] and cat1.x + vel + cat1.width < width:
        cat1.x += vel
    if KeysPressed[pygame.K_UP] and cat1.y - vel > height / 2:
        cat1.y -= vel
    if KeysPressed[pygame.K_DOWN] and cat1.y + vel + cat1.height < height:
        cat1.y += vel

#counts when cats get hit, subs lives, removes bullet from screen 
def shotcounter(cat1_attacks, cat2_attacks, cat1, cat2):
    for attack in cat1_attacks:
        attack.y -= velocity 
        if cat2.colliderect(attack):
            pygame.event.post(pygame.event.Event(cat2_hit))
            cat1_attacks.remove(attack)
        elif attack.y <= 0:
            cat1_attacks.remove(attack)
    for attack in cat2_attacks:
        attack.y += velocity 
        if cat1.colliderect(attack):
            pygame.event.post(pygame.event.Event(cat1_hit))
            cat2_attacks.remove(attack)
        elif attack.y >= height:
            cat2_attacks.remove(attack)

#winner text is displayed and the game is closed after 1500 milliseconds
def winner(text):
    text = font.render(text, 1, catgame)
    window.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)


def main():
    #This is where the characters are placed on the screen
    cat1= pygame.Rect(width / 2 - 50, height * 0.75 - 50, cat1width, cat1length)
    cat2 = pygame.Rect(width / 2 - 50, height / 4 - 50, cat1width, cat1length)

    #A list counting character attacks
    cat1_attacks = []
    cat2_attacks = []
    
    #Character HP
    cat1HP = 9
    cat2HP = 9

    clock = pygame.time.Clock()

    #This while loop runs the game until the quit function is true, which is when the game is over
    while True:
        global cat2wins, cat1wins 
        #The fps of the game is controlled by the clock
        clock.tick(fps)
        #This checks if the game should be over and ends the while loop running the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = False

            #when a bullet is shot based on key pressed 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(cat1_attacks) < maxhits:
                    attack = pygame.Rect(cat1.x + cat1.width / 2, cat1.y, 8, 30)
                    cat1_attacks.append(attack)
                    
                if event.key == pygame.K_SPACE and len(cat2_attacks) < maxhits:
                    attack = pygame.draw.circle(window, purple, (cat2.x + cat2.width / 2, cat2.y + 63), 11)
                    cat2_attacks.append(attack)
                    
            
            #hit: they lose health and a meow is played 
            if event.type == cat1_hit:
                cat1HP -= 1
                meow.play()
            if event.type == cat2_hit:
                cat2HP -= 1
                meow.play()
            

        #calling the defined functions
        shotcounter(cat1_attacks, cat2_attacks, cat1, cat2)
        KeysPressed = pygame.key.get_pressed()
        cat2move(KeysPressed, cat2)
        cat1move(KeysPressed, cat1)
        gamewindow(cat1, cat2, cat2_attacks, cat1_attacks, cat1HP, cat2HP)
        
        #shows which cat is still alive, theyre displayed as the winner 
        winnermessage= ""
        if cat1HP <= 0:
            winnermessage= "cat2 wins!"
            cat2wins =+ 1 
        if cat2HP <= 0:
            winnermessage= "cat1 wins!"
            cat1wins =+ 1 
        if winnermessage!= "":
            winner(winnermessage)
            break
    


if __name__ == "__main__":
    while True:
        games = int(input('how many games (1 or 2)?: ')) #my unique change: u can play once twice 
    
        if games == 1:
            for i in range(games):
                main()
            pygame.quit() #game over, window shuts 
    
            if cat1wins > cat2wins:
                print('cat1 wins!')
            elif cat2wins > cat1wins:
                print('cat2 wins!')
            else:
                print('tie game!')
        
            break 

        elif games == 2: 
            for i in range(games):
                main()
            pygame.quit() #game over, window shuts 
            if cat1wins > cat2wins:
                print('cat1 wins!')
            elif cat2wins > cat1wins:
                print('cat2 wins!')
            else:
                print('tie game!')
            break

        else:  
            continue 
    

    
 
