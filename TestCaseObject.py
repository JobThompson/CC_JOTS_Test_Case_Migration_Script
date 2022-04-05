import numbers
import fnmatch

numbers = []
for i in range(100):
    numbers.append(str(i))

class TestCaseObject():
    def __init__(self, body, parent_issue) -> None:
        self.parent_issue = parent_issue
        self.title = parent_issue.name
        self.key = parent_issue.key
        self.folder = self._get_folder()
        self.body = body
        self.isTestCase = self._check_if_test_case()
        self.test_type = self._check_test_type()
        self.description = self._get_description()
        self.steps = self._get_steps()
        self.test_data = self._get_test_data()

    def _get_folder(self):
        if str((self.parent_issue.column)).lower().startswith('sprint'):
            return 'JOTSW'
        else:
            return str(self.parent_issue.column)

    def _check_if_test_case(self):
        body = self.body.split('\n')
        if fnmatch.filter(body, '*#Test Case*') != []:
            return True
        else:
            return False

    def _check_test_type(self):
        body = self.body.split('\n')
        test_type = fnmatch.filter(body, '*Type:*')
        try:
            if 'r-' in test_type[0].lower().strip(' '):
                return 'regression'
            else:
                return 'functional'
        except Exception:
            return 'unknown'

    def _get_steps(self):
        if self.isTestCase is False:
            return None
        steps = []
        body = self.body.split('\n')
        for i in body:
            if list(filter((i.replace(' ','')).startswith, numbers)) != []:
                step = i
                step = (''.join([i for i in step[0:3] if not i.isdigit()]) + step[3:]).lstrip('.')
                if ' ' in step[0:1]:
                    step = step[1:]
                steps.append(step)
        return steps

    def _get_description(self):
        if self.isTestCase is False:
            return None
        body = self.body.split('\n')
        description = fnmatch.filter(body, '*Case Description:*')
        try:
            description = description[0].replace('>Case Description:', '').replace('> Case Description:', '')
            if ' ' in description[0:1]:
                description = description[1:]
        except Exception:
            description = f'{self.title} has no case description'
        return description

    def _get_test_data(self):
        if self.isTestCase is False:
            return None
        body = self.body.split('\n')
        test_data = fnmatch.filter(body, '*Needed Data:*')
        try:
            test_data = test_data[0].replace('> Needed Data:', '').replace('>Needed Data:', '')
            if ' ' in test_data[0:1]:
                test_data = test_data[1:]
        except Exception:
            test_data = None
        return test_data
