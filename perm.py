import slitherlinky

layout = \
  [ ((0,1), (1,0))
  , ((0,3), (1,0))
  , ((0,5), (1,0))
  , ((1,7), (0,1))
  , ((3,7), (0,1))
  , ((5,7), (0,1))
  , ((7,9), (1,0))
  , ((7,7), (1,0))
  , ((7,5), (1,0))
  , ((5,0), (0,1))
  , ((7,0), (0,1))
  , ((9,0), (0,1))
  ]

allclues = [ list(map(int, x)) for x in
  [ '0123', '0132', '0213', '0231', '0312', '0321'
  , '1023', '1032', '1203', '1302', '2013', '2103'
  ] ]

def setup(s, clueset):
    s.solution = None
    s.height = 11
    s.width = 11
    s.cells = [[None for x in range(11)] for x in range(11)]
    for ((x,y), (dx,dy)), clue in zip(layout, clueset):
        s.cells[x][y] = clue[0]
        s.cells[x+dx][y+dy] = clue[1]
        s.cells[x+2*dx][y+2*dy] = clue[2]
        s.cells[x+3*dx][y+3*dy] = clue[3]

def count_potential_solutions(chosen):
    s = slitherlinky.Slitherlinky()
    setup(s, chosen)
    #for line in s.cells:
    #    print(''.join(['.' if x is None else str(x) for x in line]))
    s.generate_cell_constraints()
    s.generate_loop_constraints()
    s.call_sat_solver(validate=False)
    if s.solution is not None:
        return 1
    return 0

def search(chosen, available):
    if len(chosen) < 7:
        print(len(chosen))
    elif len(chosen) == 7:
        print('7', end='', flush=True)
    if len(available) == 0:
        s = slitherlinky.Slitherlinky()
        setup(s, chosen)
        try:
            s.generate_cell_constraints()
            s.generate_loop_constraints()
            s.call_sat_solver(verify=True)
        except Exception as e:
            print(e)
            return
        if s.solution is not None:
            print()
            for line in s.cells:
                print(''.join(['.' if x is None else str(x) for x in line]))
        return

    if count_potential_solutions(chosen) == 0:
        return

    for i in range(len(available)):
        n = available[i]
        rest = available[:i] + available[i+1:]
        search(chosen + [n], rest)
        search(chosen + [n[::-1]], rest)

if __name__ == '__main__':
    search([], allclues)
