import array
import typing

F1 = {'Name': 'O', 'Number': 1, 'Color': 'Rose',
      'Height': 1, 'Width': 5, 'Angle': 0, 'Mirror': False, 'Shape': [[1, 1, 1, 1, 1]],
      'Options': [[0, False], [90, False]]}
F2 = {'Name': 'Q', 'Number': 2, 'Color': 'Orange',
      'Height': 2, 'Width': 4, 'Angle': 0, 'Mirror': False, 'Shape': [[1, 1, 1, 1], [1, 0, 0, 0]],
      'Options': [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]]}
F3 = {'Name': 'Y', 'Number': 3, 'Color': 'Brown',
      'Height': 2, 'Width': 4, 'Angle': 0, 'Mirror': False, 'Shape': [[1, 1, 1, 1], [0, 1, 0, 0]],
      'Options': [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]]}
F4 = {'Name': 'S', 'Number': 4, 'Color': 'Black',
      'Height': 2, 'Width': 4, 'Angle': 0, 'Mirror': False, 'Shape': [[0, 1, 1, 1], [1, 1, 0, 0]],
      'Options': [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]]}
F5 = {'Name': 'V', 'Number': 5, 'Color': 'Dark Blue',
      'Height': 3, 'Width': 3, 'Angle': 0, 'Mirror': False, 'Shape': [[1, 1, 1], [1, 0, 0], [1, 0, 0]],
      'Options': [[0, False], [90, False], [180, False], [270, False]]}
F6 = {'Name': 'P', 'Number': 6, 'Color': 'Light Blue',
      'Height': 2, 'Width': 3, 'Angle': 0, 'Mirror': False, 'Shape': [[1, 1, 1], [1, 1, 0]],
      'Options': [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]]}
F7 = {'Name': 'U', 'Number': 7, 'Color': 'Yellow',
      'Height': 2, 'Width': 3, 'Angle': 0, 'Mirror': False, 'Shape': [[1, 1, 1], [1, 0, 1]],
      'Options': [[0, False], [90, False], [180, False], [270, False]]}
F8 = {'Name': 'Z', 'Number': 8, 'Color': 'Grey',
      'Height': 3, 'Width': 3, 'Angle': 0, 'Mirror': False, 'Shape': [[1, 0, 0], [1, 1, 1], [0, 0, 1]],
      'Options': [[0, False], [90, False], [0, True], [90, True]]}
F9 = {'Name': 'R', 'Number': 9, 'Color': 'Light Green',
      'Height': 3, 'Width': 3, 'Angle': 0, 'Mirror': False, 'Shape': [[1, 0, 0], [1, 1, 1], [0, 1, 0]],
      'Options': [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]]}
FA = {'Name': 'T', 'Number': 10, 'Color': 'Dark Green',
      'Height': 3, 'Width': 3, 'Angle': 0, 'Mirror': False, 'Shape': [[1, 1, 1], [0, 1, 0], [0, 1, 0]],
      'Options': [[0, False], [90, False], [180, False], [270, False]]}
FB = {'Name': 'W', 'Number': 11, 'Color': 'Cherry',
      'Height': 3, 'Width': 3, 'Angle': 0, 'Mirror': False, 'Shape': [[1, 1, 0], [0, 1, 1], [0, 0, 1]],
      'Options': [[0, False], [90, False], [180, False], [270, False]]}
