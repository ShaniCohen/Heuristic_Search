import config as c
# get null position

def null_piece(position):
    for row in range(4):
        for column in range(4):
            if position[row][column] == None:
                return row, column


def neighbors(x, y):
    return [(x_, y_) for (x_, y_) in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            if 0 <= x_ and x_ < 4 and 0 <= y_ and y_ < 4]


def moves(position):
    # null_cell = null_piece(position)
    null_cell_row, null_cell_col = null_piece(position=position)
    movable = neighbors(x=null_cell_row, y=null_cell_col)

    # rep = []
    # for (x, y) in movable:
    #     pos_new = position
    #     moved = position[x][y]
    #     pos_new[null_cell_row][null_cell_col] = moved
    #     pos_new[x][y] = None
    #     rep.append((moved, tuple(pos_new)))

    rep = []
    for (x, y) in movable:
        moved = position[x][y]
        new_position = []
        for row in range(4):
            new_row = []
            for column in range(4):
                # if (row, column) == null_cell:
                if (row, column) == (null_cell_row, null_cell_col):
                    new_row.append(position[x][y])
                elif (row, column) == (x, y):
                    new_row.append(position[null_cell_row][null_cell_col])
                else:
                    new_row.append(position[row][column])
            new_position.append((tuple(new_row)))
        rep.append((moved, tuple(new_position)))
    return rep


def display(position):
    for row in range(4):
        for column in range(4):
            if position[row][column]:
                print("{:>2} ".format(position[row][column])),
            else:
                print(" _ "),
        print()


def find_piece(position, num=None):
    for row in range(4):
        for column in range(4):
            if position[row][column] == num:
                return row, column


def signmatch(n1, n2):
    if n1 > 0 and n2 > 0:
        return True
    elif n1 < 0 and n2 < 0:
        return True
    else:
        return False


def find_linear_conflicts(in_board):
    # Add only 1 per piece in linear conflict. This will lead to a total of 2 for every conflicted pair.
    lin_conf_total = 0
    for i in range(4):  # rows
        for z in range(4):  # pieces
            tile = in_board[i][z]
            ny, nx = find_piece(position=in_board, num=tile)
            ny_, nx_ = find_piece(position=c.WIN, num=tile)
            for o in range(4):  # other tiles in that row
                other_tile = in_board[i][o]
                if other_tile != tile:
                    oy, ox = find_piece(position=in_board, num=other_tile)
                    oy_, ox_ = find_piece(position=c.WIN, num=other_tile)
                    if ny == oy and ny_ == oy_:
                        if (nx_ > ox > nx) or (nx > ox > nx_) or (ox < nx < ox_) or (ox > nx > ox_) or (
                                nx == ox_ and not signmatch(n1=nx_ - nx, n2=ox_ - ox)):
                            # The last part is so that, if they are traveling in the same direction, they aren't counted
                            lin_conf_total += 1
            for j in range(4):  # other tiles in that column
                other_tile = in_board[j][z]
                if other_tile != tile:
                    oy, ox = find_piece(position=in_board, num=other_tile)
                    oy_, ox_ = find_piece(position=c.WIN, num=other_tile)
                    if nx == ox and nx_ == ox_:
                        if (ny_ > oy > ny) or (ny > oy > ny_) or (oy < ny < oy_) or (oy > ny > oy_) or (
                                ny == oy_ and not signmatch(n1=ny_ - ny, n2=oy_ - oy)):
                            lin_conf_total += 1
    return lin_conf_total


def eval_pos(board, pathlength, e):
    total = 0
    for num in [None] + list(range(1, 15 + 1)):
        (x, y) = find_piece(position=board, num=num)
        (x_, y_) = find_piece(position=c.WIN, num=num)
        total += abs(x - x_) + abs(y - y_)
    total += find_linear_conflicts(in_board=board)
    return total * e + pathlength