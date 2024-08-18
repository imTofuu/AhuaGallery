"""
Module made to create simple reusable functions in for the Ahua Gallery application
Drew Bryan      30 July 2024
"""

import math
from sys import argv as ARGUMENTS
import os

TERMINAL_WIDTH: int = os.get_terminal_size().columns

path = []


def addToPath(name: str):
    path.append(name)


def popPath():
    path.pop()


def removeFromPath(name: str):
    path.remove(name)


def clear():
    os.system(ARGUMENTS[1])  # Use platform specific clear string. This is passed in the run scripts
    for i in path:
        print(f"> {i} ", end="")
    print("\n")


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


def booleanResponse(message) -> bool:
    while True:
        response = input(message + " (y / n): ").lower()

        if response == "y":
            return True
        elif response == "n":
            return False


def stringResponse(message) -> str:
    return input(message + ": ")


def numberResponse(message, lbound=-math.inf, ubound=math.inf) -> float:
    while True:
        response = input(message + ": ")

        try:
            response = float(response)
        except ValueError:
            print("Enter valid response")
            continue

        if response > ubound or response < lbound:
            print("Enter valid response")
            continue

        return response


def continuePrompt():
    input("Enter to continue")
