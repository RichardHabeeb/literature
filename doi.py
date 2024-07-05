import yaml
import requests

with open('_data/papers.yaml', 'r') as file:
    papers = yaml.safe_load(file)

    for paper in papers:
        data = None

        if 'doi' in paper:
            continue

        try:
            url = 'https://api.crossref.org/works?query.title=' + paper['title']
            response = requests.get(url)

            data = response.json()

            for item in data["message"]["items"]:
                if(item['title'][0].lower() == paper['title'].lower()):
                    print(item['title'], item['DOI'])
                    paper['doi'] = item['DOI']
                    break
        except Exception as e:
            print(e)
            continue

    with open('_data/papers-doi.yaml', 'w') as output:
        yaml.dump(papers, output, allow_unicode=True)
