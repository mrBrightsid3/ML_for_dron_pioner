from pioneer_sdk import Pioneer, Camera
import cv2
import numpy as np
import time

pioneer_mini = Pioneer()
camera = Camera()
min_v = 1300
max_v = 1700
FLAG = False
sum_alerts = 0


def pendulum(sum_alerts):
    print("pendulum")
    right_pwoer = 1470
    left_power = 1530
    while True:
        ch_1 = 1500
        ch_2 = 1500
        ch_3 = 1500
        ch_4 = 1500
        ch_5 = 2000
        TURN = False
        confidence, class_id, camera_frame = detection_of_bottle()
        if confidence > 0.5 and classes[class_id] == "bottle":
            print("see a bottle")
            sum_alerts += 1
            TURN = not (TURN)
            time.sleep(1)
        elif TURN == True:
            right_pwoer += 5
            ch_2 = right_pwoer  # кручение вправо
            sum_alerts = 0
        elif TURN == False:
            left_power -= 5
            ch_2 = left_power  # кручение влево
            sum_alerts = 0

        pioneer_mini.send_rc_channels(
            channel_1=ch_1,
            channel_2=ch_2,
            channel_3=ch_3,
            channel_4=ch_4,
            channel_5=ch_5,
        )
        time.sleep(0.02)
        if sum_alerts > 50:
            fly_to_bottle()


def fly_to_bottle():
    print("fly to bottle")


def detection_of_bottle(camera):
    frame = camera.get_frame()
    if frame is not None:
        camera_frame = cv2.imdecode(
            np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR
        )
        if FLAG:
            print("working...")
            blob = cv2.dnn.blobFromImage(
                camera_frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False
            )
            net.setInput(blob)
            outs = net.forward(output_layers)
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                return confidence, class_id, camera_frame
    return 0, None, camera_frame


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
            confidence, class_id, camera_frame = detection_of_bottle(camera)
            if confidence > 0.5 and classes[class_id] == "bottle":
                print("see a bottle")
                time.sleep(6)
                pendulum()

            else:
                ch_1 = 1590  # поднятие
                ch_2 = 1600  # кручени
                pass

                cv2.imshow("pioneer_camera_stream", camera_frame)
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
