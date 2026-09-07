import configparser
import socket
import json
from smtplib import SMTP_SSL
from email.message import EmailMessage
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')

host = config.get('EMAIL', 'SERVER_HOST')
port = config.getint('EMAIL', 'SERVER_PORT')
MY_EMAIL_LOGIN = config.get('EMAIL', 'EMAIL_LOGIN')
SMTP_HOST = config.get('EMAIL', 'SMTP_HOST')
SMTP_PORT = config.getint('EMAIL', 'SMTP_PORT')
EMAIL_PASSWORD = config.get('EMAIL', 'EMAIL_PASSWORD')


def validate_email(email):
    if not email or not isinstance(email, str):
        return False

    email = email.strip()

    if '@' not in email:
        return False

    parts = email.split('@')
    if len(parts) != 2:
        return False

    user, domain = parts

    if not user or not domain:
        return False

    if '.' not in domain:
        return False

    return True


def validate_message(message):
    if len(message) > 1000:
        return False

    return True


def create_email_message(to_email, message_text, ticket_id):
    msg = EmailMessage()
    msg['From'] = MY_EMAIL_LOGIN
    msg['To'] = to_email
    msg['Subject'] = f"[Ticket #{ticket_id}] Mailer"
    msg.set_content(message_text)

    return msg


def send_email(to_email, message_text, ticket_id):
    email_msg = create_email_message(to_email, message_text, ticket_id)

    with SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(MY_EMAIL_LOGIN, EMAIL_PASSWORD)
        smtp.send_message(email_msg)
        print(f"Письмо #{ticket_id} отправлено на {to_email}")

        admin_msg = EmailMessage()
        admin_msg['From'] = MY_EMAIL_LOGIN
        admin_msg['To'] = MY_EMAIL_LOGIN
        admin_msg['Subject'] = f"[Ticket #{ticket_id}] Mailer (копия)"
        admin_msg.set_content(f"Отправлено письмо на {to_email} с текстом:\n\n{message_text}")
        smtp.send_message(admin_msg)

    return True


def log_success(ticket_id, email, message_preview):
    with open('success_request.log', 'a', encoding='utf-8') as f:
        log_entry = f"Ticket #{ticket_id} | To: {email} | Message: {message_preview[:50]}... | {datetime.now()}\n"
        f.write(log_entry)


def log_error(email, message_text, message_error):
    with open('error_request.log', 'a', encoding='utf-8') as f:
        error = f"To: {email} | Error: {message_error} | Message: {message_text[:50]}... | {datetime.now()}\n"
        f.write(error)


def process_client_data(data):
    ticket_counter = 0
    request = json.loads(data)
    user_email = request.get('email', '').strip()
    message_text = request.get('message', '').strip()
    is_email_valid = validate_email(user_email)
    if not is_email_valid:
        log_error(user_email, message_text, "Ошибка валидации email")
        return False

    is_message_valid = validate_message(message_text)
    if not is_message_valid:
        log_error(user_email, message_text, "Ошибка валидации сообщения")
        return False

    ticket_counter += 1

    email_sent = send_email(user_email, message_text, ticket_counter)
    if not email_sent:
        log_error(user_email, message_text, "Ошибка отправки email")
        return False

    log_success(ticket_counter, user_email, message_text)
    return True


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Сервер запущен на {host}:{port}")
        print("Ожидание подключений...")
        print()

        while True:
            client_socket, client_address = server_socket.accept()

            with client_socket:
                print(f'Соединение установлено: {client_address}')

                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    client_socket.send("Пустые данные".encode('utf-8'))
                    continue

                success = process_client_data(data)
                if success:
                    client_socket.send("OK".encode('utf-8'))
                else:
                    client_socket.send("Ошибка".encode('utf-8'))


if __name__ == "__main__":
    start_server()