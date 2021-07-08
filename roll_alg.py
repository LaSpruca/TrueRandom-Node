from odrv_wrapper import Odrive_Arm
import time
import random
import dice_content
import statistics

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
        arm.move_blocking(pos)
    arm.move_blocking((0.5,0.5,0.5))
    time.sleep(1)

def roll_read_dice_procedure():
    global ODRIVE_LOCK
    while ODRIVE_LOCK:
        time.sleep(random.random()*2)
    ODRIVE_LOCK = True
    # Roll Dice
    if odrive_enabled:
        roll_dice()
    else:
        print("Using Odrive")
        time.sleep(1)

    result = dice_content.get_dice()
    print("\n\nAVERAGED RESULT:",result)
    f = open("state.txt","w")
    f.write("Last Roll: "+ str(result))

    ODRIVE_LOCK = False
    
    f.close()
    return result

if __name__=="__main__":
    while True:
        roll_read_dice_procedure()
        time.sleep(2)
