class Mp_Potion():
    """
    This is an Item class for an MP potion that heals the player
    Anner
    """
    def __init__(self, character, name="MP Potion", description="Restores 20 MP.", restore=20):
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
        
        # Check if the player has an MP potion in their inventory
        if self.character.items["MP Potion"][1] > 0:
            # Restore player MP
            healed_mp = min(self.character.max_mp - self.character.mp, self.restore)
            self.character.mp += healed_mp
            # Decrease potion count
            item_name, amount = self.character.items["MP Potion"]
            self.character.items["MP Potion"] = (item_name, amount - 1)
            return healed_mp
        else:
            return 0