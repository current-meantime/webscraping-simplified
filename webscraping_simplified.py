# pip install bs4 requests
from math import ceil  # metoda, której użyjemy do zaokrąglania wyniku dzielenia w górę
import requests  # biblioteka do pobierania zawartości stron internetowych
from bs4 import BeautifulSoup  # do parsowania HTML i wyciągania z niego rzeczy
from urllib.parse import urljoin  # do łączenia elementów URL
from pathlib import Path  # do tworzenia ścieżek w systemie plików
from time import sleep  # żeby nie zaspamować strony


def get_total_results(soup):
    """Pobiera całkowitą liczbę wyników z nagłówka strony."""
    # `soup` to obiekt BeautifulSoup, który jest sparsowanym HTML
    # `find` to metoda, która znajduje pierwszy element pasujący do podanego selektora
    # `div` to element `div` w HTML, który zawiera nagłówek
    # `view-header` to klasa CSS, która identyfikuje elementy zawierające nagłówek
    # `get_text` to metoda, która zwraca tekst zawarty w elemencie
    header = soup.find("div", class_="view-header")
    if header:
        text = header.get_text()
        parts = text.strip().split()
        if "of" in parts: # wiemy że w nagłówku będzie coś w stylu "1-100 of 1234", więc szukamy "of"
            try:
                # `index` to metoda, która zwraca indeks pierwszego wystąpienia podanego elementu
                total = int(parts[parts.index("of") + 1])
                return total
            except ValueError:
                pass
    return 0


def calculate_pages(records_found, items_per_page):
    """Oblicza liczbę stron na podstawie liczby rekordów i elementów na stronę."""
    # `ceil` to funkcja, która zaokrągla liczbę w górę
    # `records_found` to liczba tekstów obecnych na stronie pod wskazanymi parametrami
    # `items_per_page` to liczba tekstów, które się wyswietlą na jednej stronie
    # `pages_count` to liczba stron, które będą potrzebne do wyświetlenia wszystkich tekstów
    pages_count = ceil(records_found / items_per_page)
    return pages_count


def generate_page_links(start_date, end_date, items_per_page, pages_count):
    """Generuje linki do stron zawierających linki do tekstów."""
    pages_with_links = []
    for page_num in range(pages_count):
        page_with_links = (
            f"https://www.presidency.ucsb.edu/advanced-search?field-keywords=&field-keywords2=&field-keywords3=&from%5Bdate%5D={start_date}&to%5Bdate%5D={end_date}&person2=&items_per_page={items_per_page}&page={page_num}"
        )
        pages_with_links.append(page_with_links)
    return pages_with_links


def fetch_links_to_texts(pages_with_links, base_url):
    """Zbiera linki do tekstów z podanych stron."""
    links_to_texts = []
    for page in pages_with_links:
        print(f"\nGoing to page {page}")
        response = requests.get(page).text
        soup = BeautifulSoup(response, "html.parser")
        
        # `td` to elementy `td` w HTML, które zawierają linki do tekstów
        # `select` to metoda, która wybiera elementy na podstawie selektora CSS
        # `views-field` to klasa CSS, która identyfikuje elementy zawierające linki do tekstów
        # `views-field-title` to klasa CSS, która identyfikuje elementy zawierające tytuły tekstów
        # `a` to elementy `a` w HTML, które są linkami
        # `href` to atrybut, który zawiera adres URL linku
        for td in soup.select("td.views-field.views-field-title a"):
            href = td.get("href", "")
            if href.startswith("/documents/"):
                # `urljoin` to funkcja, która łączy bazowy URL z adresem URL linku
                links_to_texts.append(urljoin(base_url, href))
        break  # skracamy na potrzeby prezentacji
    return links_to_texts


def save_text_to_file(filepath, text):
    """Zapisuje tekst do pliku."""
    # `filepath` to ścieżka do pliku, w którym chcemy zapisać tekst
    # `text` to tekst, który chcemy zapisać
    # `open` to funkcja, która otwiera plik w trybie zapisu
    # `w` oznacza, że plik zostanie nadpisany, jeśli już istnieje
    # `encoding="utf-8"` oznacza, że plik będzie zapisany w kodowaniu UTF-8
    # `file` to zmienna, która przechowuje uchwyt do otwartego pliku
    # `file.write` to metoda, która zapisuje tekst do pliku
    # `with open` to konstrukcja, która automatycznie zamyka plik po zakończeniu bloku, przez co jest bezpieczna
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(text)


def append_text_to_file(filepath, text):
    """Dodaje tekst do pliku zbiorczego."""
    # `a` oznacza, że plik zostanie otwarty w trybie dopisywania
    with open(filepath, "a", encoding="utf-8") as file:
        file.write(text + "\n\n")


