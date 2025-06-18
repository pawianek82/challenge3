from picarx import Picarx
from time import sleep
from vilib import Vilib
from robot_hat import Ultrasonic

px = Picarx()
ultra = Ultrasonic('D2')  # adjust port if needed

def clamp_number(num, a, b):
    return max(min(num, max(a, b)), min(a, b))

def turn_around(speed=50, duration=1.5):
    px.set_dir_servo_angle(30)
    px.forward(speed)
    sleep(duration)
    px.set_dir_servo_angle(-30)
    px.forward(speed)
    sleep(duration)
    px.stop()


def drive_forward(distance_time=2, speed=40):
    px.set_dir_servo_angle(0)
    px.forward(speed)
    sleep(distance_time)
    px.stop()


def main():
    Vilib.camera_start()
    Vilib.display()
    Vilib.color_detect('green')

    turn_around()
    drive_forward()

    x_angle = 0
    dir_angle = 0

    passed_gate = False
    while not passed_gate:
        if ultra.get_distance() < 10:
            px.stop()
            continue

        if Vilib.detect_obj_parameter['color_n'] != 0:
            cx = Vilib.detect_obj_parameter['color_x']
            cw = Vilib.detect_obj_parameter['color_w']

            if cw > 200:
                px.forward(30)
                sleep(3)
                px.stop()
                passed_gate = True
                break

            if cx < 200:
                dir_angle -= 1
            elif cx > 440:
                dir_angle += 1
            else:
                dir_angle = 0
            dir_angle = clamp_number(dir_angle, -30, 30)
            px.set_dir_servo_angle(dir_angle)
            px.forward(30)
        else:
            px.stop()
            x_angle += 5
            if x_angle > 35:
                x_angle = -35
            px.set_cam_pan_angle(x_angle)

        sleep(0.05)

if __name__ == '__main__':
    try:
        main()
    finally:
        Vilib.camera_close()
        px.stop()
        sleep(0.1)
