import socket
import time

N = 4
data = []
buffer = []
timeSleep = [0, 0, 5, 0, 0]


def add_to_data():
    for d in buffer:
        if d == find_next_num():
            data.append(d)
        else:
            return f"REJ-{find_next_num()}"
    return f"RR-{find_next_num()}"


def find_next_num():
    if len(data) == 0 or int(data[-1]) == 7:
        return str(0)
    else:
        return str(int(data[-1]) + 1)


def server():
    time_index = 0

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
            buffer.append(send_data)

        if len(buffer) == N or send_data == "end":
            print(f"buffer of received frames in server: {buffer}")
            delay = timeSleep[time_index]
            ack_str = add_to_data()
            buffer.clear()

            if delay > 4:
                time.sleep(4)
            else:
                time.sleep(delay)
                print(f"server send {ack_str} to client")
                conn.send(ack_str.encode())

            time_index += 1


server()
