import arcade
import random
from operator import add

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Psychedelic Lines"

FOLLOW_DISTANCE = 10


class Line:
    def __init__(self):
        self.points = [0, 0, 0, 0]
        self.diff = [0, 0, 0, 0]
        self.color = arcade.color.WHITE_SMOKE


class LineRunner(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.line_list = []

    def on_draw(self):
        arcade.start_render()
        for line in self.line_list:
            arcade.draw_line(*line.points, line.color)

    def update(self, delta_time):
        comp = [SCREEN_WIDTH, SCREEN_HEIGHT] * 2
        for line in self.line_list:
            line.points = list(map(add, line.points, line.diff))

            for i in range(len(line.points)):
                if line.points[i] <= 0 or line.points[i] >= comp[i]:
                    line.diff[i] *= -1

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
        line = Line()

        if len(self.line_list) == 0:
            line.points = [random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT), random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT)]
            line.diff = [random.randrange(-3, 3), random.randrange(-3, 3), random.randrange(-3, 3), random.randrange(-3, 3)]
        else:
            last_line = self.line_list[-1]
            line.points = [last_line.points[i] + FOLLOW_DISTANCE * last_line.diff[i] for i in range(len(line.points))]
            line.diff = last_line.diff[:]

        self.line_list.append(line)


def main():

    line_runner = LineRunner()
    # line_runner.setup()
    arcade.run()


if __name__ == "__main__":
    main()
