import arcade
import random
from arcade.types import Rect
from Hp_Potion import Hp_Potion
from Mp_Potion import Mp_Potion

# --- Scaling and room size ---
SCALE = 2
ROOM_WIDTH = 40
ROOM_HEIGHT = 20

# --- MiniMap class ---
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

        # Mark start room visited
        neighbors, _, looted = self.maze[self.character.currentPosition]
        self.maze[self.character.currentPosition] = (neighbors, True, looted)
        
        
    def draw(self, screen_width, screen_height, margin=20, alpha=255):
        """Draw the minimap in the upper-right corner."""
        ox = screen_width - self.width - margin
        oy = screen_height - self.height - margin
        drawn_connections = set()

        line_color = (*arcade.color.WHITE[:3], int(alpha))
        visited_color = (*arcade.color.YELLOW[:3], int(alpha))
        unvisited_color = (*arcade.color.BLUE[:3], int(alpha))
        end_color = (*arcade.color.RED[:3], int(alpha))
        looted_color = (*arcade.color.GREEN[:3], int(alpha))
        
        # Draw paths first
        for room, (neighbors, visited, _) in self.maze.items():
            if visited:
                room_x, room_y = self.positions[room]
                room_x = ox + room_x * SCALE
                room_y = oy + room_y * SCALE

                for target, dir_name, conn_label in neighbors:
                    if conn_label in self.connections and self.connections[conn_label][0] and conn_label not in drawn_connections:
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
                        elif dir_name == "Backward":
                            start_x = room_x + ROOM_WIDTH / 2
                            start_y = room_y
                            end_x = target_x + ROOM_WIDTH / 2
                            end_y = target_y + ROOM_HEIGHT

                        arcade.draw_line(start_x, start_y, end_x, end_y, line_color, 2)
                        drawn_connections.add(conn_label)

        # Draw rooms
        for room, (neighbors, visited, looted) in self.maze.items():
            if visited:
                x, y = self.positions[room]
                x = ox + x * SCALE
                y = oy + y * SCALE
                if room == self.character.currentPosition: color = visited_color 
                elif room == "End": color = end_color
                elif looted == True: color = looted_color
                else: color = unvisited_color
                arcade.draw_lbwh_rectangle_outline(x, y, ROOM_WIDTH, ROOM_HEIGHT, color, 2)


