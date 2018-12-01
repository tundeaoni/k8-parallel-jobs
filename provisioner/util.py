import yaml,sys
from jinja2 import Template

def usage():
    scriptName = sys.argv[0]
    print "Usage\n"
    print "Help : "
    print "  " + scriptName + " help  \n"
    print "provision : "
    print "  " + scriptName + " provision  \n"

def fromYaml(sourceFile):
    with open(sourceFile, "r") as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print exc
            return False

def toYaml(destinationFile, data):
    # print destinationFile , data
    with open(destinationFile, "w+") as outfile:
        try:
            yaml.dump(data, outfile, default_flow_style=True)
            return True
        except yaml.YAMLError as exc:
            print exc
            return False

# https://gist.github.com/keithweaver/b0912519d410b7e2ab3c98bf350bcfc2
def getFileContent(pathAndFileName):
    with open(pathAndFileName, 'r') as theFile:
        # Return a list of lines (strings)
        # data = theFile.read().split('\n')
        # Return as string without line breaks
        # data = theFile.read().replace('\n', '')
        # Return as string
        data = theFile.read()
        return data

def render(template_file , values):
    content = getFileContent(template_file)
    # t  = Template(content)
    return Template(content).stream(values)
    # return t.render(values)
