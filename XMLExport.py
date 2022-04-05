from operator import indexOf
import xml.etree.ElementTree as gfg 

class XMLExporter():
    def __init__(self, testCases, board_name, name) -> None:
        self.testCases = testCases
        self.board_name = board_name
        self.filename = f'export/{name}.xml'
        self.xml_str = self._create_xml_str_base()
        with open(self.filename, 'wb') as f:
            self.xml_str.write(f)

    def _create_xml_str_base(self):
        root = gfg.Element("project")

        projectID = gfg.SubElement(root, "projectId")
        projectID.text = '10009'

        projectKey = gfg.SubElement(root, "projectKey")
        projectKey.text = 'QD'

        exportDate = gfg.SubElement(root, "exportDate")
        exportDate.text = '2022-04-04 15:44:29 UTC'

        folders = gfg.SubElement(root, "folders")
        folder = gfg.SubElement(folders, "folder")
        folder.attrib["fullPath"] = f'Regression Test/{self.board_name}'
        folder.attrib["index"] = str(1)
        
        testCases = gfg.SubElement(root, "testCases")
        for i in self.testCases:
                testCase = gfg.SubElement(testCases, "testCase")

                createdBy = gfg.SubElement(testCase, "createdBy")
                createdBy.text = 'Job Thompson'

                createdOn = gfg.SubElement(testCase, "createdOn")
                createdOn.text = '2022-04-04 15:44:29 UTC'

                issues = gfg.SubElement(testCase, "issues")
                issue = gfg.SubElement(issues, "issue")
                key = gfg.SubElement(issue, "key")
                key.text = i.key
                summary = gfg.SubElement(issue, "summary")
                summary.text = i.title

                name = gfg.SubElement(testCase, "name")
                name.text = f'{i.title}'

                objective = gfg.SubElement(testCase, "objective")
                objective.text = f'{i.description}'

                precondition = gfg.SubElement(testCase, "precondition")
                precondition.text = f'<![CDATA[]]>'

                status = gfg.SubElement(testCase, "status")
                status.text = f'Draft'

                testScript = gfg.SubElement(testCase, "testScript")
                testScript.attrib["type"] = "steps"
                steps = gfg.SubElement(testScript, "steps")

                for e in i.steps:
                    step = gfg.SubElement(steps, "step")
                    customFields = gfg.SubElement(step, "customFields")
                    step.attrib["index"] = str(indexOf(i.steps, e))
                    description = gfg.SubElement(step, "description")
                    description.text = f'{e}'
                    expectedResult = gfg.SubElement(step, "expectedResult")
                    expectedResult.text = f'<![CDATA[]]>'

        return gfg.ElementTree(root)
