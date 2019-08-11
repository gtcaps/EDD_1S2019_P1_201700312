import curses
from curses import textpad
from Structures.DoubleCircularList import DoubleCircularList, DoubleCircularNode
from Structures.DoubleLinkedList import DoubleLinkedList
from Structures.Stack import Stack
from Structures.Queue import Queue
from Classes.BulkLoading import BulkLoading
from Classes.Player import Player
from Classes.Position import Position

#PLAYER WHO PLAY THE GAME
player_selected = None
#PLAYERS_CIRCULAR LIST STRUCTURE
players_list = None
#SNAKE DOUBLE LIST STRUCTURE
snake_list = None
#LEVELS STACK STRUCTURE
level1 = Stack()
level2 = Stack()
level3 = Stack()
#SCOREBOARD QUEUE
scoreboard_queue = Queue()

#VELOCITY OF THE GAME
velocity = 300

def init_structures(window):
    global  snake_list, players_list
    height, width = window.getmaxyx()

    players_list = DoubleCircularList()

    # DEFINE THE FIRST 3 NODES OF THE SNAKE AND INSERT INTO THE LIST
    snake_list = DoubleLinkedList()
    first_node = Position((width / 2) + 2, (height / 2))
    second_node = Position((width / 2), (height / 2))
    third_node = Position((width / 2) - 2, (height / 2))

    snake_list.insert_in_back(first_node.x_position, first_node.y_position)
    snake_list.insert_in_back(second_node.x_position, second_node.y_position)
    snake_list.insert_in_back(third_node.x_position, third_node.y_position)

def defaultSetting(window):
    window.border(0)
    # MEDIDAS DE LA TERMINAL
    height_size, width_size = window.getmaxyx()
    x_center = lambda a="": int((width_size / 2) - (len(a) / 2))
    y_center = int(height_size / 2)

    return x_center, y_center

def velocity_level(level):
    if level is 1 or 0:
        default_velocity = 300
    elif level > 1:
        cont = level
        while cont > 0:
            if default_velocity > 100:
                default_velocity -= 100
            else:
                default_velocity -= 50
            cont -= 1
    return int(default_velocity)

velocity = velocity_level(1)

def setTitle(window, title, x):
    window.addstr(0, x(title), title)

def menu(window, option_selected):
    x, y = defaultSetting(window)

    # TITULO
    setTitle(window, "Snake Reloaded Main Menu", x)

    #Opciones del Menu
    options = ("Play","Scoreboard","User Selection","Reports","Bulk Loading","Exit")

    cont = -3
    opt_select = None
    for option in options:
        if option is options[option_selected]:
            window.attron(curses.color_pair(1))
            window.addstr( y + cont, x(option), option)
            window.attroff(curses.color_pair(1))
            opt_select = option_selected
        else:
            window.addstr(y + cont, x(option), option)
        cont += 1
    window.refresh()
    return opt_select

def snake(window):
    global player_selected, players_list
    x, y = defaultSetting(window)

    if player_selected is not None:
        window.clear()
        game(window, player_selected, x)
    else:
        player_name = ""
        window.addstr(y - 4, x("PLEASE WRITE A PLAYER NAME TO PLAY RELOAD SNAKE"),"PLEASE WRITE A PLAYER NAME TO PLAY RELOAD SNAKE")
        window.addstr(y - 3, x("PLAYER NAME: "), "PLAYER NAME: ")
        window.addstr(y, x("PRESS [ESC] TO BACK TO THE MAIN MENU"), "PRESS [ESC] TO BACK TO THE MAIN MENU")
        while 1:
            key_s = window.getch()

            if key_s == 27:
                window.clear()
                menu(window, 0)
                break
            elif key_s >= 65 and key_s <= 90 or key_s >= 97 and key_s <= 122 or key_s >= 48 and key_s <= 57 or key_s == 95:
                if len(player_name) < 12:
                    player_name += str(chr(key_s))
                window.addstr(y - 3, x("PLAYER NAME: ") + len("PLAYER NAME: "), player_name, curses.A_UNDERLINE)
            elif key_s == 8:
                player_name = player_name[:len(player_name) - 1]
                window.addstr(y - 3, x("PLAYER NAME: ") + len("PLAYER NAME: "), "                           ", )
                window.addstr(y - 3, x("PLAYER NAME: ") + len("PLAYER NAME: "), player_name)
            elif (key_s == curses.KEY_ENTER or key_s in [10, 13]) and player_name is not "":
                if players_list is not None:
                    players_list.add(player_name)
                else:
                    players_list = DoubleCircularList()
                    players_list.add(player_name)

                aux_player_node = players_list.head
                for player in range(0,players_list.size):
                    if aux_player_node.player.name is player_name:
                        break
                    else:
                        aux_player_node = aux_player_node.next

                player_selected = aux_player_node.player
                window.addstr(y - 3, x("PLAYER NAME: ") , "                                           ")
                window.addstr(y - 3, x(" ") - 13 , "USUARIO CREADO CORRECTAMENTE")
                window.addstr(y + 3, x("PRESS [J] TO PLAY") , "PRESS [J] TO PLAY")

                while 1:
                    key_ans = window.getch()
                    if key_ans == 74 or key_ans == 106:
                        window.clear()
                        game(window, player_selected, x)
                        break
                    elif key_ans == 27:
                        window.clear()
                        menu(window, 0)
                        break
                    else:
                        window.addstr(y + 3, x("PRESS [J] TO PLAY"), "PRESS [J] TO PLAY")
                break



        window.refresh()

