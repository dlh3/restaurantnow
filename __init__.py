from django.core.files import File

# Project settings, available as project.locale
locale = {}

def loadSettings(fileloc):
    try:
        filedat = File(open(fileloc))
        for line in filedat:
            parseLine(line)
    except IOError:
        print "Failed to open " + fileloc
        pass
    except IndexError:
        pass

def parseLine(line):
    if len(line.strip()) == 0 or line.startswith(('[', '#')):
        return
    keypair = line.split('=', 1)
    locale[keypair[0].strip()] = keypair[1].strip()


loadSettings('settings/default/default.ini')
loadSettings('settings/store.ini')
