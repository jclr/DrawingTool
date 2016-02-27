from DrawingTool import DrawingTool
import sys

if not len(sys.argv) == 2:
  print "Usage: testDrawingTool.py <path to input file>"
  exit()

draw = DrawingTool(sys.argv[1], 'pass')

# Test readInput
expected = [
  ['C', '20', '4'],
  ['L', '1', '2', '6', '2'],
  ['L','6','3','6', '4'],
  ['R','16','1','20','3'],
  ['B','10','3','o']]
actual = draw.readInput('input/testIn.txt')
assert(actual == expected)

# Test initCanvas
expected = [
  [None, None, None, None],
  [None, None, None, None],
  [None, None, None, None],
  [None, None, None, None]]
draw.initCanvas(4, 4)
assert(draw.xDim == 4)
assert(draw.yDim == 4)
assert(draw.canvas == expected)

# Test printBoard (ensure borders are being drawn correctly)
expected = " ----\n|    |\n|    |\n|    |\n|    |\n ----"
actual = draw.printBoard()
print(actual)
assert(actual == expected)

# Test drawHorizLine
expected = [
  ['x', 'x', 'x', 'x'],
  [None, None, None, None],
  [None, None, None, None],
  [None, None, None, None]]
draw.drawHorizLine(0, 0, 3)
print(draw.printBoard())
assert(draw.canvas == expected)

# Test drawVertLine
draw = DrawingTool('input/testIn.txt', 'output/testOut.txt')
draw.initCanvas(4, 4)
expected = [
  ['x', None, None, None],
  ['x', None, None, None],
  ['x', None, None, None],
  ['x', None, None, None]]
draw.drawVertLine(0, 0, 3)
print(draw.printBoard())
assert(draw.canvas == expected)

# Test drawRectangle
draw = DrawingTool('input/testIn.txt', 'output/testOut.txt')
draw.initCanvas(4, 4)
expected = [
  ['x', 'x', 'x', None],
  ['x', None, 'x', None],
  ['x', None, 'x', None],
  ['x', 'x', 'x', None]]
draw.drawRectangle(0, 0, 2, 3)
print(draw.printBoard())
assert(draw.canvas == expected)

# Test bucketFill
draw = DrawingTool('input/testIn.txt', 'output/testOut.txt')
draw.initCanvas(4, 4)
expected = [
  ['x', 'x', 'x', 'o'],
  ['x', 'x', 'x', 'o'],
  ['x', 'o', 'o', 'o'],
  ['x', 'o', 'o', 'o']]
draw.drawVertLine(0, 0, 3)
draw.drawRectangle(1, 0, 2, 1)
draw.bucketFill(2, 2, 'o')
print(draw.printBoard())
assert(draw.canvas == expected)

# Test ensureBounds
# Test negative y
assert(not draw.ensureBounds(0, -1))
# Test negative x
assert(not draw.ensureBounds(-1, 1))
# Test overflow y
assert(not draw.ensureBounds(3, 6))
# Test overflow x
assert(not draw.ensureBounds(6, 3))
# Test in bounds
assert(draw.ensureBounds(2, 3))

print("All tests passed!")















