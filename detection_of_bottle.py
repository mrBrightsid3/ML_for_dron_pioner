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
