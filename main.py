import curses
import random
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
players_list = DoubleCircularList()
#SNAKE DOUBLE LIST STRUCTURE
snake_list = None
#LEVELS STACK STRUCTURE
actual_level = 1
level1 = Stack()
level2 = Stack()
level3 = Stack()
#SCOREBOARD QUEUE
scoreboard_queue = Queue()

#VELOCITY OF THE GAME
velocity = 300
direction = "right"

def init_structures(window):
    global  snake_list, players_list, player_selected
    height, width = window.getmaxyx()

    
    if player_selected is not None:
        player_selected.score = 0
    
    level1 = Stack()
    level2 = Stack()
    level3 = Stack()

    # DEFINE THE FIRST 3 NODES OF THE SNAKE AND INSERT INTO THE LIST
    snake_list = DoubleLinkedList()
    first_node = Position((width / 2) + 1, (height / 2))
    second_node = Position((width / 2), (height / 2))
    third_node = Position((width / 2) - 1, (height / 2))

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


def setTitle(window, title, x):
    window.addstr(0, x(title), title)

def menu(window, option_selected):
    x, y = defaultSetting(window)
    init_structures(window)


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
    global player_selected, players_list, actual_level
    actual_level = 1
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

def food(height, width):
    global snake_list
    food = None
    
    while food is None:
        food = Position(random.randint(5,width - 5), random.randint(5, height - 5))

        head_snake = snake_list.head
        while head_snake is not None:
            if ( head_snake.position.x_position is food.x_position ) and (  head_snake.position.y_position is food.y_position ):
                food = None
                break
            else:
                head_snake = head_snake.next
        return food

def refresh_snake(window):
    global snake_list
    aux_head_snake = snake_list.head
    while aux_head_snake is not None:
        window.addstr(aux_head_snake.position.y_position, aux_head_snake.position.x_position, " ")
        aux_head_snake = aux_head_snake.next

    aux_head_snake = snake_list.head
    while aux_head_snake is not None:
        window.addstr(aux_head_snake.position.y_position, aux_head_snake.position.x_position, "#")
        aux_head_snake = aux_head_snake.next

def verify_snake_dead():
    global snake_list

    snake_head = snake_list.head
    snake_tail = snake_list.tail

    same = 0
    head = snake_list.head
    while head is not None:
        if (head.position.x_position == snake_head.position.x_position) and (head.position.y_position == snake_head.position.y_position):
            same += 1 
        
        head = head.next

    if same is not snake_list.size:
        aux_head = snake_list.head.next.next

        while aux_head is not None:
            if (snake_head.position.x_position == aux_head.position.x_position) and (snake_head.position.y_position == aux_head.position.y_position):
                return True
            else:
                aux_head = aux_head.next 

        aux_tail = snake_list.tail.behind.behind

        while (aux_tail is not None):
            if (snake_tail.position.x_position == aux_tail.position.x_position) and (snake_tail.position.y_position == aux_tail.position.y_position ):
                return True
            else:
                aux_tail = aux_tail.behind

    return False
    
def random_food():
     return random.choice(["*","+","+","*","+","+","*","+"])
        

