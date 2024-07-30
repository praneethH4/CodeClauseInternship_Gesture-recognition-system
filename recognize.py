def get_landmark_position(landmark, width, height):
    return int(landmark.x * width), int(landmark.y * height)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape
            thumb_tip = get_landmark_position(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP], w, h)
            index_finger_tip = get_landmark_position(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP], w, h)

            cv2.circle(frame, thumb_tip, 5, (0, 255, 0), -1)
            cv2.circle(frame, index_finger_tip, 5, (0, 255, 0), -1)

            distance = np.linalg.norm(np.array(thumb_tip) - np.array(index_finger_tip))
            if distance < 50:  # You can adjust the threshold
                cv2.putText(frame, 'Gesture: Pinch', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, 'Gesture: Open', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
