import math
from graphics import Circle, GraphWin, Line, Point, Polygon, Rectangle


def main():
    size, colours = get_inputs()
    win, patches = display_patchwork(size, colours)
    edit_patchwork(win, patches)


def get_inputs():
    valid_sizes = ["5", "7", "9"]
    size = ""

    while size not in valid_sizes:
        size = input("\nPlease enter a common value for the width and "
                     "height of the patchwork size (5, 7, or 9): ")
        # Remove whitespace
        size = size.replace(" ", "")[0]

        if size in valid_sizes:
            print("You have chosen patchwork size {0} × {0}.".format(size))
        else:
            print("Error: You have not chosen a valid size.")

    valid_colours = ["blue", "green", "magenta", "orange", "pink", "red"]
    colours = []

    while len(colours) < 3:
        colour = input("\nPlease enter colour #" + str(len(colours) + 1) +
                       " (red, green, blue, magenta, orange, or pink): ")
        # Remove whitespace and convert to lowercase
        colour = colour.replace(" ", "").lower()

        if colour in valid_colours and colour not in colours:
            colours.append(colour)
            print("You have chosen the colour {0}.".format(colour))
        elif colour in colours:
            print("Error: You have already chosen this colour.")
        else:
            print("Error: You have not chosen a valid colour.")

    return int(size), colours


def display_patchwork(size, colours):
    size = size * 100
    win = GraphWin("Patchwork Sampler", size, size)
    win.setBackground("white")
    patches = []

    for row in range(0, size, 100):
        for column in range(0, size, 100):
            colour = choose_colour(column, row, size, colours)

            if row == column:
                patch = draw_patch_two(win, column, row, colour)
            else:
                patch = draw_patch_one(win, column, row, colour)

            patches.append(patch)

    return win, patches


def choose_colour(column, row, size, colours):
    if 100 <= row <= size - 200 and 100 <= column <= size - 200:
        colour = colours[2]
    elif row % 200 == 0 and column % 200 == 0:
        colour = colours[0]
    else:
        colour = colours[1]

    return colour


def draw_patch_one(win, x, y, colour):
    patch_shapes = []
    even_positions, odd_positions = [20, 60], [0, 40, 80]

    # Loop through the rows and columns of the patch
    # to define the square, tilted square, and inner circle
    for row in range(0, 100, 20):
        for column in range(0, 100, 20):
            square = Rectangle(Point(x + column, y + row),
                               Point(x + column + 20, y + row + 20))

            # Set the square fill colour if
            # it is in rows 2 or 4 or columns 1, 3, or 5
            if row in even_positions or column in odd_positions:
                square.setFill(colour)

            # Set the tilted square if
            # it is in rows 1, 3, or 5 and columns 2 or 4
            if row in odd_positions and column in even_positions:
                tilted_square = Polygon(Point(x + column, y + row + 10),
                                        Point(x + column + 10, y + row),
                                        Point(x + column + 20, y + row + 10),
                                        Point(x + column + 10, y + row + 20))
                tilted_square.setFill(colour)
                patch_shapes.append(tilted_square)

            circle = Circle(Point(x + column + 10, y + row + 10), 5)
            circle.setFill("white")

            for shape in [square, circle]:
                patch_shapes.append(shape)

            patch_box = draw_patch_box(x, y)

    for shape in patch_shapes:
        shape.draw(win).setOutline("")

    drawn, design, elements = True, "1", [patch_box, patch_shapes]
    return [colour, drawn, design, x, y, elements]


def draw_patch_two(win, x, y, colour):
    patch_shapes = []

    # Loop through the diagonal points of the patch
    for i in range(0, 110, 10):
        # Define lines for the top/bottom and left/right sections
        line1 = Line(Point(x + i, y), Point(x + 100 - i, y + 100))
        line2 = Line(Point(x, y + i), Point(x + 100, y + 100 - i))

        patch_shapes.append(line1)
        patch_shapes.append(line2)

        patch_box = draw_patch_box(x, y)

    for shape in patch_shapes:
        shape.draw(win).setFill(colour)

    drawn, design, elements = True, "2", [patch_box, patch_shapes]
    return [colour, drawn, design, x, y, elements]


def draw_patch_box(x, y):
    patch_box = Rectangle(Point(x, y), Point(x + 100, y + 100))
    patch_box.setWidth(5)
    return patch_box


def edit_patchwork(win, patches):
    complete = False
    colour_choices = ["r", "g", "b", "m", "o", "p"]
    colours = ["red", "green", "blue", "magenta", "orange", "pink"]

    while not complete:
        nearest_x, nearest_y = get_click(win)

        for patch in patches:
            # Retrieve patch details from individually drawn patches
            patch_colour, patch_drawn, patch_design = patch[0], patch[1], patch[2]
            patch_x, patch_y = patch[3], patch[4]
            patch_box = patch[5][0]

            if nearest_x == patch_x and nearest_y == patch_y:
                # Select the patch and begin retrieving key presses
                patch_box.draw(win).setWidth(5)
                key = ""

                while key != "return":
                    key = win.getKey().lower()

                    if key == "d" and patch_drawn:
                        # Delete the patch and redraw the box encasing it
                        patch_drawn = delete_patch(patch)
                        patch_box.draw(win)
                    elif key == "s" and patch_drawn:
                        # Delete and redraw the patch with the opposite design
                        patch_drawn = delete_patch(patch)

                        new_patch = switch_patch(win, patch_x, patch_y,
                                                 patch_colour, patch_design)
                        patch_colour, patch_drawn, \
                            patch_design, patch_box = update_patch(
                                new_patch, patch)

                        patch_box.draw(win)
                    elif key in colour_choices and not patch_drawn:
                        # Choose the colour corresponding to the input
                        patch_colour = colours[colour_choices.index(key)]

                        # Delete and redraw the patch box with design 2
                        patch_box.undraw()

                        new_patch = draw_patch_two(win, patch_x, patch_y,
                                                   patch_colour)
                        patch_colour, patch_drawn, \
                            patch_design, patch_box = update_patch(
                                new_patch, patch)

                        patch_box.draw(win)
                # Deselect the patch
                patch_box.undraw()


def delete_patch(selected_patch):
    # Undraw each patch element
    patch_box, patch_shapes = selected_patch[5][0], selected_patch[5][1]
    patch_box.undraw()

    for shape in patch_shapes:
        shape.undraw()

    selected_patch[1] = False
    return selected_patch[1]


def switch_patch(win, x, y, patch_colour, patch_design):
    if patch_design == "1":
        new_patch = draw_patch_two(win, x, y, patch_colour)
    else:
        new_patch = draw_patch_one(win, x, y, patch_colour)
    return new_patch


def update_patch(new_patch, selected_patch):
    for detail in range(len(new_patch)):
        selected_patch[detail] = new_patch[detail]

    patch_colour, patch_drawn, \
        patch_design, patch_box = selected_patch[0], selected_patch[1], \
        selected_patch[2], selected_patch[5][0]

    return patch_colour, patch_drawn, patch_design, patch_box


def get_click(win):
    click = win.getMouse()
    nearest_x, nearest_y = math.floor(click.getX() / 100) * 100, \
        math.floor(click.getY() / 100) * 100
    return nearest_x, nearest_y


main()
