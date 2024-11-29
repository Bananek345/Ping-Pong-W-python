import curses
import random

# Ustawienia okna
stdscr = curses.initscr()
curses.curs_set(0)
sh, sw = stdscr.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

# Ustawienia piłki i paletek
ball = [sh // 2, sw // 2]
ball_direction = [1, 1]  # kierunek piłki
paddle1 = [sh // 2, 1]  # paletka gracza 1
paddle2 = [sh // 2, sw - 2]  # paletka gracza 2
paddle_height = 3

# Punkty
score1 = 0
score2 = 0

# Rysowanie paletek
def draw_paddles():
    for i in range(-paddle_height // 2, paddle_height // 2 + 1):
        w.addch(paddle1[0] + i, paddle1[1], '|')
        w.addch(paddle2[0] + i, paddle2[1], '|')

# Rysowanie piłki
def draw_ball():
    w.addch(ball[0], ball[1], 'O')

# Rysowanie wyniku
def draw_score():
    w.addstr(0, sw // 4, f"Gracz 1: {score1}", curses.A_BOLD)
    w.addstr(0, 3 * sw // 4, f"Gracz 2: {score2}", curses.A_BOLD)

# Główna pętla gry
while True:
    w.clear()
    draw_score()
    draw_paddles()
    draw_ball()
    w.refresh()

    # Ruch piłki
    ball[0] += ball_direction[0]
    ball[1] += ball_direction[1]

    # Sprawdzenie kolizji z górną i dolną krawędzią
    if ball[0] in [0, sh - 1]:
        ball_direction[0] *= -1

    # Sprawdzenie kolizji z paletkami
    if (ball[1] == paddle1[1] and paddle1[0] - paddle_height // 2 <= ball[0] <= paddle1[0] + paddle_height // 2) or \
       (ball[1] == paddle2[1] and paddle2[0] - paddle_height // 2 <= ball[0] <= paddle2[0] + paddle_height // 2):
        ball_direction[1] *= -1

    # Sprawdzenie, czy piłka wyszła poza ekran
    if ball[1] <= 0:  # Gracz 2 zdobywa punkt
        score2 += 1
        ball[0] = sh // 2
        ball[1] = sw // 2
        ball_direction = [random.choice([-1, 1]), random.choice([-1, 1])]
    elif ball[1] >= sw - 1:  # Gracz 1 zdobywa punkt
        score1 += 1
        ball[0] = sh // 2
        ball[1] = sw // 2
        ball_direction = [random.choice([-1, 1]), random.choice([-1, 1])]

    # Ruch paletek
    key = w.getch()
    if key == ord('a') and paddle1[0] > paddle_height // 2:
        paddle1[0] -= 1
    elif key == ord('z') and paddle1[0] < sh - paddle_height // 2 - 1:
        paddle1[0] += 1
    elif key == curses.KEY_UP and paddle2[0] > paddle_height // 2:
        paddle2[0] -= 1
    elif key == curses.KEY_DOWN and paddle2[0] < sh - paddle_height // 2 - 1:
        paddle2[0] += 1

curses.endwin()