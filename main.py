import time
import requests
import urllib.request
from glob import glob
from bs4 import BeautifulSoup
from datetime import datetime


def send_attachments_telegram(token, chat_id):
    # URL dell'endpoint Telegram per inviare documenti
    url = f"https://api.telegram.org/bot{token}/sendDocument"

    # cerco tutti i file PDF nella directory corrente
    pdf_files = glob("*.pdf")

    # itero sui file PDF trovati
    for file_path in pdf_files:
        try:
            # Invia la richiesta POST con il file PDF come allegato
            response = requests.post(url, data={"chat_id": chat_id}, files={"document": open(file_path, "rb")})

            # Controlla lo status code della risposta
            if response.status_code == 200:
                print(f"File {file_path} inviato a chat ID {chat_id}!")
            else:
                print(f"Errore nell'invio del file {file_path}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Errore nella richiesta HTTP: {e}")


def send_custom_message_on_telegram(custom_msg):
    # definisco il token e il chat_id
    token = 'INSERISCI_IL_TUO_TOKEN'
    chat_id = 'INSERISCI IL TUO CHAT_ID'

    # invio il messaggio
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={custom_msg}"
    requests.get(url).json()


def send_message_on_telegram(token, chat_id, msg_type):
    # definisco il messaggio
    default_message = 'Messaggio di default.'
    first_message = 'La pagina è stata aggiornata'
    last_message = 'Il mio lavoro qui è finito 🫡 '

    # seleziono il messaggio da inviare
    if msg_type == 0:
        message = first_message
    elif msg_type == 1:
        message = last_message
    else:
        message = default_message

    # invio il messaggio
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()


def setup_bot_telegram():
    # definisco il token e il chat_id
    token = 'INSERISCI_IL_TUO_TOKEN'
    chat_id = 'INSERISCI IL TUO CHAT_ID'
    message = 'La pagina è stata aggiornata.'

    # invio il messaggio e gli allegati
    send_message_on_telegram(token, chat_id, 0)
    send_attachments_telegram(token, chat_id)
    send_message_on_telegram(token, chat_id, 1)


def download_attachment(soup):
    # cerco tramite classe
    campi_documento = soup.findAll('div', attrs={'class': 'campoOggetto48'})

    # ciclo su tutti i campi
    for campo in campi_documento:

        # estraggo il nome del file
        nome_documento = campo.find('a').text

        # documenti di cui non mi interessa scaricare il .pdf
        nome_documento_bando = 'Bando di Concorso per l_assegnazione delle borse di studio ERASMUS  Anno Accademico 2023_2024_SIGNED.pdf'
        nome_documento_guida = 'MINIGUIDA COMPILAZIONE DOMANDA ERASMUS_2023-24.pdf'
        if nome_documento != nome_documento_bando and nome_documento != nome_documento_guida:
            # estraggo il link dall'attributo href
            link = campo.find('a').get('href')

            # scarico il file
            urllib.request.urlretrieve(link, nome_documento)


def on_page_update(soup):
    # scarico gli allegati
    download_attachment(soup)

    # invio un messaggio su telegram
    setup_bot_telegram()


def print_last_scrape_time():
    # inizializzo il tempo
    date_time = datetime.now()

    # memorizzo l'ora, i minuti e i secondi
    hh = str(date_time.hour)
    mm = str(date_time.minute)
    ss = str(date_time.second)

    # li stampo
    print('Scraped at: ' + hh + ':' + mm + ':' + ss)


def start_scraping(soup):
    while True:
        # invio un messaggio
        send_custom_message_on_telegram('controllo il sito.. 🕵🏻')

        # cerco tramite id
        creation_and_last_edit_date = soup.find('div', attrs={'id': 'dataAggiornamento12537'})

        # memorizzo la prima data in una variabile
        creation_date = creation_and_last_edit_date.text.split(' ')[3]

        # memorizzo la seconda data in una variabile
        last_edit_date = creation_and_last_edit_date.text.split(' ')[6]

        # confronto le due date
        if creation_date != last_edit_date:
            on_page_update(soup)
            break
        else:
            send_custom_message_on_telegram('niente di nuovo ☹️')

        # aspetto 30 minuti prima di ricontrollare
        time.sleep(10*60)


def before_scraping():
    # url del sito
    quote_page = 'https://unical.portaleamministrazionetrasparente.it/index.php?id_oggetto=22&id_doc=12537'

    # scarico il codice html della pagina
    page = urllib.request.urlopen(quote_page)

    # creo un oggetto BeautifulSoup
    soup = BeautifulSoup(page, 'html.parser')

    return soup


def main():
    # stampo e invio un messaggio su telegram
    running_msg = 'operativo 🫡'
    print(running_msg)
    send_custom_message_on_telegram(running_msg)

    # operazioni preliminari
    soup = before_scraping()

    # avvio lo scraper
    start_scraping(soup)


# main
if __name__ == '__main__':
    main()
