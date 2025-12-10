import arcade
import os
import random
from PIL import Image
from io import BytesIO

class NightBorne:
    """
    This is a regular enemy class, it has stats, animations,
    a basic attack and special moves
    Anner, Tiffany
    """

    SPRITE_SCALE = 5.0
    COLUMNS = 23
    ROWS = 5
    FRAME_WIDTH  = 80
    FRAME_HEIGHT = 80

    _cached_frames = None  # only load once

    def __init__(self):
        """This is the class setrup"""
        
        self.name = "NightBorne"
        self.hp = 100
        self.max_hp = 100
        self.atk = 16
        self.defense = 9
        self.spd = 14

        # Load frames
        if NightBorne._cached_frames is None:
            NightBorne._cached_frames = NightBorne._load_frames()

        self.frames = NightBorne._cached_frames

        self.sprite = arcade.Sprite(scale=self.SPRITE_SCALE)
        self.sprite.texture = self.frames[0]
        self.sprite.visible = False


    @staticmethod
    def _load_frames():
        """
        Loads and returns the sprite sheet for this boss
        sliced into frames in a list
        """
        
        path = os.path.join("Simple_RPG", "Art", "Enemies", "NightBorne.png")
        sheet = Image.open(path).convert("RGBA")
        sheet_width, sheet_height = sheet.size

        NightBorne.FRAME_WIDTH  = sheet_width  // NightBorne.COLUMNS
        NightBorne.FRAME_HEIGHT = sheet_height // NightBorne.ROWS

        # Stores the sliced sprites/frames
        frames = []
        for row in range(NightBorne.ROWS):
            for col in range(NightBorne.COLUMNS):
                left   = col * NightBorne.FRAME_WIDTH
                top    = sheet_height - (row+1) * NightBorne.FRAME_HEIGHT
                right  = left + NightBorne.FRAME_WIDTH
                bottom = top  + NightBorne.FRAME_HEIGHT

                frame = sheet.crop((left, top, right, bottom))
                temp = BytesIO()
                frame.save(temp, format="PNG")
                temp.seek(0)
                frames.append(arcade.load_texture(temp))

        return frames


    # Animations
    def idle_sprite(self):
        """Returns the boss enemys idle sprite"""
        return self.sprite
    
    def attack_animation(self):
        """Returns the boss enemys attack frames"""
        return self.frames[46:58]
    
    def hurt_animation(self):
        """Returns the boss enemys hurt frames"""
        return self.frames[23:28]
    
    def death_animation(self):
        """Returns the boss enemys death frames"""
        return self.frames[0:23]
    
    def special_animation(self):
        """Returns the boss enemys special move frames"""
        return self.frames[92:101]


    def calc_damage(self, guard, character):
        """
        Calculates and returns how much damage this enemy attack does
        
        Args:
            guard: Whether or not the player has the guard buff active
            
            character: The instance of character the game is using
        """
        
        damage = max(0, self.atk - character.defense)
        if guard > 0:
            damage = round(damage / 2)
            guard -= 1
        return damage, guard


    def decide_action(self, battle):
        """
        This method determines what action the boss will take on its turn
        It will return a number representing its decision
        Different actions have different chances of 
        triggering depending on the bosses HP
        
        Args:
            battle: The instance of BattleScreen the game is using
        """
        
        num = random.randint(1, 100)

        # More likely to heal when HP is at or below 40%
        if self.hp <= 40:
            
            # Try heal (40%)
            if num <= 40:
                healed_amount = self.heal()
                battle.start_enemy_hp_animation = True
                return 1, healed_amount
            
            # Try debuff (20%) only if useful
            if 40 < num <= 60 and (battle.guard > 0 or battle.overclock > 0 or battle.repair > 0):
                self.debuff(battle)
                return 2, None
            
            # Otherwise attack (remaining 40% - 60%)
            return 3, None
        

        else:

            # Heal chance only if below 75% HP (20%)
            if self.hp <= 75 and num <= 20:
                healed_amount = self.heal()
                battle.start_enemy_hp_animation = True
                return 1, healed_amount

            # Debuff (10%) only if relevant
            if 20 < num <= 30 and (battle.guard > 0 or battle.overclock > 0 or battle.repair > 0):
                self.debuff(battle)
                return 2, None
            
            # Otherwise attack (remaining 70–80%)
            return 3, None
        
        
    def heal(self):
        """This method handles the healing special move"""
        healed_hp = min(self.max_hp - self.hp, 40)
        self.hp += healed_hp
        return healed_hp
    
   
    def debuff(self, battle):
        """This method handles the debuff special move"""
        battle.overclock = 0
        battle.guard = 0
        battle.repair = 0