import time
import mouse
import random
while True:
    get_position_of_mouse = mouse.get_position()
    time.sleep(10)
    new_position = mouse.get_position()
    go_to = random.randint(10,300)
    if get_position_of_mouse == new_position:
       mouse.move(go_to,go_to)