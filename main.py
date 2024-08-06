import util

import sqlite3

connection = sqlite3.connect("AhuaGallery.db")


def operationCreateItemSection():
    pass


def operationCreateItemMaterial():
    pass


def operationAddItem():
    cursor = connection.cursor()

    if util.booleanResponse("Create new section?"):
        operationCreateItemSection()

    if util.booleanResponse("Create new material?"):
        operationCreateItemMaterial()

    name = util.stringResponse("Name")
    price = util.numberResponse("Price")

    sections = cursor.execute("SELECT * FROM section").fetchall()

    i = 1
    for section in sections:
        util.printCenter(i, ". ", section[1])

    item_section = sections[int(util.numberResponse("Section", 1, len(sections))) - 1]

    materials = cursor.execute("SELECT * FROM material").fetchall()

    i = 1
    for material in materials:
        util.printCenter(i, ". ", material[1])

    item_material = materials[int(util.numberResponse("Material", 1, len(materials))) - 1]

    cursor.execute("INSERT INTO item (name, price, item_section, item_material) VALUES(?, ?, ?, ?)",
                   (name, price, item_section[0], item_material[0]))

    connection.commit()

    util.clear()
    print("\n")

    print(f"Created item with properties:"
          f"\nName: {name}"
          f"\nPrice: {price}"
          f"\nSection: {item_section[1]}"
          f"\nMaterial: {item_material[1]}")

    util.continuePrompt()


def operationRemoveItem():
    print("remove item")


def operationQuit():
    print("quit")
    connection.close()
    exit(0)


OPERATIONS = [
    ("Add item", operationAddItem),
    ("Remove item", operationRemoveItem),
    ("Create item section", operationCreateItemSection),
    ("Create item material", operationCreateItemMaterial),
    ("Quit", operationQuit)
]


def chooseOperation():
    i = 1
    for operation in OPERATIONS:
        util.printCenter(i, ". ", operation[0])
        i += 1

    response = int(util.numberResponse("Operation", 1, len(OPERATIONS)))

    OPERATIONS[response - 1][1]()


def openMainMenu():
    util.clear()
    print("\n\n")
    util.printCenter("Te Puia Museum Item Manager")
    print()

    chooseOperation()


if __name__ == '__main__':
    while True:
        openMainMenu()