def game(window, player_selected, x):
    global snake_list, level1, level2, level3, velocity, direction, actual_level
    window.border(0)
    setTitle(window, " SNAKE RELOADED ", x)
    window.addstr(49, 4, "[ESC] to pause")
    window.addstr(0, 4, "Score : " + str(player_selected.score))
    window.addstr(0, 96, "Player: " + player_selected.name.strip())
    window.addstr(48, x("[I] = UP       [K] = DOWN       [L] = RIGHT       [J] = LEFT"), "[I] = UP       [K] = DOWN       [L] = RIGHT       [J] = LEFT")
    window.nodelay(1)
    window.timeout(150)

    #DEFINE THE GAME AREA
    height, width = window.getmaxyx()
    textpad.rectangle(window, 2, 3, height - 3, width - 3)


    #DEFINE THE DEFAULT DIRECTION OF THE SNAKE
    direction = "right"

    #PRINT THE SNAKE IN THE GAME AREA AND THE FIRST FOOD
    aux_head_snake = snake_list.head
    while aux_head_snake is not None:
        window.addstr(aux_head_snake.position.y_position, aux_head_snake.position.x_position, "#")
        aux_head_snake = aux_head_snake.next

    food_snake = food(height, width)
    type_of_food = "+"
    window.addstr(food_snake.y_position, food_snake.x_position, type_of_food)

    #MOVING THE SNAKE WITH THE KEYS
    x = 0
    y = 0
    while 1:
        key = window.getch()
        head_snake = snake_list.head.position

        if key == -1:
            key = code_direction(direction)
        
        if player_selected.score >= 15 and player_selected.score < 30 :
            actual_level = 2
            window.timeout(50)
        elif player_selected.score >= 30:
            actual_level = 3
            window.timeout(25)
        else:
            actual_level = actual_level
        
        
        if (key == 76 or key == 108) and direction is not "left":#L ------------------------------------------------------------------------>
            direction = "right"
            new_head = Position(head_snake.x_position + 1, head_snake.y_position)
        elif (key == 74 or key == 106 ) and direction is not "right": #J <-----------------------------------------------------------------------
            direction = "left"
            new_head = Position(head_snake.x_position - 1, head_snake.y_position)
        elif key == 73 or key == 105 and direction is not "down": #I UP <-----------------------------------------------------------------------
            direction = "up"
            new_head = Position(head_snake.x_position, head_snake.y_position - 1)
        elif key == 75 or key == 107 and direction is not "up": #K DOWN <-----------------------------------------------------------------------
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
                    if actual_level is 1:
                        level1.graph("Level 1")
                    elif actual_level is 2:
                        level2.graph("Level 2")
                    elif actual_level is 3:
                        level3.graph("Level 3")
            

            if res:
                break
        if new_head.x_position is (width - 4):
            new_head.x_position = 5
        elif new_head.x_position is 4:
            new_head.x_position = width - 5
        elif new_head.y_position is (height - 3):
            new_head.y_position = 4
        elif new_head.y_position is 2:
            new_head.y_position = height - 5

        snake_list.insert_in_front(new_head.x_position, new_head.y_position)
        window.addstr(new_head.y_position, new_head.x_position, "#")

        #VERIFY IF THE SNAKE EAT A FOOD
        head_snake = snake_list.head.position
        tail_snake = snake_list.tail.position
        
        if ((head_snake.x_position == food_snake.x_position) and (head_snake.y_position == food_snake.y_position)):
            if type_of_food is "+":

                if actual_level is 1:
                    level1.push(food_snake.x_position, food_snake.y_position)
                elif actual_level is 2:
                    level2.push(food_snake.x_position, food_snake.y_position)
                elif actual_level is 3:
                    level3.push(food_snake.x_position, food_snake.y_position)


                
                player_selected.score = player_selected.score + 1
                window.addstr(0, 4, "Score : " + str(player_selected.score) + " ")
            elif type_of_food is "*":
                window.nodelay(0)
                
                if snake_list.size > 3:
                    snake_list.delete_in_front()
                    snake_list.delete_in_front()
                

                if player_selected.score > 0:
                    player_selected.score = player_selected.score - 1
                    window.addstr(0, 4, "Score : " + str(player_selected.score) + "  ")

                if actual_level is 1:
                    level1.pop()
                elif actual_level is 2:
                    level2.pop()
                elif actual_level is 3:
                    level3.pop()

                refresh_snake(window)
                window.nodelay(1)

            food_snake = food(height, width)
            type_of_food = random_food()
            try:
                window.addstr(food_snake.y_position, food_snake.x_position, type_of_food)
            except:
                continue
        elif (tail_snake.x_position == food_snake.x_position) and (tail_snake.y_position == food_snake.y_position):
            if type_of_food is "+":
                
                if actual_level is 1:
                    level1.push(food_snake.x_position, food_snake.y_position)
                elif actual_level is 2:
                    level2.push(food_snake.x_position, food_snake.y_position)
                elif actual_level is 3:
                    level3.push(food_snake.x_position, food_snake.y_position)

                player_selected.score = player_selected.score + 1
                window.addstr(0, 4, "Score : " + str(player_selected.score) + "  ")
            elif type_of_food is "*":
                window.nodelay(0)

                if snake_list.size > 3:
                    snake_list.delete_in_front()
                    snake_list.delete_in_front()

                if player_selected.score > 0:
                    player_selected.score = player_selected.score - 1
                    window.addstr(0, 4, "Score : " + str(player_selected.score) + "  ")

                if actual_level is 1:
                    level1.pop()
                elif actual_level is 2:
                    level2.pop()
                elif actual_level is 3:
                    level3.pop()


                refresh_snake(window)
                window.nodelay(1)
     

            food_snake = food(height, width)
            type_of_food = random_food()
            try:
                window.addstr(food_snake.y_position, food_snake.x_position, type_of_food)
            except:
                continue
        else:
            last = snake_list.tail   
            window.addstr(last.position.y_position, last.position.x_position, " ")
            snake_list.delete_in_back()

        


        #VERIFY IF THE SNAKE IS DEAD
        if verify_snake_dead():
            window.addstr( int(height/2), int((width/2) - len("Game Over")/2) ,"Game Over")
            window.addstr( int(height/2), int((width/2) - len("[Press ESC to Save Score]")/2) ,"[Press ESC to Save Score]")
            window.nodelay(0)

            while 1:
                k = window.getch()
                if k is 27:
                    global scoreboard_queue
                    if(scoreboard_queue.size is 10):
                        scoreboard_queue.dequeue
                    scoreboard_queue.enqueue(player_selected.name, player_selected.score)
                    window.clear()
                    menu(window,0)
                    break
            break
        window.refresh()

