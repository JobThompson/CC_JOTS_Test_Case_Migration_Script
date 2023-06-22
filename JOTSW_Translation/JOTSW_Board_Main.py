from jira import JIRA
from JOTSW_Board_Issue_Object import JOTSWIssueObject
from XMLExport import XMLExporter

jira = JIRA('https://Temp.atlassian.net', basic_auth=('', ''))

def main():
    issues = []
    start_range = 0
    while start_range <= 700:
        issues_in_proj = jira.search_issues('project=JOTW and labels != Migrate_to_Zephyr', maxResults=100, startAt=start_range)
        for i in issues_in_proj:
            issues.append(JOTSWIssueObject(i, jira))
        start_range += 100

    test_cases = []
    for issue in issues:
        test_cases = test_cases + (issue.return_test_cases())

    XMLExporter(test_cases, 'JOTS - Warrant', 'JOTSW')

if __name__ == "__main__":
    main()
