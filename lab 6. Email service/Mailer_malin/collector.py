import email
from imaplib import IMAP4_SSL
import time
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')

IMAP_PORT = config.getint('EMAIL', 'IMAP_PORT')
IMAP_HOST = config.get('EMAIL', 'IMAP_HOST')
ADMIN_EMAIL = config.get('EMAIL', 'EMAIL_LOGIN')
ADMIN_PASSWORD = config.get('EMAIL', 'EMAIL_PASSWORD')

PERIOD_CHECK = config.getint('EMAIL', 'PERIOD_CHECK')


def is_ticket_subject(subject):
    if not subject:
        return False, None

    subject = subject.strip()
    if len(subject) < 18:
        return False, None

    if subject[:9] != '[Ticket #':
        return False, None

    if subject[-8:] != '] Mailer':
        return False, None

    try:
        ticket_id = subject[9:-8]
        if not ticket_id.isdigit():
            return False, None

        return True, ticket_id
    except Exception:
        return False, None


def log_success(ticket_id, message_body):
    try:
        log_entry = f"\nTicket #{ticket_id} | Message: {message_body}\n | {datetime.now()}"
        with open('success_request.log', 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except OSError:
        print("\nОшибка записи в success_request.log")


def log_error(message_body):
    try:
        log_entry = f"\nMessage: {message_body} | {datetime.now()}"
        with open('error_request.log', 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except OSError:
        print("\nОшибка записи в error_request.log")


def check_email():
    print(f"Проверка почты...")

    try:
        with IMAP4_SSL(IMAP_HOST, IMAP_PORT) as mail:
            mail.login(ADMIN_EMAIL, ADMIN_PASSWORD)
            mail.select('INBOX')
            status, messages = mail.search(None, 'UNSEEN')

            if status != 'OK':
                print("Не удалось выполнить поиск писем")
                return

            email_ids = messages[0].split()

            if not email_ids:
                print("Нет новых непрочитанных писем")
                return

            print(f"Найдено {len(email_ids)} новых писем")

            for email_id in email_ids:
                email_id_str = email_id.decode()

                status, msg_data = mail.fetch(email_id, '(RFC822)')

                if status != 'OK' or not msg_data or msg_data[0] is None:
                    print(f"Не удалось получить письмо ID: {email_id_str}")
                    continue

                if not isinstance(msg_data[0], tuple) or len(msg_data[0]) < 2:
                    print(f"Некорректная структура данных письма ID: {email_id_str}")
                    continue

                raw_email = msg_data[0][1]

                if raw_email is None:
                    print(f"Пустое тело письма ID: {email_id_str}")
                    continue

                email_message = email.message_from_bytes(raw_email)

                subject = email_message['Subject']

                message_text = email_message.get_payload()

                if not message_text:
                    if email_message.is_multipart():
                        message_text = "[Multipart сообщение]"
                    else:
                        message_text = "[Пустое сообщение]"

                is_ticket, ticket_id = is_ticket_subject(subject)

                if is_ticket:
                    log_success(ticket_id, message_text)
                    print(f"Обработан тикет #{ticket_id}")
                else:
                    log_error(message_text)
                    print(f"Письмо не является тикетом: {subject[:50]}...")

    except Exception as e:
        print(f"Ошибка при проверке почты: {e}")


def main():
    while True:
        check_email()
        time.sleep(PERIOD_CHECK)


if __name__ == "__main__":
    main()