def code_direction(strring):
    if strring is "up":
        return 73
    elif strring is "down":
        return 75
    elif strring is "left":
        return 74
    elif strring is "right":
        return 76
    return None

#FALTA LAS COMIDAS
def game(window, player_selected, x):
    global snake_list, level1, level2, level3, velocity
    window.border(0)
    setTitle(window, " SNAKE RELOADED ", x)
    window.addstr(49, 4, "[ESC] to pause")
    window.addstr(0, 4, "Score : " + str(player_selected.score))
    window.addstr(0, 96, "Player: " + player_selected.name.strip())
    window.addstr(48, x("[I] = UP       [K] = DOWN       [L] = RIGHT       [J] = LEFT"), "[I] = UP       [K] = DOWN       [L] = RIGHT       [J] = LEFT")
    window.nodelay(1)
    window.timeout(velocity)

    #DEFINE THE GAME AREA
    height, width = window.getmaxyx()
    textpad.rectangle(window, 2, 3, height - 3, width - 3)


    #DEFINE THE DEFAULT DIRECTION OF THE SNAKE
    direction = "right"

    #PRINT THE SNAKE IN THE GAME AREA
    aux_head_snake = snake_list.head
    while aux_head_snake is not None:
        window.addstr(aux_head_snake.position.y_position, aux_head_snake.position.x_position, "#")
        aux_head_snake = aux_head_snake.next

    #MOVING THE SNAKE WITH THE KEYS
    x = 0
    y = 0
    while 1:
        key = window.getch()
        head_snake = snake_list.head.position

        if key == -1:
            key = code_direction(direction)

        if key == 76 or key == 108:#L ------------------------------------------------------------------------>
            direction = "right"
            new_head = Position(head_snake.x_position + 2, head_snake.y_position)
        elif key == 74 or key == 106: #J <-----------------------------------------------------------------------
            direction = "left"
            new_head = Position(head_snake.x_position - 2, head_snake.y_position)
        elif key == 73 or key == 105: #I UP <-----------------------------------------------------------------------
            direction = "up"
            new_head = Position(head_snake.x_position, head_snake.y_position - 1)
        elif key == 75 or key == 107: #K DOWN <-----------------------------------------------------------------------
            direction = "down"
            new_head = Position(head_snake.x_position, head_snake.y_position + 1)
        elif key == 27:
            window.nodelay(0)
            string = "[1] = MAIN MENU         [2] = GRAPH THE SNAKE LIST         [3] = GRAPH THE STACK SCORE"
            window.addstr(height - 2, int((width/2) - (len(string)/2)), string)
            window.addstr(height - 1, 4, "[ESC] to resume")
            title = "SNAKE RELOADED - PAUSE"
            window.addstr(0, int((width/2) - (len(title)/2)), title)
            while 1:
                key_ans = window.getch()
                res = False
                if key_ans == 27:
                    window.nodelay(1)
                    string = "                                                                                              "
                    window.addstr(height - 2, int((width / 2) - (len(string) / 2)), string)
                    menu_options = "[I] = UP       [K] = DOWN       [L] = RIGHT       [J] = LEFT"
                    window.addstr(height - 2, int((width/2) - (len(menu_options)/2)), menu_options)
                    title = "    SNAKE RELOADED    "
                    window.addstr(0, int((width / 2) - (len(title) / 2)), title)
                    window.addstr(height - 1, 4, "[ESC] to pause ")
                    window.refresh()
                    break
                elif key_ans == 49:
                    window.clear()
                    res = True
                    menu(window, 0)
                    break
                elif key_ans == 50:
                    snake_list.graph()
                elif key_ans == 51:
                    level1.graph("Level 1")
            if res:
                break
        if new_head.x_position is (width - 4):
            new_head.x_position = 4
        elif new_head.x_position is 4:
            new_head.x_position = width - 4
        elif new_head.y_position is (height - 3):
            new_head.y_position = 3
        elif new_head.y_position is 2:
            new_head.y_position = height - 4

        snake_list.insert_in_front(new_head.x_position, new_head.y_position)
        window.addstr(new_head.y_position, new_head.x_position, "#")

        last = snake_list.tail
        window.addstr(last.position.y_position, last.position.x_position, " ")
        snake_list.delete_in_back()

        window.refresh()

