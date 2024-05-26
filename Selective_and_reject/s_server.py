import socket
import time

N = 4
data = []
buffer = []
timeSleep = [0, 0, 5, 0, 0]


def add_to_data():
    sort_buffer()

    for d in buffer.copy():
        if d == find_next_num():
            data.append(d)
            buffer.remove(d)
        else:
            print(f"data in server: {data}")
            return f"SREJ-{find_next_num()}"
    return f"RR-{find_next_num()}"


def sort_buffer():

    buffer.sort()
    if buffer.__contains__('0') and buffer.__contains__('7'):
        first_index = 0
        for i in range(0, len(buffer)):
            if int(buffer[i]) != int(buffer[i + 1]) - 1:
                first_index = i + 1
                break

        new_buffer = []
        new_buffer.extend(buffer[first_index:len(buffer)])
        new_buffer.extend(buffer[0:first_index])
        buffer.clear()
        buffer.extend(new_buffer)


def find_next_num():
    if len(data) == 0 or int(data[-1]) == 7:
        return str(0)
    else:
        return str(int(data[-1]) + 1)


def server():
    time_index = 0
    without_ack_frames = 0

    ip = "127.0.0.1"
    port = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))

    s.listen()
    print("Listening")
    conn, addr = s.accept()
    send_data = 0

    while send_data != "end":
        send_data = conn.recv(1024).decode()
        # print(f"data received in server: {send_data}")

        if send_data == "RR(p=1)":
            print(f"server should send RR-{find_next_num()} in response of RR(p=1)")
            conn.send(f"RR-{find_next_num()}".encode())
            continue

        if send_data != "end":
            without_ack_frames += 1
            buffer.append(send_data)

        if without_ack_frames == N or send_data == "end":
            print(f"buffer of received frames in server: {buffer}")
            delay = timeSleep[time_index]
            ack_str = add_to_data()

            if delay > 4:
                time.sleep(4)
            else:
                time.sleep(delay)
                print(f"server send {ack_str} to client")
                conn.send(ack_str.encode())

            time_index += 1
            without_ack_frames = 0


server()
