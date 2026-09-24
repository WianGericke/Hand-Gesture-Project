# Dependency imports
import cv2


# Error classes for the Capture object class
class CaptureError(Exception):
    "Generic Capture Object error"
    pass

class CameraError(CaptureError):
    "Failure to open camera"
    pass

class FrameRetrievalError(CaptureError):
    "Failure to recveive frame from camera"
    pass

# Capture object class
# Each capture object will receive a camera index for which device to use,
# along with a number of retries to perform in the case a frame pull fails
class Capture:
    def __init__(self, camera_index=0, num_retries=5):
        self.camera = camera_index
        self.retry_limit = num_retries
        self.camera_feed = None

    def start(self):
        if (self.camera_feed is None):
            self.camera_feed = cv2.VideoCapture(self.camera)

            if (not self.camera_feed.isOpened()):
                raise CameraError (f"Camera with index: {self.camera} failed to open")

    def get_frame(self):
        # Check that the capture object has been started so that frames can be pulled
        if (self.camera_feed is None):
            raise FrameRetrievalError (f"Camera with index: {self.camera} is not open, no frame to retrieve")

        # attempt to pull a frame
        ret, frame = self.camera_feed.read()

        # check that a frame was recieved
        if (not ret):
            for i in range(self.retry_limit):
                ret, frame = self.camera_feed.read()
                if ret:
                    return frame
            else:
                raise FrameRetrievalError (f"Camera with index: {self.camera} failed to produce frames")
        return frame

    def stop(self):
        if not (self.camera_feed is None):
            self.camera_feed.release()
            self.camera_feed = None