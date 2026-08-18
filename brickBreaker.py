#!/usr/bin/env python3
from ev3dev2.display import Display
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from PIL import ImageDraw
import time



paddleX = 89
paddleWidth = 40
disp = Display()
draw = ImageDraw.Draw(disp.image)
btn = Button()
sound = Sound()
ballX = 89
ballY = 100
ballspeedX = 3
ballspeedY = -3
ballSize = 5
bricks = []

def updateScreen():
    draw.rectangle((0, 0, 178, 127), fill='white')
    draw.rectangle((paddleX - paddleWidth // 2, 110, paddleX + paddleWidth // 2, 120), fill='black')
    draw.ellipse((ballX - ballSize, ballY - ballSize, ballX + ballSize, ballY + ballSize), fill='black')
    for obj in bricks:
        draw.rectangle((obj[4], obj[5], obj[6], obj[7]), fill='black')
    disp.update()

def genBricks(lvl):
    bricks.clear()
    if lvl == 1:
        num = 1
        for j in range(1,5):
            for i in range(1,10):
                w = (178 // 10)
                h = 10
                x = i * (178 // 10)
                y = num * 10
                bricks.append([x, y, w, h,x + 1, y + 1, x + w - 2, y + h - 2])


            num += 1
    if lvl == 2:
            num = 1
            for j in range(1,5):
                for i in range(1,10):
                    w = (178 // 10)
                    h = 10
                    x = i * (178 // 10)
                    y = num * 10
                    bricks.append([x, y, w, h,x + 1, y + 1, x + w - 2, y + h - 2])
    
    
                num += 2
    if lvl == 3:
                num = 1
                for j in range(1,5):
                    for i in range(1,5):
                        w = (178 // 10)
                        h = 10
                        x = i * (178 // 10) * 2
                        y = num * 10
                        bricks.append([x, y, w, h,x + 1, y + 1, x + w - 2, y + h - 2])
        
        
                    num += 1
def moveBall():
    global ballX, ballY
    ballX += ballspeedX
    ballY += ballspeedY

level = 0

sound.set_volume(10)
    
def gameLoop():
    global ballspeedX, ballspeedY, paddleX, ballX, ballY, bricks, level
    while True:
        time.sleep(0.01)
        if btn.left:
            paddleX -= 5
        if btn.right:
            paddleX += 5
        paddleX = max(paddleWidth // 2, min(178 - paddleWidth // 2, paddleX))
        moveBall()
        if ballX <= 5 or ballX >= 173:
            ballspeedX = -ballspeedX
        if ballY <= 5 or ballY >= 107:
            if ballY >= 107:
                ballY = 107
                if (ballX >= (paddleX - paddleWidth // 2) + 3 and ballX <= (paddleX + paddleWidth // 2) + 3):
                    
                    if ballX < (paddleX):
                        ballspeedX = -abs(ballspeedX)
                        
                    else:
                        ballspeedX = abs(ballspeedX)
                        
                        
                else:
                    break
                    sound.beep("",Sound.PLAY_WAIT_FOR_COMPLETE)
            ballspeedY = -ballspeedY
            moveBall()
        touching = False
        for obj in bricks[:]:
            left = obj[0]
            right = obj[0] + obj[2]
            top = obj[1]
            bottom = obj[1] + obj[3]
            ballLeft = ballX - ballSize // 2
            ballRight = ballX + ballSize // 2
            ballTop = ballY - ballSize // 2
            ballBottom = ballY + ballSize // 2
            if ballRight > left and ballLeft < right and ballTop < bottom and ballBottom > top:
                bricks.remove(obj)
                if ballLeft + 4 > right or ballRight - 4 < left:
                    ballspeedX = -ballspeedX
                    moveBall()
                    touching = True
                else:
                    ballspeedY = -ballspeedY
                    moveBall()
                    touching = True
        if (touching and len(bricks) == 0) or level == 0:
            level += 1
            genBricks(level)
            time.sleep(0.2)
            sound.play_tone(540,duration=0.3,volume=10)
            while True:
                    time.sleep(0.01)
                    if btn.left:
                        paddleX -= 5
                    if btn.right:
                        paddleX += 5
                    paddleX = max(paddleWidth // 2, min(178 - paddleWidth // 2, paddleX))
                    ballX = paddleX
                    ballY = 105
                    if btn.enter:
                        ballspeedX = 3
                        ballspeedY = -3  
                        break
                    updateScreen()
        elif touching:
            sound.play_tone(240,duration=0.05,volume=10)

        updateScreen()



gameLoop() 
