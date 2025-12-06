import arcade
import random
from arcade.types import Rect
from Hp_Potion import Hp_Potion
from Mp_Potion import Mp_Potion
from PIL import Image
from io import BytesIO
from Necromancer import Necromancer


# --- Scaling and room size ---
SCALE = 2
ROOM_WIDTH = 40
ROOM_HEIGHT = 20

# --- MiniMap class ---
class MiniMap:
    '''
    MiniMap class.

    Attributes:
        positions: The positions of the rooms.
    '''
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
        '''
        Initializes the minimap.

        Args:
            character: The character.
            maze: The maze.
            connections: The connections in the maze.
        '''
        self.character = character
        self.maze = maze
        self.connections = connections
        self.width = 140 * SCALE
        self.height = 140 * SCALE

        # Mark start room visited
        neighbors, _, looted = self.maze[self.character.currentPosition]
        self.maze[self.character.currentPosition] = (neighbors, True, looted)
        
        
    def draw(self, screen_width, screen_height, margin=20, alpha=255):
        '''
        Draws the minimap in the upper-right corner.

        Args:
            screen_width: The width of the screen.
            screen_height: The height of the screen.
            margin: The margin of the minimap.
            alpha: The alpha value for the minimap.
        '''
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
                    # Draw connection if both rooms are visited (not just if connection is visited)
                    target_visited = self.maze.get(target, (None, False, False))[1]
                    if target_visited and conn_label not in drawn_connections:
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
                
                # Determine color: current position takes priority, then End, then looted, then visited
                if room == self.character.currentPosition: 
                    color = visited_color  # Yellow for current position
                elif room == "End": 
                    color = end_color  # Red for End room
                elif looted: 
                    color = looted_color  # Green for looted rooms
                else: 
                    color = unvisited_color  # Blue for visited but not looted
                