def scrape_and_save_texts(links_to_texts, output_directory, all_texts_file):
    """Scrapuje teksty z linków i zapisuje je do plików."""
    for link in links_to_texts:
        try:
            response = requests.get(link).text
            soup = BeautifulSoup(response, "html.parser")

            # wyciągamy treść przemówienia z elementu 'div'
            speech_div = soup.find("div", class_="field-docs-content")
            speech_text = speech_div.get_text(separator="\n", strip=True) if speech_div else ""

            # dynamicznie tworzymy nazwę i ścieżkę pliku
            title = link.split("/")[-1] + ".txt"
            filepath = Path(output_directory) / title

            # zapisujemy dany tekst do osobnego pliku (oprócz tego zbiorczego)
            save_text_to_file(filepath, speech_text)
            print(f"\n----- INFO: '{title}' saved to '/parsing_output'.")

            # zapisujemy dany tekst do pliku zbiorczego
            append_text_to_file(all_texts_file, speech_text)

            sleep(0.5)  # czekamy chwilę żeby nie zaspamować strony zapytaniami

        except Exception as e:
            print(f"Error occured. Error: {e}")


def main():
    # parametry zapytań
    year_to_scrape = 2020 # rok, który chcemy przeszukać - można zmienić na dowolny
    start_date = f"01-01-{year_to_scrape}"
    end_date = f"12-31-{year_to_scrape}"
    # wiemy, że strona wyświetli maksymalnie 100 wyników na stronę, więc ustawiamy to na 100
    items_per_page = 100  # Im więcej na stronie tym lepiej, żeby nie przechodzić przez większą ilość stron niż trzeba

    print(f"\nINFO: items_per_page is set to {items_per_page}.")

    # Pobieramy pierwszą stronę, aby określić liczbę wyników
    base_url = "https://www.presidency.ucsb.edu"
    first_page_url = (
        f"https://www.presidency.ucsb.edu/advanced-search?field-keywords=&field-keywords2=&field-keywords3=&from%5Bdate%5D={start_date}&to%5Bdate%5D={end_date}&person2=&items_per_page={items_per_page}&page=0"
    )
    print(f"\nINFO: first_page_url is set to {first_page_url}.")
    
    # `requests`` to biblioteka, która pozwala na wysyłanie zapytań HTTP
    # `requests.get` to funkcja, która wysyła zapytanie HTTP GET do podanego URL
    # `first_page_url` to adres URL pierwszej strony, którą chcemy pobrać
    # `text` to metoda, która zwraca odpowiedź w formacie tekstowym
    # `response` to zmienna, która przechowuje odpowiedź serwera
    response = requests.get(first_page_url).text

    # parsujemy raw HTML za pomocą BeautifulSoup, czyli biblioteki, która ułatwia
    # nawigację i wyciąganie danych z HTML lub XML
    # `response` to surowy HTML, który pobraliśmy wcześniej
    # `soup` to obiekt BeautifulSoup, który jest sparsowanym HTML
    # argument `html.parser` wyznacza parser, który używamy do przetwarzania HTML
    soup = BeautifulSoup(response, "html.parser")
    
    # funkcja `get_total_results` analizuje HTML i wyciąga liczbę wyników z nagłówka strony
    # dlatego jako argument podajemy `soup`, czyli obiekt BeautifulSoup, który jest sparsowanym HTML
    # i zawiera wszystkie elementy strony
    records_found = get_total_results(soup)
    print(f"\nINFO: Found {records_found} records.")

    # obliczamy liczbę stron
    pages_count = calculate_pages(records_found, items_per_page)

    # generujemy linki do stron zawierających linki do tekstów
    pages_with_links = generate_page_links(start_date, end_date, items_per_page, pages_count)
    print(f"\nINFO: pages_with_links contains {len(pages_with_links)} links to cycle through.\n")

    # pobieramy linki do tekstów
    links_to_texts = fetch_links_to_texts(pages_with_links, base_url)
    print(f"\nWe got {len(links_to_texts)} links to texts out of {records_found}")
    print("\nPrinting first 5 links:\n")
    print(links_to_texts[:5])  # Sprawdźmy pierwsze kilka linków do tekstów

    # przygotowujemy się do zapisywania tekstów
    # `Path` to klasa, która reprezentuje ścieżkę do pliku lub katalogu
    # `__file__` to zmienna, która zawiera ścieżkę do aktualnego pliku
    # `parent` to atrybut, który zwraca katalog nadrzędny pliku
    # `mkdir` to metoda, która tworzy katalog, jeśli nie istnieje
    # `exist_ok=True` oznacza, że nie zgłosi błędu, jeśli katalog już istnieje
    this_script_file_path = Path(__file__)
    this_script_directory = this_script_file_path.parent
    output_directory = this_script_directory / "parsing_output"
    output_directory.mkdir(exist_ok=True)

    # tworzymy zbiorczy plik dla wszystkich tekstów
    # formatowanie nie będzie idealne, ale użyjemy .txt, bo jest prosty i wszystkim znany
    all_texts_file = Path(output_directory) / "all_texts.txt"

    # scrapujemy teksty i zapisujemy je
    scrape_and_save_texts(links_to_texts, output_directory, all_texts_file)

    print("Scraping zakończony.")


if __name__ == "__main__":
    main()