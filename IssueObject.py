from TestCaseObject import TestCaseObject

class IssueObject():
    def __init__(self, i, jira) -> None:
        self.jira = jira
        self.column = i.fields.status.name
        self.key = i.key
        self.name = i.fields.summary
        self.url = i.self
        self.ID = i.id
        self.comments = self._get_comments()
        self.labels = i.fields.labels

    def _get_comments(self):
        comments = []
        commentObjects = self.jira.comments(self.key)
        for i in commentObjects:
            comments.append(i.body)
        return comments

    def return_comments(self):
        return self.comments

    def create_test_cases(self):
        test_cases = []
        for i in self.comments:
            test_case = TestCaseObject(i, self)
            if test_case.isTestCase is True and test_case.test_type != 'regression' and test_case.test_type != 'unknown':
                test_cases.append(test_case)
        return test_cases