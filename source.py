import pgzrun
import random

WIDTH = 1000  
HEIGHT = 700

game_over = False

# Car size : 166 * 94 -> 30 * 17
# 메인 자동차 이미지
car_main = Actor("car-main")
car_main.pos = 1000 // 2, HEIGHT - 94 // 2

# dashboard image
dashboard = Actor("dashboard", topleft=(10,350))

# steering wheel image
steering_wheel = Actor("steering-wheel", topright=(975,300))

# car speed
left_speed = 0
right_speed = 0
center_speed = 0

# variable for cars on each line
l_y = 0
r_y = 0
c_y = 0

# variable that limits maximum amount of cars drawn on the screen
line = 1
line_2 = 1

# variable for sound effect when the car crashes
crash = 0

# variable for timer and score
timer = 0
score = 0

# spawning 70 cars on the left line, seen image while playing is 50 cars, 
# rest of the cars (20 cars) are for the exit animation of the cars.
l_car = []
x = 510
y = 350
for car in range(1, 71, 1):
    if(car >= 50):
        text = "car_1_50"
    else:
        text = "car_1_"+str(car)

    actor = Actor(text)
    actor.pos = x, y
    x -= 5.12
    y += 6.06

    l_car.append(actor)

# spawning 70 cars on the right line, seen image while playing is 50 cars, 
# rest of the cars (20 cars) are for the exit animation of the cars.
r_car = []
x = 570
y = 350
for car in range(1, 71, 1):
    if(car >= 50):
        text = "car_2_50"
    else:
        text = "car_2_"+str(car)

    actor = Actor(text)
    actor.pos = x, y
    x += 3.6
    y += 6.06

    r_car.append(actor)

# spawning 70 cars on the center line, seen image while playing is 50 cars, 
# rest of the cars (20 cars) are for the exit animation of the cars.
c_car = []
x = 540
y = 350
for car in range(1, 71, 1):
    if(car >= 50):
        text = "car_3_50"
    else:
        text = "car_3_"+str(car)

    actor = Actor(text)
    actor.pos = x, y
    x -= 0.8
    y += 6.06

    c_car.append(actor)


# drawing on the screen
def draw():
    global left_speed, right_speed, center_speed

    screen.blit("background", (0, 0))   # background setting
    # screen.fill("black")
    if(game_over != True):
        screen.draw.text(str(round(timer, 3)), topleft=(10,10), color=(255,0,0), fontsize=30)
        screen.draw.text(str(round(score)), midtop=(500,10), color=(0,0,0), fontsize=50, background="white")

        car_main.draw()
        dashboard.draw()
        steering_wheel.draw()

        # left line 
        l_l = int(left_speed)
        if(line == 1 or line_2 == 1):
            l_car[l_l].draw()

        # right line
        r_l = int(right_speed)
        if(line == 3 or line_2 == 3):
            r_car[r_l].draw()

        # center line
        c_l = int(center_speed)
        if(line == 2 or line_2 == 2):
            c_car[c_l].draw()

    if(game_over):
        screen.clear()
        screen.blit("end", (0, 0))   # background setting
        screen.draw.text(str(round(score)), center=(500,270), color=(255,255,255), fontsize=150, owidth=1, ocolor="red")

# resetting the cars postition
def speed_reset():
    global left_speed, right_speed, center_speed
    left_speed = 0
    right_speed = 0
    center_speed = 0

def update():

    global left_speed, right_speed, center_speed
    global game_over, line, line_2, crash, timer, score

    if(not(game_over)):
        timer += 1 / 60
        score += 1 / 60
    
        # speed of the car, random speed
        left_speed += random.uniform(0.1, 1.0)
        right_speed += random.uniform(0.1, 1.0)
        center_speed += random.uniform(0.1, 1.0)

        # keyboard input
        if(keyboard.left): 
            car_main.x = car_main.x - 10
            if(car_main.x < 250):
                car_main.x = 250
        elif(keyboard.right): 
            car_main.x = car_main.x + 10
            if(car_main.x > 750):
                car_main.x = 750
            

        # respawning car if it goes off the screen
        if(left_speed >= 70):
            score += 10
            left_speed = 0
        if(right_speed >= 70):
            score += 10
            right_speed = 0
        if(center_speed >= 70):
            score += 10
            center_speed = 0

        # drawing cars on the line
        if(left_speed == 0 and (line == 1 or line_2 == 1)):     # situation when left car goes out of screen
            line = random.randint(1, 3)
            line_2 = random.randint(1, 3)
            speed_reset()
        if(right_speed == 0 and (line == 3 or line_2 == 3)):    # situation when right car goes out of screen
            line = random.randint(1, 3)
            line_2 = random.randint(1, 3)
            speed_reset()
        if(center_speed == 0 and (line == 2 or line_2 == 2)):   # situation when center car goes out of screen
            line = random.randint(1, 3)
            line_2 = random.randint(1, 3)
            speed_reset()
        
        # when two cars crash into each others
        if(car_main.colliderect(l_car[int(left_speed)]) and (line == 1 or line_2 == 1)):
            if(crash == 0):
                sounds.background.stop()
                sounds.crash.play()
                crash = 1
            game_over = True
        if(car_main.colliderect(r_car[int(right_speed)]) and (line == 3 or line_2 == 3)):
            if(crash == 0):
                sounds.background.stop()
                sounds.crash.play()
                crash = 1
            game_over = True
        if(car_main.colliderect(c_car[int(center_speed)]) and (line == 2 or line_2 == 2)):
            if(crash == 0):
                sounds.background.stop()
                sounds.crash.play()
                crash = 1
            game_over = True

sounds.background.play(-1)  # background music infinite repetition
pgzrun.go()