def reports_window(window):
    x, y = defaultSetting(window)
    setTitle(window, "Snake Reloaded - Reports", x)
    window.addstr(y - 15, x("------- REPORTS -------") , "------- REPORTS -------")
    window.addstr(y - 10, x("------- REPORTS -------") - 3, "PRESS KEY [1] = SNAKE REPORT")
    window.addstr(y - 8, x("------- REPORTS -------") - 3, "PRESS KEY [2] = SCORE REPORT")
    window.addstr(y - 6, x("------- REPORTS -------") - 3, "PRESS KEY [3] = SCOREBOARD REPORT")
    window.addstr(y - 4, x("------- REPORTS -------") - 3, "PRESS KEY [4] = USERS REPORT")
    window.addstr(y , x("PRESS KEY [ESC] TO BACK TO MAIN MENU"), "PRESS KEY [ESC] TO BACK TO MAIN MENU")

    while 1:
        key = window.getch()

        if key == 49:
            snake_list.graph()
        elif key == 50:
            level1.graph("Level 1")
        elif key == 51:            
            scoreboard_queue.graph()
        elif key == 52:
            players_list.graph()
        elif key == 27:
            window.clear()
            menu(window, 3)
            break

def user_selection(window):
    global players_list, player_selected
    player = player_selected
    if player_selected is None:
        player = Player("ANYONE")
    user = None

    x, y = defaultSetting(window)
    setTitle(window, "Snake Reloaded - User Selection", x)
    window.addstr(y - 7, x("<-------ACTUAL PLAYER: {}------->".format(player.name.strip())),"<-------ACTUAL PLAYER: {}------->".format(player.name.strip()))
    window.addstr(y + 1, x("Press [ESC] to back to the main menu"), "Press [ESC] to back to the main menu")
    if players_list is None or players_list.size is 0:
        window.addstr(y - 3, x("ANY USER, CHARGE A .CSV FILE IN A BULK LOADING OPTION OR CREATE A NEW USER"),"ANY USER, CHARGE A .CSV FILE IN A BULK LOADING OPTION OR CREATE A NEW USER")
    else:
        user = players_list.head
        window.addstr(y - 3, x(user.player.name), user.player.name)
        window.addstr(y - 3, 70, "---> (L)")
        window.addstr(y - 3, 40, "(K) <---")
        window.addstr(y, x("Press [Enter] to select a player"), "Press [Enter] to select a player")
        window.refresh()

    while 1:
        x, y = defaultSetting(window)
        setTitle(window, "Snake Reloaded - User Selection", x)
        key_s = window.getch()
        window.clear()
        window.addstr(y - 7, x("<-------ACTUAL PLAYER: {}------->".format(player.name.strip())),"<-------ACTUAL PLAYER: {}------->".format(player.name.strip()))

        if key_s == 27:
            window.clear()
            menu(window, 2)
            break
        elif (key_s == 76 or key_s == 108) and players_list is not None:
            user = user.next
            window.addstr(y - 3, x(user.player.name), user.player.name)
            window.addstr(y - 3, 70, "---> (L)")
            window.addstr(y - 3, 40, "(K) <---")
            window.addstr(y, x("Press [Enter] to select a player"), "Press [Enter] to select a player")
        elif (key_s == 107 or key_s == 75) and players_list is not None:
            user = user.back
            window.addstr(y - 3, x(user.player.name), user.player.name)
            window.addstr(y - 3, 70, "---> (L)")
            window.addstr(y - 3, 40, "(K) <---")
            window.addstr(y, x("Press [Enter] to select a player"), "Press [Enter] to select a player")
        elif key_s == curses.KEY_ENTER or key_s in [10, 13] and players_list is not None:
            if(players_list.size is not 0):
                window.addstr(y - 3, x(user.player.name), user.player.name)
                window.addstr(y - 3, 70, "---> (L)")
                window.addstr(y - 3, 40, "(K) <---")
                window.addstr(y, x("Player Selected"), "Player Selected")
                player = player_selected = user.player
                window.addstr(y - 7, x("<-------ACTUAL PLAYER: {}------->".format(player.name.strip())),"<-------ACTUAL PLAYER: {}------->".format(player.name.strip()))
            else:
                window.addstr(y - 3, x("ANY USER, CHARGE A .CSV FILE IN A BULK LOADING OPTION OR CREATE A NEW USER"),"ANY USER, CHARGE A .CSV FILE IN A BULK LOADING OPTION OR CREATE A NEW USER")
        else:
            if players_list is None:
                window.addstr(y - 3, x("ANY USER, CHARGE A .CSV FILE IN A BULK LOADING OPTION OR CREATE A NEW USER"),"ANY USER, CHARGE A .CSV FILE IN A BULK LOADING OPTION OR CREATE A NEW USER")
            else:
                window.addstr(y - 3, x(user.player.name), user.player.name)
                window.addstr(y - 3, 70, "---> (L)")
                window.addstr(y - 3, 40, "(K) <---")
                window.addstr(y, x("Press [Enter] to select a player"), "Press [Enter] to select a player")


        window.addstr(y + 1, x("Press [ESC] to back to the main menu"), "Press [ESC] to back to the main menu")
        window.refresh()

