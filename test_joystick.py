import pygame as pg

FRAME_RATE = 1
WIN_SIZE = [100, 100]

def handle_event(event):
    if event.type == pg.JOYBUTTONDOWN:
        print('PressButton', event.button)
    if event.type == pg.JOYAXISMOTION:
        if abs(event.value) >= 0.3:
            #print('AxisMotion', event.axis, event.value)
            if abs(round(event.value, 2)) == 1:
                if event.axis == 2:
                    if event.value <= 0:
                        print('moving left')
                    else:
                        print('moving right')
                elif event.axis == 3:
                    if event.value <= 0:
                        print('moving up')
                    else:
                        print('moving down')     

def main():
    pg.init()
    screen = pg.display.set_mode(WIN_SIZE)
    clock = pg.time.Clock()
    joystick = pg.joystick.Joystick(0)
    joysticks = {}
    print('NameJoystick', joystick.get_name())
    while True:
        for event in pg.event.get():
            handle_event(event)
            #print('DetectEvent', event, event.type)
            #print()
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.KEYDOWN:
                #print('key', event.unicode)
                pass

            if event.type == pg.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joystick = pg.joystick.Joystick(event.device_index)
                joysticks[joystick.get_instance_id()] = joystick
                #print(f"Joystick {joystick.get_instance_id()} connencted")

            if event.type == pg.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                #print(f"Joystick {event.instance_id} disconnected")
        clock.tick(FRAME_RATE)

if __name__ == '__main__':
    main() 