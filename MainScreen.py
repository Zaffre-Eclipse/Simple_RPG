import arcade
import random
from arcade.types import Rect
from Hp_Potion import Hp_Potion
from Mp_Potion import Mp_Potion
from Necromancer import Necromancer
from NightBorne import NightBorne
from ScreenChanger import ScreenChanger
from BattleScreen import BattleScreen

# Scaling and room size
SCALE = 2
ROOM_WIDTH = 40
ROOM_HEIGHT = 20

class MiniMap:
    """
    This class handles the Minimap and inherits the maze
    and connections from the Intro class 
    It also sets up the positions of the minimap
    rooms in the game window
    
    Anner, Tiffany, Alexandra
    """
    
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
        "Shop": (100, 25),
        "End": (40, 115)
    }

    def __init__(self, character, maze, connections):
        """This is the class setup"""
        
        self.character = character
        self.maze = maze
        self.connections = connections
        self.width = 140 * SCALE
        self.height = 140 * SCALE

        # Mark start room as visited
        neighbors, _, looted = self.maze[self.character.currentPosition]
        self.maze[self.character.currentPosition] = (neighbors, True, looted)
        
        
    def draw(self, screen_width, screen_height, margin=20, alpha=255):
        """
        Draws the minimap in the upper-right corner
        
        Args:
            screen_width: Full width of the game window in pixels
        
            screen_height: Full height of the game window in pixels
            
            margin: Distance from the right and top edge of the screen 
                    where the  minimap should be placed. Defaults to 20
        
            alpha: Transparency applied to all minimap elements 
        """
        
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
                elif room == "Shop": color = arcade.color.PURPLE
                elif looted == True: color = looted_color
                else: color = unvisited_color
                arcade.draw_lbwh_rectangle_outline(x, y, ROOM_WIDTH, ROOM_HEIGHT, color, 2)


