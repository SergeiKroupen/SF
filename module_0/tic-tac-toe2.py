# Алгоритм использует координатную плоскость цифровой клавиатуры, таким образом,
# он одномерный, что упрощает работу с ним. Также это удобно для управления игрой,
# расположив руку на цифровую клавиатуру.
# Данные хранятся в целочисленном виде: ходы первого игрока = 1, второго  = -1, пустая клетка = 0.
# Это позволяет легко искать выигрышную и предвыигрышную позицию. Сумма в первом случае
# будет 3 или -3, а во # втором: 2 или -2.
# Вывод на экран производится через отдельный список, что позволяет ввести в гейм-плей выбор
# значков для отражения хода игры.
# В коде использован декоратор для реализации шуточного гейм-плея. Достаточно ошибится или намеренно
# ввести некорректный выбор значков для игры - и значки будут менятся каждый ход.
# -----------------------------------------------------
import numpy as np

field = [0] * 9                             # массив для хранения ходов игроков
board = [' '] * 9                           # массив для непосредственного вывода на экран
marks = ['X', '#', '֍', '©', '0', 'Օ', '¥', '§', '@']     # список для выбора значка
moves_marks = [' '] * 10                    # список значков для ходов
game_ai = False                             # флаг игры с алгоритмом
easter_b = False

# -----------------------------------------------------
# приветственный экран
# -----------------------------------------------------
def start_game():
    global game_ai
    print(chr(151) * 55)
    print('|', '  \\\   // ', '|', ' ' * 10, '|', '  oooooo  ', '|')
    print('|', '    XXX   ', '|', ' ' * 10, '|', ' 00     0 ', '|')
    print('|', '  //   \\\ ', '|', ' ' * 10, '|', '  oooooo  ', '|')
    print(chr(151) * 55)
    print('|', ' ' * 10, '|', ' Давайте  ', '|', ' ' * 10, '|')
    print('|', ' ' * 10, '|', ' поиграем ', '|', ' ' * 10, '|')
    print('|', ' ' * 10, '|', '    в     ', '|', ' ' * 10, '|')
    print(chr(151) * 55)
    print('|', ' ' * 10, '|', ' ' * 10, '|', ' ' * 10, '|')
    print('|', ' крестики ', '|', ' ' * 10, '|', ' нолики !?', '|')
    print('|', ' ' * 10, '|', ' ' * 10, '|', ' ' * 10, '|')
    print(chr(151) * 55)
    game_ai = bool(int(input('Хотите потренироваться (0) или поиграть с машиной?')))


# -----------------------------------------------------
# проверка хода игрока на корректность
# -----------------------------------------------------
def ask_move():
    while True:
        m = input("Ваш ход >> ")                # получение хода игрока

        if not m.isdigit():                     # проверка на не корректный ввод текста вместао цифр
            print('Введите число!')
            continue

        move = int(m)                           # преобразование хода в тип "число"
        if (move < 1) or (move > 9):            # проверка на не корректную цифру вне координат
            print('Число от 1 до 9!')
            continue

        if field[move - 1]:                     # проверка на свободную клету для хода
            print('Клетка занята!')
            continue

        return move


# -----------------------------------------------------
# game_ai
# -----------------------------------------------------
# проверка возможности выиграть для себя или для противника
# -----------------------------------------------------
# очевидно, что потенциальная линия для победы должна содержать
# два знака своего хода и один пустой, в противном случае сумма не
# будет 2 или -2.
# для первого игрока входной параметр = 1, для второго = -1
# -----------------------------------------------------
def chance_win(player=1):
    win_row = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
               (0, 3, 6), (1, 4, 7), (2, 5, 8),
               (0, 4, 8), (2, 4, 6)]

    # проверка, есть ли возможность выиграть игроку и сделать победный ход
    for cwq in win_row:
        if field[cwq[0]] + field[cwq[1]] + field[cwq[2]] == player * 2:
            for cww in cwq:
                if field[cww] == 0:
                    field[cww] = player
                    return cww

    # проверка, есть ли возможность выиграть сопернику и предотвратить победу
    # сделав ход
    for cwq in win_row:
        if field[cwq[0]] + field[cwq[1]] + field[cwq[2]] == (- player) * 2:
            for cww in cwq:
                if field[cww] == 0:
                    field[cww] = player
                    return cww

    return False        # если позиций нет, ход не сделан


