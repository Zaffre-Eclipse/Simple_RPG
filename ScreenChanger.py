import arcade

class ScreenChanger:
    """
    This class handles the screen transitions
    It controls tutorials, menus and the shop
    Isaac
    """
    
    @staticmethod
    def draw_button(cx, cy, w, h, text="", highlighted=False, 
                    fill_color=arcade.color.BLACK, outline_color=arcade.color.RED, font_size=16):
        """
        Draw a rectangular button with  text.
        
        Args:
            cx, cy: center coordinates of the button
            w, h: width and height
            
            text: label text
            
            highlighted: if True, outline is yellow instead of default
            
            fill_color: button fill color
            
            outline_color: outline color when not highlighted
            
            font_size: size of the text
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


    def draw_game_over(self, window, game_over_options, selected_index):
        """
        Setup the Game Over screen
        
        Args:
            window: The game window
            
            game_over_options: The button options
            
            selected_index: Which button is currently selected
        """

        screen_width, screen_height = window.get_size()

        # Full black overlay
        arcade.draw_lrbt_rectangle_filled(
            0, screen_width, 0, screen_height,
            arcade.color.BLACK
        )

        # "GAME OVER" text
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

        # Button panel background
        panel_height = 80
        panel_width = 400
        panel_y = panel_height / 2 + 30

        self.draw_button(
            screen_width / 2, panel_y,
            panel_width, panel_height,
            fill_color=arcade.color.BLACK,
            outline_color=arcade.color.RED
        )

        # Draw the Restart/Quit buttons inside the panel
        spacing = 20
        button_width = 150
        button_height = 50

        total_width = len(game_over_options) * button_width + (len(game_over_options)-1) * spacing
        start_x = (screen_width - total_width) / 2

        for i, option in enumerate(game_over_options):
            cx = start_x + i * (button_width + spacing) + button_width / 2
            highlighted = (i == selected_index)
            self.draw_button(cx, panel_y, button_width, button_height, option, highlighted=highlighted)


    def draw_battle_tutorial_popup(self, window):
        """
        Draw the basic battle tutorial popup
        
        Args:
            window: The game window
        """
        
        cx = window.width / 2
        cy = window.height / 2
        w = 500
        h = 300

        # Main popup box
        self.draw_button(cx, cy, w, h, fill_color=arcade.color.BLACK, outline_color=arcade.color.RED)

        tutorial_lines = [
            "LOOKS LIKE THIS IS YOUR FIRST FIGHT",
            "DURING BATTLE YOU WILL HAVE THREE OPTIONS:",
            "YOU CAN ATTACK, USE ITEMS, OR USE A SPECIAL MOVE",
            "IF YOU CHOOSE TO ATTACK A CIRCLE WILL APPEAR",
            "IT WILL BEGIN TO ROTATE, PRESS Z WHEN THE POINTER",
            "AT THE TOP OF THE CIRCLE IS IN THE RED ZONE",
            "THIS WILL ALLOW YOU TO ATTACK AGAIN",
            "THE MORE YOU ATTACK THE FASTER IT WILL SPIN",
        ]

        for i, line in enumerate(tutorial_lines):
            arcade.draw_text(
                line,
                cx, cy + 100 - i * 30,
                arcade.color.RED,
                14,
                anchor_x="center"
            )

        # Bottom command bar
        bar_h = 80
        bar_margin = 20
        bar_cy = cy - h / 2 - bar_h / 2 - bar_margin
        self.draw_button(cx, bar_cy, w, bar_h, fill_color=arcade.color.BLACK, outline_color=arcade.color.RED)

        # OK button
        box_w = 200
        box_h = 60
        self.draw_button(cx, bar_cy, box_w, box_h, "OK", highlighted=True)


    def draw_boss_battle_tutorial_popup(self, window):
        """
        Draw the boss battle tutorial popup
        
        Args:
            window: The game window
        """
        
        cx = window.width / 2
        cy = window.height / 2
        w = 600
        h = 300

        self.draw_button(cx, cy, w, h, fill_color=arcade.color.BLACK, outline_color=arcade.color.RED)

        tutorial_lines = [
            "LOOKS LIKE THIS IS YOUR FIRST BOSS FIGHT",
            "UNLIKE NORMAL ENEMIES, BOSSES WILL ATTACK 4 TIMES",
            "WHEN IT ATTACKS A BAR, A POINTER AND AN ARROW WILL APPEAR",
            "PRESS THE SAME ARROW TO STOP THE POINTER, THE ZONE IT STOPS IN",
            "WILL DETERMINE HOW MUCH DAMAGE YOU WILL TAKE FOR THAT ATTACK:",
            "GREEN: 25%, YELLOW: 50%, ORANGE: 75%, RED: 100%",
            "PRESSING THE WRONG ARROW WILL MAKE YOU TAKE 100%"
        ]

        for i, line in enumerate(tutorial_lines):
            arcade.draw_text(
                line,
                cx, cy + 90 - i * 30,
                arcade.color.RED,
                14,
                anchor_x="center"
            )

        # Command bar
        bar_h = 80
        bar_margin = 20
        bar_cy = cy - h / 2 - bar_h / 2 - bar_margin
        self.draw_button(cx, bar_cy, w, bar_h, fill_color=arcade.color.BLACK, outline_color=arcade.color.RED)

        # OK button
        box_w = 200
        box_h = 60
        self.draw_button(cx, bar_cy, box_w, box_h, "OK", highlighted=True)


    def draw_shop_tutorial_popup(self, window):
        """
        Draw the shop tutorial popup
        
        Args:
            window: The game window
        """
        
        cx = window.width / 2
        cy = window.height / 2
        w = 500
        h = 300

        # Main popup box
        self.draw_button(cx, cy, w, h, fill_color=arcade.color.BLACK, outline_color=arcade.color.RED)

        tutorial_lines = [
            "WE'VE NOTICED YOUR HARD WORK PAWN,",
            "AND HARD WORK DESERVES A REWARD!",
            "USE THE TOUCH SCREEN ON THE WALL",
            "AS WELL AS THE GOLD YOU'VE EARNED",
            "TO BUY USEFUL ITEMS OR UPGRADES!",
            "WE'LL SEND THEM DOWN THE PIPE FOR YOU!"
        ]

        for i, line in enumerate(tutorial_lines):
            arcade.draw_text(
                line,
                cx,
                cy + 80 - i * 30,
                arcade.color.RED,
                16,
                anchor_x="center"
            )

        # Bottom bar
        bar_h = 80
        bar_margin = 20
        bar_cy = cy - h / 2 - bar_h / 2 - bar_margin

        self.draw_button(cx, bar_cy, w, bar_h, fill_color=arcade.color.BLACK, outline_color=arcade.color.RED)

        # OK button
        box_w = 200
        box_h = 60
        self.draw_button(cx, bar_cy, box_w, box_h, "OK", highlighted=True)
        

    def draw_status_popup(self, window, character, popup_options, menu_index):
        """
        Draws the status popup with stats and buttons
        
        Args:
            window: The game window
            
            character: The current playe instance
            
            popup_options: The button options
            
            menu_index: The currenty selected button
        """
        
        cx = window.width / 2
        cy = window.height / 2 + 40  # bump stats box up slightly
        w = 400
        h = 220

        # Main stats box
        self.draw_button(cx, cy, w, h,
                    fill_color=arcade.color.BLACK,
                    outline_color=arcade.color.RED)

        # Stats text
        stats_lines = [
            f"Name: {character.name}",
            f"Status: {character.title}",
            f"HP: {character.hp}/{character.max_hp}",
            f"MP: {character.mp}/{character.max_mp}",
            f"ATK: {character.atk} | DEF: {character.defense} | SPD: {character.spd}",
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

        # Command bar under stats
        bar_w = 420
        bar_h = 100
        bar_cy = cy - h / 2 - bar_h / 2 - 10

        self.draw_button(cx, bar_cy, bar_w, bar_h,
                    fill_color=arcade.color.BLACK,
                    outline_color=arcade.color.RED)

        # Row of buttons
        num_buttons = len(popup_options)
        box_w = 100
        box_h = 60
        spacing = 20

        total_width = num_buttons * box_w + (num_buttons - 1) * spacing
        start_x = cx - total_width / 2
        button_y = bar_cy

        for i, option in enumerate(popup_options):
            cx_button = start_x + i * (box_w + spacing) + box_w / 2
            self.draw_button(
                cx_button,
                button_y,
                box_w,
                box_h,
                option,
                highlighted=(i == menu_index)
            )
            
    
    def draw_equip_popup(self, window, character, popup_options, menu_index):
        """
        Draws the equipment popup with info and buttons
        
        Args:
            window: The game window
            
            character: The current playe instance
            
            popup_options: The button options
            
            menu_index: The currenty selected button
        """

        cx = window.width / 2
        cy = window.height / 2
        w = 400
        h = 220

        # Outer box using shared button style
        self.draw_button(
            cx, cy, w, h,
            fill_color=arcade.color.BLACK,
            outline_color=arcade.color.RED
        )

        # Equipment text
        equip_lines = [
            f"{character.equipment['Armor'][0]}: +{character.equipment['Armor'][1]} DEF",
            f"{character.equipment['Weapon'][0]}: +{character.equipment['Weapon'][1]} ATK",
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

        # Buttons
        num_buttons = len(popup_options)
        if num_buttons > 0:

            # Button sizing
            box_w = 200 if num_buttons == 1 else 100
            box_h = 60
            spacing = 20 if num_buttons > 1 else 0

            total_width = num_buttons * box_w + (num_buttons - 1) * spacing
            start_x = cx - total_width / 2
            button_y = cy - h / 2 + 50

            # Draw each button
            for i, option in enumerate(popup_options):
                cx_button = start_x + i * (box_w + spacing) + box_w / 2
                self.draw_button(
                    cx_button,
                    button_y,
                    box_w,
                    box_h,
                    option,
                    highlighted=(i == menu_index)
                )
                
    
    def draw_item_popup(self, window, character, popup_options, menu_index):
        """
        Draws the item popup with inventory and buttons
        
        Args:
            window: The game window
            
            character: The current playe instance
            
            popup_options: The button options
            
            menu_index: The currenty selected button
        """

        cx = window.width / 2
        cy = window.height / 2
        w = 400
        h = 220

        # Outer box using your shared button style
        self.draw_button(
            cx, cy, w, h,
            fill_color=arcade.color.BLACK,
            outline_color=arcade.color.RED
        )

        # Item counts
        item_lines = [
            f"{character.items['HP Potion'][0]}: {character.items['HP Potion'][1]}",
            f"{character.items['MP Potion'][0]}: {character.items['MP Potion'][1]}",
            f"{character.items['Gold'][0]}: {character.items['Gold'][1]}",
        ]

        for i, line in enumerate(item_lines):
            arcade.draw_text(
                line,
                cx,
                cy + h / 2 - 40 - i * 30,
                arcade.color.WHITE,
                16,
                anchor_x="center"
            )

        # Buttons
        num_buttons = len(popup_options)
        if num_buttons > 0:
            box_w = 200 if num_buttons == 1 else 100
            box_h = 60
            spacing = 20 if num_buttons > 1 else 0

            total_width = num_buttons * box_w + (num_buttons - 1) * spacing
            start_x = cx - total_width / 2
            button_y = cy - h / 2 + 50

            for i, option in enumerate(popup_options):
                cx_button = start_x + i * (box_w + spacing) + box_w / 2
                self.draw_button(
                    cx_button,
                    button_y,
                    box_w,
                    box_h,
                    option,
                    highlighted=(i == menu_index)
                )
    
    
    def draw_loot_popup(self, window, loot_popup_state, loot_popup_text):
        """
        Draw a textbox at the bottom of the screen
        
        Args:
            window: The game window
                        
            loot_popup_state: What kind of textbox this is,
                              looting, battling, descriptions, etc.
            
            loot_popup_text: The text for the text box
        """
        
        if loot_popup_state != "loot":
            return

        cx = window.width / 2
        cy = 130

        self.draw_button(
            cx,
            cy,
            400,
            50,
            loot_popup_text
        )
        
        
    def draw_shop_popup(self, window, Shop_items, shop_menu_index, character):
        """
        Draw the shop menu
        
        Args:
            window: The game window
                        
            shop_items: The items abvailable for purchase
            
            shop_menu_index: Which item is currently selected
            
            character: The current player instance
        """
        
        cx = window.width / 2
        cy = window.height / 2
        w = 500
        h = 300

        top_panel_h = h - 80
        bottom_panel_h = 80
        spacing = 20

        # Top panel
        top_panel_cy = cy + 40
        self.draw_button(cx, top_panel_cy, w, top_panel_h, fill_color=arcade.color.BLACK, outline_color=arcade.color.RED)

        # Bottom panel
        bottom_panel_cy = top_panel_cy - top_panel_h / 2 - bottom_panel_h / 2 - spacing
        self.draw_button(cx, bottom_panel_cy, w, bottom_panel_h, fill_color=arcade.color.BLACK, outline_color=arcade.color.RED)

        # Item list
        num_items = len(Shop_items)
        item_spacing = 30
        total_items_height = (num_items - 1) * item_spacing
        start_y = top_panel_cy + total_items_height / 2

        # Determine item cost
        for i, (key, value) in enumerate(Shop_items.items()):
            if key == "Exit":
                text = "Exit"
            elif isinstance(value, tuple):
                name = value[0]
                if isinstance(value[2], (int, float)):
                    # weapon/armor cost
                    cost = value[2]
                else:
                    # potion cost
                    cost = value[1]
                text = f"{name}: {cost} Gold"
            else:
                text = str(value)

            color = arcade.color.YELLOW if i == shop_menu_index else arcade.color.WHITE

            arcade.draw_text(text, cx, start_y - i * item_spacing, color, 16, anchor_x="center")

        # Gold display
        gold_amount = character.items["Gold"][1]
        arcade.draw_text(
            f"Gold: {gold_amount}",
            cx,
            start_y - num_items * item_spacing,
            arcade.color.WHITE,
            16,
            anchor_x="center"
        )

        # Description panel
        selected_key = list(Shop_items.keys())[shop_menu_index]
        desc_text = ""

        if selected_key == "Exit":
            desc_text = "Exit the shop."
        else:
            item = Shop_items[selected_key]
            if isinstance(item, tuple):
                desc_text = item[-1]

        arcade.draw_text(
            desc_text,
            cx,
            bottom_panel_cy,
            arcade.color.WHITE,
            16,
            anchor_x="center",
            anchor_y="center",
        )
        
        
    @staticmethod
    def draw_special_popup(window, character, special_menu_options, special_menu_index):
        """
        Draw the special move menu
        
        Args:
            window: The game window
            
            character: The current player instance
                        
            special_menu_options: The special move choices
            
            special_menu_index: Which special move is currently selected
        """
        
        cx = window.width / 2
        cy = window.height / 2
        w = 500
        h = 300

        top_panel_h = h - 80
        bottom_panel_h = 80

        # Selection panel
        top_panel_cy = cy + (bottom_panel_h / 2)
        arcade.draw_lrbt_rectangle_filled(
            cx - w/2, cx + w/2,
            top_panel_cy - top_panel_h/2, top_panel_cy + top_panel_h/2,
            arcade.color.BLACK
        )
        arcade.draw_lrbt_rectangle_outline(
            cx - w/2, cx + w/2,
            top_panel_cy - top_panel_h/2, top_panel_cy + top_panel_h/2,
            arcade.color.RED, 3
        )

        # Description panel
        bottom_panel_cy = cy - h/2 + bottom_panel_h/2
        bottom_bottom = bottom_panel_cy - bottom_panel_h/2 - 20
        bottom_top = bottom_panel_cy + bottom_panel_h/2 - 20
        bottom_center = (bottom_bottom + bottom_top) / 2

        arcade.draw_lrbt_rectangle_filled(
            cx - w/2, cx + w/2,
            bottom_bottom, bottom_top,
            arcade.color.BLACK
        )
        arcade.draw_lrbt_rectangle_outline(
            cx - w/2, cx + w/2,
            bottom_bottom, bottom_top,
            arcade.color.RED, 3
        )

        # List special moves
        options = list(special_menu_options)
        option_spacing = 30
        start_y = top_panel_cy + ((len(options)-1)*option_spacing)/2

        for i, key in enumerate(options):
            if key == "Exit":
                text = "Exit"
            else:
                name, desc, mp_cost = character.special[key]
                text = f"{name}: {mp_cost} MP"

            color = arcade.color.YELLOW if i == special_menu_index else arcade.color.WHITE
            arcade.draw_text(text, cx, start_y - i*option_spacing, color, 16, anchor_x="center")

        # Description bar
        selected_key = options[special_menu_index]

        if selected_key == "Exit":
            desc_text = "Return to battle menu."
        else:
            desc_text = character.special[selected_key][1]  # skill description

        arcade.draw_text(
            desc_text,
            cx,
            bottom_center,
            arcade.color.WHITE,
            16,
            anchor_x="center",
            anchor_y="center"
        )
    

    def draw_win_screen(self, window, options, selected_index):
        """
        Draw the Win screen
        
        Args:
            window: The game window
                                    
            options: The button choices
            
            selected_index: Which button is currently selected
        """
        
        screen_w, screen_h = window.get_size()

        # Background Black
        arcade.draw_lrbt_rectangle_filled(0, screen_w, 0, screen_h, arcade.color.BLACK)

        # Win text
        arcade.draw_text(
            "YOU WIN!", 
            screen_w/2, screen_h/2 + 120, 
            arcade.color.RED, 
            50, anchor_x="center", bold=True
        )

        # Decorative underline
        arcade.draw_text(
            "────────────",
            screen_w/2, screen_h/2 + 90,
            arcade.color.RED,
            40, anchor_x="center"
        )

        # Option buttons
        button_width = 200
        button_height = 50
        spacing = 40

        total_width = len(options) * button_width + (len(options)-1)*spacing
        start_x = (screen_w - total_width) / 2

        for i, option in enumerate(options):
            x = start_x + i*(button_width+spacing) + button_width/2
            y = screen_h/2 - 50

            highlight = (i == selected_index)
            outline = arcade.color.YELLOW if highlight else arcade.color.RED

            # Draw button
            arcade.draw_lrbt_rectangle_filled(x-button_width/2, x+button_width/2,
                                            y-button_height/2, y+button_height/2,
                                            arcade.color.BLACK)
            arcade.draw_lrbt_rectangle_outline(x-button_width/2, x+button_width/2,
                                            y-button_height/2, y+button_height/2,
                                            outline, 3)

            arcade.draw_text(option, x, y-10, arcade.color.WHITE, 20, anchor_x="center")
    
    
    def draw_end_popup(self, window, options, selected_index):
        """
        Draw boss battle confirmation pupup
        
        Args:
            window: The game window
                                    
            options: The button choices
            
            selected_index: Which button is currently selected
        """
        
        screen_w, screen_h = window.get_size()

        # Popup panel dimensions
        w, h = 600, 200
        cx, cy = screen_w/2, screen_h/2

        # Panel background
        arcade.draw_lrbt_rectangle_filled(cx-w/2, cx+w/2, cy-h/2, cy+h/2, arcade.color.BLACK)
        arcade.draw_lrbt_rectangle_outline(cx-w/2, cx+w/2, cy-h/2, cy+h/2, arcade.color.RED, 3)

        # Title text
        arcade.draw_text(
            "Do you want to face the final boss and exit the dungeon?",
            cx, cy+45,
            arcade.color.WHITE,
            18, anchor_x="center", align="center"
        )

        # Two button layout
        button_w, button_h = 120, 50
        spacing = 160
        y = cy - 40

        for i, option in enumerate(options):
            x = cx + (i - 0.5) * spacing
            self.draw_button(
                x, y,
                button_w, button_h,
                text=option,
                highlighted=(i == selected_index),
                fill_color=arcade.color.BLACK
            )