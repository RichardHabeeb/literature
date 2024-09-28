import yaml
import requests
import bibtexparser
import time


def doi_lookup(title):
    try:
        url = 'https://api.crossref.org/works?query.title=' + title.replace(" ", "+")
        response = requests.get(url)

        data = response.json()

        for item in data["message"]["items"]:
            if(item['title'][0].lower() == title.lower()):
                return item['DOI']
    except Exception as e:
        print(e)

    return None

def dblp_lookup(title):
    title = title.replace("{","").replace("}","").strip()
    url = 'https://dblp.org/search/publ/api?q=' + title.replace(" ", "+") + '&format=json'
    response = requests.get(url)
    time.sleep(2)
    try:
        data = response.json()
    except:
        return None

    if "hit" not in data["result"]["hits"]:
        return None

    for item in data["result"]["hits"]["hit"]:
        if(item['info']['title'].lower().rstrip('.') == title.lower().rstrip('.')):
            return item['info']['ee']
        else:
            print("---", item['info']['title'])

    return None

if __name__ == "__main__":

    with open("import.bib") as bibtex_file:
        library = bibtexparser.load(bibtex_file)

        with open("_data/papers.yaml") as papers_file:
            entries = yaml.safe_load(papers_file)

            for entry in library.entries:
                if entry['ID'] not in [e['ID'] for e in entries]:
                    entries.append(entry)
                else:
                    print(f"Skipping {entry['ID']}")

            entries = sorted(entries, key=lambda n: n['year'] if 'year' in n else '9999')

            for paper in entries:
                if (paper['ENTRYTYPE'] == 'article' or paper['ENTRYTYPE'] == 'inproceedings'):
                    if 'doi' not in paper and 'url' not in paper:
                        print("Looking up", paper['title'])
                        doi = doi_lookup(paper['title'])
                        if doi:
                            print("Found DOI for", paper['title'], "doi:", doi)
                            paper['doi'] = doi
                            continue

                        url = dblp_lookup(paper['title'])
                        if url:
                            print("Found URL for", paper['title'], "url:", url)
                            paper['url'] = url

                        print("================")



            yaml.dump(entries, open("_data/papers.yaml", "w"))