# -----------------------------------------------------
# game_ai
# -----------------------------------------------------
# поиск возможного хода
# -----------------------------------------------------
# Алгоритм пытается найти с начала центр, потом самый свободный угол, потом, возможно
# просто пустой угол, и уже в конце - любую оставшуюся пустую клетку у стороны
# -----------------------------------------------------
def make_move(player=1):
    # массив со всеми "углами" и смежными с ними клетками
    corners = [(0, 3, 1, 2, 6), (2, 1, 5, 0, 8), (8, 5, 7, 2, 6), (6, 7, 3, 0, 8)]
    last_field = [1, 5, 7, 3]

    # если это первый ход - идем в центр
    if field[4] == 0:
        field[4] = player
        return 4

    # если не первый ход - проверяем углы и выбираем такой свободный, который будет дальше всего
    # от хода противника. это будет угол, где никакая клетка по вертикали и горизонтали от угла
    # не занята ходами противника и сам угол свободный.
    for mmq in range(4):
        if all([field[corners[mmq][0]] != -player,
               field[corners[mmq][1]] != -player,
               field[corners[mmq][2]] != -player,
               field[corners[mmq][3]] != -player,
               field[corners[mmq][4]] != -player,
               field[corners[mmq][0]] == 0]):
            mm = corners[mmq][0]
            field[mm] = player
            return mm

    # если совсем свободного угла нет - проверяем углы и выбираем свобный
    for mmq in range(4):
        if field[corners[mmq][0]] == 0:
            mm = corners[mmq][0]
            field[mm] = player
            return mm

    # свободных углов нет - выбираем первую свободную клетку
    for mmq in last_field:
        if field[last_field[mmq]] == 0:
            mm = last_field[mmq]
            field[mm] = player
            return mm


# -----------------------------------------------------
# проверка выигрыша какого-либо из игроков
# -----------------------------------------------------
def check_win():
    # все выигрышные комбинации находятся по вертикалям, горизонталям и диагоналям
    win_row = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
               (0, 3, 6), (1, 4, 7), (2, 5, 8),
               (0, 4, 8), (2, 4, 6)]

    # если по выигрышным линиям сумма состаит 3 или -3 - кто-то победил...
    for cw_q in win_row:

        if field[cw_q[0]] + field[cw_q[1]] + field[cw_q[2]] == 3:
            print(chr(151) * 55)
            print(f'{marks[mark1]}{marks[mark1]}{marks[mark1]} (Первый игрок) выиграли !! ')
            print(chr(151) * 55)
            return True

        elif field[cw_q[0]] + field[cw_q[1]] + field[cw_q[2]] == -3:
            print(chr(151) * 55)
            print(f'{marks[mark2]}{marks[mark2]}{marks[mark2]} (Второй игрок) выиграли !! ')
            print(chr(151) * 55)
            return True

    return False


# -----------------------------------------------------
# декоратор для вывода на экран с перемешиванием значков ходов (шутка такая)
# -----------------------------------------------------
def easter_joke(fn):
    def wrapper(*args, **kwargs):
        global easter_b, mark1, mark2       # передаю переменные внутрь декоратора

        if easter_b:                        # если пасхалка включена - запустим рандом для значков
            mark1, mark2, easter_b = easter_marks()

        result = fn(*args, **kwargs)
        return result

    return wrapper


