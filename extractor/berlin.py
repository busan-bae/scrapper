from bs4 import BeautifulSoup
import requests


headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
}

def extract_berlin_jobs(keyword, headers):
    """   
    Berlin Startup Jobs 웹사이트에서 특정 프로그래밍 언어에 대한 채용 공고를 추출합니다.
    :param keyword: 프로그래밍 언어
    :param headers: 헤더 정보
    """
    all_jobs = []
    url = f"https://berlinstartupjobs.com/skill-areas/{keyword}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return print(f"{response.status_code} Error occurred")
    soup = BeautifulSoup(response.content, "html.parser")
    data = soup.find("ul", class_="jobs-list-items")
    jobs = data.find_all("li", class_="bjs-jlid")
    for job in jobs:
        position = job.find("h4", class_="bjs-jlid__h").text
        company = job.find("a", class_="bjs-jlid__b").text
        location = "Berlin"
        link = job.find("h4", class_="bjs-jlid__h").find("a")["href"]
        job_dict = {
            "position": position,
            "company": company,
            "location": location,
            "link": link
        }
        all_jobs.append(job_dict)
    return all_jobs
