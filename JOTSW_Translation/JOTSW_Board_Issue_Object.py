from pprint import pprint
from JOTSW_TestCaseObject import JOTWSTestCase
import fnmatch

starting_list_values = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '#',
]

class JOTSWIssueObject():
    def __init__(self, i, jira) -> None:
        self.jira = jira
        self.column = i.fields.status.name
        self.key = i.key
        self.name = i.fields.summary
        self.url = i.self
        self.ID = i.id
        self.comments = self._get_comments()
        self.labels = i.fields.labels
        self.test_cases = []
        self.check_if_test_case()

    def _get_comments(self):
        comments = []
        commentObjects = self.jira.comments(self.key)
        for i in commentObjects:
            comments.append(i.body)
        return comments

    def check_if_test_case(self):
        for i in self.comments:
            body = i.split('\n')
            if fnmatch.filter(body, '*Test Case*') != []:
                self._split_test_cases(i)

    def _split_test_cases(self, i):
        comment = i.split('Test Case:')
        for e in comment:
            steps = self._get_test_case_steps(e)
            test_type = self._get_test_type(e)
            description = self._get_test_case_description(e)
            if steps != [] and 'has no case description' not in description and test_type != 'unknown' and test_type != 'regression':
                pprint(f'{self.key} - {self.name}')
                test_case = JOTWSTestCase(self, steps, description, test_type)
                self.test_cases.append(test_case)
        

    def _get_test_case_steps(self, comment):
        test_case = comment.split('\n')
        steps = []
        for i in test_case:
            if list(filter((i.replace(' ','')).startswith, starting_list_values)) != [] and 'Test Steps:' not in i:
                step = i
                step = (''.join([i for i in step[0:3] if not i.isdigit()]) + step[3:]).lstrip('.').lstrip('#')
                if ' ' in step[0:1]:
                    step = step[1:]
                steps.append(step)
        return steps
        
    def _get_test_type(self, comment):
        test_case = comment.split('\n')
        test_type = fnmatch.filter(test_case, '*Type:*')
        try:
            if 'r-' in test_type[0].lower().strip(' '):
                return 'regression'
            else:
                return 'functional'
        except Exception:
            return 'unknown'

    def _get_test_case_description(self, comment):
        body = comment.split('\n')
        description = fnmatch.filter(body, '*Case Description:*')
        try:
            description = description[0].replace('>Case Description:', '').replace('> Case Description:', '').replace('Case Description:', '').strip('*')
            if ' ' in description[0:1]:
                description = description[1:]
        except Exception:
            description = f'{self.name} has no case description'
        return description

    def return_test_cases(self):
        return self.test_cases