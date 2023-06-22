from jira import JIRA
from IssueObject import IssueObject
from XMLExport import XMLExporter

jira = JIRA('https://Temp.atlassian.net', basic_auth=('', ''))

def main():
    issues = []
    start_range = 0
    while start_range <= 400:
        issues_in_proj = jira.search_issues('project=QD and labels != Migrate_to_Zephyr', maxResults=100, startAt=start_range)
        for i in issues_in_proj:
            issues.append(IssueObject(i, jira))
        start_range += 100

    test_cases = []
    for issue in issues:
        test_cases = test_cases + (issue.create_test_cases())
    
    JOTSW = []
    LEETS = []
    JURY = []
    REACT_REUSABLE = []
    REACT_STARTER_APP = []

    for i in test_cases:
        if str(i.folder).lower() == 'JOTSW'.lower():
            JOTSW.append(i)
        elif str(i.folder).lower() == 'LEETS'.lower():
            LEETS.append(i)
        elif str(i.folder).lower() == 'JURY'.lower():
            JURY.append(i)
        elif str(i.folder).lower() == 'REACT REUSABLE LIBRARY'.lower():
            REACT_REUSABLE.append(i)
        elif str(i.folder).lower() == 'REACT STARTER APP'.lower():
            REACT_STARTER_APP.append(i)

    XMLExporter(JOTSW, 'JOTS - Warrant', 'JOTSW')
    XMLExporter(LEETS, 'Leets', 'LEETS')
    XMLExporter(JURY, 'Jury', 'Jury')
    XMLExporter(REACT_REUSABLE, 'React Reusable Library', 'React_Reusable')
    XMLExporter(REACT_STARTER_APP, 'React Starter App', 'React_Starter_App')

if __name__ == "__main__":
    main()
