import socket
import time

data = [0, 1, 2, 3, 4, 5, 7, 0, 1, 2, 3, 4, "end"]  # k = 3
N = 4  # window_size
buffer = []


# index = 0


def delete_before(num):
    for d in buffer.copy():
        if d == int(num):
            break
        else:
            buffer.remove(d)


def handle_ack(acked_data):
    ack_type = acked_data.split("-")[0]
    ack_number = acked_data.split("-")[1]
    if ack_type == "RR":
        delete_before(ack_number)
    elif ack_type == "SREJ":
        buffer.clear()
        buffer.append(int(ack_number))


def client():
    index = 0
    ip = "127.0.0.1"
    port = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    while index < len(data):
        # sending frames
        if len(buffer) < N:
            while len(buffer) < N and index < len(data):
                buffer.append(data[index])
                index += 1

            print(f"frames send by client: {buffer}")
            for d in buffer:
                time.sleep(.5)
                s.send(str(d).encode())

            s.settimeout(4)

        try:
            acked_data = s.recv(1024).decode()
            print(f"acked data in client: {acked_data}")
            handle_ack(acked_data)
        except socket.timeout:
            print("time out !!!! ----> send RR(p=1)")
            s.send(f"RR(p=1)".encode())

            acked_data = s.recv(1024).decode()
            print(f"acked data in response of RR(p=1): {acked_data}")
            should_send_num = acked_data.split("-")[1]
            delete_before(should_send_num)

        time.sleep(5)


time1 = time.time()
client()
time2 = time.time()
duration = time2 - time1
print(f"duration {duration}")