# --- MainScreen as a View ---
class MainScreen(arcade.View):
    def __init__(self, character, maze, connections):
        super().__init__()
        self.character = character
        self.maze = maze
        self.connections = connections
        self.minimap = MiniMap(character, maze, connections)
        
        self.bg_alpha = 0       # for image fade
        self.text_alpha = 0     # for text fade
        self.fade_speed_bg = 300
        self.fade_speed_text = 300
        self.text_delay = 1    # Seconds before text fades in
        self.frame_count = 0
        self.text_timer = 0.0   # elapsed time since fade started
        
        self.popup_state  = None  # None, "status", "equip"
        self.menu_index = 0       # which of Equip/Item/Exit is highlighted
        self.menu_options = ["Equip", "Item", "Exit"]
        self.popup_options  = []
        self.Equipment = character.equipment
        
        self.loot_popup_state = None    # None or "loot"
        self.loot_popup_text = ""       # text to display
        self.loot_popup_timer = 0.0     # auto-hide timer
        self.loot_popup_duration = 2.0  # seconds to show

        self.fade_in_complete = False  # Tracks if room fade-in is done
        
        self.hp_potion = Hp_Potion(self.character)
        self.mp_potion = Mp_Potion(self.character)

    
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        
        # Draw room background
        art_title = "_".join(option for _, option, _ in self.maze[self.character.currentPosition][0] if option != "Backward")
        if art_title == "":
            art_title = "Backward"
        texture = arcade.load_texture(f"Simple_RPG/Art/Room_Backgrounds/{art_title}.png")
        screen_width, screen_height = self.window.get_size()
        
        # Create a rectangle covering the whole screen
        rect = Rect(
            left=0,
            right=screen_width,
            bottom=0,
            top=screen_height,
            width=screen_width,
            height=screen_height,
            x=screen_width / 2,   # center x
            y=screen_height / 2   # center y
            )
        
        # Draw texture with alpha
        arcade.draw_texture_rect(
            texture,
            rect,
            alpha=int(self.bg_alpha)  # room fade
            )

        
        # Draw minimap
        self.minimap.draw(screen_width, screen_height, alpha=int(self.bg_alpha))

        # Draw bottom-centered movement options
        current = self.character.currentPosition
        neighbors, _, looted = self.maze[current]

        directions = [dir_name.upper() for _, dir_name, _ in neighbors]
        directions += ["Z - Investigate", "X - Check Stats"]
        movement_line = " | ".join(directions)
        
        font_size = 16
        text = arcade.Text(movement_line, 0, 0, arcade.color.WHITE, font_size)
        text.x = (screen_width - text.content_width) / 2

        # text.y = 40
        text.draw()
        
        # --- Draw status popup if open
        if self.popup_state is not None:
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

            # If status popup, draw stats text
            if self.popup_state == "status":
                stats_lines = [
                    f"Name: {self.character.name}",
                    f"Status: {self.character.title}",
                    f"HP: {self.character.hp}/{self.character.max_hp}",
                    f"MP: {self.character.mp}/{self.character.max_mp}",
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
            # Only draw the command bar for the status popup
            # We draw a 2nd container UNDER the main stats box.
            # Inside that container, 3 smaller selectable boxes go in a row.
            if self.popup_state == "status":
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
                
                # draw buttons (status popup buttons)
                num_buttons = len(self.popup_options)
                box_w = 100
                box_h = 60
                spacing = 20
                total_width = num_buttons * box_w + (num_buttons - 1) * spacing
                start_x = cx - total_width / 2
                box_center_y = bar_cy

                for i, option in enumerate(self.popup_options):
                    bx_left = start_x + i * (box_w + spacing)
                    bx_right = bx_left + box_w
                    by_top = box_center_y + box_h / 2
                    by_bottom = box_center_y - box_h / 2

                    outline_color = arcade.color.YELLOW if i == self.menu_index else arcade.color.RED

                    arcade.draw_lrbt_rectangle_filled(
                        left=bx_left, right=bx_right, top=by_top, bottom=by_bottom, color=arcade.color.BLACK
                    )
                    arcade.draw_lrbt_rectangle_outline(
                        left=bx_left, right=bx_right, top=by_top, bottom=by_bottom, color=outline_color, border_width=2
                    )
                    arcade.draw_text(
                        option,
                        (bx_left + bx_right) / 2,
                        box_center_y - 8,
                        arcade.color.WHITE,
                        16,
                        anchor_x="center"
                    )
                
            # Draw button (reusable for equip or items)
            else:
                # Draw equipment info when in equip menu
                if self.popup_state == "equip":
                    equip_lines = [
                        f"{self.character.equipment['Armor'][0]}: + {self.character.equipment['Armor'][1]} DEF",
                        f"{self.character.equipment['Weapon'][0]}: + {self.character.equipment['Weapon'][1]} ATK",
                    ]
                    for i, line in enumerate(equip_lines):
                        arcade.draw_text(
                            line,
                            cx,
                            cy + 40 - i * 30,
                            arcade.color.WHITE,
                            16,
                            anchor_x="center"
                        )
                
                if self.popup_state == "Item":
                    equip_lines = [
                        f"{self.character.items['HP Potion'][0]}: {self.character.items['HP Potion'][1]}",
                        f"{self.character.items['MP Potion'][0]}: {self.character.items['MP Potion'][1]}",
                    ]
                    for i, line in enumerate(equip_lines):
                        arcade.draw_text(
                            line,
                            cx,
                            cy + 40 - i * 30,
                            arcade.color.WHITE,
                            16,
                            anchor_x="center"
                        )
                
                num_buttons = len(self.popup_options)
                if num_buttons > 0:
                    box_w = 200 if num_buttons == 1 else 100
                    box_h = 60
                    spacing = 20 if num_buttons > 1 else 0
                    total_width = num_buttons * box_w + (num_buttons - 1) * spacing
                    start_x = cx - total_width / 2
                    box_center_y = cy - h / 2 + 50

                    for i, option in enumerate(self.popup_options):
                        bx_left = start_x + i * (box_w + spacing)
                        bx_right = bx_left + box_w
                        by_top = box_center_y + box_h / 2
                        by_bottom = box_center_y - box_h / 2

                        outline_color = arcade.color.YELLOW if i == self.menu_index else arcade.color.RED


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
        # --- Show loot/investigation popup (if active) ---
        if self.loot_popup_state == "loot":
            cx = self.window.width / 2
            cy = 100  # position near bottom of screen
            w = 400
            h = 60

            # Background box
            arcade.draw_lrbt_rectangle_filled(
                left=cx - w/2, right=cx + w/2,
                top=cy + h/2, bottom=cy - h/2,
                color=arcade.color.BLACK
            )
            arcade.draw_lrbt_rectangle_outline(
                left=cx - w/2, right=cx + w/2,
                top=cy + h/2, bottom=cy - h/2,
                color=arcade.color.YELLOW, border_width=2
            )

            # Text message
            arcade.draw_text(
                self.loot_popup_text,
                cx, cy - 8,
                arcade.color.WHITE,
                16,
                anchor_x="center"
            )



    def generate_Item(self):
        items = []
        num = random.randint(1,10)
        if num == 1 or num == 2:
            items.append("HP Potion")
        num = random.randint(1,10)
        if num == 1 or num == 2:
            items.append("MP Potion")
        return items


    def on_key_press(self, key, modifiers):
        # Only allow movement if fade-in is complete
        if not self.fade_in_complete:
            return
        
        current = self.character.currentPosition
        neighbors, visited, looted = self.maze[current]
        
        # X always toggles stats open/closed
        if key == arcade.key.X:
            if self.popup_state == "status":
                self.popup_state = None
            else:
                self.popup_state = "status"
                self.menu_index = 0
                self.popup_options = self.menu_options.copy()
            return
        
        # Handle Investigating
        if key == arcade.key.Z:
            neighbors, visited, looted = self.maze[current]
            if looted == False:
                loot = self.generate_Item()
                for item in loot:
                    self.character.pickup(item)
                self.maze[current] = (neighbors, visited, True)
                
                if loot:
                    self.loot_popup_text = "You found: " + ", ".join(loot)
                else:
                    self.loot_popup_text = "Nothing was found here."
                self.loot_popup_state = "loot"
                self.loot_popup_timer = 0.0
            else:
                self.loot_popup_text = "This room has already been investigated."
                self.loot_popup_state = "loot"
                self.loot_popup_timer = 0.0
        
        # Handle popup navigation
        if self.popup_state is not None:
            # Left/right to navigate menu
            if key == arcade.key.RIGHT:
                self.menu_index = (self.menu_index + 1) % len(self.popup_options)
            elif key == arcade.key.LEFT:
                self.menu_index = (self.menu_index - 1) % len(self.popup_options)
            # Enter to select
            elif key == arcade.key.ENTER:
                selected = self.popup_options[self.menu_index]

                # Status popup actions
                if self.popup_state == "status":
                    if selected == "Exit":
                        self.popup_state = None
                    elif selected == "Equip":
                        self.popup_state = "equip"
                        self.menu_index = 0
                        self.popup_options = ["EXIT"]
                    elif selected == "Item":
                        self.popup_state = "Item"
                        self.menu_index = 0
                        self.popup_options = ["Use HP", "Use MP","EXIT"]

                # Equip popup actions
                elif self.popup_state == "equip":
                    if selected == "EXIT":
                        self.popup_state = None
                
                # Item popup actions
                elif self.popup_state == "Item":
                    if selected == "EXIT":
                        self.popup_state = None
                        
                    elif selected == "Use HP":
                        healed = self.hp_potion.use()
                        if healed > 0:
                            self.loot_popup_text = f"You used an HP Potion and restored {healed} HP!"
                        else:
                            self.loot_popup_text = "You have no HP Potions left!"
                        self.loot_popup_state = "loot"
                        self.loot_popup_timer = 0.0
                        
                    elif selected == "Use MP":
                        restored = self.mp_potion.use()
                        if restored > 0:
                            self.loot_popup_text = f"You used an MP Potion and restored {restored} MP!"
                        else:
                            self.loot_popup_text = "You have no MP Potions left!"
                        self.loot_popup_state = "loot"
                        self.loot_popup_timer = 0.0
                        
            return
        
        # Movement Handling
        dir_map = {
            arcade.key.LEFT: "Left",
            arcade.key.RIGHT: "Right",
            arcade.key.UP: "Forward",
            arcade.key.DOWN: "Backward",
        }
        direction = dir_map.get(key)
        if not direction:
            return
        
        # --- Only reset fade if a valid move occurs ---
        moved = False

        for target, dir_name, conn_label in neighbors:
            if dir_name == direction:
                # --- Mark the current room before leaving ---
                curr_neighbors, curr_visited, curr_looted = self.maze[current]
                # Keep looted status as-is (don't reset it)
                self.maze[current] = (curr_neighbors, True, curr_looted)
                
                # Update player position
                self.character.currentPosition = target
                n, visited, looted = self.maze[target]
                self.maze[target] = (n, True, looted)

                if conn_label in self.connections:
                    visited, data = self.connections[conn_label]
                    if not visited:
                        self.connections[conn_label] = (True, data)
                moved = True
                break
            
        # Reset fade for new room
        if moved == True:
            self.bg_alpha = 0
            self.text_alpha = 0
            self.text_timer = 0
            self.fade_in_complete = False 
    
    def on_update(self, delta_time: float):
        """Update fade animation each frame."""
        # --- Fade in room background ---
        if self.bg_alpha < 255:
            self.bg_alpha += self.fade_speed_bg * delta_time
            if self.bg_alpha > 255:
                self.bg_alpha = 255

        # --- Fade in text after delay ---
        self.text_timer += delta_time
        if self.text_timer >= self.text_delay and self.text_alpha < 255:
            self.text_alpha += self.fade_speed_text * delta_time
            if self.text_alpha > 255:
                self.text_alpha = 255
        
        # --- Check if fade-in is complete ---
        if self.bg_alpha >= 255 and self.text_alpha >= 255:
            self.fade_in_complete = True
            
        # --- Loot popup timer ---
        if self.loot_popup_state == "loot":
            self.loot_popup_timer += delta_time
            if self.loot_popup_timer >= self.loot_popup_duration:
                self.loot_popup_state = None
            
        
        
