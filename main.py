"""
Program made to manage the items in Ahua Gallery automatically using a database.
Drew Bryan      30 July 2024
"""

import util

import sqlite3
import tabulate

connection = sqlite3.connect("AhuaGallery.db")


def chooseTable():
    cursor = connection.cursor()

    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    tables.pop(0)  # Remove the first entry, 'sqlite_sequence'

    i = 1
    for table in tables:
        util.printCenter(i, ". ", table[0])
        i += 1

    return tables[int(util.numberResponse("Table", 1, len(tables))) - 1][0]


def chooseFields(table):
    cursor = connection.cursor()

    fields = cursor.execute(f"PRAGMA table_info('{table}')").fetchall()

    i = 1
    for field in fields:
        util.printCenter(i, ". ", field[1])
        i += 1

    selectedFieldIndices = []
    while True:
        fieldsResponse = util.stringResponse("Fields")

        def resp(respondedFields) -> bool:
            for response in respondedFields.split(" "):
                if response == "":
                    continue
                try:
                    response = int(response)
                except ValueError:
                    selectedFieldIndices.clear()
                    print("Enter valid response")
                    return False

                if response < 1 or response > len(fields):
                    selectedFieldIndices.clear()
                    print("Enter valid response")
                    return False

                selectedFieldIndices.append(response)
            return True

        if resp(fieldsResponse):
            break

    fieldHeadings = []

    resultsString = "SELECT "
    for selectedField in selectedFieldIndices:
        fieldHeadings.append(fields[selectedField - 1][1])
        resultsString += (", " if selectedField != selectedFieldIndices[0] else "") + fields[selectedField - 1][1]
    resultsString += f" FROM {table}"

    return cursor.execute(resultsString).fetchall(), fieldHeadings


def operationCreateItemSection():
    util.addToPath("Create section")

    cursor = connection.cursor()

    util.clear()

    util.printCenter("A section is the category of item e.g. Baskets, Tools")

    name = util.stringResponse("Pick name for section")

    util.clear()

    print(f"Creating section with properties:"
          f"\nName: {name}")

    if not util.booleanResponse("Are you sure you want to create this section?"):
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

    util.printCenter("A material is what the item is made of e.g. Flax, Wood")

    name = util.stringResponse("Pick name for material")

    util.clear()

    print(f"Creating material with properties:"
          f"\nName: {name}")

    if not util.booleanResponse("Are you sure you want to create this material?"):
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
        return

    util.clear()

    while not len(cursor.execute("SELECT * FROM material").fetchall()):
        print("There are no existing materials, so you must create one.")
        util.continuePrompt()
        return

    util.clear()

    if util.booleanResponse("Create new section?"):
        operationCreateItemSection()

    if util.booleanResponse("Create new material?"):
        operationCreateItemMaterial()

    name = util.stringResponse("Pick name for item")
    price = util.numberResponse("Pick price for item")

    sections = cursor.execute("SELECT * FROM section").fetchall()

    util.printCenter("Sections:")

    i = 1
    for section in sections:
        util.printCenter(i, ". ", section[1])
        i += 1

    chosenSectionIndex = int(util.numberResponse("Pick section (type number)", 1, len(sections))) - 1
    item_section = sections[chosenSectionIndex]

    materials = cursor.execute("SELECT * FROM material").fetchall()

    util.printCenter("Materials:")

    i = 1
    for material in materials:
        util.printCenter(i, ". ", material[1])
        i += 1

    chosenMaterialIndex = int(util.numberResponse("Pick material (type number)", 1, len(materials))) - 1
    item_material = materials[chosenMaterialIndex]

    util.clear()

    print(f"Creating item with properties:"
          f"\nName: {name}"
          f"\nPrice: {price}"
          f"\nSection: {item_section[1]}"
          f"\nMaterial: {item_material[1]}")

    if not util.booleanResponse("Are you sure you want to create this item?"):
        util.popPath()
        return

    cursor.execute("INSERT INTO item (name, price, item_section, item_material) VALUES(?, ?, ?, ?)",
                   (name, price, item_section[0], item_material[0]))
    connection.commit()

    util.popPath()


def operationRemoveItem():
    util.addToPath("Remove item")

    util.clear()

    cursor = connection.cursor()

    util.printCenter("Items:")

    items = cursor.execute(f"""
        SELECT item.id, item.name, item.price, section.section_name, material.material_name
        FROM item
        INNER JOIN main.section section ON section.section_id = item.item_section
        INNER JOIN main.material material on material.material_id = item.item_material
        """).fetchall()

    print(tabulate.tabulate(items, ["ID", "Name", "Price", "Section", "Material"]))

    item = None
    removeID = None
    while True:
        try:
            removeID = int(util.numberResponse("Type ID to remove"))
            item = [cursor.execute(f"""
                    SELECT item.name, item.price, section.section_name, material.material_name
                    FROM item
                    INNER JOIN main.section section ON section.section_id = item.item_section
                    INNER JOIN main.material material on material.material_id = item.item_material
                    WHERE item.id = {removeID}""").fetchall()[0]]
            break
        except IndexError:
            print("Input a valid ID")

    util.printCenter("Removing item with values:")
    print(tabulate.tabulate(item, ["Name", "Price", "Section", "Material"]))

    if not util.booleanResponse("Are you sure you want to remove this item?"):
        util.popPath()
        return

    cursor.execute(f"DELETE FROM item WHERE id = {removeID}")
    connection.commit()

    util.popPath()


def operationQuit():
    util.addToPath("Quit")

    util.clear()

    if not util.booleanResponse("Are you sure you want to quit?"):
        util.popPath()
        return

    connection.close()
    exit(0)


def operationQueryItem():
    util.addToPath("Query item")

    util.clear()

    util.printCenter("Choose the table to be queried on")

    selectedTable = chooseTable()

    util.printCenter("Choose the fields to return from the query. Enter their indices in a space seperated format")

    results, fieldHeadings = chooseFields(selectedTable)

    util.addToPath("Query results")
    util.clear()

    print(tabulate.tabulate(results, fieldHeadings))

    util.continuePrompt()

    util.popPath()

    util.popPath()


OPERATIONS = [
    ("Add item", operationAddItem),
    ("Query item(s)", operationQueryItem),
    ("Remove item", operationRemoveItem),
    ("Create item section", operationCreateItemSection),
    ("Create item material", operationCreateItemMaterial),
    ("Quit", operationQuit)
]


def chooseOperation():
    util.printCenter("Enter the number of the operation you would like to perform")

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