def reports_window(window):
    global level1, level2, level3
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
            if actual_level is 1:
                level1.graph("Level 1")
            elif actual_level is 2:
                level2.graph("Level 2")
            elif actual_level is 3:
                level3.graph("Level 3")
        elif key == 51:            
            scoreboard_queue.graph()
        elif key == 52:
            players_list.graph()
        elif key == 27:
            window.clear()
            menu(window, 3)
            break

def user_selection(window):
    window.nodelay(0)
    window.timeout(-5)
    global players_list, player_selected
    player = player_selected
    if player is None:
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

def window_score_board(window):
    global scoreboard_queue
    x, y = defaultSetting(window)
    setTitle(window, "Snake Reloaded - Scoreboard", x)
    window.addstr(y - 15, x("------- SCOREBOARD -------") , "------- SCOREBOARD -------")

    if scoreboard_queue is None or scoreboard_queue.size == 0:
        window.addstr(y - 10, x("THE SCOREBOARD IS EMPTY"), "THE SCOREBOARD IS EMPTY")
    else:
        aux_head = scoreboard_queue.head
        cont = 10
        pos = 1
        while aux_head is not None:
            window.addstr(y - cont, x("------- SCOREBOARD -------"), "{}. {} ----> {} Points".format(pos, aux_head.player.name.strip(), aux_head.player.score))
            aux_head = aux_head.next
            cont -= 2
            pos += 1


    window.addstr(y , x("PRESS KEY [ESC] TO BACK TO MAIN MENU"), "PRESS KEY [ESC] TO BACK TO MAIN MENU")

    while 1:
        key = window.getch()

        if key == 27:
            window.clear()
            menu(window,1)
            window.refresh()
            break

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
            elif opt_selected is 1:
               window_score_board(window)
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