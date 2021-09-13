import sublime
import sublime_plugin


class CancerSwitchVersion(sublime_plugin.TextCommand):
    def run(self, edit):

        Selected = self.view.sel()

        for sel in Selected:
            inputs = self.view.substr(sel).strip()
            printPage = ''

            for line in inputs.splitlines():

                replace_arr = [['.CN','.CH'],['_CN','_CH'],['"CN','"CH'],['>CN<','>CH<'],['<!--CN-->','<!--CH-->'],['@fir',''],['autosum.2','autosum.5'],['style="dev" cond="not gv.isSST() and (gv.survey.root.state.dev or gv.survey.root.state.testing)"','where="execute,survey,report"'],['@LongValidate','LongValidate(this)'],[',bmrhide.3',''],['bmrhide.3,',''],['uses="bmrhide.3"',''],['hide:list="','ss:hidelist="'],['<style copy="ShowHideColumnC2" />','<style copy="ShowHideColumnC2" /> \n <style copy="bmrhide"/>'],['<style copy="ShowHideColumnC2"/>','<style copy="ShowHideColumnC2" /> \n <style copy="bmrhide"/>'],['<style copy="ShowHideColumnC3" />','<style copy="ShowHideColumnC3" /> \n <style copy="bmrhide"/>'],['<style copy="ShowHideColumnC3"/>','<style copy="ShowHideColumnC3" /> \n <style copy="bmrhide"/>'],['<style copy="ShowHideColumnC4" />','<style copy="ShowHideColumnC4" /> \n <style copy="bmrhide"/>'],['<style copy="ShowHideColumnC4"/>','<style copy="ShowHideColumnC4" /> \n <style copy="bmrhide"/>'],['uses="fir.2,bmrhide.3"',''],['OpenSpecifyChkAll(99)',''],['OpenSpecifyChkAll(98)',''],['OpenSpecifyChk(99)',''],['OpenSpecifyChk(98)','']]
                for replace_item in replace_arr:
                    if replace_item[0] in line:
                        line = line.replace(replace_item[0],replace_item[1])

                printPage += line + "\n"


            self.view.replace(edit, sel, printPage)
