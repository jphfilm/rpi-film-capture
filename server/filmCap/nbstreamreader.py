from threading import Thread
from Queue import Queue, Empty

class NonBlockingStreamReader:

    def __init__(self, stream, event):
        self.strm = stream
        self.que = Queue()
	self.event = event

        def populateQueue(stream, queue, event):
            while not event.is_set():
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
		     break

        self.thr = Thread(target = populateQueue,
                args = (self.strm, self.que, self.event))
        self.thr.daemon = True
        self.thr.start() #start collecting lines from the stream

    def readline(self, timeout = None):
        try:
            return self.que.get(block = timeout is not None,
                    timeout = timeout)
        except Empty:
            return None

class UnexpectedEndOfStream(Exception): pass
