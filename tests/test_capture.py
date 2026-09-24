import cv2
from capture.capture import Capture, CaptureError

cap_obj = None

print("Commands: create | start | frame | stop | quit")

while True:
    command = input("> ").strip().lower()

    if command == "create":
        cap_obj = Capture()
        print("Capture object created.")

    elif command == "start":
        if cap_obj is None:
            print("No capture object yet — run 'create' first.")
            continue
        try:
            cap_obj.start()
            print("Camera started.")
        except CaptureError as e:
            print(f"Error starting camera: {e}")

    elif command == "frame":
        if cap_obj is None:
            print("No capture object yet — run 'create' first.")
            continue
        try:
            frame = cap_obj.get_frame()
            print(f"Got frame with shape: {frame.shape}")
            cv2.imshow("Test Frame", frame)
            cv2.waitKey(1)
        except CaptureError as e:
            print(f"Error getting frame: {e}")

    elif command == "stop":
        if cap_obj is None:
            print("No capture object yet — run 'create' first.")
            continue
        cap_obj.stop()
        cv2.destroyAllWindows()
        print("Camera stopped.")

    elif command == "quit":
        if cap_obj is not None:
            cap_obj.stop()
        cv2.destroyAllWindows()
        print("Exiting.")
        break

    else:
        print("Unknown command. Use: create | start | frame | stop | quit")
