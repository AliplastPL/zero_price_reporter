import os
from azure.communication.email import EmailClient
from log import printandlog


def get_connection_string():
    conn_str = os.environ.get("COMMUNICATION_SERVICES_CONNECTION_STRING")
    if conn_str:
        return conn_str

    # Fallback to config.txt if file exists
    config_path = "config.txt"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                for line in f:
                    if "COMMUNICATION_SERVICES_CONNECTION_STRING=" in line:
                        return line.split("=", 1)[1].strip()
        except Exception as e:
            printandlog(f"Błąd podczas czytania pliku konfiguracyjnego: {str(e)}")

    return None


AZURE_CONNECTION_STRING = get_connection_string()
SENDER_ADDRESS = "donotreply@aliplast.pl"


def format_email_body(data):
    if not data:
        return "Brak danych."

    body = "Wykryto rekordy z zerową ceną w systemie (srbsol):\n\n"

    # Extract headers from the first record
    headers = list(data[0].keys())
    body += " | ".join(headers) + "\n"
    body += "-" * (len(" | ".join(headers)) + 5) + "\n"

    # Rows
    for row in data:
        row_values = [str(val).strip() for val in row.values()]
        body += " | ".join(row_values) + "\n"

    return body


def send_notification_email(data, recipients):
    if not AZURE_CONNECTION_STRING:
        printandlog("Błąd: Nie znaleziono klucza Azure (AZURE_CONNECTION_STRING).")
        return

    if not recipients.get("to"):
        printandlog("Błąd: Brak adresatów (TO). Mail nie został wysłany.")
        return

    try:
        email_client = EmailClient.from_connection_string(AZURE_CONNECTION_STRING)

        message = {
            "content": {
                "subject": "Raport: Zerowe ceny w systemie (srbsol)",
                "plainText": format_email_body(data)
            },
            "recipients": recipients,
            "senderAddress": SENDER_ADDRESS
        }

        printandlog("Wysyłanie maila...")
        poller = email_client.begin_send(message)
        result = poller.result(timeout=60)
        printandlog(f"Mail wysłany pomyślnie. ID: {result.get('id') if result else 'N/A'}")
    except Exception as e:
        printandlog(f"Błąd podczas wysyłania maila: {str(e)}")
