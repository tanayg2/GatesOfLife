import sys, pygame
import random
import time

SCREEN_SIZE = WIDTH, HEIGHT = 640, 480
DEAD_COLOR = 0, 0, 0
ALIVE_COLOR = 0, 255, 0
CELL_SIZE = 10

class GatesOfLife:
    def __init__(self):

        while True:
            textIn = input("Enter 'R' for randomized generation, or 'L' for logic gate simulation:\n")
            if textIn is 'R':
                self.runType = 'R'
                self.inputValue = "0"
                break
            elif textIn is 'L':
                self.runType = 'L'
                print("Program currently only simulates a NOT gate.")
                self.inputValue = input("Enter either 0 or 1 to simulate a value on the NOT gate:\n")
                '''
                print("Program limited to two inputs and 1 gate.")
                self.gateType = input("Enter gate type ('AND', 'OR', 'NOT')")
                if self.gateType is 'NOT':
                    self.input1 = input("Enter value of input")
                else:
                    self.input1 = input("Enter value of input 1:\n")
                    self.input2 = input("Enter value of input 2:\n")
                '''

                break
            else:
                print("Invalid input, try again")

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clearScreen()
        pygame.display.flip()

        self.initGrids()


    def initGrids(self):
        self.numColumns = int(WIDTH / CELL_SIZE)
        self.numRows = int(HEIGHT / CELL_SIZE)
        print("Columns: %d\nRows: %d" % (self.numColumns, self.numRows))

        def zeroGrid():
            newGrid = []
            for col in range(self.numColumns):
                rows = [0] * self.numRows
                newGrid.append(rows)
            return newGrid

        self.grids = []
        self.grids.append(zeroGrid())
        self.grids.append(zeroGrid())

        self.activeGrid = 0
        self.inactiveGrid = 1

        if self.runType is 'R':
            self.setGrid(None, 0)
        else:
            self.drawGliderGun(0, 0, 0, 0)
        self.drawGrid()


        print(self.grids[0])
        print(self.grids[1])

    def initLogicGrid(self):
        '''
        if self.gateType is 'NOT':
            pass
        '''
        pass


    def setGrid(self, value=None, grid=0):
        for col in range(self.numColumns):
            for row in range(self.numRows):
                if value is None:
                    cellValue = random.choice([0, 1])
                else:
                    cellValue = value
                self.grids[grid][col][row] = cellValue


    def drawGrid(self):
        self.clearScreen()
        for col in range(self.numColumns):
            for row in range(self.numRows):
                if self.grids[self.activeGrid][col][row] == 0:
                    color = DEAD_COLOR
                else:
                    color = ALIVE_COLOR

                pygame.draw.circle(self.screen,
                                   color,
                                   (int(col * CELL_SIZE + (CELL_SIZE / 2)),
                                   int(row * CELL_SIZE + (CELL_SIZE / 2))),
                                   int(CELL_SIZE / 2),
                                   0)
        pygame.display.flip()

    def clearScreen(self):
        self.screen.fill(DEAD_COLOR)

    def updateGeneration(self):
        for col in range(self.numColumns):
            for row in range(self.numRows):
                newCellValue = self.checkNeighbor(col, row)
                self.grids[self.inactiveGrid][col][row] = newCellValue

        newActiveGrid = self.inactiveGrid
        self.inactiveGrid = self.activeGrid
        self.activeGrid = newActiveGrid
        self.setGrid(value=0, grid=self.inactiveGrid)



    def checkNeighbor(self, col, row) -> int:
        # 1. Any live cell with two or three live neighbours survives.
        # 2. Any dead cell with three live neighbours becomes a live cell.
        # 3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.
        numAliveNeighbors = 0
        numAliveNeighbors += self.getCell(col - 1, row - 1)
        numAliveNeighbors += self.getCell(col - 1, row)
        numAliveNeighbors += self.getCell(col - 1, row + 1)
        numAliveNeighbors += self.getCell(col, row - 1)
        numAliveNeighbors += self.getCell(col, row + 1)
        numAliveNeighbors += self.getCell(col + 1, row - 1)
        numAliveNeighbors += self.getCell(col + 1, row)
        numAliveNeighbors += self.getCell(col + 1, row + 1)

        currentCellValue = self.getCell(col, row)
        newCellValue = currentCellValue


        # Rules for life and death
        if self.getCell(col, row) == 1:  # alive
            if numAliveNeighbors > 3:  # Overpopulation
                return 0
            if numAliveNeighbors < 2:  # Underpopulation
                return 0
            if numAliveNeighbors == 2 or numAliveNeighbors == 3:
                return 1
        elif self.getCell(col, row) == 0:  # dead
            if numAliveNeighbors == 3:
                return 1  # come to life

        return self.getCell(col, row)



    #Returns value of given cell, if cell doesn't exist, return 0
    def getCell(self, col, row) -> int:
        try:
            cellValue = self.grids[self.activeGrid][col][row]
        except:
            cellValue = 0
        return cellValue

    #Draws a glider, top left corner at given coordinates
    #Default is false
    # 14 x 36 rectangle I think
    #TODO: Make it point in indicated direction
    #TODO: Vary state

    def setCell(self, col, row, value):
        self.grids[self.activeGrid][col][row] = value

    def drawGliderGun(self, col, row, direction, value):
        def drawTrigger(col, row):
            # Left component
            #     xx
            #   x    x
            #  x      x
            #  x    x xx
            #  x      x
            #   x    x
            #     xx
            self.setCell(col, row + 2, 1)
            self.setCell(col, row + 3, 1)
            self.setCell(col, row + 4, 1)

            self.setCell(col + 1, row + 1, 1)
            self.setCell(col + 1, row + 5, 1)

            self.setCell(col + 2, row, 1)
            self.setCell(col + 2, row + 6, 1)

            self.setCell(col + 3, row, 1)
            self.setCell(col + 3, row + 6, 1)

            self.setCell(col + 4, row + 3, 1)

            self.setCell(col + 5, row + 1, 1)
            self.setCell(col + 5, row + 5, 1)

            self.setCell(col + 6, row + 2, 1)
            self.setCell(col + 6, row + 3, 1)
            self.setCell(col + 6, row + 4, 1)

            self.setCell(col + 7, row + 3, 1)


        def drawProducer(col, row):
            # Right Component
            # x
            # x x
            #    xx
            #    xx
            #    xx
            # x x
            # x

            self.drawStopper(col, row + 2)
            self.drawStopper(col, row + 3)

            self.setCell(col + 2, row + 1, 1)
            self.setCell(col + 2, row + 5, 1)

            self.setCell(col + 4, row, 1)
            self.setCell(col + 4, row + 1, 1)
            self.setCell(col + 4, row + 5, 1)
            self.setCell(col + 4, row + 6, 1)


        self.drawStopper(col + 1, row + 5)

        drawTrigger(col + 11, row + 3)

        drawProducer(col + 21, row + 1)

        self.drawStopper(col + 35, row + 3)

        print(self.grids[self.activeGrid])




    # 2 x 2 square
    # Verified
    def drawStopper(self, col, row):
        self.setCell(col, row, 1)
        self.setCell(col + 1, row, 1)
        self.setCell(col, row + 1, 1)
        self.setCell(col + 1, row + 1, 1)


    def drawInputGlider(self, col, row):
        if self.inputValue is "1":
            self.setCell(col, row + 1, 1)
            self.setCell(col, row + 2, 1)

            self.setCell(col + 1, row, 1)
            self.setCell(col + 1, row + 2, 1)

            self.setCell(col + 2, row + 2, 1)


    def drawEater(self, col, row):
        pass


    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print("key pressed")
                if event.unicode == 's':
                    print("Toggling pause.")
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True

                elif event.unicode == 'r':
                    #Doesn't work properly yet
                    print("Randomizing grid.")
                    self.activeGrid = 0
                    self.setGrid(None, self.activeGrid)  # randomize
                    self.setGrid(0, self.inactiveGrid)  # set to 0
                    self.drawGrid()
                elif event.unicode == 'q':
                    print("Exiting.")
                    self.game_over = True
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        self.paused = False
        i = 0
        while True:
            self.handleEvents()

            if not self.paused:
                self.updateGeneration()

                if i % 27 == 0:
                    self.drawInputGlider(55, 0)

                self.drawGrid()
                i += 1
                time.sleep(0.001)



if __name__ == '__main__':
    game = GatesOfLife()
    game.run()
