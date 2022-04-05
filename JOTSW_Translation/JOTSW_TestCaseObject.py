class JOTWSTestCase():
    def __init__(self, parent_issue, steps, description, test_type) -> None:
        self.parent_issue = parent_issue
        self.title = parent_issue.name
        self.key = parent_issue.key
        self.test_type = test_type
        self.description = description
        self.steps = steps