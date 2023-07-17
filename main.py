from pioneer_sdk import Pioneer, Camera
import cv2
import numpy as np
import time
from get_coordinates import get_coordinates

pioneer_mini = Pioneer()
camera = Camera()
min_v = 1300
max_v = 1700
FLAG = False
sum_alerts = 0
SAW_A_BOTTLE_FIRST_TIME = False
x = None


def fly_to_bottle(x, y):
    ch_1 = 1500
    ch_2 = 1500
    ch_3 = 1500
    ch_4 = 1500
    ch_5 = 2000
    img_width = 480
    img_height = 320
    center_x_coef = 0.3
    center_y_coef = 0.3
    left_x_bound = img_width * center_x_coef
    right_x_bound = img_width - img_width * center_x_coef
    top_y_bound = img_height * center_y_coef
    bottom_y_bound = img_height - img_height * center_y_coef
    if x:
        if (
            x >= left_x_bound
            and x <= right_x_bound
            and y <= bottom_y_bound
            and y >= top_y_bound
        ):
            ch_3 = 1400
            print("вперед")
        if x < left_x_bound:
            ch_2 = 1650
            print("влево")
        elif x > right_x_bound:
            ch_2 = 1350
            print("вправо")
        if y < top_y_bound:
            ch_1 = 1670
            print("вверх")
        elif y > bottom_y_bound:
            ch_1 = 1450
            print("вниз")
        pioneer_mini.send_rc_channels(
            channel_1=ch_1,
            channel_2=ch_2,
            channel_3=ch_3,
            channel_4=ch_4,
            channel_5=ch_5,
        )


if __name__ == "__main__":
    print(
        """
    1 -- arm
    2 -- disarm
    3 -- takeoff
    4 -- land
    b -- check battery
    space -- on/off autopilot
    ↶q  w↑  e↷    i-↑
    ←a      d→     k-↓
        s↓"""
    )

    try:
        while True:
            if not (SAW_A_BOTTLE_FIRST_TIME):
                ch_1 = 1500
                ch_2 = 1500
                ch_3 = 1500
                ch_4 = 1500
                ch_5 = 2000
            if FLAG:
                frame = camera.get_cv_frame()
                x, y = get_coordinates(frame)
                if SAW_A_BOTTLE_FIRST_TIME:  # если он ее видит не в первый раз
                    fly_to_bottle(x, y)
                elif x and not (
                    SAW_A_BOTTLE_FIRST_TIME
                ):  # если он ее видит в первый раз
                    SAW_A_BOTTLE_FIRST_TIME = True
                    print("see a marker")
                    pioneer_mini.send_rc_channels(
                        channel_1=ch_1,
                        channel_2=ch_2,
                        channel_3=ch_3,
                        channel_4=ch_4,
                        channel_5=ch_5,
                    )

                elif not (SAW_A_BOTTLE_FIRST_TIME):  # поиск бутылки самый первый раз
                    ch_1 = 1600  # поднятие
                    pioneer_mini.send_rc_channels(
                        channel_1=ch_1,
                        channel_2=ch_2,
                        channel_3=ch_3,
                        channel_4=ch_4,
                        channel_5=ch_5,
                    )
                    # ch_2 = 1640  # кручени влево

                # elif SAW_A_BOTTLE_FIRST_TIME:

                #      # если он не видит но видел ее хоть раз
                #     # ch_2 = 1475  # медленное кручение вправо
                #     pass
            frame = camera.get_cv_frame()

            cv2.imshow("pioneer_camera_stream", frame)
            key = cv2.waitKey(1)
            if key == 27:  # esc
                print("esc pressed")
                cv2.destroyAllWindows()
                pioneer_mini.land()
                break
            elif key == ord("1"):
                pioneer_mini.arm()
            elif key == ord("2"):
                pioneer_mini.disarm()
            elif key == ord("3"):
                time.sleep(2)
                pioneer_mini.arm()
                time.sleep(1)
                pioneer_mini.takeoff()
                time.sleep(2)
            elif key == ord("4"):
                time.sleep(2)
                pioneer_mini.land()
                time.sleep(2)
            elif key == ord("w"):
                ch_3 = min_v
            elif key == ord("s"):
                ch_3 = max_v
            elif key == ord("a"):
                ch_4 = min_v
            elif key == ord("d"):
                ch_4 = max_v
            elif key == ord("q"):
                ch_2 = 2000
            elif key == ord("e"):
                ch_2 = 1000
            elif key == ord("i"):
                ch_1 = 2000
            elif key == ord("k"):
                ch_1 = 1000
            elif key == ord(" "):
                FLAG = not (FLAG)
                if FLAG:
                    print("autopilot on")
                else:
                    print("autopilot off")
            elif key == ord("b"):
                print(pioneer_mini.get_battery_status())
            # print(ch_2)
            if x or not (FLAG):
                pioneer_mini.send_rc_channels(
                    channel_1=ch_1,
                    channel_2=ch_2,
                    channel_3=ch_3,
                    channel_4=ch_4,
                    channel_5=ch_5,
                )
            time.sleep(0.02)
    finally:
        time.sleep(1)
        pioneer_mini.land()

        pioneer_mini.close_connection()
        del pioneer_mini
