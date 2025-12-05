import cloudscraper
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
    """   
    We Work Remotely 웹사이트에서 특정 프로그래밍 언어에 대한 채용 공고를 추출합니다.
    :param keyword: 프로그래밍 언어
    :param headers: 헤더 정보
    """
    scraper = cloudscraper.create_scraper()
    all_jobs = []
    url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}"
    response = scraper.get(url)
    if response.status_code != 200:
        return print(f"{response.status_code} Error occurred")
    soup = BeautifulSoup(response.content, "html.parser")
    data = soup.find("div", id='search-results')
    jobs = data.find_all("li", class_="new-listing-container")
    for job in jobs:
        position = job.find('h3', class_="new-listing__header__title").text
        company = job.find("p", class_="new-listing__company-name").text
        location = job.find("p", class_="new-listing__company-headquarters").text
        link = job.find_all("a")[1]["href"]
        job_dict = {
            "position": position,
            "company": company,
            "location": location,
            "link": f"https://weworkremotely.com{link}"
        }
        all_jobs.append(job_dict)
    return all_jobs