# --- MainScreen as a View ---
class MainScreen(arcade.View):
    '''
    MainScreen class.

    Attributes:
        character: The character.
        maze: The maze.
        connections: The connections in the maze.
        minimap: The minimap.
        bg_alpha: The alpha value for the background.
        text_alpha: The alpha value for the text.
        fade_speed_bg: The speed of the background fade.
        fade_speed_text: The speed of the text fade.
        text_delay: The delay before the text fades in.
        frame_count: The current frame count.
        text_timer: The elapsed time since the fade started.
        popup_state: The state of the popup.
        menu_index: The index of the menu.
        menu_options: The options of the menu.
        popup_options: The options of the popup.
        Equipment: The equipment of the character.
        loot_popup_state: The state of the loot popup.
        loot_popup_text: The text of the loot popup.
        loot_popup_timer: The timer of the loot popup.
        loot_popup_duration: The duration of the loot popup.
        fight_alpha: The alpha value for the fight.
        fight_fade_speed: The speed of the fight fade.
        fight_text_alpha: The alpha value for the fight text.
        room_textures: The textures of the rooms.
        room_texture: The texture of the current room.
        enemies: The enemies in the fight.
        fight_sprites: The sprites of the fight.
        turn: The turn of the fight.
        fight_menu_index: The index of the fight menu.
        fight_buttons: The buttons of the fight menu.
        player_display_hp: The hp of the player.
        game_over: The state of the game over.
        game_over_menu_index: The index of the game over menu.
        game_over_options: The options of the game over menu.
    '''
    def __init__(self, character, maze, connections):
        super().__init__()
        self.character = character
        self.maze = maze
        self.connections = connections
        self.minimap = MiniMap(character, maze, connections)
        
        self.bg_alpha = 0       # for image fade
        self.text_alpha = 0     # for text fade
        self.fade_speed_bg = 500
        self.fade_speed_text = 500
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
        
        self.in_fight = False       # Are we currently in a fight?
        self.fight_enemy = None     # Optional: enemy sprite / data
        self.fight_alpha = 0        # Fade for room background during fight
        self.fight_fade_speed = 500
        self.fight_text_alpha = 0
        
        # cache for current room background
        self.room_textures = {}  # key: art_title, value: arcade.Texture
        self.room_texture = None
                
        # Create an enemy list
        self.enemies =[Necromancer()]
        self.fight_sprites = arcade.SpriteList()
        
        self.turn = "player"
        
        # Tracks which fight button is highlighted
        self.fight_menu_index = 0
        self.fight_buttons = ["Attack", "Items"]
        
        self.player_display_hp = self.character.hp
        
        # GAME OVER logic
        self.game_over = False
        self.game_over_menu_index = 0
        self.game_over_options = ["Restart", "Quit"]

    
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
    
    
    def restart_game(self):
        """Reset the game to initial state."""
        # Reset character
        self.character.reset()
        
        # Reset maze (mark all rooms unvisited except start)
        for room, (neighbors, _, looted) in self.maze.items():
            visited = (room == "Start")
            self.maze[room] = (neighbors, visited, False)

        # Reset connections
        for conn_label in self.connections:
            visited, data = self.connections[conn_label]
            self.connections[conn_label] = (False, data)
            
        # Reset minimap
        self.minimap = MiniMap(self.character, self.maze, self.connections)


        # Reset fight state
        self.in_fight = False
        self.fight_enemy = None
        self.fight_sprites = arcade.SpriteList()
        self.turn = "player"
        
        # Reset popups
        self.popup_state = None
        self.loot_popup_state = None

        # Reset fade
        self.bg_alpha = 0
        self.text_alpha = 0
        self.fade_in_complete = False
        
        # Reset Game Over flag
        self.game_over = False
        self.game_over_menu_index = 0
        
        # Reset Hp bars
        self.player_display_hp = self.character.hp
        self.current_enemy_display_hp = 0



    
    def load_enemy_sprite(self, enemy_name, scale=3.0):
        """
        Loads an enemy sprite and splits its sprite sheet into frames.
        Returns a tuple: (arcade.Sprite, list_of_frames)
        """
        sheet_path = f"Art/Enemies/{enemy_name}.png"
        frame_width = 160
        frame_height = 128
        columns = 17
        rows = 7

        # Load sheet as PIL image
        sheet_image = Image.open(sheet_path).convert("RGBA")
        sheet_width, sheet_height = sheet_image.size

        frames = []
        for row in range(rows):
            for col in range(columns):
                left = col * frame_width
                top = sheet_height - (row + 1) * frame_height
                right = left + frame_width
                bottom = top + frame_height
                frame_image = sheet_image.crop((left, top, right, bottom))

                temp_file = BytesIO()
                frame_image.save(temp_file, format="PNG")
                temp_file.seek(0)

                texture = arcade.load_texture(temp_file)
                frames.append(texture)

        # Create sprite
        sprite = arcade.Sprite()
        sprite.texture = frames[0]
        sprite.scale = scale
        sprite.visible = False

        return sprite, frames


    def draw_enemy_hp_bar(self, bar_width=100, bar_height=10):
        '''
        Draws the enemy hp bar.

        Args:
            bar_width: The width of the enemy hp bar.
            bar_height: The height of the enemy hp bar.
        '''
        enemy = self.current_enemy
        sprite = self.fight_enemy

        if enemy is None or sprite is None:
            return

        fill_ratio = max(self.current_enemy_display_hp / enemy.max_hp, 0)
        filled_width = bar_width * fill_ratio

        cx = sprite.center_x
        cy = sprite.center_y + sprite.height / 2 + 15

        left = cx - bar_width / 2
        right = cx + bar_width / 2
        bottom = cy - bar_height / 2
        top = cy + bar_height / 2

        # Draw background bar
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.DARK_GRAY)
        # Draw filled portion
        arcade.draw_lrbt_rectangle_filled(left, left + filled_width, bottom, top, arcade.color.GREEN)
        # Outline
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.WHITE, 2)


    def draw_player_hp_bar(self, bar_width=100, bar_height=12):
        player = self.character
        if not player:
            return

        # --- Calculate HP ratio ---
        fill_ratio = max(self.player_display_hp / player.max_hp, 0)
        filled_width = bar_width * fill_ratio

        # --- Position: just above the fight menu ---
        screen_width, screen_height = self.window.get_size()
        cx = screen_width / 2 - 70
        cy = 60 + 30  # fight menu height (≈60) + gap

        left = cx - bar_width / 2
        right = cx + bar_width / 2
        bottom = cy - bar_height / 2
        top = cy + bar_height / 2

        # --- Background bar ---
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.DARK_GRAY)
        
        color = arcade.color.GREEN
        arcade.draw_lrbt_rectangle_filled(left, left + filled_width, bottom, top, color)
        # --- Outline ---
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.WHITE, 2)

        # --- Text label ---
        hp_text = f"HP: {player.hp}/{player.max_hp}"
        text_width = len(hp_text) * 7  # rough width estimate for spacing
        text_x = left - text_width - 20  # small gap to left of bar
        text_y = cy - (bar_height / 2)  # vertically centered
        arcade.draw_text(hp_text, text_x, text_y, arcade.color.WHITE, 14, bold=True)

    
    def attack_enemy(self):
        weapon_name, weapon_bonus = self.character.equipment["Weapon"]
        damage = self.character.atk + weapon_bonus
        defense = getattr(self.current_enemy, "defense", 0)  # default 0 if not defined
        total_damage = max(0, damage - defense)

        # Subtract HP from enemy
        self.current_enemy.hp = max(0, self.current_enemy.hp - total_damage)

        # Show damage popup
        self.loot_popup_text = f"You dealt {total_damage} damage to {self.current_enemy.name}!"
        self.loot_popup_state = "loot"
        self.loot_popup_timer = 0.0
        
        # Check if enemy is defeated
        if self.current_enemy.hp <= 0:
            self.loot_popup_text = f"You defeated {self.current_enemy.name}!"
            self.loot_popup_state = "loot"
            self.loot_popup_timer = 0.0
            self.in_fight = False  # End fight
            self.fight_enemy.visible = False
            self.fight_sprites = arcade.SpriteList()
            return

        # End player turn and prepare enemy's turn
        self.turn = "enemy"
        self.enemy_action_timer = 0.0
        
        
    def enemy_attack(self):
        # Simple enemy AI — always attacks for now
        damage = max(0, self.current_enemy.atk - self.character.defense)
        self.character.hp = max(0, self.character.hp - damage)

        self.loot_popup_text = f"{self.current_enemy.name} attacked! You took {damage} damage!"
        self.loot_popup_state = "loot"
        self.loot_popup_timer = 0.0

        # Check if player is defeated
        if self.character.hp <= 0:
            self.loot_popup_text = "You were defeated..."
            self.in_fight = False
            self.fight_enemy.visible = False
            self.fight_sprites = arcade.SpriteList()
            return

        # Switch back to player's turn
        self.turn = "player"
        
        
    def close_item_menu(self):
        self.popup_state = None
        self.item_menu_index = 0


    def draw_game_over(self):
        """Draw the Game Over screen with a bordered panel for buttons."""
        screen_width, screen_height = self.window.get_size()

        # Full screen black overlay
        arcade.draw_lrbt_rectangle_filled(0, screen_width, 0, screen_height, arcade.color.BLACK)
        
        # Game over text
        arcade.draw_text(
            "GAME OVER",
            screen_width / 2,
            screen_height / 2 + 50,
            arcade.color.RED,
            40,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        
        # Panel for buttons
        panel_height = 80
        panel_width = 400
        panel_y = panel_height / 2 + 30  # 30 px above bottom
        
        # Draw panel (filled + border)
        self.draw_button(
            screen_width / 2, panel_y, panel_width, panel_height,
            fill_color=arcade.color.BLACK, outline_color=arcade.color.RED
        )
        
        # Draw buttons inside panel
        spacing = 20
        button_width = 150
        button_height = 50
        total_width = len(self.game_over_options) * button_width + (len(self.game_over_options)-1) * spacing
        start_x = (screen_width - total_width) / 2
        for i, option in enumerate(self.game_over_options):
            cx = start_x + i * (button_width + spacing) + button_width / 2
            highlighted = (i == self.game_over_menu_index)
            self.draw_button(cx, panel_y, button_width, button_height, option, highlighted=highlighted)

    
    @staticmethod
    def draw_button(cx, cy, w, h, text="", highlighted=False, 
                    fill_color=arcade.color.BLACK, outline_color=arcade.color.RED, font_size=16):
        """
        Draw a rectangular button with optional text.
        
        Parameters:
        - cx, cy: center coordinates of the button
        - w, h: width and height
        - text: label text (optional)
        - highlighted: if True, outline is yellow instead of default
        - fill_color: button fill color
        - outline_color: outline color when not highlighted
        - font_size: size of the text
        """
        if highlighted:
            outline_color = arcade.color.YELLOW

        left = cx - w / 2
        right = cx + w / 2
        top = cy + h / 2
        bottom = cy - h / 2

        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, fill_color)
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, outline_color, 2)

        if text:
            arcade.draw_text(text, cx, cy - 8, arcade.color.WHITE, font_size, anchor_x="center")

        
    # Inside your MainScreen class
    def draw_status_popup(self):
        """Draws the status popup with stats and buttons."""
        cx = self.window.width / 2
        cy = self.window.height / 2 + 40  # bump stats box a little higher
        w = 400
        h = 220

        # --- Draw the main stats box ---
        self.draw_button(cx, cy, w, h, fill_color=arcade.color.BLACK, outline_color=arcade.color.RED)

        # --- Draw stats text ---
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

        # --- Draw command bar under stats box ---
        bar_w = 420
        bar_h = 100
        bar_cy = cy - h / 2 - bar_h / 2 - 10
        self.draw_button(cx, bar_cy, bar_w, bar_h, fill_color=arcade.color.BLACK, outline_color=arcade.color.RED)

        # --- Draw the row of buttons ---
        num_buttons = len(self.popup_options)
        box_w = 100
        box_h = 60
        spacing = 20
        total_width = num_buttons * box_w + (num_buttons - 1) * spacing
        start_x = cx - total_width / 2
        box_center_y = bar_cy

        for i, option in enumerate(self.popup_options):
            cx_button = start_x + i * (box_w + spacing) + box_w / 2
            self.draw_button(cx_button, box_center_y, box_w, box_h, option, highlighted=(i == self.menu_index))

    
    def draw_equip_popup(self):
        """Draw the equipment popup."""
        cx = self.window.width / 2
        cy = self.window.height / 2
        w = 400
        h = 220

        # Draw outer box
        arcade.draw_lrbt_rectangle_filled(cx - w/2, cx + w/2, cy - h/2, cy + h/2, arcade.color.BLACK)
        arcade.draw_lrbt_rectangle_outline(cx - w/2, cx + w/2, cy - h/2, cy + h/2, arcade.color.RED, 3)

        # Draw equipment info
        equip_lines = [
            f"{self.character.equipment['Armor'][0]}: +{self.character.equipment['Armor'][1]} DEF",
            f"{self.character.equipment['Weapon'][0]}: +{self.character.equipment['Weapon'][1]} ATK",
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

        # Draw buttons
        num_buttons = len(self.popup_options)
        if num_buttons > 0:
            box_w = 200 if num_buttons == 1 else 100
            box_h = 60
            spacing = 20 if num_buttons > 1 else 0
            total_width = num_buttons * box_w + (num_buttons - 1) * spacing
            start_x = cx - total_width / 2
            box_center_y = cy - h / 2 + 50

            for i, option in enumerate(self.popup_options):
                cx_button = start_x + i * (box_w + spacing) + box_w / 2
                self.draw_button(cx_button, box_center_y, box_w, box_h, option, highlighted=(i == self.menu_index))


    def draw_item_popup(self):
        """Draw the item popup."""
        cx = self.window.width / 2
        cy = self.window.height / 2
        w = 400
        h = 220

        # Outer box
        arcade.draw_lrbt_rectangle_filled(cx - w/2, cx + w/2, cy - h/2, cy + h/2, arcade.color.BLACK)
        arcade.draw_lrbt_rectangle_outline(cx - w/2, cx + w/2, cy - h/2, cy + h/2, arcade.color.RED, 3)

        # Draw item counts
        equip_lines = [
            f"{self.character.items['HP Potion'][0]}: {self.character.items['HP Potion'][1]}",
            f"{self.character.items['MP Potion'][0]}: {self.character.items['MP Potion'][1]}",
        ]
        for i, line in enumerate(equip_lines):
            arcade.draw_text(
                line,
                cx,
                cy + h/2 - 40 - i * 30,
                arcade.color.WHITE,
                16,
                anchor_x="center"
            )

        # Draw buttons
        num_buttons = len(self.popup_options)
        if num_buttons > 0:
            box_w = 200 if num_buttons == 1 else 100
            box_h = 60
            spacing = 20 if num_buttons > 1 else 0
            total_width = num_buttons * box_w + (num_buttons - 1) * spacing
            start_x = cx - total_width / 2
            box_center_y = cy - h / 2 + 50

            for i, option in enumerate(self.popup_options):
                cx_button = start_x + i * (box_w + spacing) + box_w / 2
                self.draw_button(cx_button, box_center_y, box_w, box_h, option, highlighted=(i == self.menu_index))
        
    
    def draw_fight_buttons(self):
        screen_width, screen_height = self.window.get_size()
        cx = screen_width / 2
        h = 60
        cy = h / 2 + 10
        w = 400
        arcade.draw_lrbt_rectangle_filled(cx - w/2, cx + w/2, cy - h/2, cy + h/2, arcade.color.BLACK)
        arcade.draw_lrbt_rectangle_outline(cx - w/2, cx + w/2, cy - h/2, cy + h/2, arcade.color.RED, 3)

        buttons = ["Attack", "Items"]
        box_w = 120
        box_h = h - 20
        spacing = 20
        start_x = cx - (len(buttons) * box_w + (len(buttons) - 1) * spacing)/2
        for i, option in enumerate(buttons):
            cx_button = start_x + i * (box_w + spacing) + box_w / 2
            self.draw_button(cx_button, cy, box_w, box_h, option, highlighted=(i == self.fight_menu_index))
            
    
    def draw_loot_popup(self):
        """Draws the loot popup at the bottom of the screen."""
        if self.loot_popup_state != "loot":
            return

        cx = self.window.width / 2
        cy = 130
        self.draw_button(cx, cy, 400, 50, self.loot_popup_text)

    
    def on_draw(self):
        self.clear()
        
        screen_width, screen_height = self.window.get_size()
        
        if self.game_over:
            self.draw_game_over()
            return
        
        # Draw room background
        art_title = "_".join(option for _, option, _ in self.maze[self.character.currentPosition][0] if option != "Backward")
        if art_title == "":
            art_title = "Backward"
        
        if art_title not in self.room_textures:
            # Load texture only if not cached
            self.room_textures[art_title] = arcade.load_texture(
                f"Art/Room_Backgrounds/{art_title}.png"
            )
        self.room_texture = self.room_textures[art_title]
        
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
            self.room_texture,
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
            # If status popup, draw stats text
            if self.popup_state == "status":
                self.draw_status_popup()
                        
            elif self.popup_state == "equip":
                self.draw_equip_popup()
                
            elif self.popup_state == "Item":
                self.draw_item_popup()
                        
        # --- Show loot/investigation popup (if active) ---
        if self.loot_popup_state == "loot":
            self.draw_loot_popup()

            
        # Battle Scene
        if self.in_fight:
            self.fight_enemy.visible = True

            # Draw room background properly scaled to window
            if self.room_texture:
                arcade.draw_texture_rect(
                    self.room_texture,
                    arcade.XYWH(
                        screen_width / 2,
                        screen_height / 2,
                        screen_width,
                        screen_height
                    ),
                    alpha=int(self.fight_alpha)
                )
                
            # Draw enemy sprite (with fade-in)
            if hasattr(self, "fight_sprites") and self.fight_sprites:
                for sprite in self.fight_sprites:
                    sprite.alpha = int(self.fight_text_alpha)
                self.fight_sprites.draw()
            
            # Draw HP bar above Necromancer
            self.draw_enemy_hp_bar()
            
            # Draw **player HP bar above fight menu**
            self.draw_player_hp_bar()
            
             # --- Draw item popup on top if active ---
            if self.popup_state == "Item":
                self.draw_item_popup()   # Draws the Item menu above everything

            # --- Draw fight buttons only if item menu is not active ---
            else:
                self.draw_fight_buttons()
                
            # --- Draw loot popup if active ---
            self.draw_loot_popup()
            

    def generate_Item(self):
        items = []
        num = random.randint(1,10)
        if num == 1 or num == 2:
            items.append("HP Potion")
        num = random.randint(1,10)
        if num == 1 or num == 2:
            items.append("MP Potion")
        return items

    
    def try_fight(self):
        chance = 1.0  # 30% chance for a fight
        if random.random() < chance:
            self.start_fight()
    
            
    def start_fight(self):
        self.in_fight = True
        self.fight_alpha = 0       # fade out current room
        self.fight_text_alpha = 0
        
        self.enemy_action_timer = 0.0  # delay before enemy acts
        self.enemy_action_delay = 2.0  # seconds between turns

        
        # Randomly pick an enemy
        enemy_index = 0  # right now always 0, later random.randint(0, len(self.enemies)-1)
        self.current_enemy = self.enemies[enemy_index]
        
        # Load sprite dynamically
        self.fight_enemy, self.fight_frames = self.load_enemy_sprite(self.current_enemy.name)
    
        # Reset enemy HP for a new fight
        self.current_enemy.hp = self.current_enemy.max_hp
        # for smooth HP bar animation
        self.current_enemy_display_hp = self.current_enemy.hp
            
        # Position sprite in middle
        screen_width, screen_height = self.window.get_size()
        self.fight_enemy.center_x = screen_width / 2
        self.fight_enemy.center_y = screen_height / 2 + 20
        self.fight_enemy.visible = True
        
        # Ensure sprite list contains the enemy
        self.fight_sprites.append(self.fight_enemy)
        
        # Clear bottom options
        self.popup_state = None
        self.loot_popup_state = None
        
        # --- Determine who goes first ---
        # --- Determine turn order based on SPD ---
        if self.character.spd > self.current_enemy.spd:
            self.turn = "player"
        else:
            self.turn = "enemy"  # enemy goes first if tie or faster
        
        
    def open_item_menu(self):
        """Opens the Item menu popup."""
        self.popup_state = "Item"
        self.menu_index = 0
        self.popup_options = ["Use HP", "Use MP", "EXIT"]
        
        
    def handle_item_menu_selection(self, selected):
        """Handles using items (HP/MP potions) and closing the item menu."""
        if selected == "EXIT":
            self.popup_state = None
            return

        # Use HP potion
        if selected == "Use HP":
            if self.character.items.get("HP Potion", [None, 0])[1] > 0:
                healed = self.hp_potion.use()
                self.loot_popup_text = f"You used an HP Potion and restored {healed} HP!"
            else:
                self.loot_popup_text = "You have no HP Potions left!"

        # Use MP potion
        elif selected == "Use MP":
            if self.character.items.get("MP Potion", [None, 0])[1] > 0:
                restored = self.mp_potion.use()
                self.loot_popup_text = f"You used an MP Potion and restored {restored} MP!"
            else:
                self.loot_popup_text = "You have no MP Potions left!"

        # Show the loot popup in battle
        self.loot_popup_state = "loot"
        self.loot_popup_timer = 0.0
        
        # --- Close item menu ---
        self.close_item_menu()  # Make sure this hides the item popup/menu
        
        self.turn = "enemy"
        self.enemy_action_timer = 0.0


    def on_key_press(self, key, modifiers):
        # Only allow input if fade-in is complete
        if not self.fade_in_complete:
            return
        
        # --- Game Over menu navigation ---
        if self.game_over:
            if key == arcade.key.RIGHT:
                self.game_over_menu_index = (self.game_over_menu_index + 1) % len(self.game_over_options)
            elif key == arcade.key.LEFT:
                self.game_over_menu_index = (self.game_over_menu_index - 1) % len(self.game_over_options)
            elif key == arcade.key.ENTER:
                selected = self.game_over_options[self.game_over_menu_index]
                if selected == "Restart":
                    self.restart_game()
                elif selected == "Quit":
                    arcade.close_window()
            return  # Skip all other inputs when game over

        # --- Popup navigation (overworld or battle) ---
        if self.popup_state is not None:
            if key == arcade.key.RIGHT:
                self.menu_index = (self.menu_index + 1) % len(self.popup_options)
            elif key == arcade.key.LEFT:
                self.menu_index = (self.menu_index - 1) % len(self.popup_options)
            elif key == arcade.key.ENTER:
                selected = self.popup_options[self.menu_index]

                # --- Status popup ---
                if self.popup_state == "status":
                    if selected == "Exit":
                        self.popup_state = None
                    elif selected == "Equip":
                        self.popup_state = "equip"
                        self.menu_index = 0
                        self.popup_options = ["EXIT"]
                    elif selected == "Item":
                        self.open_item_menu()

                # --- Equip popup ---
                elif self.popup_state == "equip":
                    if selected == "EXIT":
                        self.popup_state = None

                # --- Item popup ---
                elif self.popup_state == "Item":
                    self.handle_item_menu_selection(selected)

            return  # Skip other inputs while popup is open

        # --- Battle menu navigation (not in popup) ---
        if self.in_fight and self.turn == "player":
            if key == arcade.key.RIGHT:
                self.fight_menu_index = (self.fight_menu_index + 1) % len(self.fight_buttons)
            elif key == arcade.key.LEFT:
                self.fight_menu_index = (self.fight_menu_index - 1) % len(self.fight_buttons)
            elif key == arcade.key.ENTER:
                selected = self.fight_buttons[self.fight_menu_index]
                if selected == "Attack":
                    self.attack_enemy()
                elif selected == "Items":
                    self.open_item_menu()
                    self.fight_menu_index = 0  # deselect fight buttons
            return

        # --- Overworld X key toggles status ---
        if key == arcade.key.X:
            if self.popup_state == "status":
                self.popup_state = None
            else:
                self.popup_state = "status"
                self.menu_index = 0
                self.popup_options = self.menu_options.copy()
            return

        # --- Overworld Z key investigates rooms ---
        if key == arcade.key.Z:
            current = self.character.currentPosition
            neighbors, visited, looted = self.maze[current]
            if not looted:
                loot = self.generate_Item()
                for item in loot:
                    self.character.pickup(item)
                self.maze[current] = (neighbors, visited, True)

                self.loot_popup_text = "You found: " + ", ".join(loot) if loot else "Nothing was found here."
                self.loot_popup_state = "loot"
                self.loot_popup_timer = 0.0
            else:
                self.loot_popup_text = "This room has already been investigated."
                self.loot_popup_state = "loot"
                self.loot_popup_timer = 0.0

            return

        # --- Movement handling ---
        dir_map = {
            arcade.key.LEFT: "Left",
            arcade.key.RIGHT: "Right",
            arcade.key.UP: "Forward",
            arcade.key.DOWN: "Backward",
        }
        direction = dir_map.get(key)
        if not direction:
            return

        current = self.character.currentPosition
        neighbors, visited, looted = self.maze[current]
        moved = False

        for target, dir_name, conn_label in neighbors:
            if dir_name == direction:
                curr_neighbors, curr_visited, curr_looted = self.maze[current]
                self.maze[current] = (curr_neighbors, True, curr_looted)

                self.character.currentPosition = target
                n, visited, looted = self.maze[target]
                self.maze[target] = (n, True, looted)

                if conn_label in self.connections:
                    visited, data = self.connections[conn_label]
                    if not visited:
                        self.connections[conn_label] = (True, data)
                moved = True

                # Check for fight
                self.try_fight()
                break

        if moved:
            self.bg_alpha = 0
            self.text_alpha = 0
            self.text_timer = 0
            self.fade_in_complete = False

    
    def on_update(self, delta_time: float):
        """Update fade animation each frame."""
        
        # --- Smooth PLAYER HP bar update ---
        if hasattr(self, "player_display_hp") and hasattr(self, "character"):
            diff = self.player_display_hp - self.character.hp
            if abs(diff) > 0.1:
                self.player_display_hp -= diff * min(1, 5 * delta_time)
            else:
                self.player_display_hp = self.character.hp
        
        # --- Check for Game Over after HP animation ---
        if self.player_display_hp <= 0 and not getattr(self, "game_over", False):
            self.character.hp = 0
            self.game_over = True
            self.loot_popup_state = None
            self.in_fight = False
        
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
        
        # --- Battle Fading ---     
        if self.in_fight:
            # Smooth HP bar update
            if self.current_enemy:
                diff = self.current_enemy_display_hp - self.current_enemy.hp
                if abs(diff) > 0.1:  # small threshold to prevent jitter
                    # Reduce by a fraction of the difference per frame for smoothness
                    self.current_enemy_display_hp -= diff * min(1, 5 * delta_time)
                else:
                    self.current_enemy_display_hp = self.current_enemy.hp


            # --- Fade in fight visuals ---
            if self.fight_alpha < 255:
                self.fight_alpha += self.fight_fade_speed * delta_time
                if self.fight_alpha > 255:
                    self.fight_alpha = 255
            if self.fight_text_alpha < 255:
                self.fight_text_alpha += self.fight_fade_speed * delta_time
                if self.fight_text_alpha > 255:
                    self.fight_text_alpha = 255
            
            if self.in_fight and self.turn == "enemy":
                self.enemy_action_timer += delta_time
                if self.enemy_action_timer >= self.enemy_action_delay:
                    self.enemy_attack()

                    
