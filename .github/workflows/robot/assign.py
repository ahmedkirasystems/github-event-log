import os
import json
from github import Github

def read_file(filename):
    try:
        return open(filename, 'r', encoding="utf8")
    except IOError:
        print("Could not read file:", filename)

def main():
    # Read environment variables
    event_path_file = os.environ.get("GITHUB_EVENT_PATH")
    reviewer = os.environ.get("REVIEWER")
    github_token = os.environ.get("GITHUB_TOKEN")

    # Read file
    data = json.load(read_file(event_path_file))

    # Get info from data
    pr = data['pull_request']['number']
    github_repo = data['repository']['full_name']

    # First create a Github instance:
    # using an access token
    client = Github(github_token)

    repo = client.get_repo(github_repo)
    probj = repo.get_pull(pr)
    issue = repo.get_issue(pr)
    print("Adding comment to the PR")
    issue.create_comment("Adding `" + reviewer + "` as reviewer(s) PR to")
    print("Adding reviewer to the ticket")
    probj.create_review_request(reviewers=[reviewer])

if __name__ == "__main__":
    main()
