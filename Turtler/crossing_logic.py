from turtle import Turtle
from random import randint


# sets up lane markings
class Graphics:
    def __init__(self):
        self.lane_pos = [(-225, -250), (-213, -200), (-213, -150), (-213, -100), (-225, -50), (-225, 0), (-213, 50),
                         (-213, 100), (-225, 150), (-225, 200)]
        self.lane_graphics = []
        for pos in self.lane_pos:
            if pos == self.lane_pos[0] or \
                    pos == self.lane_pos[-1] or \
                    pos == self.lane_pos[4] or \
                    pos == self.lane_pos[5]:
                graphic = Turtle(visible=False)
                graphic.penup()
                graphic.setpos(pos)
                graphic.pensize(5)
                graphic.pendown()
                graphic.forward(450)
                self.lane_graphics.append(graphic)
            else:
                graphic = Turtle(visible=False)
                graphic.penup()
                graphic.setpos(pos)
                while graphic.xcor() < 225:
                    graphic.pendown()
                    graphic.forward(20)
                    graphic.penup()
                    graphic.forward(20)
                self.lane_graphics.append(graphic)


# displays and keeps track of the current level
class Level(Turtle):
    def __init__(self):
        super().__init__()
        self.current_level = 0
        self.hideturtle()
        self.penup()
        self.pencolor("black")
        self.setpos(-165, 275)

    def next(self):
        self.current_level += 1
        message = "Level: " + str(self.current_level)
        self.clear()
        self.write(message, align="center", font=("Bit5x3", 20, "normal"))


# displays and keeps track of the current number of lives
class Lives(Turtle):
    def __init__(self):
        super().__init__()
        self.current_lives = 3
        self.hideturtle()
        self.penup()
        self.pencolor("black")
        self.setpos(165, 275)
        message = "Lives: " + str(self.current_lives)
        self.write(message, align="center", font=("Bit5x3", 20, "normal"))

    def subtract_life(self):
        self.current_lives -= 1
        if self.current_lives < 0:
            message = "Lives: " + str(0)
        else:
            message = "Lives: " + str(self.current_lives)
        self.clear()
        self.write(message, align="center", font=("Bit5x3", 20, "normal"))


# creates and animates the turtle
class GameTurtle(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.color("green")
        self.setheading(90)
        self.setpos(-3, -277)

    def move_up(self):
        self.setheading(90)
        if self.ycor():
            self.forward(50)

    def move_down(self):
        self.setheading(270)
        if self.ycor() > -227:
            self.forward(50)

    def move_left(self):
        self.setheading(180)
        if self.xcor() > -154:
            self.forward(50)

    def move_right(self):
        self.setheading(0)
        if self.xcor() < 151:
            self.forward(50)

    def reset_turtle(self):
        self.setpos(-3, -277)
        self.setheading(90)


# creates and animates the cars, also adjusts difficulty by car speed and number of cars per lane
class Cars:
    def __init__(self):
        self.lanes = [(-245, -225), (-245, -175), (-245, -125), (-245, -75),
                      (245, 25), (245, 75), (245, 125), (245, 175)]
        self.cars_onscreen = []
        self.hidden_cars = []
        self.max_cars_in_lane = 1
        self.car_speed = 10

    def initialize_lanes(self):
        for position in self.lanes:
            self.populate_lane(position)

    def populate_lane(self, lane):
        stop = randint(1, self.max_cars_in_lane)
        cars_per_lane = range(1, stop + 1, 1)
        for _ in cars_per_lane:
            self.create_car(lane)

    def create_car(self, lane):
        x = randint(-244, 244)
        y = lane[1]
        if self.hidden_cars:
            new_car = self.hidden_cars.pop()
            new_car.setpos(x, y)
            if y < 0:
                new_car.setheading(0)
            else:
                new_car.setheading(180)
            new_car.showturtle()
            self.cars_onscreen.append(new_car)
        else:
            new_car = Turtle("car")
            new_car.penup()
            new_car.setpos(x, y)
            if y < 0:
                new_car.setheading(0)
            else:
                new_car.setheading(180)
            self.cars_onscreen.append(new_car)

    def move(self, level):
        for car in self.cars_onscreen:
            if car.ycor() > 0:
                if car.xcor() < -245:
                    y = car.ycor()
                    car.setpos(250, y)
            elif car.ycor() < 0:
                if car.xcor() > 245:
                    y = car.ycor()
                    car.setpos(-255, y)
            slope = 20 / 99
            y_intercept = 970 / 99
            self.car_speed = round(slope * level + y_intercept)
            car.forward(self.car_speed)

    def increase_max_cars_in_lane(self, level):
        slope = 1 / 33
        y_intercept = 32 / 33
        max_cars_in_lane = round(slope * level + y_intercept)
        self.max_cars_in_lane = max_cars_in_lane

    def reset_lanes(self):
        x = 0
        while len(self.cars_onscreen) > 0:
            car = self.cars_onscreen.pop()
            car.hideturtle()
            self.hidden_cars.append(car)
            x += 1
