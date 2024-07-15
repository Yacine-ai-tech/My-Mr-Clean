import requests
from bs4 import BeautifulSoup

def request_github_trending(url):
    response = requests.get(url)
    return response

def extract(page):
    S = BeautifulSoup(page.text, 'html.parser')
    html_repos = S.find_all('a')
    return html_repos

def transform(html_repos):
    repositories_data = []
    for R in html_repos:
        developer = R.find('a', {'class':'muted-link'})
        repository_name = R.find('h3')
        nbr_stars = R.find('div', {'class': 'f6 text-gray mt-2'})
        repositories_data.append({'developer': developer, 'repository_name': repository_name, 'nbr_stars':nbr_stars})
    return repositories_data

def format(repositories_data):
    csv = "Developer, Repository Name, Number of stars\n"
    for R in repositories_data:
        csv += f"{R['developer']}, {R['repository_name']}, {R['nbr_stars']}\n"
    return csv























