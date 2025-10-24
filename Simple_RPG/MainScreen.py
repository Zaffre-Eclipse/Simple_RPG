import arcade

SCALE = 2
ROOM_WIDTH = 40
ROOM_HEIGHT = 20

class MiniMap:
    positions = {
        "Start": (50, 45),
        "Room 1": (70, 25),
        "Room 2": (10, 45),
        "Room 3": (10, 75),
        "Room 4": (25, 30),
        "Room 5": (55, 5),
        "Room 6": (50, 75),
        "Room 7": (110, 5),
        "Room 8": (85, 75),
        "Room 9": (85, 45),
        "Room 10": (110, 60),
        "Room 11": (110, 85),
        "Room 12": (85, 115),
        "Room 13": (10, 95),
        "Room 14": (50, 95),
        "Room 15": (10, 5),
        "Room 16": (100, 25),
        "End": (40, 115)
    }

    def __init__(self, character, maze, connections):
        self.character = character
        self.maze = maze
        self.connections = connections
        self.width = 140 * SCALE
        self.height = 140 * SCALE

        # Mark starting room as visited
        neighbors, _ = self.maze[self.character.currentPosition]
        self.maze[self.character.currentPosition] = (neighbors, True)

    def draw(self, screen_width, screen_height, margin=20):
        """Draw the minimap in the upper-right corner."""
        ox = screen_width - self.width - margin
        oy = screen_height - self.height - margin
        drawn_connections = set()

        # Draw paths first
        for room, (neighbors, visited) in self.maze.items():
            if visited:
                room_x, room_y = self.positions[room]
                room_x = ox + room_x * SCALE
                room_y = oy + room_y * SCALE

                for target, dir_name, conn_label in neighbors:
                    if (
                        conn_label in self.connections
                        and self.connections[conn_label][0]
                        and conn_label not in drawn_connections
                    ):
                        target_x, target_y = self.positions[target]
                        target_x = ox + target_x * SCALE
                        target_y = oy + target_y * SCALE

                        if dir_name == "Left":
                            start_x = room_x
                            start_y = room_y + ROOM_HEIGHT / 2
                            end_x = target_x + ROOM_WIDTH
                            end_y = target_y + ROOM_HEIGHT / 2
                        elif dir_name == "Right":
                            start_x = room_x + ROOM_WIDTH
                            start_y = room_y + ROOM_HEIGHT / 2
                            end_x = target_x
                            end_y = target_y + ROOM_HEIGHT / 2
                        elif dir_name == "Forward":
                            start_x = room_x + ROOM_WIDTH / 2
                            start_y = room_y + ROOM_HEIGHT
                            end_x = target_x + ROOM_WIDTH / 2
                            end_y = target_y
                        else:  # "Backward"
                            start_x = room_x + ROOM_WIDTH / 2
                            start_y = room_y
                            end_x = target_x + ROOM_WIDTH / 2
                            end_y = target_y + ROOM_HEIGHT

                        arcade.draw_line(
                            start_x, start_y, end_x, end_y,
                            arcade.color.WHITE, 2
                        )
                        drawn_connections.add(conn_label)

        # Draw rooms
        for room, (neighbors, visited) in self.maze.items():
            if visited:
                x, y = self.positions[room]
                x = ox + x * SCALE
                y = oy + y * SCALE
                color = (
                    arcade.color.YELLOW
                    if room == self.character.currentPosition
                    else arcade.color.BLUE
                )
                arcade.draw_lbwh_rectangle_outline(
                    x, y, ROOM_WIDTH, ROOM_HEIGHT,
                    color, 2
                )


