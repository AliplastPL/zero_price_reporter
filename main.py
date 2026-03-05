from log import printandlog
from data import get_db_connection, fetch_zero_price_data, fetch_email_recipients
from sender import send_notification_email


def main():
    con = get_db_connection()
    if not con:
        return

    try:
        cursor = con.cursor()

        # 1. Pobierz dane o zerowych cenach
        data = fetch_zero_price_data(cursor)

        # 2. Sprawdź czy są wyniki - jeśli nie, kończymy
        if not data:
            printandlog("Brak rekordów z OLSALP=0. Program kończy działanie.")
            return

        printandlog(f"Znaleziono {len(data)} rekordów. Przygotowywanie wysyłki...")

        # 3. Pobierz adresatów
        recipients = fetch_email_recipients(cursor)

        # 4. Wyślij powiadomienie
        send_notification_email(data, recipients)

    except Exception as e:
        printandlog(f"Błąd krytyczny w głównym procesie: {str(e)}")
    finally:
        con.close()
        printandlog("Połączenie z bazą danych zamknięte.")


if __name__ == "__main__":
    main()
