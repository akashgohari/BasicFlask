from models.item import ItemModel

item = ItemModel.find_an_item("iPad")
print(item)