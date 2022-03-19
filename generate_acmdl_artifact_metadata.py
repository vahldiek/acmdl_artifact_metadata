import csv
from os import read
import sys
from datetime import datetime

def generate_acmdl_artifact_metafile(authors, artifactDOI, relatedDOI, paperTitle, description, badges, zipfile="", readme=""):

    # print(f"Generating metadata for {paperTitle} receiving {badges} by {authors} in {artifactDOI} {relatedDOI}")

    return generate_acmdl_artifact_metafile_header(artifactDOI, paperTitle) + '\n' \
            + generate_acmdl_artifact_metafile_authors(authors) + '\n' \
            + generate_acmdl_artifact_metafile_footer(relatedDOI, description, zipfile, readme, badges)

def generate_acmdl_artifact_metafile_header(artifactDOI, paperTitle):
    # Generate header
    return f'<?xml version="1.0" encoding="UTF-8"?>\n' \
            f'<mets xmlns="http://www.loc.gov/METS/" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/METS/ http://www.loc.gov/standards/mets/mets.xsd" TYPE="artifact-doe">\n' \
            f' <mets:dmdSec xmlns:mets="http://www.loc.gov/METS/" ID="DMD">\n' \
            f'    <mets:mdWrap MDTYPE="MODS">\n' \
            f'      <mets:xmlData>\n' \
            f'        <mods xmlns="http://www.loc.gov/mods/v3" xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods.xsd">\n' \
            f'          <mods:identifier xmlns:mods="http://www.loc.gov/mods/v3" type="doi">{artifactDOI}</mods:identifier>\n' \
            f'          <mods:titleInfo xmlns:mods="http://www.loc.gov/mods/v3" ID="title">\n' \
            f'            <mods:title>Implementation of the article &quot;{paperTitle}&quot;</mods:title>\n' \
            f'            <mods:subTitle />\n' \
            f'          </mods:titleInfo>'

def generate_acmdl_artifact_metafile_authors(authors):
    str_ret = ""
    # Generate authors
    i = 0
    for a in authors:
        str_ret += f'          <mods:name xmlns:mods="http://www.loc.gov/mods/v3" ID="artseq-{i}">\n' \
            f'            <mods:namePart type="given">{a["first"]}</mods:namePart>\n' \
            f'            <mods:namePart type="family">{a["last"]}</mods:namePart>\n' \
            f'            <mods:namePart type="termsOfAddress"></mods:namePart>\n' \
            f'            <mods:displayForm>{a["first"]} {a["last"]}</mods:displayForm>\n' \
            f'            <mods:nameIdentifier type="ORCID"></mods:nameIdentifier>\n' \
            f'            <mods:role>\n' \
            f'              <mods:roleTerm>Contributor</mods:roleTerm>\n' \
            f'            </mods:role>\n' \
            f'            <mods:nameIdentifier type="email">{a["email"]}</mods:nameIdentifier>\n' \
            f'            <mods:affiliation>{a["aff"]}</mods:affiliation>\n' \
            f'          </mods:name>\n' \

        # make author sequence number unique
        i += 1

    return str_ret

