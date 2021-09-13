import sublime,sublime_plugin,re

# clean whitespace
def cleanInput(input):
    #CLEAN UP THE TABS
    input = re.sub("\t+", " ", input)
    #CLEAN UP SPACES
    input = re.sub("\n +\n", "\n\n", input)
    #CLEAN UP THE EXTRA LINE BREAKS
    input = re.sub("\n{2,}", "\n", input)
    return input
    #CLEAN UP INITIAL SPACES AND THE EXTRA LINE BREAKS
    input = re.sub("\n\s{2,}", "\n", input)

class CohnMakeCols(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            sels = self.view.sel()
            input = ''
            for sel in sels:
                count = 0
                printPage = ''

                input = self.view.substr(sel)
                input = cleanInput(input)
                input = input.strip().split("\n")

                for x in range(0,len(input)):
                    input[x] = re.sub("^[a-zA-Z0-9]{1,2}[\.:\)][ \t]+", "\n", input[x])

                for line in input:
                    printPage += "  <$(type) label=\"$(t){lbl}\">{txt}</$(type)>\n".format(lbl=str(count+1), txt=input[count].strip())
                    count += 1

                self.view.replace(edit,sel, printPage.strip('\n'))
        except Exception as e:
            print (e)