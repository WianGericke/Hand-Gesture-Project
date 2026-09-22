# importing dependencies
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2
import time

# Hand line drawing utils
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

# Hand line drawing function
def draw_landmarks_on_image(rgb_image, detection_result):
  hand_landmarks_list = detection_result.hand_landmarks
  handedness_list = detection_result.handedness
  annotated_image = np.copy(rgb_image)

  # Loop through the detected hands to visualize.
  for idx in range(len(hand_landmarks_list)):
    hand_landmarks = hand_landmarks_list[idx]
    handedness = handedness_list[idx]

    # Conversion from new data structure to legacy for ease of rendering
    landmark_list_proto = landmark_pb2.NormalizedLandmarkList()

    for idx in range(len(hand_landmarks)):
        finger_point = hand_landmarks[idx]
        point_x, point_y, point_z = finger_point.x, finger_point.y, finger_point.z
        landmark = landmark_pb2.NormalizedLandmark(x=point_x, y=point_y, z=point_z)
        landmark_list_proto.landmark.append(landmark)

    # Draw the hand landmarks.
    mp_drawing.draw_landmarks(
      annotated_image,
      landmark_list_proto,
      mp_hands.HAND_CONNECTIONS,
      mp_drawing_styles.get_default_hand_landmarks_style(),
      mp_drawing_styles.get_default_hand_connections_style())

    # Get the top left corner of the detected hand's bounding box.
    height, width, _ = annotated_image.shape
    x_coordinates = [landmark.x for landmark in hand_landmarks]
    y_coordinates = [landmark.y for landmark in hand_landmarks]
    text_x = int(min(x_coordinates) * width)
    text_y = int(min(y_coordinates) * height) - MARGIN

    if handedness[0].category_name == "Left":
       handedness[0].category_name = "right"
    else:
       handedness[0].category_name = "left"

    # Draw handedness (left or right hand) on the image.
    cv2.putText(annotated_image, f"{handedness[0].category_name}",
                (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

  return annotated_image

# Creating global variables
# Cv2 variable for controlling webcam
feed = cv2.VideoCapture(0)

# Create HandLandmark objects to track hands
BaseOptions = mp.tasks.BaseOptions
handLandmarker = mp.tasks.vision.HandLandmarker
handLandmarker_options = mp.tasks.vision.HandLandmarkerOptions
vision_running_mode = mp.tasks.vision.RunningMode

options = handLandmarker_options(
    base_options = BaseOptions(
        model_asset_path='hand_landmarker.task',
        delegate=BaseOptions.Delegate.CPU
    ),
    running_mode = vision_running_mode.VIDEO,
    num_hands = 2)

landmarker = handLandmarker.create_from_options(options)

# Camera test
# Camera not working
if not feed.isOpened():
    print("Camera can't be opened :()")
    exit()

# create a start time for video timestamps
start_time = time.time()

# Camera is working
while True:
    # Frame-by-frame capture
    ret, frame = feed.read()

    # If frame cannot be found
    if not ret:
        print("Can't retrieve frame...\nExiting...\n")
        break

    # IMAGE PROCESSING
    # Capture current time for timestamp
    # Open cv frame from camera feed is to be flipped for UX
    curr_time = time.time() - start_time
    curr_time = int(curr_time*1000)
    flipped_frame = cv2.flip(frame, 1)

    # flipped frame is then converted into a MediaPipe image for hand analysis
    rgb_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    hand_landmarker_results = landmarker.detect_for_video(mp_image, curr_time)

    annotated_image = draw_landmarks_on_image(flipped_frame, hand_landmarker_results)

    cv2.imshow("Video Feed (Flipped)", annotated_image)

    # quit option
    if (cv2.waitKey(1) == ord('q')):
        break

# Close down opencv
feed.release()
cv2.destroyAllWindows()