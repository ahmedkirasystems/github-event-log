import os
import sys
import json
from github import Github


def read_file(filename):
    try:
        return open(filename, "r", encoding="utf8")
    except IOError:
        print("Could not read file:", filename)


def main():
    # Read environment variables
    event_path_file = os.environ.get("GITHUB_EVENT_PATH")
    github_token = os.environ.get("GITHUB_TOKEN")
    reviewer = os.environ.get("REVIEWER")

    # Read file
    data = json.load(read_file(event_path_file))

    # Get info from data
    pr = data['pull_request']['number']
    github_repo = data['repository']['full_name']
    github_org = github_repo.split('/')[0]

    # First create a Github instance:
    # using an access token
    client = Github(github_token)

    # Obtain Team membership
    # org = client.get_organization(github_org)
    # team = org.get_team_by_slug(team)
    # team_members = team.get_members()

    # Get repo info
    repo = client.get_repo(github_repo)

    # Get PR
    probj = repo.get_pull(pr)
    # Current head commit to ensure that's been approved
    head_sha = probj.head.sha
    # Get reviews
    reviews = probj.get_reviews()

    # number of approvals to be provided
    approvals = 0
    # team_approvals = 0

    # Loop over all the reviews
    for review in reviews:

        # Get users info from the review
        user = review.user

        # Select ones which are approved and are provided against current sha
        if review.state == "APPROVED" and review.commit_id == head_sha and user.login == reviewer:

            # Check out many approvals were provided
            approvals += 1

    # If approval count is less than 2
    if approvals >= 1: # and team_approvals >= 1:
        message = (
            """
               Approval count `%s` meets the requirement of >= `1`
               """
            % (approvals)
        )
        print(message)
        print("Required approvals have been provided")
        issue.create_comment(message)
    else:
        print("Approval count is less than 2\nExiting with error")
        issue.create_comment("Required approvals haven't been met")
        sys.exit(1)


if __name__ == "__main__":
    main()
