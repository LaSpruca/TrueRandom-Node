from odrv_wrapper import Odrive_Arm
import time
import random
import dice_content

odrive_enabled = True


print("Initialize")
if odrive_enabled:
    arm = Odrive_Arm()
print("ODrive Booted")

ODRIVE_LOCK = False


def roll_dice():
    for i in range(10):
        x_direction = i%2==0
        x_pos = random.random()/2+0.5*x_direction
        pos = (x_pos,random.random(),random.random())
        arm.move_traj(pos)
    arm.move_traj((0.5,0.5,0.5))
    time.sleep(3)

def roll_read_dice_procedure():
    global ODRIVE_LOCK
    while ODRIVE_LOCK:
        time.sleep(random.random()*2)
    ODRIVE_LOCK = True
    # Roll Dice
    if odrive_enabled:
        roll_dice()
    else:
        time.sleep(1)
    # Read dice
    result = dice_content.get_dice()
    ODRIVE_LOCK = False
    return result
