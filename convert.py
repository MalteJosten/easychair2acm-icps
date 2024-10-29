import csv
import sys

NAME = sys.argv[1]
PROCEEDING_ID = sys.argv[2]
PAPER_TYPE = sys.argv[3]
COPYRIGHT_CONTACT = sys.argv[4]

fields = ["proceedingID", "event_tracking_number/theirnumber", "paper_type", "thetitle", "prefix", "first_name", "middle_name", "last_name", "suffix", "author_sequence_no", "contact_author", "ACM_profile_id", "ACM_client_no", "orcid", "email", "department_school_lab", "institution/AFFILIATION", "city", "state_province", "country", "secondary_department_school_lab", "secondary_institution", "secondary_city", "secondary_state_province", "secondary_country", "section_title", "section_seq_no", "published_article_number", "start_page", "end_page", "article_seq_no", "art_submission_date", "art_approval_date", "source", "abstract"]

papers = {}
authors = []
co_authors = {}

with open("papers.csv", "r") as papers_file:
    papers_reader = csv.reader(papers_file, delimiter=",")
    next(papers_reader)
    for entry in papers_reader:
        if entry[4] == "ACCEPT":
            papers[entry[0]] = entry[1]

with open("authors.csv", "r") as authors_file:
    authors_reader = csv.reader(authors_file, delimiter=",")
    next(authors_reader)
    for entry in authors_reader:
        if (entry):
            names = entry[1].split(" ")
            if len(names) == 1:
                first_name = ""
                last_name = names[0]
            else:
                first_name = names[0]
                last_name = names[-1]

            authors.append({
                "paper-id": entry[0],
                "first_name": first_name,
                "last_name": last_name,
                "email": entry[2],
                "country": entry[3],
                "affiliation": entry[4]
            })

with open("co_authors.csv", "r") as co_authors_file:
    co_authors_reader = csv.reader(co_authors_file, delimiter=",")
    next(co_authors_reader)
    for entry in co_authors_reader:
        co_authors[entry[0]] = entry[2]

metadata = []
author_counter = {}

for author in authors:
    meta_entry = [""] * len(fields)
    paper_id = author["paper-id"]

    if not author["paper-id"] in author_counter.keys():
        author_counter[paper_id] = 1

    meta_entry[0] = PROCEEDING_ID
    meta_entry[1] = paper_id
    meta_entry[2] = PAPER_TYPE
    meta_entry[3] = papers[paper_id]
    meta_entry[5] = author["first_name"]
    meta_entry[7] = author["last_name"]
    meta_entry[9] = author_counter[paper_id]
    meta_entry[10] = "yes" if author["email"] == co_authors[paper_id] else "no"
    meta_entry[14] = author["email"]
    meta_entry[16] = author["affiliation"]
    meta_entry[19] = author["country"]
    meta_entry[33] = COPYRIGHT_CONTACT

    author_counter[paper_id] = author_counter[paper_id] + 1

    metadata.append(meta_entry)

with open(f"{NAME}-icps.csv", "w") as metadata_file:
    metadata_writer = csv.writer(metadata_file, delimiter=',')
    metadata_writer.writerow(fields)
    for entry in metadata:
        metadata_writer.writerow(entry)

print("Done.")
