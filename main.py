import util

import sqlite3

connection = sqlite3.connect("AhuaGallery.db")


def operationCreateItemSection():
    util.addToPath("Create section")

    cursor = connection.cursor()

    util.clear()

    name = util.stringResponse("Name")

    util.clear()

    print(f"Creating section with properties:"
          f"\nName: {name}")

    if not util.booleanResponse("Create section?"):
        util.popPath()
        util.clear()
        return

    cursor.execute(f"INSERT INTO section (section_name) VALUES('{name}')")
    connection.commit()

    util.popPath()
    util.clear()


def operationCreateItemMaterial():
    util.addToPath("Create material")

    cursor = connection.cursor()

    util.clear()

    name = util.stringResponse("Name")

    util.clear()

    print(f"Creating material with properties:"
          f"\nName: {name}")

    if not util.booleanResponse("Create material?"):
        util.popPath()
        util.clear()
        return

    cursor.execute(f"INSERT INTO material (material_name) VALUES('{name}')")
    connection.commit()

    util.popPath()
    util.clear()


def operationAddItem():
    util.addToPath("Add item")

    cursor = connection.cursor()

    util.clear()

    while not len(cursor.execute("SELECT * FROM section").fetchall()):
        print("There are no existing sections, so you must create one.")
        util.continuePrompt()
        operationCreateItemSection()

    util.clear()

    while not len(cursor.execute("SELECT * FROM material").fetchall()):
        print("There are no existing materials, so you must create one.")
        util.continuePrompt()
        operationCreateItemMaterial()

    util.clear()

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

    util.clear()

    print(f"Creating item with properties:"
          f"\nName: {name}"
          f"\nPrice: {price}"
          f"\nSection: {item_section[1]}"
          f"\nMaterial: {item_material[1]}")

    if not util.booleanResponse("Create item?"):
        util.popPath()
        return

    cursor.execute("INSERT INTO item (name, price, item_section, item_material) VALUES(?, ?, ?, ?)",
                   (name, price, item_section[0], item_material[0]))
    connection.commit()

    util.popPath()


def operationRemoveItem():
    util.addToPath("Remove item")

    util.clear()

    print("remove item")

    util.popPath()


def operationQuit():
    util.addToPath("Quit")

    util.clear()

    if not util.booleanResponse("Quit?"):
        util.popPath()
        return

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
    util.addToPath("Main Menu")

    util.clear()
    util.printCenter("Te Puia Museum Item Manager")
    print()

    chooseOperation()

    util.popPath()


if __name__ == '__main__':
    while True:
        openMainMenu()
