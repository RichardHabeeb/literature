import requests
import bibtexparser
import time
import sys
from difflib import SequenceMatcher


def doi_lookup(title):
    try:
        title = title.replace("{","").replace("}","").strip()
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
    title = title.replace("{","").replace("}","").replace(":","").strip()
    url = 'https://dblp.org/search/publ/api?q=' + title.replace(" ", "+") + '&format=json'
    response = requests.get(url)
    try:
        data = response.json()
    except:
        return None

    if "hit" not in data["result"]["hits"]:
        return None

    title_norm = title.lower().rstrip('.')


    for item in data["result"]["hits"]["hit"]:
        item_title_norm = item['info']['title'].lower().rstrip('.').replace(":","").replace("&apos;","'").strip()
        if(item_title_norm == title_norm):
            if "ee" in item['info']:
                return item['info']['ee']
            elif "url" in item['info']:
                return item['info']['url']
            else:
                print(item['info'])
                return None


    hits = sorted(data["result"]["hits"]["hit"],
        key=lambda x: SequenceMatcher(
            None,
            title_norm,
            x['info']['title'].lower().rstrip('.').strip()).ratio())

    print("\tDBLP Miss. Top 5 matches:")

    for i,item in enumerate(hits):
        print("\t{}: \"{}\" @ {}".format(i, item['info']['title'], item['info']))

    res = input("Choose the best match (0-4) or press enter to skip:")
    if res:
        return hits[int(res)]['info']['ee']

    return None


def bibtex_add_doi(filepath):
    library = bibtexparser.parse_file(filepath)

    try:
        for paper in library.entries:
            if (paper['ENTRYTYPE'] == 'article' or paper['ENTRYTYPE'] == 'inproceedings'):
                if 'doi' not in paper and 'url' not in paper and 'note' not in paper:

                    print("Title: \"{}\"".format(paper['title']))
                    time.sleep(1.5)
                    doi = doi_lookup(paper['title'])
                    if not doi:
                        url = dblp_lookup(paper['title'])
                        if url and url.startswith("https://doi.org/"):
                            doi = url.replace("https://doi.org/", "")

                    if doi:
                        print("\t{}".format(doi))
                        paper['doi'] = doi
                    elif url:
                        print("\t{}".format(url))
                        paper['note'] = "Available at \url\{{}\}".format(url)



    except KeyboardInterrupt:
        print("Stopping...")

    bibtex_format = bibtexparser.BibtexFormat()
    bibtex_format.indent = '    '
    bibtex_format.block_separator = '\n\n'
    bib_str = bibtexparser.write_string(library, bibtex_format=bibtex_format)
    return bib_str


if __name__ == "__main__":
    res = bibtex_add_doi(sys.argv[1])
    with open(sys.argv[2], 'w') as f:
        f.write(res)


