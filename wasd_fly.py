from pioneer_sdk import Pioneer, Camera
import cv2
import numpy as np
import time
import math

pioneer_mini = Pioneer()
camera = Camera()
min_v = 1300
max_v = 1700
d = 8
numbers_of_selections = [0] * d
sums_of_rewards = [0] * d
dict_of_commands = {0 : 'w', 1 : 's', 2 : 'a', 3 : 'd',
                        4 : 'q', 5 : 'e', 6 : 'i', 7 : 'k'}



def ucb_where_to_fly(square, n = 0):
    ad = 0
    max_upper_bound = 0
    for i in range(0, d):
        if (numbers_of_selections[i] > 0):
            average_reward = sums_of_rewards[i] / numbers_of_selections[i]
            delta_i = math.sqrt(3/2 * math.log(n + 1) / numbers_of_selections[i])
            upper_bound = average_reward + delta_i
        else:
            upper_bound = 1e400
        if upper_bound > max_upper_bound:
            max_upper_bound = upper_bound 
            ad = i 
    numbers_of_selections[ad] = numbers_of_selections[ad] + 1
    reward = square 
    sums_of_rewards[ad] = sums_of_rewards[ad] + reward 
    n += 1
    return(ad)

FLAG = False

def detection_of_bottle(camera_frame):
    blob = cv2.dnn.blobFromImage(camera_frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    for out in outs:
        for detection in out:            
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] == 'bottle':
                return True
    return False


if __name__ == "__main__":
    print(
        """
    1 -- arm
    2 -- disarm
    3 -- takeoff
    4 -- land
    ↶q  w↑  e↷    i-↑
    ←a      d→     k-↓
        s↓"""
    )

    try:
        net = cv2.dnn.readNet('yolov3-tiny.weights', 'yolov3-tiny.cfg')
        with open('coco.names', 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

        while True:
            ch_1 = 1500
            ch_2 = 1500
            ch_3 = 1500
            ch_4 = 1500
            ch_5 = 2000
            frame = camera.get_frame()
            if frame is not None:
                camera_frame = cv2.imdecode(
                    np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR
                )
                if FLAG:
                    print("working...")
                    if detection_of_bottle(camera_frame):
                                print('see a bottle')
                                """w = int(detection[2] * 416)
                                h = int(detection[3] * 416)
                                sqare = w * h
                                result_action = ucb_where_to_fly(sqare)
                                if dict_of_commands[result_action] == "w":
                                    ch_3 = min_v
                                if dict_of_commands[result_action] == "s":  
                                    ch_3 = max_v
                                if dict_of_commands[result_action] == "a":
                                    ch_4 = min_v
                                if dict_of_commands[result_action] == "d":
                                    ch_4 = max_v
                                if dict_of_commands[result_action] == "q":
                                    ch_2 = 2000
                                if dict_of_commands[result_action] == "e":
                                    ch_2 = 1000
                                if dict_of_commands[result_action] == "i":
                                    ch_1 = 2000
                                if dict_of_commands[result_action] == "k":
                                    ch_1 = 1000"""   
                    else:
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
            elif key == ord(' '):
                FLAG = not(FLAG)
            elif key == ord('b'):
                print(pioneer_mini.get_battery_status())
            
                
            pioneer_mini.send_rc_channels(
                channel_1=ch_1,
                channel_2=ch_2,
                channel_3=ch_3,
                channel_4=ch_4,
                channel_5=ch_5,
            )
            time.sleep(0.02)
            #print(FLAG)
    finally:
        time.sleep(1)
        pioneer_mini.land()

        pioneer_mini.close_connection()
        del pioneer_mini