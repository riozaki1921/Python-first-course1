import socket
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

host = config.get('client', 'client_host')
port = config.getint('client', 'client_port')

def get_user_input():
    print("==========MAILER===========")
    message_to = input("Кому отправим? ")
    message = input('Введите текст сообщения: ')
    return message, message_to


def send_to_server(message, message_to):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        data = {
            'email': message_to,
            'message': message
        }
        s.send(json.dumps(data).encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
        return response


def main():
    while True:
        message, message_to = get_user_input()
        response = send_to_server(message, message_to)

        if response == "OK":
            print("Отправлено!")
        else:
            print(f"Ошибка: {response}")

        retry = input("Повторить ввод? -> Нажмите н/Y: ").lower()
        if retry != 'н' and retry != 'y':
            print("Завершение работы.")
            break


if __name__ == "__main__":
    main()