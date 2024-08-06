from sys import argv as ARGUMENTS
import os

TERMINAL_WIDTH: int = os.get_terminal_size().columns


# -- UTIL ------------------------------------------------------------------------------------------->


def clear():
    os.system(ARGUMENTS[1])  # Use platform specific clear string


def getHalfTerminalOffset(length: int) -> str:
    halfTerminal: int = int(TERMINAL_WIDTH / 2)
    halfString: int = int(length / 2)

    return " " * (halfTerminal - halfString)


def printCenter(*messages):
    stringLength: int = 0
    for message in messages:
        stringLength += len(str(message))

    print(getHalfTerminalOffset(stringLength) + str(messages[0]), end="")
    for message in messages:
        if message == messages[0]:
            continue
        print(message, end="")
    print()


# -- USAGE ------------------------------------------------------------------------------------------->


OPERATIONS = [
    "Add item",
    "Remove item"
]


def chooseOperation():
    i = 1
    for operation in OPERATIONS:
        printCenter(i, ". ", operation)
        i += 1


def openMainMenu():
    clear()
    print("\n\n")
    printCenter("Te Puia Museum Item Manager")
    print("\n")

    chooseOperation()


if __name__ == '__main__':
    openMainMenu()
