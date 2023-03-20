import time
import requests
import urllib.request
from bs4 import BeautifulSoup


def send_message_on_telegram(message):
    # definisco il token, la chat_id e il messaggio
    token = '6274356700:AAHt9JWd5N5VLnfSyMaMUeB05L_JM8IkAwA'
    chat_id = '157846555'

    # invio il messaggio
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url).json())


def download_attachment():  # TODO
    #cerco tutti gli allegati
    pass



def on_page_update():  # TODO: scaricare i pdf
    # voglio scaricare tutti i pdf
    # TODO

    send_message_on_telegram('La pagina è stata aggiornata.')


def scraping():
    while True:
        # url del sito
        quote_page = 'https://unical.portaleamministrazionetrasparente.it/index.php?id_oggetto=22&id_doc=12537'

        # scarico il codice html della pagina
        page = urllib.request.urlopen(quote_page)

        # creo un oggetto BeautifulSoup
        soup = BeautifulSoup(page, 'html.parser')

        # cerco tramite id
        creation_and_last_edit_date = soup.find('div', attrs={'id': 'dataAggiornamento12537'})
        # print(creation_and_last_edit_date) # <div class="dataAggiornamento" id="dataAggiornamento12537">Contenuto creato il 02-02-2023 aggiornato al 02-02-2023</div>

        # memorizzo la prima data in una variabile
        creation_date = creation_and_last_edit_date.text.split(' ')[3]
        print(f'creato in data {creation_date}.')  # 02-02-2023

        # memorizzo la seconda data in una variabile
        last_edit_date = creation_and_last_edit_date.text.split(' ')[6]
        print(f'modificato in data {last_edit_date}.')  # 02-02-2023 (per ora)

        # confronto le due date
        if creation_date != last_edit_date:
            print('La pagina è stata aggiornata.')
            on_page_update()
            send_message_on_telegram('Il mio lavoro qui è finito. 🫡')
            break

        # aspetto 30 minuti prima di ricontrollare
        time.sleep(30 * 60)


def main():
    print('Running...')
    # scraping()
    send_message_on_telegram('Prova')  # for test purposes only


# main
if __name__ == '__main__':
    main()
