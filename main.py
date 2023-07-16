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


def fly_to_bottle():
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
    while True:
        frame = camera.get_cv_frame()
        x, y = get_coordinates(frame)
        if x:
            if (
                x >= left_x_bound
                and x <= right_x_bound
                and y <= bottom_y_bound
                and y >= top_y_bound
            ):
                ch_3 = 1600
                print("вперед")
            if x < left_x_bound:
                ch_2 = 1600
                print("влево")
            elif x > right_x_bound:
                ch_2 = 1400
                print("вправо")
            if y < top_y_bound:
                ch_1 = 1600
                print("вверх")
            elif y > bottom_y_bound:
                ch_1 = 1400
                print("вниз")
            pioneer_mini.send_rc_channels(
                channel_1=ch_1,
                channel_2=ch_2,
                channel_3=ch_3,
                channel_4=ch_4,
                channel_5=ch_5,
            )
        else:
            return 0  # потерял


def detection_of_bottle(i_want_return_detection=False):
    frame = camera.get_frame()
    confidence = 0
    class_id = None
    if frame is not None:
        camera_frame = cv2.imdecode(
            np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR
        )

        print("working...")
        blob = cv2.dnn.blobFromImage(
            camera_frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False
        )
        net.setInput(blob)
        outs = net.forward(output_layers)
        for out in outs:
            for detection in out:
                scores = detection[5:]
                current_class_id = np.argmax(scores)
                current_confidence = scores[current_class_id]
                if current_confidence > confidence:
                    confidence = current_confidence
                    class_id = current_class_id
        i_see_the_bottle = confidence > 0.5 and classes[class_id] == "bottle"
    if i_want_return_detection:
        return detection, i_see_the_bottle
    else:
        return confidence, class_id, camera_frame


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
        net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
        with open("coco.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

        while True:
            ch_1 = 1500
            ch_2 = 1500
            ch_3 = 1500
            ch_4 = 1500
            ch_5 = 2000
            if FLAG:
                # confidence, class_id, camera_frame = detection_of_bottle()
                frame = camera.get_cv_frame()
                x, y = get_coordinates(frame)
                if x and SAW_A_BOTTLE_FIRST_TIME:  # если он ее видит не в первый раз
                    fly_to_bottle()
                elif x and not (
                    SAW_A_BOTTLE_FIRST_TIME
                ):  # если он ее видит в первый раз
                    SAW_A_BOTTLE_FIRST_TIME = True
                    print("see a bottle")
                    pioneer_mini.send_rc_channels(
                        channel_1=ch_1,
                        channel_2=ch_2,
                        channel_3=ch_3,
                        channel_4=ch_4,
                        channel_5=ch_5,
                    )

                    time.sleep(5)
                    print("поспали")
                    # тут туплю, после сна че делаем?

                elif not (
                    SAW_A_BOTTLE_FIRST_TIME
                ):  # если он не видит + если он ни разу не видел
                    ch_1 = 1570  # поднятие
                    ch_2 = 1640  # кручени влево
                    # поиск бутылки самый первый раз

                elif SAW_A_BOTTLE_FIRST_TIME:  # если он не видит но видел ее хоть раз
                    ch_2 = 1475  # медленное кручение вправо

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