FC = {'Name': 'X', 'Number': 12, 'Color': 'Red',
      'Height': 3, 'Width': 3, 'Angle': 0, 'Mirror': False, 'Shape': [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
      'Options': [[0, False]]}

ARR = [F1, F2, F3, F4, F5, F6, F7, F8, F9, FA, FB, FC]


def rotate(source: dict, angle: int) -> dict:
    result = {'Name': source['Name'], 'Number': source['Number'], 'Color': source['Color'],
              'Height': source['Height'], 'Width': source['Width'], 'Angle': angle,
              'Mirror': source['Mirror'], 'Shape': source['Shape']}
    if angle == 90 or angle == -270:
        result['Height'] = source['Width']
        result['Width'] = source['Height']
        result['Shape'] = [[0 for i in range(result['Width'])] for j in range(result['Height'])]
        for j in range(source['Height']):
            for i in range(source['Width']):
                result['Shape'][i][result['Width'] - 1 - j] = source['Shape'][j][i]
    elif angle == 180 or angle == -180:
        result['Shape'] = [[0 for i in range(result['Width'])] for j in range(result['Height'])]
        for j in range(source['Height']):
            for i in range(source['Width']):
                result['Shape'][result['Height'] - 1 - j][result['Width'] - 1 - i] = source['Shape'][j][i]
    elif angle == 270 or angle == -90:
        result['Height'] = source['Width']
        result['Width'] = source['Height']
        result['Shape'] = [[0 for i in range(result['Width'])] for j in range(result['Height'])]
        for j in range(source['Height']):
            for i in range(source['Width']):
                result['Shape'][result['Height'] - 1 - i][j] = source['Shape'][j][i]
    return result


def mirror(source: dict) -> dict:
    result = {'Name': source['Name'], 'Number': source['Number'], 'Color': source['Color'],
              'Height': source['Height'], 'Width': source['Width'], 'Angle': source['Angle'],
              'Mirror': not(source['Mirror']), 'Shape': source['Shape']}
    result['Shape'] = [[0 for i in range(result['Width'])] for j in range(result['Height'])]
    for j in range(source['Height']):
        for i in range(source['Width']):
            result['Shape'][j][result['Width'] - 1 - i] = source['Shape'][j][i]
    return result


def multiprint(source: dict):
    caption = '#' + str(source['Number']) + ' - ' + source['Name'] + ' - ' + str(source['Angle']) + ' - ' + str(source['Mirror'])
    print(caption)
    print(''.join(['-' for i in range(len(caption))]))
    for j in range(source['Height']):
        print(' '.join(map(str,source['Shape'][j])))
    print(''.join(['-' for i in range(len(caption))]))


def print_shape(shape: list):
    print(''.join(['-' for i in range(2* len(shape[0]) - 1)]))
    for j in range(len(shape)):
        print(' '.join(map(str,shape[j])))
    #print(''.join(['-' for i in range(2 * len(shape[0]) - 1)]))


def orientate(task: dict) -> dict:
    l = []
    c = 0
    f = 0
    for figure in task['Figures']:
        l.append([])
        for option in figure['Options']:
            ready_figure = rotate(mirror(figure) if option[1] else figure, option[0])
            if task['Width'] < ready_figure['Width'] or task['Height'] < ready_figure['Height']:
                continue
            #multiprint(ready_figure)
            for j in range(task['Height'] - ready_figure['Height'] + 1):
                for i in range(task['Width'] - ready_figure['Width'] + 1):
                    field = [[0 for a in range(task['Width'])] for b in range(task['Height'])]
                    for n in range(ready_figure['Height']):
                        for m in range(ready_figure['Width']):
                            field[j+n][i+m] = ready_figure['Shape'][n][m]
                    #print_shape(field)
                    l[f].append(field)
                    c = c + 1
        f = f + 1
    return {'Height': task['Height'], 'Width': task['Width'], 'Figures': task['Figures'], 'Counter': c, 'List': l}


def merge(field_a: list, field_b: list) -> (list, bool):
    if field_a is None:
        return field_b[:], True
    elif field_b is None:
        return field_a[:], True
    else:
        result = [[0 for a in range(len(field_a[0]))] for b in range(len(field_a))]
        checker = True
        for j in range(len(field_a)):
            for i in range(len(field_a[j])):
                tmp = field_a[j][i] + field_b[j][i]
                result[j][i] = tmp
                if tmp > 1:
                    checker = False
        return result, checker


def check(field: list) -> bool:
    s = 0
    z = 0
    for j in range(len(field)):
        for i in range(len(field[j])):
            s = s + field[j][i]
            if field[j][i] == 0: z = z + 1
    return s == len(field) * len(field[0]) and z == 0


def solve(task: dict, shift: int = 0, field: list = None) -> (dict, bool):
    l = task['List']
    for c in range(len(l[shift])):
        merged, checker = merge(field, l[shift][c])
        if checker:
            if len(l) > shift + 1:
                fields, checker = solve(task, shift + 1, merged)
                if checker:
                    fields[shift] = l[shift][c]
                    return fields, checker
            else:
                checker = check(merged)
                if checker:
                    return {shift: l[shift][c]}, checker
    return {}, False


def print_result(fields: dict):
    separator = ''.join(['-' for i in range((2 * len(fields[0][0]) - 1 + 3) * len(fields) - 3)])
    print(separator)
    for j in range(len(fields[0])):
        content = ''
        for f in range(len(fields)):
            content = content + ' '.join(map(str, fields[f][j])) + '   '
        print(content)
    print(separator)


T3A = {'Height': 5, 'Width': 3, 'Figures': [F2, F3, FA]}
T3B = {'Height': 5, 'Width': 3, 'Figures': [F4, F6, F7]}

T4A = {'Height': 5, 'Width': 4, 'Figures': [F2, F3, F6, FA]}

T5A = {'Height': 5, 'Width': 5, 'Figures': [F2, F3, F6, FA, FB]}

T6A = {'Height': 5, 'Width': 6, 'Figures': [F2, F3, F6, F8, FA, FB]}

T7A = {'Height': 5, 'Width': 7, 'Figures': [F2, F3, F5, F6, F8, FA, FB]}
fields, rc = solve(orientate(T7A))
print_result(fields)



#print(F2)
#print(rotate(mirror(F2), 0))
#print(mirror(rotate(F2, 90)))
