import arcade
import random
from operator import add

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 650
SCREEN_TITLE = "Psychedelic Lines"

FOLLOW_DISTANCE = 10
MAX_DX = MAX_DY = 3


class Line:
    def __init__(self):
        self.points = [0, 0, 0, 0]
        self.diff = [0, 0, 0, 0]
        self.color = arcade.color.WHITE_SMOKE


class DController:
    """
    Control UI Element for dx and dy of lines
    """

    def __init__(self, center_x, center_y, width, height, max_value_x, max_value_y, value_x, value_y):
        self.is_pressed = False
        self.center_x = self.knob_x = center_x
        self.center_y = self.knob_y = center_y
        self.width = width
        self.height = height
        self.max_value_x = max_value_x
        self.max_value_y = max_value_y
        self.value_x = value_x
        self.value_y = value_y
        self.knob_radius = 5
        self.x_bound_min = self.center_x + (self.width / 2) - self.knob_radius
        self.x_bound_max = self.center_x - (self.width / 2) + self.knob_radius
        self.y_bound_min = self.center_y + (self.height / 2) - self.knob_radius
        self.y_bound_max = self.center_y - (self.height / 2) + self.knob_radius

    def draw(self):
        arcade.draw_rectangle_outline(self.center_x, self.center_y, self.width, self.height,
                                      color=arcade.color.WHITE_SMOKE)
        arcade.draw_circle_filled(self.knob_x, self.knob_y, self.knob_radius, (255, 255, 80))

    def is_knob_pressed(self, x, y):
        dist_x = self.knob_x - x
        dist_y = self.knob_y - y
        self.is_pressed = (dist_x ** 2 + dist_y ** 2) <= self.knob_radius ** 2
        return self.is_pressed

    def mouse_motion(self, x, y):
        if self.is_pressed:
            self.drag_knob(x, y)

    def drag_knob(self, x, y):
        if self.x_bound_max < x < self.x_bound_min:
            self.knob_x = x
        if self.y_bound_max < y < self.y_bound_min:
            self.knob_y = y

        self.value_x = (self.knob_x - self.center_x) / ((self.x_bound_max - self.x_bound_min)/2) * self.max_value_x
        self.value_y= (self.knob_y - self.center_y) / ((self.x_bound_max - self.x_bound_min)/2) * self.max_value_y
        print(self.value_x, self.value_y)

    def release(self):
        self.is_pressed = False


def check_mouse_press_for_controller(x, y, controller_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for controller in controller_list:
        if controller.is_knob_pressed(x, y):
            continue


class LineRunner(arcade.Window):

    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, SCREEN_TITLE)
        self.line_list = []
        self.controller_list = []

    def setup(self):
        line = Line()
        line.points = [random.randrange(CANVAS_WIDTH),
                       random.randrange(CANVAS_HEIGHT) + (WINDOW_HEIGHT - CANVAS_HEIGHT),
                       random.randrange(CANVAS_WIDTH),
                       random.randrange(CANVAS_HEIGHT) + (WINDOW_HEIGHT - CANVAS_HEIGHT)]
        line.diff = [random.randrange(MAX_DX * 100) / 100 for _ in line.diff]
        self.line_list.append(line)

        self.controller_list.append(DController(600, 25, 40, 40, MAX_DX, MAX_DY, 0, 0))
        self.controller_list.append(DController(660, 25, 40, 40, MAX_DX, MAX_DY, 0, 0))

    def on_draw(self):
        arcade.start_render()
        for line in self.line_list:
            arcade.draw_line(*line.points, line.color)
        for controller in self.controller_list:
            controller.draw()

    def update(self, delta_time):
        comp = [CANVAS_WIDTH, CANVAS_HEIGHT + (WINDOW_HEIGHT - CANVAS_HEIGHT)] * 2
        for line in self.line_list:
            line.points = list(map(add, line.points, line.diff))

            for i in range(len(line.points)):
                if line.points[i] <= 0 or line.points[i] >= comp[i]:
                    line.diff[i] *= -1

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """

        controller_active = False
        for controller in self.controller_list:
            if controller.is_knob_pressed(x, y):
                controller_active = True

        if not controller_active:
            line = Line()

            last_line = self.line_list[-1]
            line.points = [last_line.points[i] - FOLLOW_DISTANCE * last_line.diff[i] for i in range(len(line.points))]
            line.diff = last_line.diff[:]

            self.line_list.append(line)

    def on_mouse_motion(self, x, y, dx, dy):
        for controller in self.controller_list:
            controller.mouse_motion(x, y)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        for controller in self.controller_list:
            controller.release()


def main():
    line_runner = LineRunner()
    line_runner.setup()
    arcade.run()


if __name__ == "__main__":
    main()
