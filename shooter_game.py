from pygame import *
import random
from time import time as timer
mixer.init()
font.init()
font1 = font.Font(None, 100)
font2 = font.Font(None,36)
mixer.music.load("GameFiles/space.ogg")
firesound = mixer.Sound("GameFiles/fire.ogg")
menumusic = mixer.Sound("GameFiles/MenuMusic.mp3")

"""БАЗОВЫЕ НАСТРОЙКИ"""

win_width = 700
win_height = 500
FPS = 60
bullet_speed = 5
music = True
bullet_sfx = True

EasyDifficultySettings = {"Enemies": 3, 
"Asteroids": 2, 
"PlayerSpeed":10,
"BasePlayerHealth":5,
"WinRequirement": 10,
"MaxEnemySpeed": 5,
"LossRequirement": 5,
"ReloadTime": 1
}

NormalDifficultySettings = {"Enemies": 5, 
"Asteroids": 3, 
"PlayerSpeed":8,
"BasePlayerHealth":3,
"WinRequirement": 15,
"MaxEnemySpeed": 10,
"LossRequirement": 3,
"ReloadTime": 2
}

HardDifficultySettings = {"Enemies": 7, 
"Asteroids": 3,
"PlayerSpeed":7,
"BasePlayerHealth":3,
"WinRequirement": 20,
"MaxEnemySpeed": 10,
"LossRequirement": 3,
"ReloadTime": 3
}

ExtremeDifficultySettings = {"Enemies": 10, 
"Asteroids": 5, 
"PlayerSpeed":5,
"BasePlayerHealth":1,
"WinRequirement": 25,
"MaxEnemySpeed": 99999,
"LossRequirement": 1,
"ReloadTime": 3.5
}

Enemies = 5
Asteroids = 3
PlayerSpeed = 8
BasePlayerHealth = 3
WinRequirement = 15
MaxEnemySpeed = 10
LossRequirement = 3
RealodTime = 2
PlrHealth = BasePlayerHealth

"""ВНУТРИИГРОВЫЕ НАСТРОЙКИ"""

difficulty = "Normal"

"""-----------------------"""

def SetDifficulty():
    global difficulty
    global Enemies
    global Asteroids
    global PlayerSpeed
    global BasePlayerHealth
    global PlrHealth
    global WinRequirement
    global MaxEnemySpeed
    global LossRequirement
    global ReloadTime
    global EasyDifficultySettings
    global NormalDifficultySettings
    global HardDifficultySettings
    global ExtremeDifficultySettings
    if difficulty == "Easy":
        Enemies = EasyDifficultySettings["Enemies"]
        Asteroids = EasyDifficultySettings["Asteroids"]
        PlayerSpeed = EasyDifficultySettings["PlayerSpeed"]
        BasePlayerHealth = EasyDifficultySettings["BasePlayerHealth"]
        PlrHealth = BasePlayerHealth
        WinRequirement = EasyDifficultySettings["WinRequirement"]
        MaxEnemySpeed = EasyDifficultySettings["MaxEnemySpeed"]
        LossRequirement = EasyDifficultySettings["LossRequirement"]
        ReloadTime = EasyDifficultySettings["ReloadTime"]
    elif difficulty == "Normal":
        Enemies = NormalDifficultySettings["Enemies"]
        Asteroids = NormalDifficultySettings["Asteroids"]
        PlayerSpeed = NormalDifficultySettings["PlayerSpeed"]
        BasePlayerHealth = NormalDifficultySettings["BasePlayerHealth"]
        PlrHealth = BasePlayerHealth
        WinRequirement = NormalDifficultySettings["WinRequirement"]
        MaxEnemySpeed = NormalDifficultySettings["MaxEnemySpeed"]
        LossRequirement = NormalDifficultySettings["LossRequirement"]
        ReloadTime = NormalDifficultySettings["ReloadTime"]
    elif difficulty == "Hard":
        Enemies = HardDifficultySettings["Enemies"]
        Asteroids = HardDifficultySettings["Asteroids"]
        PlayerSpeed = HardDifficultySettings["PlayerSpeed"]
        BasePlayerHealth = HardDifficultySettings["BasePlayerHealth"]
        PlrHealth = BasePlayerHealth
        WinRequirement = HardDifficultySettings["WinRequirement"]
        MaxEnemySpeed = HardDifficultySettings["MaxEnemySpeed"]
        LossRequirement = HardDifficultySettings["LossRequirement"]
        ReloadTime = HardDifficultySettings["ReloadTime"]
    elif difficulty == "Extreme":
        Enemies = ExtremeDifficultySettings["Enemies"]
        Asteroids = ExtremeDifficultySettings["Asteroids"]
        PlayerSpeed = ExtremeDifficultySettings["PlayerSpeed"]
        BasePlayerHealth = ExtremeDifficultySettings["BasePlayerHealth"]
        PlrHealth = BasePlayerHealth
        WinRequirement = ExtremeDifficultySettings["WinRequirement"]
        MaxEnemySpeed = ExtremeDifficultySettings["MaxEnemySpeed"]
        LossRequirement = ExtremeDifficultySettings["LossRequirement"]
        ReloadTime = ExtremeDifficultySettings["ReloadTime"]
    else:
        return False
    return True


