from bs4 import BeautifulSoup
import requests

def extract_web3_jobs(keyword, headers):
    """   
    web3.career 웹사이트에서 특정 프로그래밍 언어에 대한 채용 공고를 추출합니다.
    :param keyword: 프로그래밍 언어
    :param headers: 헤더 정보
    """
    all_jobs = []
    url = f"https://web3.career/{keyword}-jobs"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return print(f"{response.status_code} Error occurred")
    soup = BeautifulSoup(response.content, "html.parser")
    data = soup.find("tbody", class_="tbody")
    jobs = data.find_all("tr", attrs={"data-jobid": True})
    for job in jobs:
        position = job.find("h2" ,class_="fw-bold").text
        company = job.find("h3").text
        location = job.find_all("td")[3].text
        link = job.find("a")["href"]
        job_dict = {
            "position": position,
            "company": company,
            "location": location,
            "link": f"https://web3.career{link}"
        }
        all_jobs.append(job_dict)
    return all_jobs