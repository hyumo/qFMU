

import ast

def convert_from_string(data):
    # see https://github.com/numpy/numpy/blob/b235f9e701e14ed6f6f6dcba885f7986a833743f/numpy/matrixlib/defmatrix.py#L14
    for char in '[]':
        data = data.replace(char, '')

    rows = data.split(';')
    newdata = []
    count = 0
    for row in rows:
        trow = row.split(',')
        newrow = []
        for col in trow:
            temp = col.split()
            newrow.extend(map(ast.literal_eval, temp))
        if count == 0:
            Ncols = len(newrow)
        elif len(newrow) != Ncols:
            raise ValueError("Rows not the same size.")
        count += 1
        newdata.append(newrow)
    return newdata