# -----------------------------------------------------
# вывод на экран игрового поля с ходами игроков
# PS уже задекорирована пасхалкой
# -----------------------------------------------------
@easter_joke
def show_board(sm1="X", sm2="Օ"):

    for q in range(9):                              # цикл для пробразования данных в графический интерфейс
        if field[q] == 1:
            board[q] = sm1
        elif field[q] == -1:
            board[q] = sm2

    print('  ИГРОВАЯ КООРДИНАТНАЯ ПЛОСКОСТЬ')       # вывод на экран подсказки для координат ходов и
    print('(совпадает с цифровой клавиатурой)')     # текущего состояния игрового поля - доски

    print(chr(151) * 16)
    print("| 7 | 8 | 9 |", " " * 7, board[6], "|", board[7], "|", board[8])
    print(chr(151) * 16, " " * 6, chr(151) * 15)
    print("| 4 | 5 | 6 |", " " * 7, board[3], "|", board[4], "|", board[5])
    print(chr(151) * 16, " " * 6, chr(151) * 15)
    print("| 1 | 2 | 3 |", " " * 7, board[0], "|", board[1], "|", board[2])
    print(chr(151) * 16)


# -----------------------------------------------------
# рандомное перемешивание значков для отображения ходов (шутка такая)
# -----------------------------------------------------
def easter_marks():
    em1 = np.random.randint(0, len(marks))
    em2 = np.random.randint(0, len(marks))
    return em1, em2, True


# -----------------------------------------------------
# выбор игроком значков для отображения на доске
# -----------------------------------------------------
def choose_mark():

    print('Выберите значки для игры с начала для первого, а через пробел - ')
    print('второго игрока из предложенного списка. Индекс - начиная с нуля.')
    print(marks)

    inp = input(">> ")
    inp_split = inp.split()

    # если игрок выберет оба значка корректно, то и игра пойдет с выбранными значками,
    # если нет - игровые значки станут менятся каждый ход
    if len(inp.split()) == 2:
        m1, m2 = inp_split

        if m1.isdigit() and m2.isdigit():
            m1, m2 = list(map(int, inp_split))

            if -1 < m1 < len(marks) and -1 < m2 < len(marks):
                print(f'Вы выбрали для первого игрока: {marks[m1]}. А для второго - {marks[m2]}')
                print(chr(151) * 50)

                for cm_q in range(len(marks)+1):
                    moves_marks[cm_q] = marks[m1] if cm_q % 2 else marks[m2]
                return m1, m2, False

    print("Любите шуточки? Я тоже! Давайте повеселимся!")

    m1, m2, e = easter_marks()
    return m1, m2, e


start_game()
show_board()                            # вывод на экран текущего игрового поля

mark1, mark2, easter_b = choose_mark()  # выборо игроком значков для игры
w = 1


while True:                              # цикл для всего иргового времени: всего ходов в игре - 9
    # очередь игры игрока
    turn = 1 if w % 2 else -1           # переменная для хранения очередности хода крестиков и ноликов
    q = ask_move() - 1
    field[q] = turn                     # запись хода игрока

    show_board(marks[mark1], marks[mark2])       # вывод на экран текущего игрового поля
    print(f"                    Походил {marks[mark1] if turn == 1 else marks[mark2]}...")
    if check_win():                     # проверяем выигрыш ...
        break                           # ... если кто-то выиграл - конец игры.

    if w == 9:                          # девять ходов - это конец игры.
        print(chr(151)*20)
        print('Ничья')                  # раз нет победителей - ничья
        print(chr(151)*20)
        break

    w += 1                              # подсчитываем ход

    if not game_ai:
        continue

    # ------------------------
    # чередь игры алгоритма
    # ------------------------
    turn = 1 if w % 2 else -1           # переменная для хранения очередности хода крестиков и ноликов

    if chance_win(turn):
        show_board(marks[mark1], marks[mark2])  # вывод на экран текущего игрового поля
        if check_win():
            print(f"                    Походил {marks[mark2]}...")
            break
    else:
        make_move(turn)
        show_board(marks[mark1], marks[mark2])  # вывод на экран текущего игрового поля
        print(f"                    Походил {marks[mark2]}...")
    w += 1                              # подсчитываем ход