class MainScreen(arcade.View):
    def __init__(self, character, maze, connections):
        """This is the class setup"""
        
        super().__init__()

        # OVERWORLD STATE
        self.character = character
        self.maze = maze
        self.connections = connections
        self.minimap = MiniMap(character, maze, connections)

        self.win = False
        self.bg_alpha = 0
        self.text_alpha = 0
        self.fade_speed_bg = 600
        self.fade_speed_text = 600
        self.text_delay = 0.5
        self.text_timer = 0
        self.fade_in_complete = False

        # UI POPUPS
        self.popup_state = None
        self.menu_index = 0
        self.menu_options = ["Equip", "Item", "Exit"]
        self.popup_options = []
        self.item_menu_index = 0

        self.loot_popup_state = None
        self.loot_popup_text = ""
        self.loot_popup_timer = 0
        self.loot_popup_duration = 2.0

        # POTIONS
        self.hp_potion = Hp_Potion(self.character)
        self.mp_potion = Mp_Potion(self.character)

        # SCREEN CHANGER UTILS
        self.screen_changer = ScreenChanger()

        # FIGHT ENTRY + RENDER STATE
        self.in_fight = False
        self.in_boss_fight = False

        self.fight_alpha = 0
        self.fight_text_alpha = 0
        self.fight_fade_speed = 500

        self.current_enemy = None
        self.fight_enemy = None
        self.fight_sprites = arcade.SpriteList()
        
        self.fight_buttons_visible = True
        self.hp_bar_visible = True
        self.hp_label_visible = True
        
        self.enemy_action_timer = 0
        self.enemy_action_delay = 0

        # Player choice menu in battle
        self.fight_menu_index = 0
        self.fight_buttons = ["Attack", "Items", "Special"]

        # GAME OVER
        self.game_over = False
        self.game_over_menu_index = 0
        self.game_over_options = ["Restart", "Quit"]

        # ROOM BACKGROUNDS
        self.room_textures = {}
        self.room_texture = None

        # ENEMY LISTS
        self.enemies = [Necromancer()]
        self.boss_list = [NightBorne()]

        # SHOP
        self.shop_tutorial_seen = False
        self.left_shop = False
        self.shop_menu_index = 0

        self.Shop_items = {
            "Armor +1": ("Armor +1", 2, 15, "Increase DEF by 2"),
            "Weapon +1": ("Weapon +1", 2, 15, "Increase ATK by 2"),
            "Hp Potion": ("Hp Potion", 10, "Restores 20 HP"),
            "Mp Potion": ("Mp Potion", 10, "Restores 20 MP"),
            "Exit": "Exit"
        }

        # MUSIC
        self.music_volume = 0.5
        self.fade_speed = 1.5
        self.fade_delay = 0.05
        self.overworld = "Simple_RPG/Music/Forest_Carnival.wav"
        self.battle_music = "Simple_RPG/Music/battle.mp3"
        self.shop = "Simple_RPG/Music/Shop.mp3"
        self.win_music = "Simple_RPG/Music/Win.mp3"

        self.transition_active = False
        self.fade_direction = None
        self.target_music_path = None
        self.new_music_player = None
        self.current_music_player = arcade.play_sound(
            arcade.load_sound(self.overworld),
            volume=self.music_volume,
            loop=True
        )
        
        # SFX
        self.current_sfx = None
        self.sfx_speed = 1
        self.footsteps_sfx = arcade.load_sound("Simple_RPG/SFX/Footsteps.wav")
        self.loot_sfx = arcade.load_sound("Simple_RPG/SFX/Loot.wav")
        self.button_sfx = arcade.load_sound("Simple_RPG/SFX/Button.wav")
        self.hit_sfx = arcade.load_sound("Simple_RPG/SFX/Hit.wav")
        self.necromancer_attack_sfx = arcade.load_sound("Simple_RPG/SFX/necromancer_attack.wav")
        
        # MISC STATE
        self.post_fight_cooldown = 1
        self.shop_transition_cooldown = 0
        self.battle_tutorial_seen = False
        self.boss_battle_tutorial_seen = False
        
        # BATTLE SYSTEM
        self.battle = BattleScreen(self)


    def transition_music(self, new_music_path):
        """
        Begins fading from the current track to a new one
        
        Args:
            new_music_path: The new music track
        """
        
        if not self.transition_active:
            self.transition_active = True
            self.fade_direction = "out"
            self.target_music_path = new_music_path
            
    
    def start_new_music(self):
        """
        Load and begin playback of the pending music track
        after the old one finishes fading out
        """
        
        new_sound = arcade.load_sound(self.target_music_path)
        self.new_music_player = arcade.play_sound(new_sound, volume=0, loop=True)
        self.fade_direction = "in"
            
    
    def update_music_fade(self, delta_time):
        """
        Gradually fades out current track, swaps and fades in a new one
        """
        if not self.transition_active:
            return

        fade_step = self.fade_speed * delta_time

        # Fade out phase
        if self.fade_direction == "out":
            if self.current_music_player:
                new_volume = max(0, self.current_music_player.volume - fade_step)
                self.current_music_player.volume = new_volume

                if new_volume <= 0:
                    self.current_music_player.pause()
                    self.current_music_player = None
                    self.start_new_music()
            else:
                # No current music just start new
                self.start_new_music()

        # Fade in phase
        elif self.fade_direction == "in" and self.new_music_player:
            new_volume = min(self.music_volume, self.new_music_player.volume + fade_step)
            self.new_music_player.volume = new_volume

            if new_volume >= self.music_volume:
                # Transition complete
                self.current_music_player = self.new_music_player
                self.new_music_player = None
                self.transition_active = False
                self.fade_direction = None
                self.target_music_path = None
    
    
    def restart_game(self):
        """Reset the game to initial state."""

        # Reset character stats
        self.character.reset()

        # Reset maze visitation
        for room, (neighbors, _, looted) in self.maze.items():
            visited = (room == "Start")
            self.maze[room] = (neighbors, visited, False)

        # Reset connections
        for conn_label in self.connections:
            _, data = self.connections[conn_label]
            self.connections[conn_label] = (False, data)

        # Reset minimap
        self.minimap = MiniMap(self.character, self.maze, self.connections)

        # Overworld fields
        self.in_fight = False
        self.in_boss_fight = False
        self.current_enemy = None
        self.fight_enemy = None
        self.fight_sprites = arcade.SpriteList()
        self.fight_menu_index = 0

        # Popups
        self.popup_state = None
        self.loot_popup_state = None
        self.loot_popup_text = ""
        self.menu_index = 0
        self.popup_options = []

        # Fade values
        self.bg_alpha = 0
        self.text_alpha = 0
        self.fade_in_complete = False
        self.text_timer = 0
        self.fight_alpha = 0

        # Game Over
        self.game_over = False
        self.game_over_menu_index = 0

        # Shop reset
        self.left_shop = False
        self.shop_tutorial_seen = False
        self.Shop_items = {
            "Armor +1": ("Armor +1", 2, 15, "Increase DEF by 2"),
            "Weapon +1": ("Weapon +1", 2, 15, "Increase ATK by 2"),
            "Hp Potion": ("Hp Potion", 10, "Restores 20 HP"),
            "Mp Potion": ("Mp Potion", 10, "Restores 20 MP"),
            "Exit": "Exit"
        }

        # reset battlescreen state
        self.battle.turn = "player"

        # Reset Player Display HP/MP
        self.battle.player_display_hp = self.character.hp
        self.battle.player_display_mp = self.character.mp
        self.battle.start_hp_animation = False
        self.battle.start_mp_animation = False

        # Reset attack QTE states
        self.battle.attack_animation_active = False
        self.battle.attack_waiting_for_input = False
        self.battle.attack_total_damage = 0
        self.battle.attack_hits = 0
        self.battle.total_attack_hits = 0

        # Reset dodge QTE state
        self.battle.dodge_active = False
        self.battle.dodge_waiting_for_input = False
        self.battle.enemy_attack_animation_active = False
        self.battle.pointer_moving = False
        self.battle.dodge_delay_timer = 0
        self.battle.current_dodge_arrow = None
        self.battle.dodge_direction = None
        self.battle.dodge_result_timer = 0
        self.battle.boss_attack_animation_played = False

        # Reset buffs
        self.battle.overclock = 0
        self.battle.guard = 0
        self.battle.repair = 0
        self.battle.repair_pending = False
        self.battle.repair_timer = 0

        # reset tutorials
        self.battle_tutorial_seen = False
        self.boss_battle_tutorial_seen = False

        # Reset music
        self.transition_active = False
        self.fade_direction = None
        self.target_music_path = None
        self.new_music_player = None
        self.transition_music(self.overworld)
    
    
    def on_draw(self):
        """
        This method keeps track of what's supposed to be on screen every
        frame and interatcs with the BattleScreen and ScreenChanger classes
        """
        
        self.clear()
        screen_width, screen_height = self.window.get_size()
        
        # Draw game over screen
        if self.game_over:
            self.screen_changer.draw_game_over(
                self.window,
                self.game_over_options,
                self.game_over_menu_index
                )
            return
        
        # Draw win screen
        if self.win:
            self.screen_changer.draw_win_screen(self.window, self.popup_options, self.menu_index)
            return
        
        # Draw room background
        if self.character.currentPosition == "Shop":
            art_title = "Shop"
        else:
            art_title = "_".join(option for _, option, _ in self.maze[self.character.currentPosition][0] if option != "Backward")
        if art_title == "":
            art_title = "Backward"
        
        # Load room texture if it's not cached
        if art_title not in self.room_textures:
            self.room_textures[art_title] = arcade.load_texture(
                f"Simple_RPG/Art/Room_Backgrounds/{art_title}.png"
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
            x=screen_width / 2,
            y=screen_height / 2
            )
        
        # Draw texture with alpha
        arcade.draw_texture_rect(
            self.room_texture,
            rect,
            alpha=int(self.bg_alpha)
            )


        # Draw minimap
        self.minimap.draw(screen_width, screen_height, alpha=int(self.bg_alpha))

        # Draw bottom-centered movement options
        current = self.character.currentPosition
        neighbors, _, looted = self.maze[current]

        directions = [dir_name.upper() for _, dir_name, _ in neighbors]
        
        # Add Z and X options
        if current == "Shop":
            directions += ["Z - Use Shop", "X - Check Stats"]
        else:
            directions += ["Z - Investigate", "X - Check Stats"]
        movement_line = " | ".join(directions)
        
        font_size = 16
        text = arcade.Text(movement_line, 0, 0, arcade.color.WHITE, font_size)
        text.x = (screen_width - text.content_width) / 2
        text.draw()
        
        
        # Draw popup if one is open
        if self.popup_state is not None:
            
            # If status popup draw stats
            if self.popup_state == "status":
                self.screen_changer.draw_status_popup(
                    self.window,
                    self.character,
                    self.popup_options,
                    self.menu_index,
                    )
            
            # If equip popup draw equipment info        
            elif self.popup_state == "equip":
                self.screen_changer.draw_equip_popup(
                    self.window,
                    self.character,
                    self.popup_options,
                    self.menu_index,
                    )
            
            # If item popup draw inventory info        
            elif self.popup_state == "Item":
                self.screen_changer.draw_item_popup(
                    self.window,
                    self.character,
                    self.popup_options,
                    self.menu_index,
                    )
            
            # Draw the shop tutorial
            elif self.popup_state == "shop_tutorial":
                self.screen_changer.draw_shop_tutorial_popup(self.window)
                
            # Draw the shop menu
            elif self.popup_state == "shop":
                self.screen_changer.draw_shop_popup(
                    self.window,
                    self.Shop_items,
                    self.shop_menu_index,
                    self.character,
                    )
            
            elif self.popup_state == "battle_tutorial":
                self.screen_changer.draw_battle_tutorial_popup(self.window)
                
            elif self.popup_state == "boss_battle_tutorial":
                self.screen_changer.draw_boss_battle_tutorial_popup(self.window)
                        
        # This loot popup serves as a miscelannous tool
        # that we use for many purposes throughout the game
        # It's more of a text box
        if self.loot_popup_state == "loot":
            self.screen_changer.draw_loot_popup(
                self.window,
                self.loot_popup_state,
                self.loot_popup_text,
                )

        
        # Battle Scene
        if (self.in_fight and self.battle_tutorial_seen == True) or (self.in_boss_fight and self.boss_battle_tutorial_seen == True):
            
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
                
            if self.battle.enemy_sprite_attack_animation_active:
                self.fight_sprites.draw()
                
            elif self.battle.enemy_death_animation_active:
                self.fight_sprites.draw()
                return
                
            # Draw enemy sprite
            if hasattr(self, "fight_sprites") and self.fight_sprites:
                for sprite in self.fight_sprites:
                    sprite.alpha = int(self.fight_text_alpha)
                self.fight_sprites.draw()
            
            # Draw HP bar above Necromancer
            self.battle.draw_enemy_hp_bar()

            # Attack QTE
            if self.battle.attack_animation_active:
                self.battle.attack_animation_list.draw()
                self.battle.pointer_list.draw()

            # Enemy or boss attack animation OR Dodge QTE
            elif self.battle.enemy_attack_animation_active:

                # Draw enemy sprite normally
                self.fight_enemy.alpha = 255

                # Draw dodge bar only during boss QTE
                if self.battle.dodge_active or self.battle.dodge_waiting_for_input:

                    # Draw bar
                    arcade.draw_texture_rect(
                        self.battle.dodge_bar_texture,
                        arcade.XYWH(
                            self.battle.dodge_bar_x,
                            self.battle.dodge_bar_y,
                            self.battle.dodge_bar_width,
                            self.battle.dodge_bar_height
                        )
                    )

                    # Draw pointer
                    scaled_w = self.battle.pointer_width * self.battle.dodge_pointer_scale
                    scaled_h = self.battle.pointer_height * self.battle.dodge_pointer_scale
                    pointer_y = (
                        self.battle.dodge_bar_y +
                        (self.battle.dodge_bar_height / 2) +
                        (scaled_h / 2) - 5
                    )

                    arcade.draw_texture_rect(
                        self.battle.dodge_pointer_texture,
                        arcade.XYWH(
                            self.battle.pointer_x,
                            pointer_y,
                            scaled_w,
                            scaled_h
                        )
                    )

                    # Draw arrow indicator (Up/Down/Left/Right)
                    if self.battle.current_dodge_arrow:
                        arcade.draw_texture_rect(
                            self.battle.current_dodge_arrow,
                            arcade.XYWH(
                                self.battle.dodge_bar_x,
                                self.battle.dodge_arrow_y,
                                64, 64
                            )
                        )

            # Normal battle UI (player turn)
            else:
                self.battle.draw_player_hp_bar()
                self.battle.draw_player_mp_bar()

                # Draw active Buffs
                if self.battle.overclock > 0:
                    arcade.draw_text(f"Overclock: {self.battle.overclock}", screen_width/2 - 150, 100, arcade.color.WHITE, 14, bold=True)

                if self.battle.guard > 0:
                    arcade.draw_text(f"Guard: {self.battle.guard}", screen_width/2 - 30, 100, arcade.color.WHITE, 14, bold=True)

                if self.battle.repair > 0:
                    arcade.draw_text(f"Repairs: {self.battle.repair}", screen_width/2 + 90, 100, arcade.color.WHITE, 14, bold=True)

                # Item popup takes priority
                if self.popup_state == "Item":
                    self.screen_changer.draw_item_popup(
                        self.window,
                        self.character,
                        self.popup_options,
                        self.menu_index,
                    )
                else:
                    self.battle.draw_fight_buttons()

                # Loot popup
                self.screen_changer.draw_loot_popup(
                    self.window,
                    self.loot_popup_state,
                    self.loot_popup_text,
                )
            
            # Draw special popup
            if self.popup_state == "special":
                self.screen_changer.draw_special_popup(
                    self.window, 
                    self.character, 
                    self.battle.special_menu_options, 
                    self.battle.special_menu_index
                    )
        
        
        # Draw End popup
        if self.popup_state == "End":
            self.screen_changer.draw_end_popup(
                self.window,
                self.popup_options,
                self.menu_index,
            )
            return
            

    def generate_Item(self):
        """This method handle room searching for items"""
        
        items = []
        num = random.randint(1,10)
        if num == 1 or num == 2:
            items.append("HP Potion")
        num = random.randint(1,10)
        if num == 1 or num == 2:
            items.append("MP Potion")
        return items
    
                 
    def open_item_menu(self):
        """Opens the Item menu popup"""
        
        self.popup_state = "Item"
        self.menu_index = 0
        self.popup_options = ["Use HP", "Use MP", "EXIT"]
        
        
    def handle_item_menu_selection(self, selected):
        """Handles using items and closing the item menu"""
        if selected == "EXIT":
            self.popup_state = None
            return

        # Use HP potion
        if selected == "Use HP":
            if self.character.items.get("HP Potion", [None, 0])[1] > 0:
                healed = self.hp_potion.use()
                self.loot_popup_text = f"You used an HP Potion and restored {healed} HP!"
                self.battle.start_hp_animation = True
            else:
                self.loot_popup_text = "You have no HP Potions left!"

        # Use MP potion
        elif selected == "Use MP":
            if self.character.items.get("MP Potion", [None, 0])[1] > 0:
                restored = self.mp_potion.use()
                self.loot_popup_text = f"You used an MP Potion and restored {restored} MP!"
                self.battle.start_mp_animation = True
            else:
                self.loot_popup_text = "You have no MP Potions left!"

        # Show the loot popup in battle
        self.loot_popup_state = "loot"
        self.loot_popup_timer = 0.0
        
        # Close item menu
        self.popup_state = None
        self.item_menu_index = 0
        if self.in_fight == True:
            self.turn = "enemy"
        self.enemy_action_timer = 0.0
        
    
    def on_key_press(self, key, modifiers):
        """
        This method handles player key input
        
        Args:
            key: The key that was pressed
        
            modifiers: Modifier keys held down at the same time,
            such as SHIFT, CTRL, or ALT
        """
        
        # Only allow input if fade-in is complete
        if not self.fade_in_complete:
            return
        
        if self.battle.enemy_death_animation_active:
            return
        # Movement delay after finishing a fight
        if not self.in_fight and self.post_fight_cooldown > 0:
            return
        
        # Movement delay after entering the shop
        if self.shop_transition_cooldown > 0:
            return
        
        # Only block input from loot popups during combat
        if self.in_fight and (
            self.battle.attack_animation_active or 
            self.battle.attack_waiting_for_input or 
            self.battle.dodge_waiting_for_input or 
            (self.loot_popup_state == "loot" and self.battle.enemy_death_animation_active == False)):
                
            # Handle dodge QTE input
            if self.battle.dodge_waiting_for_input:
                # Map directions to keys
                direction_keys = {
                    "Up": arcade.key.UP,
                    "Down": arcade.key.DOWN,
                    "Left": arcade.key.LEFT,
                    "Right": arcade.key.RIGHT,
                }

                required_key = direction_keys[self.battle.dodge_direction]
                if key == required_key:
                    # Successful dodge (evaluated based on pointer position)
                    self.battle.dodge_waiting_for_input = False
                    self.battle.apply_dodge_result(self.current_enemy)
                else:
                    # Wrong key still applies result (counts as full damage)
                    self.battle.dodge_waiting_for_input = False
                    self.battle.apply_dodge_result(self.current_enemy, True)
                    
            # Handle attack QTE input
            if self.battle.attack_waiting_for_input:
                if key == arcade.key.Z:
                    # Player pressed Z during the attack phase
                    self.battle.handle_attack_input(self.current_enemy)
            
            # block everything else (movement, items, etc.)
            return

        # Game Over menu navigation
        if self.game_over:
            if key == arcade.key.RIGHT:
                self.sfx_speed = random.uniform(1.1, 1.15)
                self.current_sfx = arcade.play_sound(self.button_sfx, .6, 0, False, self.sfx_speed)
                self.game_over_menu_index = (self.game_over_menu_index + 1) % len(self.game_over_options)
            
            elif key == arcade.key.LEFT:
                self.sfx_speed = random.uniform(1.1, 1.15)
                self.current_sfx = arcade.play_sound(self.button_sfx, .6, 0, False, self.sfx_speed)
                self.game_over_menu_index = (self.game_over_menu_index - 1) % len(self.game_over_options)
            
            elif key == arcade.key.ENTER:
                selected = self.game_over_options[self.game_over_menu_index]
                if selected == "Restart":
                    self.restart_game()
                elif selected == "Quit":
                    arcade.close_window()
                    
            # Skip all other inputs when game over
            return
        
        # Win screen navigation
        if self.win: 
            if key == arcade.key.ENTER:
                arcade.close_window()
                return
        
        # Popup navigation (overworld or battle)
        # Shop popup
        if self.popup_state == "shop":
            
            if key == arcade.key.UP:
                self.sfx_speed = random.uniform(1.1, 1.15)
                self.current_sfx = arcade.play_sound(self.button_sfx, .6, 0, False, self.sfx_speed)
                self.shop_menu_index = (self.shop_menu_index - 1) % len(self.Shop_items)
            
            elif key == arcade.key.DOWN:
                self.sfx_speed = random.uniform(1.1, 1.15)
                self.current_sfx = arcade.play_sound(self.button_sfx, .6, 0, False, self.sfx_speed)
                self.shop_menu_index = (self.shop_menu_index + 1) % len(self.Shop_items)
            
            elif key == arcade.key.ENTER:
                selected_key = list(self.Shop_items.keys())[self.shop_menu_index]
                
                if selected_key == "Exit":
                    self.popup_state = None
                else:
                    shop_item = self.Shop_items[selected_key]
                    
                    # Determine gold cost
                    if "Armor" in selected_key or "Weapon" in selected_key:
                        # index 2 for equipment
                        cost = shop_item[2]
                    else:
                        # index 1 for potions
                        cost = shop_item[1]
                    
                    gold_item_name, gold_amount = self.character.items["Gold"]

                    if gold_amount >= cost:
                        # Deduct gold
                        self.character.items["Gold"] = (gold_item_name, gold_amount - cost)

                        if "Armor" in selected_key:
                            # Update equipment and stats
                            self.character.equipment["Armor"] = (selected_key, shop_item[1])
                            self.character.defense += shop_item[1]
                            
                            # Remove from shop so it can't be bought again
                            del self.Shop_items[selected_key]
                            self.loot_popup_text = f"You bought {selected_key}! DEF increased by {shop_item[1]}."
                            
                        elif "Weapon" in selected_key:
                            # Update equipment and stats
                            self.character.equipment["Weapon"] = (selected_key, shop_item[1])
                            self.character.atk += shop_item[1]
                            
                            # Remove from shop so it can't be bought again
                            del self.Shop_items[selected_key]
                            self.loot_popup_text = f"You bought {selected_key}! ATK increased by {shop_item[1]}."
                            
                        else:
                            # Use the corresponding potion class to increment inventory
                            if selected_key.lower().startswith("hp"):
                                self.character.pickup("HP Potion")
                                inv_name = "HP Potion",
                            elif selected_key.lower().startswith("mp"):
                                self.character.pickup("MP Potion")
                                inv_name = "MP Potion"
                            else:
                                inv_name = selected_key
                                self.character.pickup(inv_name)

                            self.loot_popup_text = f"Purchased 1 {inv_name} for {cost} Gold!"

                    else:
                        self.loot_popup_text = "Not enough Gold!"

                    # Show short popup
                    self.loot_popup_state = "loot"
                    self.loot_popup_timer = 0.5

            # skip all other inputs while in shop
            return
        
        # Special attack popup
        if self.popup_state == "special":
            if key == arcade.key.UP:
                
                self.sfx_speed = random.uniform(1.1, 1.15)
                self.current_sfx = arcade.play_sound(self.button_sfx, .6, 0, False, self.sfx_speed)
                self.battle.special_menu_index = (self.battle.special_menu_index - 1) % len(self.battle.special_menu_options)
            
            elif key == arcade.key.DOWN:
                self.sfx_speed = random.uniform(1.1, 1.15)
                self.current_sfx = arcade.play_sound(self.button_sfx, .6, 0, False, self.sfx_speed)
                self.battle.special_menu_index = (self.battle.special_menu_index + 1) % len(self.battle.special_menu_options)
            
            elif key == arcade.key.ENTER:
                selected_option = self.battle.special_menu_options[self.battle.special_menu_index]
                if selected_option == "Exit":
                    self.popup_state = None
                    return
                
                # Handle ability
                val = self.character.special.get(selected_option)
                if not isinstance(val, tuple):
                    return

                name, desc, mp_cost = val

                if self.character.mp >= mp_cost:
                    # Deduct MP and trigger animation
                    self.character.mp -= mp_cost
                    self.battle.start_mp_animation = True

                    # Trigger specific special
                    if selected_option == "Overclock":
                        self.battle.overclock = 2
                        self.loot_popup_text = "You used Overclock!"
                    elif selected_option == "Tight Guard":
                        self.battle.guard = 2
                        self.loot_popup_text = "You used Tight Guard!"
                    elif selected_option == "Auto-Repairs":
                        self.battle.repair = 3
                        self.battle.repair_delay = 1.5
                        self.battle.repair_timer = 0
                        self.loot_popup_text = "You used Auto Repairs!"
                    
                    self.popup_state = None
                    self.battle.turn = "enemy_wait"
                    self.enemy_attack_delay = 2.0

                else:
                    self.loot_popup_text = "Not enough MP!"

                # Always show popup feedback
                self.loot_popup_state = "loot"
                self.loot_popup_timer = 0

            # skip all other inputs while in Special
            return
        
        # Navigation in popups
        if self.popup_state is not None:
            if key == arcade.key.RIGHT:
                if self.popup_state != "equip" and self.popup_state != "shop_tutorial" and self.popup_state != "battle_tutorial":
                    self.sfx_speed = random.uniform(1.1, 1.15)
                    self.current_sfx = arcade.play_sound(self.button_sfx, .6, 0, False, self.sfx_speed)
                self.menu_index = (self.menu_index + 1) % len(self.popup_options)
            
            elif key == arcade.key.LEFT:
                if self.popup_state != "equip" and self.popup_state != "shop_tutorial" and self.popup_state != "battle_tutorial":
                    self.sfx_speed = random.uniform(1.1, 1.15)
                    self.current_sfx = arcade.play_sound(self.button_sfx, .6, 0, False, self.sfx_speed)
                self.menu_index = (self.menu_index - 1) % len(self.popup_options)
            
            elif key == arcade.key.ENTER:
                selected = self.popup_options[self.menu_index]

                # Status popup
                if self.popup_state == "status":
                    if selected == "Exit":
                        self.popup_state = None
                    elif selected == "Equip":
                        self.popup_state = "equip"
                        self.menu_index = 0
                        self.popup_options = ["EXIT"]
                    elif selected == "Item":
                        self.open_item_menu()

                # Equip popup
                elif self.popup_state == "equip":
                    if selected == "EXIT":
                        self.popup_state = None

                # Item popup
                elif self.popup_state == "Item":
                    self.handle_item_menu_selection(selected)
                    if self.in_fight and selected != "EXIT":
                        self.battle.turn = "enemy"
                    
                # End popup
                elif self.popup_state == "End":
                    # End popup navigation
                    selected = self.popup_options[self.menu_index]
                    if selected == "Yes":
                        self.popup_state = "boss_battle_tutorial"
                    elif selected == "No":
                        self.popup_state = None
                
                # Shop tutorial popup
                elif self.popup_state == "shop_tutorial":
                    if key == arcade.key.ENTER:
                        self.popup_state = None
                
                # Battle tutorial popup
                elif self.popup_state == "battle_tutorial":
                    if key == arcade.key.ENTER:
                        # Dismiss popup
                        self.popup_state = None
                        # ensures it only shows once
                        self.battle_tutorial_seen = True
                        self.battle.start_fight()
                
                # Boss battle tutorial popup
                elif self.popup_state == "boss_battle_tutorial":
                    if key == arcade.key.ENTER:
                        # Dismiss popup
                        self.popup_state = None
                        # ensures it only shows once
                        self.boss_battle_tutorial_seen = True
                        self.battle.start_fight(boss_fight=True)
            
            # Skip other inputs while popup is open
            return

        # Battle menu navigation (not in popup)
        if self.in_fight and self.battle.turn == "player":
            
            # prevent player menu movement during boss special animation
            if self.battle.special_anim_active:
                return
            
            # prevent player menu movement during player HP animation
            if self.battle.start_hp_animation or self.battle.repair_pending:
                return
    
            if key == arcade.key.RIGHT:
                self.sfx_speed = random.uniform(1.1, 1.15)
                self.current_sfx = arcade.play_sound(self.button_sfx, .6, 0, False, self.sfx_speed)
                self.fight_menu_index = (self.fight_menu_index + 1) % len(self.fight_buttons)
            
            elif key == arcade.key.LEFT:
                self.sfx_speed = random.uniform(1.1, 1.15)
                self.current_sfx = arcade.play_sound(self.button_sfx, .6, 0, False, self.sfx_speed)
                self.fight_menu_index = (self.fight_menu_index - 1) % len(self.fight_buttons)
            
            elif key == arcade.key.ENTER:
                selected = self.fight_buttons[self.fight_menu_index]
                if selected == "Attack":
                    self.battle.attack_enemy()
                elif selected == "Items":
                    self.open_item_menu()
                    # deselect fight buttons
                    self.fight_menu_index = 0
                elif selected == "Special":
                    self.popup_state = "special"
                    self.battle.special_menu_index = 0
                    self.fight_menu_index = 0
            return

        # Overworld X key toggles status
        if key == arcade.key.X:
            if self.popup_state == "status":
                self.popup_state = None
            else:
                self.popup_state = "status"
                self.menu_index = 0
                self.popup_options = self.menu_options.copy()
            return
        
        # Overworld Z key investigates rooms
        if key == arcade.key.Z:
            current = self.character.currentPosition
            neighbors, visited, looted = self.maze[current]
            
            if current == "Shop":
                # Open shop popup
                self.popup_state = "shop"
                self.shop_menu_index = 0
            
            else:
                if not looted:
                    # Play Loot SFX
                    self.sfx_speed = random.uniform(1, 1.1)
                    self.current_sfx = arcade.play_sound(self.loot_sfx, 1.1, 0, False, self.sfx_speed)
                    
                    
                    # Item drop
                    loot = self.generate_Item()
                    for item in loot:
                        self.character.pickup(item)
                    self.maze[current] = (neighbors, visited, True)
                    
                    # Gold drop
                    gold_amount = random.randint(0, 4)  
                    if gold_amount > 0:
                        # Add gold directly to character
                        item_name, amount = self.character.items["Gold"]
                        self.character.items["Gold"] = (item_name, amount + gold_amount)
                        loot.append(f"{gold_amount} Gold")

                    self.loot_popup_text = "You found: " + ", ".join(loot) if loot else "Nothing was found here."
                    self.loot_popup_state = "loot"
                    self.loot_popup_timer = 0.0
                else:
                    self.loot_popup_text = "This room has already been investigated."
                    self.loot_popup_state = "loot"
                    self.loot_popup_timer = 0.0

            return


        # Movement handling
        # prevent movement during enemy turn or attack QTE
        if self.battle.turn != "player":
            return
        
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

                # Check for fight if we're not moving into the Shop
                if self.character.currentPosition != "Shop" and self.character.currentPosition != "End":
                    self.battle.try_fight()
                    break

        if moved:
            
            # Play footsetp SFX
            self.sfx_speed = random.uniform(1.15, 1.25)
            self.current_sfx = arcade.play_sound(self.footsteps_sfx, 0.7, 0, False, self.sfx_speed)
            
            # Setup room fade
            self.bg_alpha = 0
            self.text_alpha = 0
            self.text_timer = 0
            self.fade_in_complete = False
            
            # Leaving shop return to overworld music
            if self.left_shop and self.character.currentPosition != "Shop" and self.shop_transition_cooldown <= 0:
                self.music_volume = .5
                self.transition_music(self.overworld)
                self.left_shop = False
                # prevents instant retrigger
                self.shop_transition_cooldown = 2.0

            # Entering shop
            if self.character.currentPosition == "Shop" and self.shop_transition_cooldown <= 0:
                self.music_volume = .25
                self.transition_music(self.shop)
                self.left_shop = True
                # prevents overlap
                self.shop_transition_cooldown = 2.0

            
            # Check if this is the final room
            if self.character.currentPosition == "End":
                # trigger final boss popup
                self.popup_state = "End"
                self.menu_index = 0
                self.popup_options = ["Yes", "No"]
                
            # Check for Shop tutorial
            if self.character.currentPosition == "Shop" and not getattr(self, "shop_tutorial_seen", False):
                self.popup_state = "shop_tutorial"
                self.menu_index = 0
                # Only one option to dismiss
                self.popup_options = ["OK"]
                # ensures it only shows once
                self.shop_tutorial_seen = True
    
    
    def on_update(self, delta_time: float):
        """This method keeps track of what's supposed to be on screen every frame"""
        
        self.update_music_fade(delta_time)
        
        if self.shop_transition_cooldown > 0:
            self.shop_transition_cooldown -= delta_time
        
        if not self.in_fight and self.post_fight_cooldown > 0:
            self.post_fight_cooldown -= delta_time
            # ignore movement & fights until done
            return

        # Player attack logic
        if self.battle.attack_animation_active and hasattr(self.battle, "attack_animation_sprite"):
            sprite = self.battle.attack_animation_sprite

            # Rotate the pie
            sprite.angle += sprite.rotation_speed * delta_time

            # Check if rotation reached target
            if hasattr(sprite, "rotation_target") and sprite.angle >= sprite.rotation_target:
                sprite.angle = sprite.rotation_target  # clamp to target

                if self.battle.attack_hits > 0:
                    # Queue next rotation for combo
                    self.battle.attack_hits -= 1
                    sprite.rotation_target += 360
                    sprite.rotation_speed += 30
                else:

                    # Last rotation done resolve attack
                    self.battle.attack_animation_active = False
                    self.battle.resolve_attack(self.current_enemy)
        
        # Dodge QTE Logic
        if self.battle.dodge_active and self.battle.dodge_waiting_for_input:
            
            # Ensure pointer_x is initialized
            if not hasattr(self.battle, "pointer_x"):
                self.battle.pointer_x = self.battle.dodge_bar_x - self.battle.dodge_bar_width / 2

            # Delay before starting pointer
            if not getattr(self.battle, "pointer_moving", False):
                self.battle.dodge_delay_timer += delta_time
                if self.battle.dodge_delay_timer >= self.battle.dodge_start_delay:
                    self.battle.pointer_moving = True
            else:
                self.battle.pointer_x += self.battle.pointer_speed * delta_time
                
                # Clamp pointer and end dodge
                if self.battle.pointer_x >= self.battle.dodge_bar_right:
                    self.battle.pointer_x = self.battle.dodge_bar_right
                    self.battle.dodge_waiting_for_input = False
                    self.battle.pointer_moving = False
                    self.battle.apply_dodge_result(self.current_enemy)
        
        # Reset Dodge UI (separate from waiting for input)
        if self.battle.dodge_active and not self.battle.dodge_waiting_for_input:
            self.battle.dodge_result_timer += delta_time
            if self.battle.dodge_result_timer >= self.battle.dodge_result_display_time:
                # Time’s up hide dodge UI and restore battle
                self.battle.dodge_active = False
                self.battle.enemy_attack_animation_active = False
                
                self.fight_buttons_visible = True
                self.hp_bar_visible = True
                self.hp_label_visible = True
                
                self.battle.current_dodge_arrow = None
                self.battle.dodge_direction = None
                self.battle.dodge_result_timer = 0.0

        # Smooth HP bar animation for player
        self.battle.update_hp_animation(delta_time)
                
        # Smooth HP bar animation for enemy
        self.battle.update_enemy_hp_animation(delta_time)
        
        # Enemy hurt animation
        self.battle.update_enemy_hurt_animation(delta_time)
        
        # Enemy Attack Animation
        self.battle.update_enemy_attack_animation(delta_time)
        
        # Apply enemy damage after animation finishes
        self.battle.apply_pending_enemy_damage()
                
        # Enemy death animation
        self.battle.update_enemy_death_animation(delta_time)
        
        # Enemy special animation
        self.battle.update_special_animation(delta_time)

        # Auto-Repairs after enemy attack
        if self.battle.repair_pending and self.battle.repair > 0:
            # wait until HP animation finishes
            if not self.battle.start_hp_animation and self.battle.turn == "player":
                self.battle.repair_timer += delta_time
                if self.battle.repair_timer >= self.battle.repair_delay:
                    # Heal 10 HP
                    self.character.hp = min(self.character.max_hp, self.character.hp + 10)
                    # Triggers smooth HP bar update
                    self.battle.start_hp_animation = True
                    self.loot_popup_text = "Repaired 10 HP!"
                    self.loot_popup_state = "loot"
                    self.loot_popup_timer = 0.0

                    # Reset timer and decrease remaining turns
                    self.battle.repair_timer = 0.0
                    self.battle.repair -= 1
                    
                    # If no repairs left, disable pending flag
                    self.battle.repair_pending = False
                        
                    if self.battle.repair <= 0:
                        self.battle.repair_in_progress = False
        
        # Smooth MP bar animation for player
        self.battle.update_mp_animation(delta_time)
        
        # Fade in room background
        if self.bg_alpha < 255:
            self.bg_alpha += self.fade_speed_bg * delta_time
            if self.bg_alpha > 255:
                self.bg_alpha = 255

        # Fade in text after delay
        self.text_timer += delta_time
        if self.text_timer >= self.text_delay and self.text_alpha < 255:
            self.text_alpha += self.fade_speed_text * delta_time
            if self.text_alpha > 255:
                self.text_alpha = 255
        
        # Check if fade-in is complete
        if self.bg_alpha >= 255 and self.text_alpha >= 255:
            self.fade_in_complete = True
            
        # Loot popup timer
        if self.loot_popup_state == "loot":
            self.loot_popup_timer += delta_time
            if self.loot_popup_timer >= self.loot_popup_duration:
                self.loot_popup_state = None
        
        # Battle Fading
        if self.in_fight:
            
            # Block ALL enemy actions while a boss special animation is running
            if self.battle.special_anim_active:
                return

            # Fade in fight visuals
            if self.fight_alpha < 255:
                self.fight_alpha += self.fight_fade_speed * delta_time
                if self.fight_alpha > 255:
                    self.fight_alpha = 255
            if self.fight_text_alpha < 255:
                self.fight_text_alpha += self.fight_fade_speed * delta_time
                if self.fight_text_alpha > 255:
                    self.fight_text_alpha = 255

            # Check if fade-in is complete
            self.fade_in_complete = self.fight_alpha >= 255 and self.fight_text_alpha >= 255

            # Enemy attack delay
            if self.battle.turn == "enemy_wait":
                self.enemy_attack_delay -= delta_time
                if self.enemy_attack_delay <= 0:
                    self.battle.turn = "enemy"
                    self.enemy_action_timer = 0
                    self.enemy_action_delay = 0.6
            
            # Enemy turn
            if self.battle.turn == "enemy":
                self.enemy_action_timer += delta_time
                if self.enemy_action_timer >= self.enemy_action_delay:
                    # Only start attack if fade-in is done
                    if self.fade_in_complete and not getattr(self.battle, "dodge_active", False):
                        self.battle.enemy_attack(self.current_enemy)
