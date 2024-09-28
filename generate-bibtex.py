import yaml


if __name__ == "__main__":
    with open("_data/papers.yaml", "r") as yaml_file:
        with open("ref.bib", "w") as bibtex_file:
            papers = yaml.safe_load(yaml_file)
            papers.sort(key=lambda e: e['year'] if 'year' in e else '9999')
            order = {v: i for i, v in enumerate([
                'title',
                'author',
                'journal',
                'booktitle',
                'organization',
                'publisher',
                'year',
                'month'
            ])}
            for paper in papers:
                bibtex_file.write(f"@{paper['ENTRYTYPE']}{{{paper['ID']},\n")

                for key in sorted(paper.keys(), key=lambda k: order[k] if k in order else 9999):
                    if key != 'ID' and key != 'ENTRYTYPE':
                        bibtex_file.write(f"\t{key:20} = {{{paper[key]}}},\n")
                bibtex_file.write("}\n\n")




