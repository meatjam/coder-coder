import threading
import time
import math

lock = threading.Lock()


def get_formatted_time(seconds):
    h = math.floor(seconds / 3600)
    seconds = seconds - h * 3600
    m = math.floor(seconds / 60)
    seconds = seconds - m * 60
    return str(h).rjust(2, '0') + ':' + str(m).rjust(2, '0') + ':' + str(round(seconds)).rjust(2, '0')


class CounterPrint:
    def __init__(self, total_num: int, prompt_prefix=''):
        self.t = threading.Thread(target=self.__counter)
        self.total_num = total_num
        self.prefix = prompt_prefix
        self.count = 0
        self.interval = 0.5
        self.start_time = -1

    def start(self):
        self.start_time = time.time()
        self.t.start()

    def join(self):
        self.t.join()
        print('\n')

    def __counter(self):
        rjust_num = 9 + len(str(self.total_num))
        while True:
            lock.acquire()
            percentage = self.count / self.total_num
            past_seconds = time.time() - self.start_time
            left_seconds = 999999 if percentage == 0 else past_seconds / percentage - past_seconds
            print('\r' + self.prefix, ' 已完成:',
                (str(self.count) + ' | ' + str(round(100 * percentage, 2)) + '%').rjust(rjust_num), '总计:',
                self.total_num, '剩余时间:', get_formatted_time(left_seconds),
                '已用时间:', get_formatted_time(past_seconds),
                end='', flush=True)
            lock.release()
            if self.count >= self.total_num:
                break
            time.sleep(self.interval)
