from __future__ import print_function

class DrawingTool:

  # Initialize DrawingTool object with input and output files and read instruction file
  # @param inputFile file from which to read instructions
  # @param outputFile file to which to write output
  def __init__(self, inputFile, outputFile):
    self.outputFile = outputFile
    self.canvas = None
    self.instructions = self.readInput(inputFile)
    self.insSuccess = True

  # Read instructions from input file
  # @param inputFile file from which to read input
  def readInput(self, inputFile):
    with open(inputFile) as f:
      return [s.split() for s in f.readlines()]

  # Main function. Runs instructions and prints output to output file
  def draw(self):
    # Open output file for writing
    with open(self.outputFile, 'w+') as f:

      # For each instruction, parse and execute
      for ins in self.instructions:
        self.executeInstruction(ins)

        # Print board if instruction was successful
        if self.insSuccess and self.canvas:
          print(self.printBoard(), file=f)
        self.insSuccess = True

  # Constructs string representation of the canvas
  # @return sting representation of canvas
  def printBoard(self):
    board = " "
    for i in range(self.xDim):
      board = board + "-"
    board = board + "\n"
    for row in self.canvas:
        board = board + "|"
        for c in row:
          c = ' ' if c == None else c
          board = board + c
        board = board + "|\n"
    board = board + ' '
    for i in range(self.xDim):
      board = board + "-"
    return board

  # Executes the given instruction
  # @param instruction
  # @note Will ignore invalid instructions
  def executeInstruction(self, instruction):
    ins = instruction.pop(0)

    # Initialize canvas instruction
    if ins == 'C':
      if not len(instruction) == 2:
        self.insSuccess = False
        return
      instruction = [int(i) for i in instruction]
      self.initCanvas(*instruction)

    # Draw line instruction
    elif ins == 'L':
      if not len(instruction) == 4 or self.canvas == None:
        self.insSuccess = False
        return
      instruction = [int(i) - 1 for i in instruction]

      # Vertical line
      if instruction[0] == instruction[2]:
        self.drawVertLine(instruction[0], instruction[1], instruction[3])

      # Horizontal line
      elif instruction[1] == instruction[3]:
        self.drawHorizLine(instruction[1], instruction[0], instruction[2])

    # Draw rectangle instruction
    elif ins == 'R':
      if not len(instruction) == 4 or self.canvas == None:
        self.insSuccess = False
        return
      instruction = [int(i) - 1 for i in instruction]
      self.drawRectangle(*instruction)

    # Bucket fill instruction
    elif ins == 'B':
      if not len(instruction) == 3 or self.canvas == None:
        self.insSuccess = False
        return
      instruction[0] = int(instruction[0]) - 1
      instruction[1] = int(instruction[1]) - 1
      self.bucketFill(*instruction)

  # Initializes the canvas. Called on 'C' instruction
  # @param x canvas width
  # @param y canvas height
  def initCanvas(self, x, y):
    if not self.canvas == None:
      self.insSuccess = False
      return
    self.xDim = x
    self.yDim = y
    self.canvas = [[None for i in range(x)] for j in range(y)]

  # Draws horizontal line on y=y from x=a to x=b
  # @param y constant vertical position
  # @param a beginning horizontal position
  # @param b ending horizontal position
  def drawHorizLine(self, y, a, b):
    if not self.ensureBounds(a, y) or not self.ensureBounds(b, y):
      self.insSuccess = False
      return

    for i in range(a, b+1):
      self.canvas[y][i] = 'x'

  # Draws horizontal line on x=x from y=a to y=b
  # @param x constant horizontal position
  # @param a beginning vertical position
  # @param b ending vertical position
  def drawVertLine(self, x, a, b):
    if not self.ensureBounds(x, a) or not self.ensureBounds(x, b):
      self.insSuccess = False
      return
    for i in range(a, b+1):
      self.canvas[i][x] = 'x'

  # Draws hollow rectangle with corners (x1, y1), (x1, y2), (x2, y1), and (x2, y2)
  # @param x1 x-coordinate of upper left corner
  # @param y1 y-coordinate of upper left corner
  # @param x2 x-coordinate of lower right corner
  # @param y2 y-coordinate of lower right corner
  def drawRectangle(self, x1, y1, x2, y2):
    if not (self.ensureBounds(x1, y1) and self.ensureBounds(x2, y2)):
      self.insSuccess = False
      return
    self.drawHorizLine(y1, x1, x2)
    self.drawHorizLine(y2, x1, x2)
    self.drawVertLine(x1, y1, y2)
    self.drawVertLine(x2, y1, y2)

  # Fills area connexted to (x, y) with color c
  # @param x x-coordinate of starting point
  # @param y y-coordinate of starting point
  # @param c 'color' with which to fill area
  def bucketFill(self, x, y, c):
    if not self.ensureBounds(x, y):
      self.insSuccess = False
      return
    self.flood([], x, y, c)

  # Floods area directly connected to (x, y) and calls itself recursively to flood the canvas
  def flood(self, seen, x, y, c):
    # Break conditions
    if not self.ensureBounds(x, y) or self.canvas[y][x] == 'x' or (x, y) in seen:
      return

    # Add current coordinate to list of seen coordinates
    seen.append((x, y))

    # Color coordinate with new color
    self.canvas[y][x] = c

    # Flood around all adjacent coordinates
    for i in range(x-1, x+2):
      for j in range(y-1, y+2):
        self.flood(seen, i, j, c)

  # Utility function to ensure coordinate is in bounds of canvas
  # @param x x-coordinate of point
  # @param y y-coordinate of point
  def ensureBounds(self, x, y):
    return x >= 0 and y >= 0 and x < self.xDim and y < self.yDim

# Construct object and run main function
if __name__ == '__main__':
  import sys

  # Check to make sure arguments are valid
  if len(sys.argv) != 3:
    print("Usage: python DrawingTool.py <path to input file> <path to output file>")
    exit()

  # Assign cmd line args to sanely named variables
  inputFile = sys.argv[1]
  outputFile = sys.argv[2]

  # Instantiate DrawingTool and run main draw function
  draw = DrawingTool(inputFile, outputFile)
  draw.draw()
