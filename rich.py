from os.path import sys
import time
# variables
inStrings = []
#functions
def readInput():
    """ Read all of the input lines into a buffer """
    print("Paste the puzzle input here and enter a blank line")
    for inputLine in sys.stdin:
        # Strip off the carriage return
        inString = inputLine.rstrip()
        if len(inString) == 0:
            break
        inStrings.append(inString)
    return
def solvePart1():
    """ Solve part 1 of the day's puzzle """
    totalFuel = 0
    for inString in inStrings:
        mass = int(inString)
        fuel = int(mass / 3) - 2
        totalFuel += fuel
    print("Total fuel : ", totalFuel)
    return
def solvePart2():
    """ Solve part 2 of the day's puzzle """
    totalFuel = 0
    for inString in inStrings:
        mass = int(inString)
        fuel = int(mass / 3) - 2
        while fuel > 0:
            totalFuel += fuel
            fuel = int(fuel / 3) - 2
    print("Total fuel : ", totalFuel)
    return
#main code
readInput()
print("Solve Part 1")
start = int(round(time.time() * 1000))
solvePart1()
end = int(round(time.time() * 1000))
print("elapsed time ", (end-start), " ms")
print("\nSolve Part 2")
start = int(round(time.time() * 1000))
solvePart2()
end = int(round(time.time() * 1000))
print("elapsed time ", (end-start), " ms")