class Inventory:
    """
    Items are stored in the inventory in a dictionary.
        Key: Item Name
        Value: A list of item instances.
    """

    def __init__(self):
        self.items = dict()

    def add_item(self, item):
        try:
            # Check to see if the user has any existing instances of this item in their inventory dict.
            # If so, append this instance of the item to the inventory item list keyed to its name.
            if self.items[item.name]:
                self.items[item.name].append(item)
        except KeyError:
            # A KeyError means that the user's inventory dict does not have an entry for this item name. Create a key
            # for the item name and set up a list that includes the instance of this item that was passed to the method.
            self.items[item.name] = [item]

    def remove_item(self, item):
        try:
            # Check to see if this specific instance of the item object is currently in the inventory dictionary.
            # If it is, remove that instance from the item list.
            # If this is the last instance of the item in the inventory, delete the item key from the inventory dict.
            if self.items[item.name]:
                self.items[item.name].remove(item)
                if len(self.items[item.name]) < 1:
                    del self.items[item.name]
        except KeyError:
            # A KeyError means that a player does not have an instance of this object in their inventory (or it somehow
            # got keyed incorrectly, but that would be unlikely - famous last words).
            return f"You do not have that item."

    def __str__(self):
        inventory = f"Your Inventory:\n"
        inventory += f"----------------------------\n"
        for item, i in self.items.items():
            num_of_items = len(i)
            if num_of_items > 1:
                inventory += f"{item} ({num_of_items}x)\n"
            else:
                inventory += f"{item}\n"
        return inventory
