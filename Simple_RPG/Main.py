import arcade
from Character import Character
from MainScreen import MainScreen

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "CRYPTID: Red Archon"

class IntroView(arcade.View):
    def __init__(self):
        super().__init__()
        # Load the image as a sprite
        self.image_sprite = arcade.Sprite("Simple_RPG/Art/PAWN.png")

        # Position near bottom, under text
        self.image_sprite.center_x = SCREEN_WIDTH / 2
        self.image_sprite.center_y = 100   # adjust vertical position
        self.image_sprite.width = 150       # adjust size
        self.image_sprite.height = 175      # adjust size

        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.image_sprite)

        # Fade variables
        self.bg_alpha = 0       # for image fade
        self.text_alpha = 0     # for text fade
        self.fade_speed = 4
        self.text_delay = 30    # frames before text fades in
        self.frame_count = 0
        
        self.is_fading_out = False  # Tracks if the intro is currently fading out
        self.fade_out_alpha = 0     # For the overlay opacity during fade-out

        # Text lines
        self.lines = [
            "GREETINGS.",
            "WELCOME TO YOUR FIRST DAY OF TRAINING.",
            "YOU ARE PAWN.",
            "YOU ARE A WARRIOR IN THE RED ARCHON ARMY.",
            "YOU WILL BE TAKEN THROUGH THIS TESTING FACILITY.",
            "YOU WILL PRESS Z ON YOUR KEYBOARD TO CONTINUE."
        ]
        
        # Load intro/exploration music
        self.sound = arcade.load_sound("Simple_RPG/Music/Forest_Carnival.wav")
        # Play and loop intro/exploration music
        arcade.play_sound(self.sound, loop=True)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        # Fade-in image
        self.image_sprite.alpha = self.bg_alpha
        self.sprite_list.draw()

        # Draw text after delay
        if self.frame_count > self.text_delay:
            start_y = SCREEN_HEIGHT - 150
            for i, line in enumerate(self.lines):
                arcade.draw_text(
                    line,
                    SCREEN_WIDTH / 2,
                    start_y - 40 * i,
                    (255, 0, 0, self.text_alpha),
                    18 if i == 0 else 16,
                    anchor_x="center"
                )
        
        # If fading out, draw a black overlay that grows more opaque
        if self.is_fading_out:
            arcade.draw_lbwh_rectangle_filled(
                0, SCREEN_WIDTH, SCREEN_HEIGHT, 0,
                (0, 0, 0, int(self.fade_out_alpha))
            )

    def on_update(self, delta_time):
        self.frame_count += 1
        # --- Fade in sequence ---
        if not self.is_fading_out:
            if self.bg_alpha < 255:
                self.bg_alpha = min(255, self.bg_alpha + self.fade_speed)
            elif self.frame_count > self.text_delay and self.text_alpha < 255:
                self.text_alpha = min(255, self.text_alpha + self.fade_speed)
        
        # --- Fade out sequence ---
        elif self.is_fading_out:
            self.fade_out_alpha += 300 * delta_time
            if self.fade_out_alpha >= 255:
                self.fade_out_alpha = 255
                # Once fade is complete, transition to MainScreen
                player = Character()
                maze, connections = create_maze_data()
                main_view = MainScreen(player, maze, connections)
                self.window.show_view(main_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Z and self.text_alpha >= 255 and not self.is_fading_out:
            self.is_fading_out = True

# --- Maze setup (same as before) ---
def create_maze_data():
    connections = {
        "A": (False, ("Start", "Room 2")),
        "B": (False, ("Room 2", "Room 3")),
        "C": (False, ("Room 2", "Room 4")),
        "D": (False, ("Room 13", "Room 14")),
        "E": (False, ("Room 5", "Room 1")),
        "F": (False, ("Room 10", "Room 9")),
        "G": (False, ("Start", "Room 6")),
        "H": (False, ("Room 15", "Room 12")),
        "I": (False, ("Room 15", "Room 8")),
        "J": (False, ("Room 14", "Room 7")),
        "K": (False, ("Room 18", "Room 19")),
        "L": (False, ("Room 19", "Room 20")),
        "M": (False, ("Room 18", "Room 6")),
        "N": (False, ("Room 21", "Room 22")),
        "O": (False, ("Room 18", "Room 22")),
        "P": (False, ("Room 22", "End")),
        "Q": (False, ("Room 12", "Room 23")),
        "R": (False, ("Room 23", "End")),
        "S": (False, ("Room 23", "Room 24")),
        "T": (False, ("Room 24", "End")),
        "U": (False, ("Room 13", "Room 25")),
        "V": (False, ("Room 17", "Room 26"))
    }

    maze = {
        "Start": ([("Room 2", "Left", "A"), ("Room 6", "Forward", "G"), ("Room 1", "Right", "F")], False, False),
        "Room 1": ([("Room 5", "Left", "E"), ("Start", "Forward", "F")], False, False),
        "Room 2": ([("Room 3", "Forward", "B"), ("Start", "Right", "A"), ("Room 4", "Backward", "C")], False, False),
        "Room 3": ([("Room 13", "Forward", "Q"), ("Room 6", "Right", "H"), ("Room 2", "Backward", "B")], False, False),
        "Room 4": ([("Room 2", "Left", "C"), ("Room 5", "Right", "D"), ("Room 15", "Backward", "U")], False, False),
        "Room 5": ([("Room 4", "Left", "D"), ("Room 1", "Forward", "E"), ("Room 7", "Right", "J")], False, False),
        "Room 6": ([("Room 3", "Left", "H"), ("Room 8", "Right", "I"), ("Start", "Backward", "G")], False, False),
        "Room 7": ([("Room 5", "Left", "J"), ("Room 16", "Forward", "V")], False, False),
        "Room 8": ([("Room 6", "Left", "I"), ("Room 12", "Forward", "O"), ("Room 11", "Right", "M"), ("Room 9", "Backward", "K")], False, False),
        "Room 9": ([("Room 8", "Forward", "K"), ("Room 10", "Right", "L")], False, False),
        "Room 10": ([("Room 9", "Backward", "L")], False, False),
        "Room 11": ([("Room 12", "Forward", "N"), ("Room 8", "Backward", "M")], False, False),
        "Room 12": ([("End", "Left", "P"), ("Room 11", "Right", "N"), ("Room 8", "Backward", "O")], False, False),
        "Room 13": ([("End", "Forward", "R"), ("Room 14", "Right", "S"), ("Room 3", "Backward", "Q")], False, False),
        "Room 14": ([("Room 13", "Left", "S"), ("End", "Forward", "T")], False, False),
        "Room 15": ([("Room 4", "Right", "U")], False, False),
        "Room 16": ([("Room 7", "Backward", "V")], False, False),
        "End": ([("Room 13", "Left", "R"), ("Room 12", "Right", "P"), ("Room 14", "Backward", "T")], False, False)
    }

    return maze, connections



if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    intro_view = IntroView()
    window.show_view(intro_view)
    arcade.run()
