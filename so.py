import requests
from bs4 import BeautifulSoup


url = f'https://stackoverflow.com/jobs?q='


def extract_max_page(keyword):
    request = requests.get(f'{url}{keyword}')
    soup = BeautifulSoup(request.text, 'html.parser')
    pages = soup.find('div', {'class': 's-pagination'}).find_all('a')
    pages = pages[-2]
    last_page = int(pages.get_text(strip=True))
    return last_page


def extract_job(html):
    title = html.find('a').text
    link = html.find('a')['href']
    link = f'https://stackoverflow.com{link}'
    company = html.find('h3').find('span').get_text(strip=True)
    location = html.find('h3').find(
        'span', {'class': 'fc-black-500'}).get_text(strip=True)
    return {'title': title, 'company': company, 'location': location, 'link': link}


def extract_jobs(last_page, keyword):
    jobs = []
    for page in range(last_page):
        print(f'Stackoverflow: Парсинг страницы {page+1}')
        req_result = requests.get(
            f'{url}{keyword}&pg={page+1}')
        soup = BeautifulSoup(req_result.text, 'html.parser')
        job_result = soup.find_all('div', {'class': 'grid--cell fl1'})
        for job_html in job_result:
            job = extract_job(job_html)
            jobs.append(job)
    return jobs


def get_jobs(keyword):
    last_page = extract_max_page(keyword)
    jobs = extract_jobs(last_page, keyword)
    return jobs
