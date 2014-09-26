# copied from http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python
def get_line(x1, y1, x2, y2):
	points = []
	issteep = abs(y2-y1) > abs(x2-x1)
	if issteep:
		x1, y1 = y1, x1
		x2, y2 = y2, x2
	rev = False
	if x1 > x2:
		x1, x2 = x2, x1
		y1, y2 = y2, y1
		rev = True
	deltax = x2 - x1
	deltay = abs(y2-y1)
	error = int(deltax / 2)
	y = y1
	ystep = None
	if y1 < y2:
		ystep = 1
	else:
		ystep = -1
	for x in range(x1, x2 + 1):
		if issteep:
			points.append((y, x))
		else:
			points.append((x, y))
		error -= deltay
		if error < 0:
			y += ystep
			error += deltax
	# Reverse the list if the coordinates were reversed
	if rev:
		points.reverse()
	return points

def draw_dots(chars, dots):
	# find out average of Y-coordinate, for all of these in the invisible middle line
	bottom = top = 0
	for dot in dots:
		if dot[1] > 8:
			bottom += 1
		if dot[1] < 8:
			top += 1
	print "We have %d bottom pixels and %d top pixels" % (bottom, top)

	for dot in dots:
		if dot[1] == 8 and dot[0] != 8: # invisible line
			dot = (dot[0], dot[1]-1 if bottom < top or (bottom == top and dot[0] < 8) else dot[1]+1) # bugfix suitable for clock (pointer is rotated around the center)
		if dot[0] < 5 and dot[1] < 8:
			chars[0][dot[1]] |= (1<<(4-dot[0]))
		elif 5 < dot[0] < 11 and dot[1] < 8:
			chars[1][dot[1]] |= (1<<(4-(dot[0]-6)))
		elif 11 < dot[0] < 17 and dot[1] < 8:
			chars[2][dot[1]] |= (1<<(4-(dot[0]-12)))
		elif dot[0] < 5 and 8 < dot[1]:
			chars[3][dot[1]-9] |= (1<<(4-dot[0]))
		elif 5 < dot[0] < 11 and 8 < dot[1]:
			chars[4][dot[1]-9] |= (1<<(4-(dot[0]-6)))
		elif 10 < dot[0] < 17 and 8 < dot[1]:
			chars[5][dot[1]-9] |= (1<<(4-(dot[0]-12)))