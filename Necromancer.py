import arcade
import random
from PIL import Image
from io import BytesIO
import os

class Necromancer:
    """
    This is a regular enemy class, it has stats, animations,
    a drop chance for loot and a basic attack
    Tiffany
    """
    
    SPRITE_SCALE = 3.0
    FRAME_WIDTH = 160
    FRAME_HEIGHT = 128
    COLUMNS = 17
    ROWS = 7

    _cached_frames = None

    def __init__(self):
        """This is the class setrup"""
        
        self.name = "Necromancer"
        self.hp = 30
        self.max_hp = 30
        self.atk = 10
        self.defense = 5
        self.spd = 11

        # Load frames once for all Necromancers
        if Necromancer._cached_frames is None:
            Necromancer._cached_frames = Necromancer._load_frames()

        self.frames = Necromancer._cached_frames
        
        self.sprite = arcade.Sprite(scale=self.SPRITE_SCALE)
        self.sprite.texture = self.frames[0]
        self.sprite.visible = False

    @staticmethod
    def _load_frames():
        """
        Loads and returns the sprite sheet for this enemy
        sliced into frames in a list
        """
        
        sheet_path = os.path.join("Simple_RPG", "Art", "Enemies", "Necromancer.png")
        sheet = Image.open(sheet_path).convert("RGBA")
        sheet_width, sheet_height = sheet.size

        # Stores the sliced sprites/frames
        frames = []
        for row in range(Necromancer.ROWS):
            for col in range(Necromancer.COLUMNS):
                left = col * Necromancer.FRAME_WIDTH
                top = sheet_height - (row + 1) * Necromancer.FRAME_HEIGHT
                right = left + Necromancer.FRAME_WIDTH
                bottom = top + Necromancer.FRAME_HEIGHT

                frame_img = sheet.crop((left, top, right, bottom))

                temp = BytesIO()
                frame_img.save(temp, format="PNG")
                temp.seek(0)
                frames.append(arcade.load_texture(temp))

        return frames

    def idle_sprite(self):
        """Returns the enemys idle sprite"""
        return self.sprite
    
    def hurt_animation(self):
        """Returns the enemys hurt frames"""
        return self.frames[17:21]
    
    def attack_animation(self):
        """Returns the enemys attack frames"""
        return self.frames[68:81]
    
    def death_animation(self):
        """Returns the enemys death frames"""
        return self.frames[0:9]
    
    def calc_damage(self, guard, character):
        """
        Calculates and returns how much damage this enemy attack does
        
        Args:
            guard: Whether or not the player has the guard buff active
            
            character: The instance of character the game is using
        """
        
        damage = max(0, self.atk - character.defense)
        if guard > 0:
            damage = round(damage/2)
            guard -= 1
        return damage, guard

    def drop_loot(self, character):
        """
        Determines and returns what loot this enemy dropped when it dies
        
        Args:            
            character: The instance of character the game is using
        """
        
        loot = None
        num = random.randint(1,10)
        if num == 1:
            loot = "HP Potion"
            character.pickup("HP Potion")
        return loot
