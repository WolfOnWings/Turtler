from turtle import Screen
from crossing_logic import *
import time

# create screen
screen = Screen()
screen.setup(width=450, height=600)
screen.title("Turtle Crossing!")
screen.register_shape("car", ((16, 30), (16, -30), (-16, -30), (-16, 30)))
screen.tracer(0)
message = "You are a turtle trying to get home. Unfortunately for you, someone built 100 roads while you were gone!\n"\
          "Use the arrow keys to get around and try to make it across them all.\n"\
          "Don't worry about typing anything, and hit 'OK' to play!"
screen.textinput(title="Welcome to Turtle!", prompt=message)
screen.listen()

# create everything else
graphics = Graphics()
level = Level()
lives = Lives()
turtle = GameTurtle()
cars = Cars()

# listen for keypress and animate turtle
screen.onkeypress(fun=turtle.move_up, key="Up")
screen.onkeypress(fun=turtle.move_down, key="Down")
screen.onkeypress(fun=turtle.move_left, key="Left")
screen.onkeypress(fun=turtle.move_right, key="Right")
screen.onkeypress(fun=turtle.reset_turtle, key="space")

# game loop
game_running = True
new_level = True
while game_running:
    if new_level:
        level.next()
        cars.initialize_lanes()
        new_level = False
    screen.update()
    time.sleep(.1)
    screen.update()
    cars.move(level.current_level)
    # collision detection
    for car in cars.cars_onscreen:
        if turtle.distance(car) < 35:
            turtle.reset_turtle()
            lives.subtract_life()
    # detect level completion
    if turtle.ycor() > 224:
        cars.reset_lanes()
        turtle.reset_turtle()
        cars.increase_max_cars_in_lane(level.current_level)
        new_level = True
    # detect win
    if level.current_level == 100:
        message = "You beat the game!!!"
        screen.textinput(title="Wow!", prompt=message)
        game_running = False
    # detect loss
    if lives.current_lives < 0:
        message = "You ran out of lives...exit these windows and try again!"
        screen.textinput(title="Ouch!", prompt=message)
        game_running = False
screen.exitonclick()
