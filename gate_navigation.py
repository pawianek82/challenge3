"""Navigate Picar-X through a narrow gate using color detection."""

from time import sleep, time

from picarx import Picarx
from robot_hat import Ultrasonic
from vilib import Vilib

px = Picarx()
ultra = Ultrasonic('D2')  # adjust port if needed

def clamp_number(num, a, b):
    return max(min(num, max(a, b)), min(a, b))

def turn_around(speed: int = 50, duration: float = 1.6) -> None:
    """Rotate the car by roughly 180 degrees."""
    px.set_dir_servo_angle(30)
    px.forward(speed)
    sleep(duration)
    px.set_dir_servo_angle(-30)
    px.forward(speed)
    sleep(duration)
    px.stop()


def drive_forward(distance_time: float = 1.0, speed: int = 40) -> None:
    """Drive straight for a short, timed distance."""
    px.set_dir_servo_angle(0)
    px.forward(speed)
    sleep(distance_time)
    px.stop()


def main() -> None:
    """Turn around, search for the gate and drive through it."""
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display()
    Vilib.color_detect("green")

    # face the gate and move a short distance forward
    turn_around()
    drive_forward()

    pan_angle = 0
    steer = 0

    passed_gate = False
    start_time = time()
    while not passed_gate and time() - start_time < 180:
        distance = ultra.get_distance()
        if distance is not None and distance < 5:
            px.stop()
            sleep(0.05)
            continue

        if Vilib.detect_obj_parameter["color_n"] != 0:
            cx = Vilib.detect_obj_parameter["color_x"]
            cw = Vilib.detect_obj_parameter["color_w"]

            if cw > 200:
                px.set_dir_servo_angle(0)
                px.forward(30)
                sleep(4)
                px.stop()
                passed_gate = True
                continue

            if cx < 300:
                steer -= 2
            elif cx > 340:
                steer += 2
            else:
                steer = 0

            steer = clamp_number(steer, -30, 30)
            px.set_dir_servo_angle(steer)
            px.forward(30)
        else:
            px.stop()
            pan_angle += 5
            if pan_angle > 35:
                pan_angle = -35
            px.set_cam_pan_angle(pan_angle)

        sleep(0.05)


if __name__ == '__main__':
    try:
        main()
    finally:
        Vilib.camera_close()
        px.stop()
        sleep(0.1)
