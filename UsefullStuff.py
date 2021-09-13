import sublime
import sublime_plugin

class DupSecValidate(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
<res label="duplicateErr1">Duplicated answers. Please enter each response only once.</res>
<res label="seqErrOE">Please specify the input sequentially, starting from the first box.</res>

  <validate>
for eachRow in this.rows:
    if ([x.val for x in this.rows if not x.empty]).count(eachRow.val) gt 1:
        error(res.duplicateErr1, row = eachRow)
    if eachRow.label != "r1" and not eachRow.empty and this.rows[eachRow.index-1].empty:
        error(res.seqErrOE, row = this.rows[eachRow.index-1])
  </validate>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class SetEmpty(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
<style label="setEmpty" arg:lefttext="XXXX" name="question.left-blank-legend"><![CDATA[
\@if not col.group
<$(tag) class="cell empty used empty-left empty-$(pos) unused ${"desktop" if this.grouping.cols else "mobile"} border-collapse">
      $(lefttext)
    </$(tag)>
\@endif
]]></style>
<style label="setEmpty" arg:lefttext="XXXX" name="question.group-column"><![CDATA[
<$(tag) class="row row-col-legends row-col-legends-top colGroup">
<td class="cell empty used empty-left empty-top unused mobile border-collapse" rowspan="2">$(lefttext)</td>
    $(elements)
    $(right)
</$(tag)>
]]></style>

<style copy="setEmpty" arg:lefttext="XXXX"/>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class GroupRowsWithOrder(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
<exec when="init">
def group_rows_with_order( question, grouped_rows, static=False ):
    current_order = [row.index for row in question.rows.order]
    new_order     = []

    if not static:
        random.shuffle(grouped_rows)

    grouped_rows     = [question.attr(row).index for row in grouped_rows]

    first_item_index = current_order.index(grouped_rows[0])

    current_order.insert(first_item_index, grouped_rows)

    for row in current_order:
        if row == grouped_rows:
            new_order = new_order + row
        elif row not in grouped_rows:
            new_order.append(row)

    question.rows.order = new_order
</exec>

  <exec>
group_rows_with_order(this, ['r5', 'r6', 'r7'])
  </exec>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class PageTimerCounter(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
<res label="timer_second">second</res>
<res label="timer_seconds">seconds</res>

<style mode="after" name="respview.client.js" with="qualMain,"><![CDATA[
<script>
$ (document).ready( function() {
    $ ('#btn_continue').hide();
    var timer = parseInt($ ('.timer-counter').text());
    var setTimerText = setInterval( function() {
        timer = timer - 1
        $ ('.timer-counter').text(String(timer))
        if (timer == 1) {
            $ ('.timer-seconds').html('${res.timer_second}');
        } else {
            $ ('.timer-seconds').html('${res.timer_seconds}');
        }
        if (timer === 0) {
            $ ('#btn_continue').show();
            $ ('.timer-wrapper').hide();
            clearInterval(setTimerText);
        }
    },1000);
});
</script>
]]></style>

<div class="timer-wrapper">The button "Continue" will be revealed after <span class="timer-counter">10</span> <span class="timer-seconds">seconds</span>.</div>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class AutosumReadOnlyCol(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
 <style name="question.footer" label="autosum_read_only" mode="after"><![CDATA[
<script>
jQuery(document).ready( function() {
    jQuery(".read_only_col").find(':text').attr('tabindex', '-1');
    var allValidInputs = jQuery('.element').not('.read_only_col').find('.input').not('.oe');
    allValidInputs.on('change keyup paste focus', function(event){
        var inputSum = 0;
        var rowTyped = 0;
        var index = allValidInputs.index(jQuery(this));
        allValidInputs.eq(index).closest('tr').find('.element').not('.read_only_col').find('.input').each(function(index,n) {
            if (jQuery(n).val() == ''){
                    inputSum += 0;
                } else {
                    inputSum += parseInt(jQuery(n).val(), 10);  
                    rowTyped += 1
                }
        });
        if (inputSum <= 100 && inputSum >= 0 && rowTyped > 0) {
            var readOnlyVal = 100 - inputSum;
            allValidInputs.eq(index).closest('tr').find('.read_only_col .input').val(readOnlyVal.toString()).trigger('change');
        } else {
            allValidInputs.eq(index).closest('tr').find('.read_only_col .input').val('').trigger('change');
        }
    }).trigger('change');
});
</script>
<style>
.read_only_col {
    pointer-events: none;
    background-color: #EBEBEB !important;
}
</style>
]]></style>

ss:colClassNames="read_only_col"
 <style copy="autosum_read_only"/>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class AutosumReadOnlyRow(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
 <style name="question.footer" label="autosum_read_only_row" mode="after"><![CDATA[
<script>
jQuery(document).ready( function() {
    jQuery(".read_only_row").find(':text').attr('tabindex', '-1');
    var allValidInputs = jQuery('.element').not('.read_only_row').find('.input').not('.oe');
    allValidInputs.on('change keyup paste focus', function(event){
        var inputSum = 0;
        var rowTyped = 0;
        var index = allValidInputs.index(jQuery(this));
        var column_index = jQuery(this).attr('id').split(".")[1];
        var activeInputs = allValidInputs.eq(index).closest('.answers').find('.element').not('.read_only_row').find('.input[id*=".' + column_index + '."]')
        var readOnlyInputs = allValidInputs.eq(index).closest('.answers').find('.read_only_row .input[id*=".' + column_index + '."]')
        activeInputs.each(function(index,n) {
            if (jQuery(n).val() == ''){
                    inputSum += 0;
                } else {
                    inputSum += parseInt(jQuery(n).val(), 10);  
                    rowTyped += 1
                }
        });
        if (inputSum <= 100 && inputSum >= 0 && rowTyped > 0) {
            var readOnlyVal = 100 - inputSum;
            readOnlyInputs.val(readOnlyVal.toString()).trigger('change');
        } else {
            readOnlyInputs.val('').trigger('change');
        }
    }).trigger('change');
});
</script>
<style>
.read_only_row {
    pointer-events: none;
    background-color: #EBEBEB !important;
}
</style>
]]></style>

ss:rowClassNames="read_only_row"
<style copy="autosum_read_only_row"/>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

#TODO: Add only copy style if numpad_style exist
class NumpadStyle(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
  <style name="el.text" label="numpad_style"><![CDATA[
\@if row.styles.ss.preText or this.styles.ss.preText
${row.styles.ss.preText or this.styles.ss.preText or ""}
\@endif
<input type="tel" name="$(name)" id="$(id)" value="$(value)" size="3" class="input text-input" style="border: 1px solid #ccc;"/>
\@if row.styles.ss.postText or this.styles.ss.postText
${row.styles.ss.postText or this.styles.ss.postText or ""}
\@endif
]]></style>

<style copy="numpad_style" cond="(device.smartphone or device.tablet)"/>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class CardsortCardratingAutosubmit(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
   <style label="cardsortAutosubmit" mode="after" name="question.footer" wrap="ready"><![CDATA[
$ ('.sq-cardsort-body').click(function() {
    if ($ ('.sq-cardsort-progress').html() == '-/-') {
        $ ('#btn_continue').trigger('click');
    }
    var cntr = 0;
    $ ('.grid tbody:nth-child(2)').find('tr').each( function() {
        if ($ (this).find(':radio').is(':checked')) {
            cntr += 1;
        }
    });
    if (cntr === $ ('.grid tbody:nth-child(2)').find('tr').length) {
        $ ('#btn_continue').trigger('click');
    }
});
]]></style>

<style mode="after" name="respview.client.js"><![CDATA[
<script>
$ (document).ready(function() {
    $ (document).on('click touch', function() {
        setTimeout(function() {
            if ($ ('.sq-cardrating-widget[data-atend]').length) {
                $ ('#btn_continue').click();
            }
        }, 500);
    });
});
</script>
]]></style>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)


class CreateAltLeftRight(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            res_dic = {}

            allcontent = self.view.substr(sublime.Region(0, self.view.size()))
            res_rows = [line for line in allcontent.splitlines() if '<res' in line]

            for res_line in res_rows:
                res_label = res_line.split('label="')[1].split('"')[0]
                res_text = res_line.split('>')[1].split('</res')[0]
                res_dic[res_label] = res_text

            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '  '

                for input in inputs.splitlines(): 
                    res_label = input.split('rightLegend="${res.')[1].split('}"')[0]
                    left_text = input.split('">')[1].split('</row>')[0]
                    right_text = res_dic[res_label]

                    printPage = printPage + input.split('">')[0] +'" alt="{} / {}"'.format(left_text,right_text) + '>' + input.split('">')[1] + '\n'

                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class CreateLeftRight(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            question_label = ''

            leftRightStyle = '''
<style name="question.after" wrap="ready">
$ (".empty-left").html("&lt;center&gt;&lt;b&gt;${res.r_statementA}&lt;/b&gt;&lt;/center&gt;")
    $ (".empty-right").html("&lt;center&gt;&lt;b&gt;${res.r_statementB}&lt;/b&gt;&lt;/center&gt;")
</style>
'''
            statementsRes = '''
<res label="r_statementA">Statement A</res>
<res label="r_statementB">Statement B</res>
'''

            question_attr = '''
  rowLegend="both"
  shuffle="rows"
  surveyDisplay="desktop"
  uses="leftright.1"'''

            allcontent = self.view.substr(sublime.Region(0, self.view.size()))
            hasRes = True if len([line for line in allcontent.splitlines() if '<res label="r_statementA">' in line]) > 0 else False

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                res_rightLeg = ''

                printPage = ''

                for input in inputs.splitlines(): 

                    if '<row' in input:
                        left_text = input.split('">')[1].split('</row>')[0].split('|')[0].strip()
                        right_text = input.split('">')[1].split('</row>')[0].split('|')[1].strip()
                        row_label = input.split('label="')[1].split('"')[0]

                        printPage = printPage + input.split('">')[0] +'"' + ' rightLegend="${res.%srightLegend%s}"'%(question_label,row_label) + ' alt="{} / {}"'.format(left_text,right_text) + '>' + left_text + '</row>\n'

                        res_rightLeg = res_rightLeg + '<res label="{0}rightLegend{1}">{2}</res>\n'.format(question_label,row_label,right_text)
                    elif 'label="' in input and '<row' not in input and '<col' not in input and '<choice' not in input and '<res' not in input and '<noanswer' not in input:
                        question_label = input.split('label="')[1].split('"')[0]
                        printPage = printPage + input.split('>')[0] + question_attr + '>\n'
                    elif '</title>' in input:
                        printPage = printPage + input + '\n' + leftRightStyle
                    else:
                        printPage = printPage + input + '\n'



                printPage = res_rightLeg + '\n\n' + printPage

                if not hasRes:
                    printPage = statementsRes + '\n\n' + printPage

                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)


