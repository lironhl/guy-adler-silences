# 1. Import the requests library
import requests
from bs4 import BeautifulSoup


PODCAST_URL = "https://www.buzzsprout.com/1812888"

def get_podcast_page_eps_links(page: int):
    resp = requests.get(PODCAST_URL, params={'page': page})
    soup = BeautifulSoup(resp.content, 'html.parser')
    return soup.find_all("a", attrs={'class': 'episode-list--link'})
    


def get_episodes():
    episodes = []
    page = 0
    episode_links = get_podcast_page_eps_links(page)

    while len(episode_links) > 0:
        episodes.extend(elink.attrs['href'] for elink in episode_links)
        
        page += 1
        episode_links = get_podcast_page_eps_links(page)
    
    return episodes



def get_episode(episode: str):
    episode_url = f"https://www.buzzsprout.com{episode}.mp3"
    return requests.get(episode_url)



def main():
    for i, eps in enumerate(get_episodes(), 1):
        resp = get_episode(eps)
        with open(f"./data/eps-{i}.mp3", "wb") as f:
            f.write(resp.content)


if __name__ == "__main__":
    main()