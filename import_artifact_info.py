import csv
import os
import sys
from collections import defaultdict
from generate_acmdl_artifact_metadata import *
import urllib.request, json, html
from shutil import copyfile, make_archive
from datetime import datetime
import html

# paper title
# 0 -> paper ID, 1 -> title, 11 -> paper DOI
# "Contact No.","Title","Author","Email","DL Paper Type","Rights Granted","Third Party","Aux. Material","Video Recording","Artistic Images","Govt. Employees","Open Access","DOI","Authorizer","Statement","CC License","Non-ACM Copyright"
def read_papers(paperCSV):
    papers = {}

    # Expected format (separated by comma): firstname, lastname, email, affiliation
    with open(paperCSV, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:

            paperID = row[0]
            if not row[0].isalnum(): # eurosys does eurosys-p??? and not directly the paper ID
                paperID = row[0][row[0].rfind("p")+1:]

            # xmlcharrrefreplace ensures that special characters are replaced with XML/HTML equivalent
            papers[paperID] = {'title': html.escape(row[1][:row[1].find("\\")]).strip(),
                        'refdoi': row[12][row[12].find("10.1145/")+len("10.1145/"):]}

    print(f'Read {len(papers)} papers.')

    return papers

# badge decision and doi dictionary
# apdxid, paperid, aa, af, rr, doi
# Generated via Excel sheet
def read_badges_doi(badgeDOICSV):
    badge_doi = {}

    # Expected format (separated by comma): firstname, lastname, email, affiliation
    with open(badgeDOICSV, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            badges = []
            if row[2] == 'Yes' or row[2] == '1':
                badges.append('available')
            if row[3] == 'Yes' or row[3] == '1':
                badges.append('functional')
            if row[4] == 'Yes' or row[4] == '1':
                badges.append('reproduced')

            # xmlcharrrefreplace ensures that special characters are replaced with XML/HTML equivalent
            badge_doi[row[0]] = {'papid': row[1],
                        'aa': row[2],
                        'af': row[3],
                        'rr': row[4],
                        'badges': ','.join(badges),
                        'doi': row[5],
                        'repository': row[6]}

    print(f'Read {len(badge_doi)} badge decisions and DOIs.')

    return badge_doi

# author dictionary
# apdxid,firstname,lastname,fullname,email,institute
# Generated via HotCRP download
def read_authors(authorCSV):
    authors = defaultdict(list)

    # Expected format (separated by comma): firstname, lastname, email, affiliation
    with open(authorCSV, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            # xmlcharrrefreplace ensures that special characters are replaced with XML/HTML equivalent
            authors[row[0]].append({'first': html.escape(row[1]),
                        'last': html.escape(row[2]),
                        'email': html.escape(row[4]),
                        'aff': html.escape(row[5])})

    print(f'Read {len(authors)} authors.')

    return authors

def import_artifact_info_zenodo(doi):

    id = doi.split('.')[2]
    url = f'https://zenodo.org/record/{id}/export/json'

    # print(f'{doi}: accesses {url} for information')

    with urllib.request.urlopen(url) as loader:
        page = html.unescape(loader.read().decode())
        page = page[page.find('{'):page.find('</pre>')]
        try:
            data = json.loads(page)
        except json.decoder.JSONDecodeError:
            print(f'doi {doi} is broken, likely updated to a new one or does not exist')
            exit()

        return data['metadata']['description']

if __name__ == '__main__':
    authors = read_authors(sys.argv[1])
    badges = read_badges_doi(sys.argv[2])
    papers = read_papers(sys.argv[3])
    outputdir = sys.argv[4]

    for apdxid, artifact in badges.items():

        id = artifact['doi'][artifact['doi'].rfind('.')+1:]
        host = artifact['doi'][artifact['doi'].find('/')+1: artifact['doi'].rfind('.')]
        out = f'{outputdir}/' if outputdir else ""
        out += f'{host}.{id}'

        if not os.path.exists(f'{out}/{host}.{id}/meta'):

            description = ""
            if "zenodo" in artifact['doi']:
                description = import_artifact_info_zenodo(artifact['doi'])

            print(f'  - tittle: "{papers[artifact["papid"]]["title"]}"\n'
                  f'    badges: "{artifact["badges"]}"\n'
                  f'    paper_url: "{papers[artifact["papid"]]["refdoi"]}"\n'
                  f'    artifact_url: "{artifact["doi"]}"\n'
                  f'    repository_url: "{artifact["repository"]}"\n')

            metadata = generate_acmdl_artifact_metafile(authors[apdxid],
                                            artifact['doi'],
                                            papers[artifact['papid']]['refdoi'],
                                            papers[artifact['papid']]['title'],
                                            description, artifact['badges'])

            os.makedirs(f'{out}/{host}.{id}/meta')
            with open(f'{out}/{host}.{id}/meta/{host}.{id}.xml', 'w') as metafile:
                metafile.write(metadata)

            copyfile('manifest.xml', f'{out}/manifest.xml')

            make_archive(f'{outputdir}/artifacts_{host}.{id}_{datetime.now().strftime("%Y%m%d")}', 'zip', f'{out}/')
