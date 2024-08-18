"""
Program made to manage the items in Ahua Gallery automatically using a database.
Drew Bryan      30 July 2024
"""

import util

import sqlite3
import tabulate

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

    util.printCenter("Choose section:")

    i = 1
    for section in sections:
        util.printCenter(i, ". ", section[1])
        i += 1

    item_section = sections[int(util.numberResponse("Section", 1, len(sections))) - 1]

    materials = cursor.execute("SELECT * FROM material").fetchall()

    util.printCenter("Choose material:")

    i = 1
    for material in materials:
        util.printCenter(i, ". ", material[1])
        i += 1

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

    cursor = connection.cursor()

    removeID = int(util.numberResponse("Enter ID to remove"))

    util.printCenter("Remove item with values:")
    util.printCenter(cursor.execute(f"SELECT * FROM item WHERE id = {removeID}").fetchall()[0])

    if not util.booleanResponse("Remove item"):
        util.popPath()
        return

    cursor.execute(f"DELETE FROM item WHERE id = {removeID}")
    connection.commit()

    util.popPath()


def operationQuit():
    util.addToPath("Quit")

    util.clear()

    if not util.booleanResponse("Quit?"):
        util.popPath()
        return

    connection.close()
    exit(0)


def operationQueryItem():
    util.addToPath("Query item")

    util.clear()

    cursor = connection.cursor()

    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    tables.pop(0)  # Remove the first entry, 'sqlite_sequence'

    util.printCenter("Choose the table to be queried on")

    i = 1
    for table in tables:
        util.printCenter(i, ". ", table[0])
        i += 1

    selectedTable = tables[int(util.numberResponse("Table", 1, len(tables))) - 1][0]

    util.printCenter("Choose the fields to return from the query. Enter their indices in a space seperated format.")

    fields = cursor.execute(f"PRAGMA table_info('{selectedTable}')").fetchall()

    i = 1
    for field in fields:
        util.printCenter(i, ". ", field[1])
        i += 1

    selectedFieldIndices = []
    while True:
        fieldsResponse = util.stringResponse("Fields")

        for response in fieldsResponse.split(" "):
            try:
                response = int(response)
            except ValueError:
                selectedFieldIndices.clear()
                print("Enter valid response")
                continue

            if response < 1 or response > len(fields):
                selectedFieldIndices.clear()
                print("Enter valid response")
                continue
            selectedFieldIndices.append(response)
        break

    fieldHeadings = []

    resultsString = "SELECT "
    for selectedField in selectedFieldIndices:
        fieldHeadings.append(fields[selectedField - 1][1])
        resultsString += (", " if selectedField != selectedFieldIndices[0] else "") + fields[selectedField - 1][1]
    resultsString += f" FROM {selectedTable}"

    results = cursor.execute(resultsString).fetchall()

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