class MainScreen(arcade.View):
    def __init__(self, character, maze, connections):
        super().__init__()
        self.character = character
        self.maze = maze
        self.connections = connections
        self.minimap = MiniMap(character, maze, connections)

        self.show_status = False  # are we in status mode
        self.menu_index = 0       # which of Equip/Item/Exit is highlighted
        self.menu_options = ["Equip", "Item", "Exit"]

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        screen_width, screen_height = self.window.get_size()

        # --- Always draw maze/minimap background
        self.minimap.draw(screen_width, screen_height)

        # --- Movement / controls line at bottom
        current = self.character.currentPosition
        neighbors, _ = self.maze[current]

        directions = [dir_name.upper() for _, dir_name, _ in neighbors]
        directions += ["Z - Investigate", "X - Check Stats"]
        movement_line = " | ".join(directions)

        movement_text = arcade.Text(
            movement_line,
            0,
            40,
            arcade.color.WHITE,
            16
        )
        movement_text.x = (screen_width - movement_text.content_width) / 2
        movement_text.draw()

        # --- Draw status popup if open
        if self.show_status:
            cx = screen_width / 2
            cy = screen_height / 2 + 40  # bump stats box a little higher
            w = 400
            h = 220

            # ========== BIG STATS WINDOW ==========
            # black fill
            arcade.draw_lrbt_rectangle_filled(
                left=cx - w / 2,
                right=cx + w / 2,
                top=cy + h / 2,
                bottom=cy - h / 2,
                color=arcade.color.BLACK,
            )

            # red outline
            arcade.draw_lrbt_rectangle_outline(
                left=cx - w / 2,
                right=cx + w / 2,
                top=cy + h / 2,
                bottom=cy - h / 2,
                color=arcade.color.RED,
                border_width=3,
            )

            # character stats text (NO "Press X to close")
            stats_lines = [
                f"Name: {self.character.name}",
                f"Status: {self.character.title}",
                f"HP: {self.character.hp}/{self.character.max_hp}",
                f"MP: {self.character.mp}%",
                f"ATK: {self.character.atk} | DEF: {self.character.defense} | SPD: {self.character.spd}",
            ]

            for i, line in enumerate(stats_lines):
                arcade.draw_text(
                    line,
                    cx,
                    cy + 70 - i * 25,
                    arcade.color.WHITE,
                    16,
                    anchor_x="center"
                )

            # ========== COMMAND BAR UNDER STATS WINDOW ==========
            # We draw a 2nd container UNDER the main stats box.
            # Inside that container, 3 smaller selectable boxes go in a row.

            bar_w = 420
            bar_h = 100

            bar_cy = cy - h / 2 - bar_h / 2 - 10  # 10px gap below stats box

            # outer bar background + outline
            arcade.draw_lrbt_rectangle_filled(
                left=cx - bar_w / 2,
                right=cx + bar_w / 2,
                top=bar_cy + bar_h / 2,
                bottom=bar_cy - bar_h / 2,
                color=arcade.color.BLACK,
            )
            arcade.draw_lrbt_rectangle_outline(
                left=cx - bar_w / 2,
                right=cx + bar_w / 2,
                top=bar_cy + bar_h / 2,
                bottom=bar_cy - bar_h / 2,
                color=arcade.color.RED,
                border_width=3,
            )

            # now the 3 option boxes inside that bar
            box_w = 100
            box_h = 60
            spacing = 20

            total_inner_width = (
                len(self.menu_options) * box_w
                + (len(self.menu_options) - 1) * spacing
            )
            start_x = cx - total_inner_width / 2
            box_center_y = bar_cy  # center vertically in the bar

            for i, option in enumerate(self.menu_options):
                # left/right bounds of this box
                bx_left = start_x + i * (box_w + spacing)
                bx_right = bx_left + box_w
                by_top = box_center_y + box_h / 2
                by_bottom = box_center_y - box_h / 2

                outline_color = (
                    arcade.color.YELLOW if i == self.menu_index
                    else arcade.color.RED
                )

                # inner fill
                arcade.draw_lrbt_rectangle_filled(
                    left=bx_left,
                    right=bx_right,
                    top=by_top,
                    bottom=by_bottom,
                    color=arcade.color.BLACK
                )

                # outline
                arcade.draw_lrbt_rectangle_outline(
                    left=bx_left,
                    right=bx_right,
                    top=by_top,
                    bottom=by_bottom,
                    color=outline_color,
                    border_width=2
                )

                # text label
                arcade.Text(
                    option,
                    (bx_left + bx_right) / 2,
                    box_center_y - 8,
                    arcade.color.WHITE,
                    16,
                    anchor_x="center"
                ).draw()

    def on_key_press(self, key, modifiers):
        # X always toggles stats open/closed
        if key == arcade.key.X:
            self.show_status = not self.show_status
            return

        # If stats window is open, we are in menu-navigation mode
        if self.show_status:
            if key == arcade.key.RIGHT:
                self.menu_index = (self.menu_index + 1) % len(self.menu_options)
            elif key == arcade.key.LEFT:
                self.menu_index = (self.menu_index - 1) % len(self.menu_options)
            elif key == arcade.key.Z:
                selected = self.menu_options[self.menu_index]
                if selected == "Exit":
                    # same effect as pressing X
                    self.show_status = False
                # "Equip" and "Item" are placeholders for future
            return

        # If stats window is NOT open, normal movement works
        current = self.character.currentPosition
        neighbors, _ = self.maze[current]

        dir_map = {
            arcade.key.LEFT: "Left",
            arcade.key.RIGHT: "Right",
            arcade.key.UP: "Forward",
            arcade.key.DOWN: "Backward",
        }
        direction = dir_map.get(key)
        if not direction:
            return

        # Move between rooms
        for target, dir_name, conn_label in neighbors:
            if dir_name == direction:
                # update current room
                self.character.currentPosition = target

                # mark room visited
                n, _ = self.maze[target]
                self.maze[target] = (n, True)

                # mark connection visited (unlocks white line)
                if conn_label in self.connections:
                    visited, data = self.connections[conn_label]
                    if not visited:
                        self.connections[conn_label] = (True, data)
                break