def generate_acmdl_artifact_metafile_footer(relatedDOI, description, zipfile, readme, badges):

    available_badges = {
        'available': '                <mods:topic authority="artifacts_available_v101">Artifacts Available</mods:topic>',
        'functional': '                <mods:topic authority="artifacts_evaluated_functional_v101">Artifacts Evaluated — Functional</mods:topic>',
        'reproduced': '                <mods:topic authority="results_reproduced_v101">Results Reproduced</mods:topic>'
    }
    str_badges =""
    for b in badges.split(','):
        str_badges += '\n' + available_badges[b]

    file1 = "" if not zipfile or not readme else f'''                <atpn:textFiles nested-label="NONE">
                    <atpn:nestedValue alt-text="Read Me">{readme}</atpn:nestedValue>
                </atpn:textFiles>
                <atpn:packageFiles nested-label="NONE">
                    <atpn:nestedValue alt-text="Artifact">{zipfile}</atpn:nestedValue>
                </atpn:packageFiles>'''

    file2 = "" if not zipfile or not readme else f'''    <mets:fileSec xmlns:mets="http://www.loc.gov/METS/">
        <mets:fileGrp ID="textFiles-group">
        <mets:file ID="textFiles-{readme}">
            <mets:FLocat LOCTYPE="URL" xlink:href="file://{readme}"></mets:FLocat>
        </mets:file>
        </mets:fileGrp>
        <mets:fileGrp ID="packageFiles-group">
        <mets:file ID="packageFiles-{zipfile}">
            <mets:FLocat LOCTYPE="URL" xlink:href="file://{zipfile}"></mets:FLocat>
        </mets:file>
        </mets:fileGrp>
    </mets:fileSec>'''

    return f'''              <mods:subject xmlns:mods="http://www.loc.gov/mods/v3" authority="artifact_type" ID="type">
                <mods:topic authority="artfc-software">software</mods:topic>
            </mods:subject>
            <mods:subject xmlns:mods="http://www.loc.gov/mods/v3" authority="reproducibility-types" ID="badges">{str_badges}
            </mods:subject>
            <mods:relatedItem xmlns:mods="http://www.loc.gov/mods/v3" displayLabel="Related Article" xlink:href="10.1145/{relatedDOI}" ID="relatedDoi01"></mods:relatedItem>
            <mods:extension xmlns:mods="http://www.loc.gov/mods/v3">
                <atpn:do-extensions xmlns:atpn="http://www.atypon.com/digital-objects" xsi:schemaLocation="http://www.atypon.com/digital-objects http://www.atypon.com/digital-objects/digital-objects.xsd">
                <atpn:description><![CDATA[<p>{description}</p>]]></atpn:description>
                <atpn:copyright>Author(s)</atpn:copyright>
                <atpn:version>1.0</atpn:version>
                <atpn:softwareDependencies />
                <atpn:hardwareDependencies />
                <atpn:installation />
                <atpn:otherInstructions />
                <atpn:eiInstallation />
                <atpn:eiParameterization />
                <atpn:eiEvaluation />
                <atpn:eiWorkflow />
                <atpn:eiOtherInstructions/>
                <atpn:dataDocumentation />
                <atpn:provenance></atpn:provenance>{file1}
                <atpn:accessCondition>free</atpn:accessCondition>
                <atpn:licenseUrl />
                <atpn:keywords nested-label="NONE">
                </atpn:keywords>
                <atpn:baseDoi>10.1145/artifact-doe-class</atpn:baseDoi>
                </atpn:do-extensions>
            </mods:extension>
            <mods:originInfo xmlns:mods="http://www.loc.gov/mods/v3">
                <mods:dateIssued encoding="iso8601">{datetime.now().strftime("%Y-%m-%d")}</mods:dateIssued>
            </mods:originInfo>
            </mods>
        </mets:xmlData>
        </mets:mdWrap>
    </mets:dmdSec>{file2}
    <mets:structMap xmlns:mets="http://www.loc.gov/METS/">
        <mets:div></mets:div>
    </mets:structMap>
</mets>'''

def read_author_csv(authorCSV):
    authors = []

    # Expected format (separated by comma): firstname, lastname, email, affiliation
    with open(authorCSV, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            # xmlcharrrefreplace ensures that special characters are replaced with XML/HTML equivalent
            authors.append({'first': row[0].encode('ascii', 'xmlcharrefreplace').decode(),
                        'last': row[1].encode('ascii', 'xmlcharrefreplace').decode(),
                        'email': row[2].encode('ascii', 'xmlcharrefreplace').decode(),
                        'aff': row[3].encode('ascii', 'xmlcharrefreplace').decode()})

    return authors

if __name__ == '__main__':
    authorCSV = sys.argv[1]
    artifactDOI = sys.argv[2]
    relatedDOI = sys.argv[3]
    paperTitle = sys.argv[4].encode('ascii', 'xmlcharrefreplace').decode()
    description = sys.argv[5].encode('ascii', 'xmlcharrefreplace').decode()
    zipfile = sys.argv[6].encode('ascii', 'xmlcharrefreplace').decode()
    readme = sys.argv[7].encode('ascii', 'xmlcharrefreplace').decode()
    badges = sys.argv[8]

    authors = read_author_csv(authorCSV)

    print(generate_acmdl_artifact_metafile(authors, artifactDOI, relatedDOI, paperTitle, description, badges, zipfile, readme))