import requests
from bs4 import BeautifulSoup


def get_unique_items(property: str, item_list: list):
    unique = []
    for item in item_list:
        unique_props = [item[property] for item in unique]
        if item[property] in unique_props:
            pass
        else:
            unique.append(item)
    return unique


def download_episode(url):
    episode_page = requests.get(url)
    episode_soup = BeautifulSoup(episode_page.content, 'html.parser')
    episode_page_links = episode_soup.find_all('a')
    episode_link = get_unique_items(
        'href',
        list(filter(lambda x: 'downloadmp4' in x['href'], episode_page_links)))

    int_page = requests.get(
        f'https://mobiletvshows.net/{episode_link[0]["href"]}')
    int_page_soup = BeautifulSoup(int_page.content, 'html.parser')
    print(int_page_soup.prettify())
    int_page_links = int_page_soup.find_all("a")
    file_link = []
    for link in int_page_links:
        href = link['href']
        print(href)
        # if 'dkey' in href and 'fileid' in href:
        #     print(href)
    # file_page_links = get_unique_items('href', list(
    #     filter(lambda x: 'dkey' in x['href'], int_page_links)))
    # print(file_page_links)

    # print(f"https://mobiletvshows.net/{file_page_links[0]['href']}")
    # file_page = requests.get(
    #     f"https://mobiletvshows.net/{file_page_links[0]['href']}")
    # file_page_soup = BeautifulSoup(file_page.content, 'html.parser')
    # file_page_inputs = file_page_soup.find_all('input')
    # return (file_links[0]['value'])
    # print(file_page_inputs)
    # return file_page_inputs


def download_season(url):
    season_page = requests.get(url)
    season_soup = BeautifulSoup(season_page.content, 'html.parser')
    season_page_links = season_soup.find_all('a')
    episode_links = get_unique_items(
        'href',
        list(filter(lambda x: 'ftype=2' in x['href'], season_page_links)))

    print("select episode")
    for index, episode in enumerate(episode_links):
        print(f"episode {index + 1}")
    episode_index = int(input()) - 1
    print(
        download_episode(
            f"https://mobiletvshows.net/{episode_links[episode_index]['href']}"
        ))


print("Download Series from mobiletvshows.net")
search_key = input("Enter Series Name: ")

search_url = f"https://mobiletvshows.net/search.php?search={search_key}&beginsearch=Search&vsearch=&by=series"

root = requests.get(search_url)
soup = BeautifulSoup(root.content, 'html.parser')
links = soup.find_all('a')

results = list(
    filter(
        lambda x: 'subfolder' in x['href'] and search_key.lower() in x['href'].
        lower(), links))

results = get_unique_items('href', results)

print(f"select 0 - {len(results)}")
for index, result in enumerate(results):
    print(
        f"[{index}] {result['href'].replace('subfolder-','').replace('.htm','')}"
    )

# catch error
series_index = int(input(""))

series_page = requests.get(
    f"https://mobiletvshows.net/{results[series_index]['href']}")

series_page_soup = BeautifulSoup(series_page.content, 'html.parser')
series_page_links = series_page_soup.find_all('a')
season_links = get_unique_items(
    'href', list(filter(lambda x: 'files' in x['href'], series_page_links)))

print("choose season ")
for index, link in enumerate(season_links):
    print(f"[{index}] {link.contents[0].text} \n")
season_index = int(input())
print(
    download_season(
        f"https://mobiletvshows.net/{season_links[season_index]['href']}"))

# for link in season_links:
#     requests.get(f"https://mobiletvshows.net/{link['href']}")
