import threading
import time

class MyThread(threading.Thread):
    def __init__(self, description, handler_detail, title):
      threading.Thread.__init__(self)
      self._description = description
      self._handler_detail = handler_detail
      self._title = title
    def run(self):
        for i in range(3):
            time.sleep(1)
            msg = "I'm "+self.name+' @ '+str(i)
            #print self._description
            ##print self.title
            ##print self.handler_detail
            print msg
def test():
    for i in range(5):
        t = MyThread(1,2,33)
        t.start()
if __name__ == '__main__':
    test()