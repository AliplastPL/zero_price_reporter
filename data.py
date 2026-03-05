import pyodbc
from datetime import datetime
from log import printandlog

DB_CONNECTION_STRING = (
    'DSN=aliplastpl;DBQ=ali800cfap,QTEMP,A800ENV,ALI800CFIC,ALI800CP6,ALI800CS,ALI800CPF,ALI800CP,AQ800CP,A800CP,SCT800AP,CVT800AP,A800AP,ICO250AP; '
    'UID=PLRAP; PWD=Ali18RAP'
)


def get_db_connection():
    try:
        printandlog("Łączenie z bazą danych...")
        con = pyodbc.connect(DB_CONNECTION_STRING)
        con.autocommit = True
        return con
    except Exception as e:
        printandlog(f"Błąd połączenia z bazą: {str(e)}")
        return None


def fetch_zero_price_data(cursor):
    current_year = datetime.now().year
    date_filter = f"{current_year}0101"

    sql_query = (
        f"select olorno as \"SO_NUMBER\", olline as \"LINE_NUMBER\", "
        f"olcuno as \"CLIENT_NUMBER\", olprdc as \"INDEKS\", OHHAND as \"HANDLER\" "
        f"from ali800cfap.srbsol left join ali800cfap.srbsoh on ohorno = olorno where oldelt >= {date_filter} and OLSALP = 0 and olstat = '' and ohstat = '' "
    )

    printandlog(f"Wykonywanie zapytania o dane: {sql_query}")
    cursor.execute(sql_query)
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results


def fetch_email_recipients(cursor):
    sql_query = "SELECT EMAIL, RECIPIENT_TYPE FROM kuba_dba.REPORT_RECIPIENTS WHERE REPORT_ID = 1 AND STATUS = ''"
    printandlog(f"Wykonywanie zapytania o adresatów: {sql_query}")
    cursor.execute(sql_query)

    recipients = {"to": [], "bcc": [], "cc": []}

    for row in cursor.fetchall():
        email = str(row[0]).strip()
        recipient_type = str(row[1]).strip().lower()

        if recipient_type == "to":
            recipients["to"].append({"address": email})
        elif recipient_type == "bcc":
            recipients["bcc"].append({"address": email})
        elif recipient_type == "cc":
            recipients["cc"].append({"address": email})
        else:
            recipients["to"].append({"address": email})

    return recipients
