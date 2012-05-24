#!/usr/bin/env python

import argparse
import csv
import re
import StringIO

OLD_SUBJECTS = "subjects"
NEW_SUBJECTS = "subjects.new"
CSV_PATH = "mapping.csv"

def subject_titles(path):
    """Given a path to a subjects file, returns a dictionary of subject keys
    mapped to subject titles.
    """
    f = open(path, "rb")
    contents = \
        StringIO.StringIO(fold_vertical_space(strip_comments(f.read())))
    return dict(line[0:2] for line in csv.reader(contents, delimiter=":"))

def strip_comments(string):
    """Strips comment lines from a string.
    """
    return re.sub(r"^#.*$", "", string, flags=re.MULTILINE)

def fold_vertical_space(string):
    """Folds vertical space in a string.
    """
    string = re.sub(r"(\n\s*)+", "\n", string)
    return re.sub(r"(?:^\n+|\n+$)", "", string)

def create_mapping_csv(csv_path, old_path, new_path):
    """Given a path to a CSV file to write, and a path to an old and new
    subjects file, produces a CSV describing differences betweeen them.
    """
    writer = csv.writer(open(csv_path, "wb"))
    writer.writerow(["Key", "Old title", "New title", "Is orphaned", "Is new"])
    
    old = subject_titles(old_path)
    new = subject_titles(new_path)

    for key in old.keys():
        old_title = old[key]
        try:
            new_title = new[key]
            orphaned = False
        except KeyError:
            new_title = "<Orphaned>"
            orphaned = True

        if old_title != new_title:
            writer.writerow([key, old_title, new_title, \
                             "yes" if orphaned else "no", "no"])

    # now for totally new departments :o
    new_keys = set(new.keys()) - set(old.keys())

    for key in new_keys:
        old_title = "<New>"
        new_title = new[key]
        writer.writerow([key, old_title, new_title, "no", "yes"])
    
def main():
    """
    """
    parser = argparse.ArgumentParser(description="Describe differences " +
                                     "between EPrints subject files.")
    parser.add_argument("old_subjects", help="Path to old subjects file.")
    parser.add_argument("new_subjects", help="Path to new subjects file.")
    parser.add_argument("out", help="Path to which to write CSV file.")
    args = parser.parse_args()

    create_mapping_csv(args.out, args.old_subjects, args.new_subjects)

if __name__ == '__main__':
    main()