def bulk_loading_users(window):
    name_file = ""
    global players_list
    window.nodelay(0)
    window.timeout(-5)
    while 1:
        x, y = defaultSetting(window)
        y = y - 4
        setTitle(window, "Snake Reloaded - Bulk Loading", x)
        window.addstr(y, 40, "Write the file(.csv) name: ")
        window.addstr(y + 4, x("Press [ESC] to back to the menu") - 2, "Press [ESC] to back to the menu")
        window.refresh()

        key_s = window.getch()
        window.clear()

        if key_s == 27:
            menu(window, 4)
            break
        elif key_s>=65 and key_s<= 90 or key_s>=97 and key_s<=122 or key_s>=48 and key_s<=57 or key_s == 95:
            name_file += str(chr(key_s))
            window.addstr(y, (40 + len("Write the file(.csv) name: ")), name_file, curses.A_UNDERLINE)
        elif key_s == 8:
            name_file = name_file[:len(name_file)-1]
            window.addstr(y, (40 + len("Write the file(.csv) name: ")), name_file, curses.A_UNDERLINE)
        elif key_s == curses.KEY_ENTER or key_s in [10, 13]:
            if players_list is not None:
                players = BulkLoading(name_file)
                if players is not None:
                    aux_player = players.head
                    for i in range(0, players.size):
                        players_list.add(aux_player.player.name)
                        aux_player = aux_player.next
                    window.addstr(y, (40 + len("Write the file(.csv) name: ")), "The File is Loaded", curses.A_UNDERLINE)
                else:
                    window.addstr(y, (40 + len("Write the file(.csv) name: ")), "File Not Found", curses.A_UNDERLINE)
            else:
                players = BulkLoading(name_file)
                if players is not None:
                    players_list = players
                    window.addstr(y, (40 + len("Write the file(.csv) name: ")), "The File is Loaded",curses.A_UNDERLINE)
                else:
                    window.addstr(y, (40 + len("Write the file(.csv) name: ")), "File Not Found", curses.A_UNDERLINE)
            name_file = ""
        else:
            window.addstr(y, (40 + len("Write the file(.csv) name: ")), name_file, curses.A_UNDERLINE)


def main(stdscr):
    curses.curs_set(0)
    curses.resize_term(50,120)
    window = curses.newwin(50, 120, 0, 0)
    init_structures(window)
    stdscr.keypad(True)


    # Creando color
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    #MENU
    opt_selected = menu(window, 0)

    while 1:
        options = (0, 1, 2, 3, 4, 5)
        key = stdscr.getch()
        window.clear()

        if key == curses.KEY_UP:
            opt_selected -= 1
            if opt_selected not in options:
                opt_selected = 0
            menu(window, opt_selected)
        elif key == curses.KEY_DOWN:
            opt_selected += 1
            if opt_selected not in options:
                opt_selected = 5
            menu(window, opt_selected)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if opt_selected is 0:
                snake(window)
            elif opt_selected is 2:
                user_selection(window)
            elif opt_selected is 3:
                reports_window(window)
            elif opt_selected is 4:
                bulk_loading_users(window)
            elif opt_selected is 5:
                break
            else:
                menu(window, opt_selected)
        elif key == 27:
            menu(window, 0)
            opt_selected = 0
        else:
            menu(window, opt_selected)
        window.refresh()

curses.wrapper(main)