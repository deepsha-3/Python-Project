import turtle
import time
from pygame import mixer

#  🎵 Music Setup (Optional)
# try:
#     mixer.init()
#     mixer.music.load(r"C:\Users\Deepsha\Music\The Weeknd,Playboi Carti-Timeless(320 Kbps).mp3")
#     mixer.music.play()
# except Exception as e:
#     print("Music error:", e)

# 🎨 Screen Setup
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Happy Birthday Animation")

# 🧁 Cake Turtle
cake = turtle.Turtle()
cake.hideturtle()
cake.speed(0)
cake.penup()
cake.goto(-100, -100)
cake.color("white")
cake.begin_fill()
cake.pendown()
for _ in range(2):
    cake.forward(140)
    cake.left(90)
    cake.forward(95)
    cake.left(90)
cake.end_fill()

# 🕯️ Candles Turtle
candles = turtle.Turtle()
candles.hideturtle()
candles.speed(0)
colors = ["red", "blue", "yellow", "green", "purple"]
x_positions = [-90, -60, -30, 0, 30]
for i in range(5):
    candles.penup()
    candles.goto(x_positions[i], 0)
    candles.color(colors[i])
    candles.setheading(90)
    candles.pendown()
    candles.forward(20)

# 🎈 Decoration Turtle
decor = turtle.Turtle()
decor.hideturtle()
decor.speed(0)
decor.penup()
decor.goto(-40, -50)
decor.pendown()
decor.setheading(0)
decor_colors = ["red", "orange", "yellow", "green", "blue", "purple", "black"]
for color in decor_colors:
    decor.color(color)
    decor.circle(10)
    decor.right(360 / len(decor_colors))
    decor.forward(10)

# 🎉 Message Turtle
message = turtle.Turtle()
message.hideturtle()
message.speed(0)
message.penup()
message.goto(-150, 50)
message.color("yellow")
message.write("Happy Birthday Deepsha!", align="left", font=("Arial", 20, "bold"))
time.sleep(1.5)

# 🎊 Bouncing Animation
for bounce in range(7):
    message.clear()
    message.goto(-150, 50 - bounce * 10)
    message.write("Happy Birthday Deepsha!", align="left", font=("Arial", 20, "bold"))
    time.sleep(0.5)

# 🧵 Finish
turtle.done()
