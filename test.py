import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN


stdscr = curses.initscr()

curses.curs_set(0) #ESTO HACE QUE NO SE MUESTRA EL CURSOS
curses.noecho() #EVITA QUE SE MUESTREN LOS CARACTERES QUE SE ESTAN ESCRIBIENDO EN LA PANTALLA 
curses.cbreak() #EVITA QUE SE TENGA QUE HACER ENTER PARA UNA ENTRADAM Y TOMA CADA CARACTER COMO UNA ENTRADA
stdscr.keypad(True) #NOS PERMITE PODER UTILIZAR LAS TECLAS Y VALORES ESPECIALES COMO ESC, DERECHA, IZQ, ABAJO, ARRIBA

stdscr.addstr(5, 5, "Hello")
stdscr.refresh()
curses.napms(3000)


#RESTABLECER TODAS LAS PROPIEDADES
curses.curs_set(1) #RESTABLECE EL CURSOS PARA QUE SE MUESTRE
curses.echo()
curses.nocbreak()
stdscr.keypad(False)
curses.endwin() #CIERRA LA VENTANA Y RESTABLECE TODO








#stdscr = curses.initscr()
#win = curses.newwin( 25, 25, 0, 0 )
#win.keypad(True)
#curses.noecho()
#curses.curs_set(0)
#win.border(0)
#win.nodelay(True)

#INITIAL SETTINGS
#key = KEY_RIGHT
#pos_x = 10
#pos_y = 10
#win.addch(pos_y,pos_x,'*')

#while key != 27:
#    win.timeout(100)
#    keystroke = win.getch()
#    if keystroke is not -1:
#        key = keystroke
#        #win.addch(pos_y,pos_x,' ')       #erase last dot
#        
#        if key == KEY_RIGHT:                #right direction
#            pos_x = pos_x + 1               #pos_x increase
#        elif key == KEY_LEFT:               #left direction
#            pos_x = pos_x - 1               #pos_x decrease
#        elif key == KEY_UP:                 #up direction
#            pos_y = pos_y - 1               #pos_y decrease
#        elif key == KEY_DOWN:               #down direction
#            pos_y = pos_y + 1               #pos_y increase
#        win.addch(pos_y,pos_x,'*')       #draw new dot

#curses.endwin()