import random
import arcade
from ScreenChanger import ScreenChanger

class BattleScreen:
    """
    This class controls the majority(90%) of the games fighting logic
    and works together with the MainScreen class as well as the enemy classes
    It handles things like turn orders, damage caluclations, fighting animations
    and some music transitioning
    Anner, Tiffany, Aexandra
    """

    def __init__(self, main):
        """
        This is the setup for this class
        
        Args:
            main: This is the instance of the Mainscreen class 
                  that the game is currently running
                  We use it to access and manipulate variables 
                  that could not be moved to this class directly
        """
        
        self.main = main
        self.window = main.window
        self.character = main.character

        self.turn = "player"

        # PLAYER HP/MP ANIMATION
        self.player_display_hp = self.character.hp
        self.player_display_mp = self.character.mp
        self.start_hp_animation = False
        self.start_mp_animation = False

        # ATTACK QTE STATE
        self.attack_animation_sprite= None
        self.pie_sprite = arcade.load_texture("Simple_RPG/Art/Attack/Pie.png")
        self.pointer_sprite = None
        self.attack_animation_list = arcade.SpriteList()
        self.pointer_list = arcade.SpriteList()

        self.attack_animation_active = False
        self.attack_waiting_for_input = False
        self.attack_hit_registered = False
        self.attack_hits = 0
        self.total_attack_hits = 0
        self.attack_total_damage = 0

        # ENEMY HP DISPLAY
        self.enemy_display_hp = 0
        self.start_enemy_hp_animation = False

        # ENEMY ATTACK ANIMATION
        self.enemy_attack_frames = []
        self.enemy_attack_frame_index = 0
        self.enemy_attack_frame_timer = 0
        self.enemy_attack_frame_duration = 0.1
        self.enemy_sprite_attack_animation_active = False
        
        # NIGHTBORNE SPECIALS ANIMATION
        self.special_anim_frames = []
        self.special_anim_index = 0
        self.special_anim_timer = 0
        self.special_anim_frame_duration = 0.12
        self.special_anim_active = False
        self.pending_special_popup = None

        # PENDING DAMAGE THAT'S APPLIED AFTER ANIMATION
        self.pending_enemy_damage = 0
        self.apply_enemy_damage_after_attack = False

        # ENEMY HURT ANIMATION
        self.enemy_hurt_frames = []
        self.enemy_hurt_frame_index = 0
        self.enemy_hurt_frame_timer = 0
        self.enemy_hurt_frame_duration = 0.15
        self.enemy_hurt_animation_active = False

        # ENEMY DEATH ANIMATION
        self.enemy_death_frames = []
        self.enemy_death_index = 0
        self.enemy_death_timer = 0
        self.enemy_death_frame_duration = 0.1
        self.enemy_death_animation_active = False

        # DODGE QTE (BOSS ONLY)
        self.dodge_active = False
        self.dodge_waiting_for_input = False
        self.enemy_attack_animation_active = False
        self.dodge_rounds_remaining = 0
        self.dodge_total_damage = 0

        # DODGE QTE BAR
        self.dodge_bar_x = 0
        self.dodge_bar_y = 0
        self.dodge_bar_left = 0
        self.dodge_bar_right = 0
        self.dodge_bar_texture = arcade.load_texture("Simple_RPG/Art/Dodge/Bar.png")
        self.dodge_bar_width = self.dodge_bar_texture.width
        self.dodge_bar_height = self.dodge_bar_texture.height

        # DODGE QTE POINTER
        self.pointer_x = 0
        self.pointer_speed = 0
        self.pointer_moving = False
        self.dodge_delay_timer = 0
        self.dodge_start_delay = 0.5
        self.dodge_pointer_texture = arcade.load_texture("Simple_RPG/Art/Attack/Pointer.png")
        self.dodge_pointer_width = self.dodge_pointer_texture.width
        self.dodge_pointer_height = self.dodge_pointer_texture.height
        self.dodge_pointer_scale = 0.5
        self.pointer_speed = self.dodge_bar_width / .8

        # DODGE QTE ARROW
        self.current_dodge_arrow = None
        self.dodge_direction = None
        self.boss_attack_animation_played = False
        
        self.dodge_down = arcade.load_texture("Simple_RPG/Art/Dodge/Down.png")
        self.dodge_right = arcade.load_texture("Simple_RPG/Art/Dodge/Right.png")
        self.dodge_up = arcade.load_texture("Simple_RPG/Art/Dodge/Up.png")
        self.dodge_left = arcade.load_texture("Simple_RPG/Art/Dodge/Left.png")
        self.dodge_list = (self.dodge_down, self.dodge_right, self.dodge_up, self.dodge_left)

        # PLAYER BUFFS
        self.overclock = 0
        self.guard = 0
        self.repair = 0
        self.repair_pending = False
        self.repair_in_progress = False
        self.repair_delay = 1.5
        self.repair_timer = 0
        self.special_menu_options = list(self.character.special.keys())
        self.special_menu_index = 0

    
    def try_fight(self):
        """Try to trigger a fight based on RNG."""
        
        chance = 1.0
        if random.random() < chance:
            if not self.main.battle_tutorial_seen:
                self.main.popup_state = "battle_tutorial"
                self.main.menu_index = 0
                self.main.popup_options = ["OK"]
            else:
                self.start_fight()

    
    def start_fight(self, boss_fight=False):
        """
        This method begins a fight sequence
        
        Args:
            boss_fight: This let's the game know whether or not this 
                        is a boss fight which is an important distinction
                        because the mechanice are different
        """
        
        # shorthand
        main = self.main

        main.in_boss_fight = boss_fight

        # Transition music
        main.music_volume = .35
        main.transition_music(main.battle_music)

        # Set fight state
        main.in_fight = True
        main.fight_alpha = 0
        main.fight_text_alpha = 0
        main.enemy_action_timer = 0
        main.enemy_action_delay = 2.0

        # Load attack animation assets
        self.load_attack_animation()

        # Pick enemy
        if boss_fight:
            main.current_enemy = random.choice(main.boss_list)
        else:
            main.current_enemy = random.choice(main.enemies)

        # Create sprite
        main.fight_enemy = main.current_enemy.idle_sprite()
        main.fight_enemy.texture = main.current_enemy.frames[0]

        # Reset HP
        main.current_enemy.hp = main.current_enemy.max_hp
        self.enemy_display_hp = main.current_enemy.hp

        # Position sprite
        sw, sh = main.window.get_size()
        main.fight_enemy.center_x = sw / 2
        main.fight_enemy.center_y = sh / 2 + 20
        main.fight_enemy.visible = True

        # Add to sprite list
        main.fight_sprites.append(main.fight_enemy)

        # Close popups
        main.popup_state = None
        main.loot_popup_state = None

        # Decide who acts first
        if main.character.spd > main.current_enemy.spd:
            self.turn = "player"
        else:
            self.turn = "enemy"
            
    
    def load_enemy_sprite(self, enemy):
        """
        This method sets the idle sprite for the current enemy being faced
        
        Args:
            enemy: The current enemy class instance
        
        Returns the enemy's idle sprite positioned for battle.
        """
        sprite = enemy.idle_sprite()

        # Position defaults — these can be adjusted later
        sprite.center_x = self.main.window.width // 2
        sprite.center_y = self.main.window.height // 2 + 20
        sprite.visible = True

        return sprite
    
    
    def draw_player_hp_bar(self):
        """Draw the players HP bar during battle."""

        bar_width=100 
        bar_height=12
        
        player = self.character
        display_hp = self.player_display_hp

        # Ratio & fill width
        fill_ratio = max(display_hp / player.max_hp, 0)
        filled_width = bar_width * fill_ratio

        # Set up position
        screen_width, screen_height = self.window.get_size()
        cx = screen_width / 2 - 118
        cy = 60 + 30

        left = cx - bar_width / 2
        right = cx + bar_width / 2
        bottom = cy - bar_height / 2
        top = cy + bar_height / 2

        # Background bar
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.DARK_GRAY)

        # Filled portion
        arcade.draw_lrbt_rectangle_filled(left, left + filled_width, bottom, top, arcade.color.GREEN)

        # Outline
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.WHITE, 2)

        # Text label
        hp_text = f"HP: {int(display_hp)}/{player.max_hp}"
        text_width = len(hp_text) * 7
        text_x = left - text_width - 20
        text_y = cy - (bar_height / 2)
        arcade.draw_text(hp_text, text_x, text_y, arcade.color.WHITE, 14, bold=True)
            
    
    def draw_player_mp_bar(self):
        """Draw the players MP bar during battle."""

        bar_width=100
        bar_height=12
        
        player = self.character
        display_mp = self.player_display_mp

        # Ratio & fill width
        fill_ratio = max(display_mp / player.max_mp, 0)
        filled_width = bar_width * fill_ratio

        # Set up position
        screen_width, screen_height = self.window.get_size()
        cx = screen_width / 2 + 199
        cy = 60 + 30

        left = cx - bar_width / 2
        right = cx + bar_width / 2
        bottom = cy - bar_height / 2
        top = cy + bar_height / 2

        # Background 
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.DARK_GRAY)

        # Fill
        arcade.draw_lrbt_rectangle_filled(left, left + filled_width, bottom, top, arcade.color.BLUE)

        # Outline
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.WHITE, 2)

        # Text
        mp_text = f"MP: {int(display_mp)}/{player.max_mp}"
        text_width = len(mp_text) * 7
        text_x = left - text_width - 25
        text_y = cy - (bar_height / 2)
        arcade.draw_text(mp_text, text_x, text_y, arcade.color.WHITE, 14, bold=True)


    def draw_enemy_hp_bar(self):
        """
        Draws the enemies HP bar during battle
        """
        
        bar_width=100
        bar_height=10
        
        enemy = self.main.current_enemy
        sprite = self.main.fight_enemy

        # Ratio & fill width
        fill_ratio = max(self.enemy_display_hp / enemy.max_hp, 0)
        filled_width = bar_width * fill_ratio

        # Positioning
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


    def update_hp_animation(self, delta_time):
        """
        Smooth HP bar animation and game over check
        
        Args:
            delta_time: Seconds since the last frame
        """
        
        # Ensures animation only runs when it's supposed to
        if not self.start_hp_animation:
            return

        diff = self.player_display_hp - self.character.hp

        # Smooth animation
        if abs(diff) > 0.1:
            self.player_display_hp -= diff * min(1, 3 * delta_time)
        else:
            self.player_display_hp = self.character.hp
            self.start_hp_animation = False  # animation complete

        # Game Over check
        if (
            self.player_display_hp <= 0 and
            not getattr(self.main, "game_over", False)
           ):
            self.character.hp = 0
            self.main.game_over = True
            self.main.loot_popup_state = None
            self.main.in_fight = False


    def update_mp_animation(self, delta_time):
        """
        Smoothly animates MP bar changes
        
        Args:
            delta_time: Seconds since the last frame
        """
        
        # Ensures animation only runs when it's supposed to
        if not self.start_mp_animation:
            return
            
        diff = self.player_display_mp - self.character.mp
        if abs(diff) > 0.1:
            self.player_display_mp -= diff * min(1, 3 * delta_time)
        else:
            self.player_display_mp = self.character.mp
            self.start_mp_animation = False
              
    
    def update_enemy_hp_animation(self, delta_time):
        """
        Smooth enemy HP bar animation
        
        Args:
            delta_time: Seconds since the last frame
        """
        
        main = self.main
        if not self.start_enemy_hp_animation:
            return

        enemy = main.current_enemy
        if not enemy:
            return

        diff = self.enemy_display_hp - enemy.hp

        # Smooth animation
        if abs(diff) > 0.1:
            self.enemy_display_hp -= diff * min(1, 3 * delta_time)
        else:
            self.enemy_display_hp = enemy.hp
            self.start_enemy_hp_animation = False
    
    
    def update_enemy_hurt_animation(self, delta_time):
        """
        Updates enemy hurt animation frames
        
        Args:
            delta_time: Seconds since the last frame
        """
        
        if not self.enemy_hurt_animation_active:
            return

        self.enemy_hurt_frame_timer += delta_time

        # Keeps track of how long every individual sprite should stay up
        if self.enemy_hurt_frame_timer >= self.enemy_hurt_frame_duration:
            self.enemy_hurt_frame_timer = 0.0
            self.enemy_hurt_frame_index += 1

            # Advances to the next sprite when appropriate
            if self.enemy_hurt_frame_index < len(self.enemy_hurt_frames):
                self.main.fight_enemy.texture = self.enemy_hurt_frames[self.enemy_hurt_frame_index]
            else:
                # Turn off aniamtion once completed and # Return to idle texture
                self.enemy_hurt_animation_active = False
                enemy = self.main.current_enemy
                self.enemy_hurt_frame_index = 0
                self.main.fight_enemy.texture = enemy.frames[0]


    def update_enemy_attack_animation(self, delta_time):
        """
        Advance frames for enemy attack animation
        
        Args:
            delta_time: Seconds since the last frame
        """
        
        # Ensures animation only runs when it's supposed to
        if not self.enemy_sprite_attack_animation_active:
            return

        frames = self.enemy_attack_frames
        self.enemy_attack_frame_timer += delta_time

        # Keeps track of how long every individual sprite should stay up
        if self.enemy_attack_frame_timer >= self.enemy_attack_frame_duration:
            self.enemy_attack_frame_timer = 0.0
            self.enemy_attack_frame_index += 1

            # Advances to the next sprite when appropriate
            if self.enemy_attack_frame_index < len(frames):
                self.main.fight_enemy.texture = frames[self.enemy_attack_frame_index]
            else:
                # Turn off aniamtion once completed and # Return to idle texture
                self.enemy_sprite_attack_animation_active = False
                self.enemy_attack_frame_index = 0
                self.main.fight_enemy.texture = self.main.current_enemy.frames[0]  # idle
                

    def apply_pending_enemy_damage(self):
        """
        Apply the stored enemy attack damage once
        the enemies attack animation is finished
        """

        # Ensures animation only runs when it's supposed to
        if not self.apply_enemy_damage_after_attack:
            return

        # Only apply damage once animation has stopped
        if not self.enemy_sprite_attack_animation_active:
            self.main.character.hp = max(0, self.main.character.hp - self.pending_enemy_damage)
            
            # Trigger player HP animation
            self.start_hp_animation = True
            
            # Reset flag
            self.apply_enemy_damage_after_attack = False


    def attack_enemy(self):
        """Start the player's attack animation and QTE."""

        # Hide battle UI and show attack animation
        self.attack_animation_active = True
        self.attack_animation_sprite.visible = True
        self.pointer_sprite.visible = True

        # Stop turns and wait for Z input
        self.turn = None
        self.attack_waiting_for_input = True
        # Track whether player pressed Z in time
        self.attack_hit_registered = False

        # Initialize combo tracking
        self.attack_hits = 0
        self.total_attack_hits = 0
        self.attack_total_damage = 0

        # Start rotation at the initial angle
        self.attack_animation_sprite.angle = 60
        self.attack_animation_sprite.rotation_target = 420
        self.attack_animation_sprite.rotation_speed = 330


    def enemy_attack(self, enemy):
        """
        Handles both normal enemy attacks and boss dodge QTE attacks
        
        Args:
            enemy: The current enemy, also determines whether this is a boss fight
        """

        # shorthand
        main = self.main

        # Boss attack
        from NightBorne import NightBorne

        if isinstance(enemy, NightBorne):

            # Boss decides its action
            decision, healed_amount = enemy.decide_action(self)
            
            # Healing
            if decision == 1:
                # Hide battle UI
                main.fight_buttons_visible = False
                main.hp_bar_visible = False
                main.hp_label_visible = False

                # Load frames for special animation
                self.special_anim_frames = enemy.special_animation()
                self.special_anim_index = 0
                self.special_anim_timer = 0
                self.special_anim_active = True

                # Store popup text to show after special animation
                self.pending_special_popup = f"The {enemy.name} healed {healed_amount} HP!"

                return

            # Debuff
            elif decision == 2:
                # Hide battle UI
                main.fight_buttons_visible = False
                main.hp_bar_visible = False
                main.hp_label_visible = False
                
                # Load frames for special animation
                self.special_anim_frames = enemy.special_animation()
                self.special_anim_index = 0
                self.special_anim_timer = 0
                self.special_anim_active = True

                # Store popup text to show special after animation
                self.pending_special_popup = f"The {enemy.name} nullified your specials!"
                return
      
            # Normal boss attack
            else:
                # Hide battle UI
                main.fight_buttons_visible = False
                main.hp_bar_visible = False
                main.hp_label_visible = False
                
                # Start Dodge QTE state
                self.dodge_waiting_for_input = True
                self.dodge_active = True
                self.enemy_attack_animation_active = True
                self.dodge_rounds_remaining = 4
                # Launch first dodge sequence
                self.start_dodge(enemy)
                return  # damage handled inside dodge

        # Regular enemy attack
        damage, self.guard = enemy.calc_damage(self.guard, self.character)

        # Play enemy attack
        main.sfx_speed = random.uniform(1, 1.1)
        main.current_sfx = arcade.play_sound(main.necromancer_attack_sfx, .5, 0, False, main.sfx_speed)
        
        # Play enemy attack animation
        self.enemy_attack_frames = enemy.attack_animation()
        self.enemy_attack_frame_index = 0
        self.enemy_attack_frame_timer = 0.0
        self.enemy_sprite_attack_animation_active = True

        # Wait until animation finishes before applying damage
        self.pending_enemy_damage = damage
        self.apply_enemy_damage_after_attack = True

        # Popup text
        main.loot_popup_text = f"{enemy.name} attacked! You took {damage} damage!"
        main.loot_popup_state = "loot"
        main.loot_popup_timer = 0.0

        # Check if player is dead
        if self.character.hp <= 0:
            main.loot_popup_text = "You were defeated..."
            main.in_fight = False
            main.fight_enemy.visible = False
            main.fight_sprites = arcade.SpriteList()
            return

        # Enable Auto-Repair if active
        if self.repair > 0:
            self.repair_pending = True
            self.repair_in_progress = True

        self.turn = "player"


    def resolve_attack(self, enemy):
        """
        Finishes the player's attack animation, applies combo damage
        and moves on to the enemy turn
        
        Args:
            enemy: The current enemy
        """

        main = self.main

        # Prevent multiple calls
        if not (self.attack_animation_active or self.attack_waiting_for_input):
            return

        # End attack animation visuals
        self.attack_waiting_for_input = False
        self.attack_animation_active = False
        self.attack_animation_sprite.visible = False
        self.pointer_sprite.visible = False

        # Apply Overclock damage boost
        if self.overclock > 0:
            self.attack_total_damage *= 2
            self.overclock -= 1

        # If damage was dealt
        if self.attack_total_damage > 0:   
            # Play hit SFX
            main.sfx_speed = random.uniform(1, 1.1)
            main.current_sfx = arcade.play_sound(main.hit_sfx, .5, 0, False, main.sfx_speed)
            
            # Apply damage
            enemy.hp = max(0, enemy.hp - self.attack_total_damage)

            # Animate enemy HP bar
            self.start_enemy_hp_animation = True

            # play enemy Hurt animation
            self.enemy_hurt_frames = enemy.hurt_animation()
            self.enemy_hurt_frame_index = 0
            self.enemy_hurt_frame_timer = 0.0
            self.enemy_hurt_animation_active = True
            main.fight_enemy.texture = self.enemy_hurt_frames[0]

            if enemy.hp > 0:
                main.loot_popup_text = (
                    f"You dealt {self.attack_total_damage} total damage to {enemy.name}!"
                )

        else:
            # If player missed
            main.loot_popup_text = f"You missed {enemy.name}!"

        # Reset combo properties
        self.attack_total_damage = 0
        self.attack_hits = 0
        self.attack_hit_registered = False

        # Show popup
        main.loot_popup_state = "loot"
        main.loot_popup_timer = 0.0

        # Check if enemy is still alive
        if enemy.hp > 0:
            # Provides time for loot popup text to be read 
            # before the enemy takes its next turn
            self.turn = "enemy_wait"
            main.enemy_attack_delay = 1.5
            main.enemy_action_timer = 0.0
            return

        # Play enemy death animation
        self.enemy_death_frames = enemy.death_animation()
        self.enemy_death_index = 0
        self.enemy_death_timer = 0.0
        self.enemy_death_animation_active = True

        # Battle ends and buffs are reset
        self.turn = "player"
        main.enemy_action_timer = 0
        self.overclock = 0
        self.guard = 0
        self.repair = 0
        
        
    def handle_attack_input(self, enemy):
        """
        Handles Z-press during the attack QTE, determines hit/miss, 
        applies damage, and continues or ends the combo
        
        Args:
            enemy: The current enemy
        """

        sprite = self.attack_animation_sprite

        # Current angle
        angle = sprite.angle % 360

        # Hit zone
        red_start = 330
        red_end = (red_start + 65) % 360

        # Detect hit with wraparound
        if red_start < red_end:
            hit = red_start <= angle <= red_end
        else:
            hit = angle >= red_start or angle <= red_end

        # If attack lands
        if hit:

            # Calculate immediate hit damage (before combo bonus)
            damage = self.character.atk
            defense = getattr(enemy, "defense", 0)
            total_damage = max(0, damage - defense)

            # Add to combo total
            self.attack_total_damage += total_damage
            self.attack_hits += 1
            self.total_attack_hits += 1

            # Speed up next spin
            sprite.rotation_speed += 50

            # Allow player to press Z again
            self.attack_waiting_for_input = True

        else:
            # Miss
            self.attack_waiting_for_input = False
            # Immediately end combo
            self.resolve_attack(enemy)

        # Continue rotating animation
        self.attack_animation_active = True


    def start_dodge(self, enemy, reset_counter=True):
        """
        Initiates boss dodge QTE using a sliding pointer across a bar
        A Boss attacks 4 times unlike a regular enemy who only attacks once
        
        Args:
            reset_counter: Determines whether this is the start 
            of the enemies turn/first attack
        """
        
        main = self.main

        # Only start if player is in a boss fight
        if not main.in_boss_fight:
            return

        # Set up round counter only on the first QTE
        if reset_counter:
            self.dodge_rounds_remaining = 4
            self.boss_attack_animation_played = False

        # UI positioning
        screen_width, screen_height = main.window.get_size()

        self.dodge_bar_x = screen_width // 2
        self.dodge_bar_y = self.dodge_bar_height // 2 + 30
        self.dodge_bar_left  = self.dodge_bar_x - self.dodge_bar_width / 2
        self.dodge_bar_right = self.dodge_bar_x + self.dodge_bar_width / 2

        # Dodge/QTE state flags
        self.dodge_waiting_for_input = True
        self.dodge_active = True
        self.pointer_moving = False
        self.dodge_delay_timer = 0.0

        # Pointer starts at left side
        self.pointer_x = self.dodge_bar_left

        # Choose arrow direction & pick arrow sprite from MainScreen
        self.dodge_direction = random.choice(["Up", "Down", "Left", "Right"])

        # Example: main.dodge_up, main.dodge_left…
        self.current_dodge_arrow = getattr(self, f"dodge_{self.dodge_direction.lower()}")

        # Position arrow sprite
        self.dodge_arrow_y = self.dodge_bar_y + self.dodge_bar_height + 40


    def draw_fight_buttons(self):
        """Draw attack, items and special buttons during battle."""
        
        main = self.main   # shorthand
        screen_width, screen_height = self.window.get_size()

        cx = screen_width / 2
        h = 60
        cy = h / 2 + 10
        w = 500

        # Background panel
        arcade.draw_lrbt_rectangle_filled(
            cx - w/2, cx + w/2, cy - h/2, cy + h/2, arcade.color.BLACK
        )
        arcade.draw_lrbt_rectangle_outline(
            cx - w/2, cx + w/2, cy - h/2, cy + h/2, arcade.color.RED, 3
        )

        # Define buttons
        buttons = ["Attack", "Items", "Special"]
        box_w = 120
        box_h = h - 20
        spacing = 20

        start_x = cx - (len(buttons) * box_w + (len(buttons) - 1) * spacing) / 2

        # Draw each button using ScreenChnager's draw_button method
        for i, option in enumerate(buttons):
            cx_button = start_x + i * (box_w + spacing) + box_w / 2
            ScreenChanger.draw_button(
                cx_button,
                cy,
                box_w,
                box_h,
                option,
                highlighted=(i == main.fight_menu_index)
            )


    def apply_dodge_result(self, enemy, forced_fail=False):
        """
        Handles a single dodge result (boss attack) and queues 
        multiple dodges
        
        Args:
            forced_fail: If the player never inputted a key press
                         or hit the wrong key then they autoamtically
                         take full damage
        """
        
        main = self.main
        character = self.character

        # Track accumulated damage
        if not hasattr(self, "dodge_total_damage"):
            self.dodge_total_damage = 0

        base_damage = max(0, enemy.atk - character.defense)

        # Determine damage multiplier
        if forced_fail or base_damage == 0:
            damage_multiplier = 1.0
            self.blocked_percent = 0
        else:
            bar_center = (self.dodge_bar_left + self.dodge_bar_right) / 2
            distance = abs(self.pointer_x - bar_center)

            # Block/Dodge zones
            half_green = 33 / 2
            yellow_outer = half_green + 31
            orange_outer = yellow_outer + 62

            if distance <= half_green:
                damage_multiplier = 0.25
            elif distance <= yellow_outer:
                damage_multiplier = 0.50
            elif distance <= orange_outer:
                damage_multiplier = 0.75
            else:
                damage_multiplier = 1.00

        # Apply damage
        damage = round(base_damage * damage_multiplier)

        if self.guard > 0:
            damage = round(damage / 2)

        old_hp = character.hp
        character.hp = max(0, character.hp - damage)
        actual_damage = old_hp - character.hp

        # Add to total
        self.dodge_total_damage += actual_damage

        # Multi-dodge handling
        if not hasattr(self, "dodge_rounds_remaining"):
            self.dodge_rounds_remaining = 3  # 4 total
        else:
            self.dodge_rounds_remaining -= 1

        if self.dodge_rounds_remaining > 0:
            # Start next QTE round
            self.dodge_active = True
            self.dodge_waiting_for_input = True
            self.enemy_attack_animation_active = True
            self.pointer_moving = False
            self.dodge_delay_timer = 0.0

            self.start_dodge(enemy, reset_counter=False)
            return

        # FINAL dodge round applies total damage
        # Play boss attack animation
        if not self.boss_attack_animation_played:
            self.enemy_attack_frames = enemy.attack_animation()
            self.enemy_sprite_attack_animation_active = True
            self.boss_attack_animation_played = True

        # Show popup
        main.loot_popup_text = (
            f"The {enemy.name} attacked! You took {self.dodge_total_damage} damage!"
        )
        main.loot_popup_state = "loot"
        main.loot_popup_timer = 0.0

        # Trigger player HP animation
        self.start_hp_animation = True

        # Update guard
        if self.guard > 0:
            self.guard -= 1

        # Reset UI
        self.dodge_active = False
        self.dodge_waiting_for_input = False
        self.enemy_attack_animation_active = False
        
        main.fight_buttons_visible = True
        main.hp_bar_visible = True
        main.hp_label_visible = True
        
        self.current_dodge_arrow = None
        self.dodge_direction = None

        if self.repair > 0:
            self.repair_pending = True

        # Cleanup
        del self.dodge_total_damage
        del self.dodge_rounds_remaining
        self.turn = "player"


    def load_attack_animation(self):
        """Loads attack animation sprites into BattleScreen"""

        screen_width, screen_height = self.window.get_size()

        # Attack sprite (Pie)
        self.attack_animation_sprite = arcade.Sprite(self.pie_sprite, scale=0.5)
        self.attack_animation_sprite.center_x = screen_width / 2
        self.attack_animation_sprite.center_y = screen_height / 6
        self.attack_animation_sprite.angle = 30
        self.attack_animation_sprite.visible = False

        # Pointer sprite
        self.pointer_sprite = arcade.Sprite(self.dodge_pointer_texture, scale=0.5)
        self.pointer_sprite.center_x = self.attack_animation_sprite.center_x
        self.pointer_sprite.center_y = (
            self.attack_animation_sprite.center_y +
            self.attack_animation_sprite.height / 2 + 10
        )
        self.pointer_sprite.visible = False
        # Dimensions for dodge pointer drawing
        self.pointer_scale = 0.5
        self.pointer_width = self.pointer_sprite.texture.width
        self.pointer_height = self.pointer_sprite.texture.height

        # SpriteLists
        self.attack_animation_list = arcade.SpriteList()
        self.attack_animation_list.append(self.attack_animation_sprite)

        self.pointer_list = arcade.SpriteList()
        self.pointer_list.append(self.pointer_sprite)


    def update_enemy_death_animation(self, delta_time):
        """
        Advance enemy death animation and handle fight cleanup
        
        Args:
            delta_time: Seconds since the last frame
        """
        main = self.main


        if not self.enemy_death_animation_active:
            return

        self.enemy_death_timer += delta_time

        # Keeps track of how long every individual sprite should stay up
        if self.enemy_death_timer >= self.enemy_death_frame_duration:
            self.enemy_death_timer = 0.0
            self.enemy_death_index += 1
            
            # Advances to the next sprite when appropriate
            if self.enemy_death_index < len(self.enemy_death_frames):
                main.fight_enemy.texture = self.enemy_death_frames[self.enemy_death_index]
            else:
                # Finish animation and perform cleanup
                self.enemy_death_animation_active = False
                if not main.in_boss_fight:
                    main.in_fight = False
                    main.fight_enemy.visible = False
                    main.fight_sprites = arcade.SpriteList()
                    main.post_fight_cooldown = 1

                    # Determine whether the enemy dropped an item
                    text = main.current_enemy.drop_loot(main.character)
                    if text == None:
                        main.loot_popup_text = f"The {main.current_enemy.name} died"
                    else:
                        main.loot_popup_text = f"The {main.current_enemy.name} dropped an {text}"

                    main.loot_popup_state = "loot"
                    main.loot_popup_timer = 0.0
                    main.transition_music(main.overworld)

                # Set-up the win screen if it was a boss fight
                else:
                    main.win = True
                    main.popup_options = ["OK"]
                    main.menu_index = 0
                    main.transition_music(main.win_music)


    def update_special_animation(self, delta_time):
        """
        Update NightBorne heal/debuff animation frames
        
        Args:
            delta_time: Seconds since the last frame
        """

        if not self.special_anim_active:
            return

        self.special_anim_timer += delta_time

        # Keeps track of how long every individual sprite should stay up
        if self.special_anim_timer >= self.special_anim_frame_duration:
            self.special_anim_timer = 0
            self.special_anim_index += 1

            # Advances to the next sprite when appropriate
            if self.special_anim_index < len(self.special_anim_frames):
                self.main.fight_enemy.texture = self.special_anim_frames[self.special_anim_index]
                return

            # Animation finished
            self.special_anim_active = False

            # Return to idle frame
            enemy = self.main.current_enemy
            self.main.fight_enemy.texture = enemy.frames[0]

            # Show popup with stored text
            self.main.loot_popup_text = self.pending_special_popup
            self.main.loot_popup_state = "loot"
            self.main.loot_popup_timer = 0.0
            self.pending_special_popup = None

            # Restore UI
            self.main.fight_buttons_visible = True
            self.main.hp_bar_visible = True
            self.main.hp_label_visible = True
            self.turn = "player"