class Hp_Potion():
    """
    This is an Item class for an HP potion that heals the player
    Tiffany
    """
    
    def __init__(self, character, name="HP Potion", description="Restores 20 HP.", restore=20):
        """This is the class setup"""
        
        self.name = name
        self.description = description
        self.restore = restore
        self.character = character
    
    def use(self):
        """
        This method uses the item from the player inventory if it's
        available, which means that it restores the players HP and 
        subtracts one HP potion form the players inventory
        """
        
        # Check if the player has an HP potion in their inventory
        if self.character.items["HP Potion"][1] > 0:
            # Restore player HP
            healed_hp = min(self.character.max_hp - self.character.hp, self.restore)
            self.character.hp += healed_hp
            # Decrease potion count
            item_name, amount = self.character.items["HP Potion"]
            self.character.items["HP Potion"] = (item_name, amount - 1)
            return healed_hp
        else:
            return 0