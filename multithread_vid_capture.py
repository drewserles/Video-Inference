import threading
import queue
import cv2
import time

# Run a video capture on a file or video device in a separate thread
# bufferless VideoCapture
class VideoCaptureHD():
    def __init__(self, file_name):
        self.run = True
        
        self.cap = cv2.VideoCapture(file_name)
        
        # Video parameters
        self.frame_rate = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.frame_time = 1/self.frame_rate
        
        self.q = queue.Queue()
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True # If a thread is a daemon it exits as soon the main process exits
        self.t.start()

  # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while 1:
            t1 = time.time()
            
            # Flag used to kill the process
            if not self.run:
                break
                
            ret, frame = self.cap.read()
            
            # Nothing returned - we're at the end of the video
            if not ret:
                self.run = False
                break

            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass

            self.q.put(frame)
            
            # Reading from hard drive. Sleep for required amount so video streams at regular fps
            sleep_time = self.frame_time - (time.time() - t1)
            if sleep_time > 0:
                time.sleep(sleep_time)

    # External method to grab most recent frame in the queue
    def read(self):
        if not self.q.empty():
            return self.q.get()
        else:
            return None
    
    # External stop and cleanup
    def stop(self):
        self.run = False
        self.cap.release()