window = display.set_mode((win_width,win_height))
display.set_caption("Шут(ер)")

bg = transform.scale(image.load("GameFiles/galaxy.jpg"),(win_width,win_height))
bullet = transform.scale(image.load("GameFiles/bullet.png"),(25,25))
player_sprite = transform.scale(image.load("GameFiles/rocket.png"),(50,70))
ufo = transform.scale(image.load("GameFiles/ufo.png"),(70,50))
steriod = transform.scale(image.load("GameFiles/asteroid.png"),(70,50))
leftArrow = transform.scale(image.load("GameFiles/left-arrow1.png"),(50,50))
rightArrow = transform.scale(image.load("GameFiles/right-arrow1.png"),(50,50))
startButton = transform.scale(image.load("GameFiles/video.png"),(70,50))
display.set_icon(player_sprite)
#класс спрайта 
class GameSprite(sprite.Sprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__()
        self.image = sprite
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
#класс спрайта игрока-наследник класса GameSprite
class Player(GameSprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__(sprite,x,y,speed)
        #движение игрока влево и вправо
    def move_player(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        elif key_pressed[K_RIGHT] and self.rect.x < win_width -60:
            self.rect.x += self.speed
    #выстрел игрока
    def shoot(self):
        global bullet_sfx
        if bullet_sfx == True:
            firesound.play()
        global bullet_speed
        bull = Bullet(bullet,self.rect.centerx,self.rect.top,bullet_speed)
        global bullets
        bullets.add(bull)
class Enemy(GameSprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__(sprite,x,y,speed)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            global missed_enemies
            missed_enemies += 1
            self.rand_pos()
    def rand_pos(self):
        randnum = random.randint(5,win_width-80)
        self.rect.y = 0
        self.rect.x = randnum
        self.speed = random.randint(1,5)
class Asteroid(GameSprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__(sprite,x,y,speed)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rand_pos()
    def rand_pos(self):
        randnum = random.randint(5,win_width-80)
        self.rect.y = 0
        self.rect.x = randnum
        self.speed = random.randint(1,5)
class Bullet(GameSprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__(sprite,x,y,speed)
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

#инициализируем игровые объекты/настройки
monsters = sprite.Group()
bullets = sprite.Group()
steroids = sprite.Group()

stat = 0
missed_enemies = 0
num_fire = 0
clock = time.Clock()
game = True
finish = True
rel_time = False
menu = True

text_win = font1.render("YOU WIN!",1,(255,255,0))
text_loss = font1.render("YOU LOSE!",1,(255,0,0))
reload_text = font2.render("Reloading...",1,(255,10,10))

leftArr = GameSprite(leftArrow,250,200,0)
rightArr = GameSprite(rightArrow,400,200,0)
startbtn = GameSprite(startButton,300,400,0)

start_time = 0
#цикл игры
SetDifficulty()
def changedifficulty(mode):
    global difficulty
    if mode == "Lower":
        if difficulty == "Normal":
            difficulty = "Easy"
            return True
        elif difficulty == "Hard":
            difficulty = "Normal"
            return True
        elif difficulty == "Extreme":
            difficulty = "Hard"
            return True
    elif mode == "Higher":
        if difficulty == "Easy":
            difficulty = "Normal"
            return True
        elif difficulty == "Normal":
            difficulty = "Hard"
            return True
        elif difficulty == "Hard":
            difficulty = "Extreme"
            return True
    return False
while game:
    if finish == False:
        for evnt in event.get():
            if evnt.type == QUIT:
                game = False
            elif evnt.type == KEYDOWN:
                if evnt.key == K_SPACE:
                    if num_fire < 5 and rel_time == False:
                        plr.shoot()
                        num_fire += 1
                        if num_fire >= 5:
                            start_time = timer()
                            rel_time = True
        #если не завершили то отрисовываем объекты
        window.blit(bg,(0,0))
        monsters.draw(window)
        bullets.draw(window)
        steroids.draw(window)
        bullets.update()
        monsters.update()
        steroids.update()
        plr.move_player()
        plr.reset()
        sprites_list = sprite.groupcollide(monsters,bullets,True,True)
        steroids_bullets_list = sprite.groupcollide(steroids,bullets,True,True)
        plr_sprites_list = sprite.spritecollide(plr,monsters,True)
        Asteroids_sprites_list = sprite.spritecollide(plr,steroids,True)
        for i in steroids_bullets_list:
            asteroid = Asteroid(steriod,random.randint(5,win_width-80),0,1)
            steroids.add(asteroid)
        for i in Asteroids_sprites_list:
            PlrHealth -= 1
            asteroid = Asteroid(steriod,random.randint(5,win_width-80),0,1)
            steroids.add(asteroid)
            if PlrHealth <= 0:
                finish = True
                menu = True
                window.blit(text_loss,(200,200))
        for i in plr_sprites_list:
            PlrHealth -= 1
            monsta_speed = random.randint(1,stat)
            if monsta_speed > MaxEnemySpeed:
                monsta_speed = MaxEnemySpeed
            monster = Enemy(ufo,random.randint(5,win_width-80),0,monsta_speed)
            monsters.add(monster)
            if PlrHealth <= 0:
                finish = True
                menu = True
                window.blit(text_loss,(200,200))
        for i in sprites_list:
            stat += 1
            monsta_speed = random.randint(1,stat)
            if monsta_speed > MaxEnemySpeed:
                monsta_speed = MaxEnemySpeed
            monster = Enemy(ufo,random.randint(5,win_width-80),0,monsta_speed)
            monsters.add(monster)
            if stat >= WinRequirement:
                finish = True
                menu = True
                window.blit(text_win,(200,200))
        if missed_enemies >= LossRequirement:
            finish = True
            menu = True
            window.blit(text_loss,(200,200))
        if rel_time == True:
            end_time = timer()
            window.blit(reload_text,(300,400))
            if end_time - start_time >= RealodTime:
                rel_time = False
                num_fire = 0
        text_stats = font2.render("Счет: "+str(stat),1,(255,255,255))
        text_lose = font2.render("Пропущено: "+str(missed_enemies),1,(255,255,255))
        text_hp = font2.render("Здоровье: "+str(PlrHealth),1,(255,255,255))
        window.blit(text_lose,(10,60))
        window.blit(text_stats,(10,30))
        window.blit(text_hp,(10,90))
        display.update()
        clock.tick(FPS)
        if finish == True:
            time.delay(3000)
    else:
        mixer.music.stop()
        window.blit(bg,(0,0))
        stat = 0
        missed_enemies = 0
        
        if menu == False:
            mixer.music.play()
            for monstre in monsters:
                monstre.kill()

            for bull in bullets:
                bull.kill()

            for hui in steroids:
                hui.kill()

            for i in range(Enemies):
                name = Enemy(ufo,random.randint(5,win_width-80),0,1)
                monsters.add(name)
            for i in range(Asteroids):
                asteroid = Asteroid(steriod,random.randint(5,win_width-80),0,1)
                steroids.add(asteroid)
            plr = Player(player_sprite,350,430,PlayerSpeed)
            finish = False
            num_fire = 0
            rel_time = False
            PlrHealth = BasePlayerHealth
            finish = False
        else:
            leftArr.reset()
            rightArr.reset()
            startbtn.reset()
            window.blit(leftArrow,(250,200))
            window.blit(rightArrow,(400,200))
            if difficulty == "Normal":
                color = (255,255,255)
            elif difficulty == "Extreme":
                color = (255,0,0)
            elif difficulty == "Hard":
                color = (155,255,255)
            elif difficulty == "Easy":
                color = (0,255,0)
            text_difficulty = font2.render(difficulty,1,color)
            window.blit(text_difficulty,(300,200))
            display.update()
            for evnt in event.get():
                if evnt.type == QUIT:
                    game = False
                elif evnt.type == MOUSEBUTTONDOWN:
                    if leftArr.rect.collidepoint(evnt.pos):
                        changedifficulty("Lower")
                    elif rightArr.rect.collidepoint(evnt.pos):
                        changedifficulty("Higher")
                    elif startbtn.rect.collidepoint(evnt.pos):
                        menu = False
                    SetDifficulty()
            clock.tick(FPS)