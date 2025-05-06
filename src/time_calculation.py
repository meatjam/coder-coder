from time import localtime, mktime, strptime, time, sleep


def wait_sleep(new_reserve_hm=(8, 30), start_ready_seconds=3) -> None:
    current_time = localtime()
    if current_time.tm_hour > new_reserve_hm[0] or (
            current_time.tm_hour == new_reserve_hm[0] and current_time.tm_min > new_reserve_hm[1]):
        ts = round(mktime(current_time)) + 86400
        target_time = localtime(ts)
    else:
        target_time = localtime()
    target_time = strptime(f'{target_time.tm_year}-{target_time.tm_mon}-{target_time.tm_mday} {new_reserve_hm[0]}:{new_reserve_hm[1]}:00', '%Y-%m-%d %H:%M:%S')
    target_ts = round(mktime(target_time)) - start_ready_seconds
    target_time = localtime(target_ts)
    print(f'预订开始时间：{target_time.tm_year}-{target_time.tm_mon}-{target_time.tm_mday} {target_time.tm_hour}:{target_time.tm_min}:{target_time.tm_sec}')
    print('等待中......')
    while True:
        seconds_left = round(target_ts - time())
        if seconds_left <= 0:
            print('\n倒计时结束，开始执行！')
            return
        left_h = seconds_left // 3600
        left_m = seconds_left % 3600 // 60
        left_s = seconds_left % 60
        print(f'\r距离开始还剩{left_h}时{left_m}分{left_s}秒', end='')
        sleep(1)
