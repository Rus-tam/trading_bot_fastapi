from datetime import datetime

current_time = round(datetime.utcnow().timestamp() * 1000)

for i in range(3, 0, -1):
    start_time = current_time - 1000 * 60000 * i
    end_time = start_time + 1000 * 60000

    normal_start_time = datetime.fromtimestamp(start_time / 1000)
    normal_end_time = datetime.fromtimestamp(end_time / 1000)

    print(normal_start_time)
    print(normal_end_time)
    print("TTT", end_time - start_time)
    print(" ")

    current_time = end_time
    end_time = 0
