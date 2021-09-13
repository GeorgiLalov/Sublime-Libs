import sublime
import sublime_plugin

class RmpdcGetVariables(sublime_plugin.TextCommand):
    def run (self,edit):
        try:
            API_NAME = ' '
            PROD_NAME = ' '
            CLASS_NAME = ' '
            CLASS_NAMES = ['Pain Relievers','Sedatives','Stimulants','Cannabinoids','Antidepressants']
            STATIC_INFO = ' '
            OTHER_PRODUCT_NAME = False
            
            B7_STATIC_INFO = 'RSNYR'
            B7_STAT_LIBS = [['PAIN','MED','HIGH','RELX','DOWN','WTDR','HURT','OTH'], 
                            ['MED','HIGH','RELX','DOWN','WTDR','HURT','OTH'], 
                            ['MED','HIGH','ATH','AWK','FOC','WGT','HURT','OTH'], 
                            ['PAIN','MED','HIGH','RELX','DOWN','WTDR','HURT','OTH'], 
                            ['PAIN','ANX','MOOD','MED','HIGH','ENRG','STRS','MOTV','HURT','OTH']]
            
            B8_STATIC_INFO = 'SPFY'
            
            B9_STAT_LIB_COLS = ['SWAL','CHEW','DISS','INH','INJ','DERM','OTH']
            B9_STAT_LIBS_ROWS = [['PAINYR','MEDYR','HIGHYR','RELXYR','DOWNYR','WTDRYR','HURTYR','OTHYR'], 
                                ['MEDYR','HIGHYR','RELXYR','DOWNYR','WTDRYR','HURTYR','OTHYR'], 
                                ['MEDYR','HIGHYR','ATHYR','AWKYR','FOCYR','WGTYR','HURTYR','OTHYR'], 
                                ['PAINYR','MEDYR','HIGHYR','RELXYR','DOWNYR','WTDRYR','HURTYR','OTHYR'], 
                                ['PAINYR','ANXYR','MOODYR','MEDYR','HIGHYR','ENRGYR','STRSYR','MOTVYR','HURTYR','OTHYR']]
            B9CHEW = False
            B9DERM = False
            HAS_LAST_QUESTION = False
            HAS_B17 = False

            B10_STATIC_INFO = 'RTEYR'
            
            B11_STATIC_INFO = 'SRCYR'
            B11_STAT_LIB = ['DOC','FORG','FFM','DLR','TAKE','ABRD','ONL','OTH']
            
            LOOP_LABEL = ' '
            InMasterSection = False
            
            TheBigCurrentSection = []
            TheSmallCurrentSection = []

            Selected = self.view.sel()
        
            for sel in Selected:
                inputs = self.view.substr(sel).strip()
                printPage = ''

                for input in inputs.splitlines(): 
                    
                    if "<!-- ============" in input and not InMasterSection:
                        TheBigCurrentSection.append(input)
                        InMasterSection = True
                    elif "<!-- ============" in input and InMasterSection:
                        for EachSmallSection in TheBigCurrentSection:
                            if 'TYPE:' in EachSmallSection:
                                STATIC_INFO = str(EachSmallSection.split('TYPE: ')[1])
                                
                            if "OTH_PROD_NAME" in EachSmallSection: 
                                PROD_NAME = str(EachSmallSection.split('OTH_PROD_NAME: ')[1])
                                OTHER_PRODUCT_NAME = True
                                
                            if '<looprow' in EachSmallSection or '<loopvar' in EachSmallSection:
                                TheSmallCurrentSection.append(EachSmallSection)
                
                            if '</looprow>' in EachSmallSection:
                                for eachLine in TheSmallCurrentSection:
                                    if "product_name" in eachLine and not OTHER_PRODUCT_NAME:
                                        PROD_NAME = str(eachLine.split('<loopvar name="product_name">')[1].split('</loopvar>')[0])
                                        if 'other or unknown' in PROD_NAME :
                                            PROD_NAME = 'API'
                                            STATIC_INFO = 'OTH'
                                        elif 'unknown' in PROD_NAME:
                                            PROD_NAME = 'UNK'
                                        elif 'other' in PROD_NAME:
                                            PROD_NAME = 'OK'
                                        else:
                                            PROD_NAME = str(eachLine.split('<loopvar name="product_name">')[1].split('</loopvar>')[0])[:3].upper()

                                    if CLASS_NAME == CLASS_NAMES[1] or CLASS_NAME == CLASS_NAMES[4]:
                                        PROD_NAME = 'API'
                                    if "looprow label" in eachLine:
                                        LOOP_LABEL = str(CLASS_NAMES.index(CLASS_NAME) + 1) + '_' + str(eachLine.split('<looprow label="')[1].split('">')[0])

                                    if 'name="liquid">1' in eachLine:
                                        B9CHEW = True
                                    if 'name="patches">1' in eachLine:
                                        B9DERM = True
                                    if 'name="last_question"' in eachLine:
                                        HAS_LAST_QUESTION = True
                                    if 'name="last_question">survey,report,summary' in eachLine:
                                        HAS_B17 = True

                                TheSmallCurrentSection = []
                        
                                #PRINT VARIABLES: 
                                #PRINT B7
                                printPage += 'B7_'+LOOP_LABEL+'\n'

                                B7_STAT_LIB = B7_STAT_LIBS[CLASS_NAMES.index(CLASS_NAME)]
                                for x in B7_STAT_LIB:
                                    printPage += 'B7_'+LOOP_LABEL+'r' + str(B7_STAT_LIB.index(x)+1) + '\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO + '_' + B7_STATIC_INFO +'_'+ x+'\n'
                                #PRINT B8         
                                printPage += 'B8_'+LOOP_LABEL + '\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO + '_' + B7_STATIC_INFO + '_SPFY'+'\n'
                                printPage += 'noanswerB8_'+LOOP_LABEL+'_n1' + '\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO + '_' + B7_STATIC_INFO + '_IDK'+'\n'
                                #PRINT B9
                                printPage += 'B9_'+LOOP_LABEL+'\n'

                                B9_STAT_LIB_ROWS = B9_STAT_LIBS_ROWS[CLASS_NAMES.index(CLASS_NAME)]
                                for r in B9_STAT_LIB_ROWS:
                                    for c in B9_STAT_LIB_COLS:
                                        if c == 'CHEW' and B9CHEW:
                                            printPage += 'B9_'+LOOP_LABEL+'r' + str(B9_STAT_LIB_ROWS.index(r)+1) +'c' + str(B9_STAT_LIB_COLS.index(c)+1) + '\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO +'_'+ r +'_'+ c + '\t\t1'+'\n'
                                        elif c == 'DERM' and not B9DERM:
                                            printPage += 'B9_'+LOOP_LABEL+'r' + str(B9_STAT_LIB_ROWS.index(r)+1) +'c' + str(B9_STAT_LIB_COLS.index(c)+1) + '\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO +'_'+ r +'_'+ c + '\t\t1'+'\n'
                                        else:
                                            printPage += 'B9_'+LOOP_LABEL+'r' + str(B9_STAT_LIB_ROWS.index(r)+1) +'c' + str(B9_STAT_LIB_COLS.index(c)+1) + '\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO +'_'+ r +'_'+ c+'\n'
                                #PRINT B10
                                printPage += 'B10_'+LOOP_LABEL + '\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO + '_' + B10_STATIC_INFO + '_SPFY'+'\n'
                                printPage += 'noanswerB10_'+LOOP_LABEL+'_n1' + '\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO + '_' + B10_STATIC_INFO + '_IDK'+'\n'
                                #PRINT B11
                                printPage += 'B11_'+LOOP_LABEL+'\n'
                                for x in B11_STAT_LIB:
                                    printPage += 'B11_'+LOOP_LABEL+'r' + str(B11_STAT_LIB.index(x)+1) + '\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO + '_' + B11_STATIC_INFO +'_'+ x+'\n'
                                #PRINT B12
                                #printPage += 'B12_'+LOOP_LABEL + '\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO + '_' + B11_STATIC_INFO + '_SPFY'+'\n'
                                #printPage += 'noanswerB12_'+LOOP_LABEL+'_n1' + '\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO + '_' + B11_STATIC_INFO + '_IDK'+'\n'

                                #PRINT B13
                                printPage += 'B13_'+LOOP_LABEL + 'r1\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO + '_RECYR'+'\n'
                                #PRINT B14
                                printPage += 'B14_'+LOOP_LABEL + 'r1\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO + '_FIRST'+'\n'
                                #PRINT B15
                                printPage += 'B15_'+LOOP_LABEL + 'Ar1\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO + '_FREQYR_MNTH'+'\n'
                                printPage += 'B15_'+LOOP_LABEL + 'Br1\t' + API_NAME +'_'+ PROD_NAME +'_'+ STATIC_INFO + '_FREQYR_WK'+'\n'

                                if HAS_LAST_QUESTION:
                                    if HAS_B17:
                                        printPage += 'B17_'+LOOP_LABEL + '\t' + API_NAME + '_API_OD'+'\n'
                                    else:
                                        printPage += 'B17_'+LOOP_LABEL + '\n'

                                '''
                                # Without B13-B15
                                #PRINT B13
                                printPage += 'B13_'+LOOP_LABEL + 'r1\t' + '\n'
                                #PRINT B14
                                printPage += 'B14_'+LOOP_LABEL + 'r1\t' + '\n'
                                #PRINT B15
                                printPage += 'B15_'+LOOP_LABEL + 'Ar1\t' + '\n'
                                printPage += 'B15_'+LOOP_LABEL + 'Br1\t' + '\n'
                                '''
                                
                                #RESET 
                                OTHER_PRODUCT_NAME = False
                                B9CHEW = False
                                B9DERM = False
                                HAS_B17 = False
                                HAS_LAST_QUESTION = False

                        TheBigCurrentSection = []
                    else:
                        TheBigCurrentSection.append(input)

                        if 'API_NAME:' in input:
                            API_NAME = str(input.split('API_NAME: ')[1])
                        if "class_name" in input:
                            CLASS_NAME = str(input.split('<loopvar name="class_name">')[1].split('</loopvar>')[0])

                self.view.replace(edit, sel, printPage)
        
        except Exception as e:
            print (e)

class RmpdcCreateLoop(sublime_plugin.TextCommand):
    CURRENT_SECTION = 0
    CURRENT_SUB_SECTION = 0
    HAS_PATCH_IN_SECTION = False
    HAS_LIQUID_IN_SECTION = False
    LIQUID = 0
    PATCH = 0
    SubBrandsInEachLoop = []
    printPage = ''

    def print_looprow (self, CLASS, API, PRODUCT_NAME):
        self.printPage += '<looprow label="' + str(self.CURRENT_SECTION) + '_' + str(self.CURRENT_SUB_SECTION) + '">' + '\n'

        self.printPage += '    <loopvar name="class_name">' + str(CLASS) + '</loopvar>' + '\n'
        self.printPage += '    <loopvar name="api_name">' + str(API) + '</loopvar>' + '\n'
        self.printPage += '    <loopvar name="product_name">' + str(PRODUCT_NAME) + '</loopvar>' + '\n'
        self.printPage += '    <loopvar name="liquid">' + str(self.LIQUID) + '</loopvar>' + '\n'
        self.printPage += '    <loopvar name="patches">' + str(self.PATCH) + '</loopvar>' + '\n'

        self.printPage += '</looprow>' + '\n\n'

    def print_class (self, CLASS, API, API_NAME, TYPE):
        self.printPage += '<!-- ===========================================================================================================' + '\n'
        self.printPage += '\t\t\t\t\tCLASS: ' + str(CLASS) + ' / API: ' + str(API) + '\n'
        self.printPage += 'API_NAME: ' + str(API_NAME) + '\n'
        self.printPage += 'TYPE: ' + str(TYPE) + '\n'
        self.printPage += '============================================================================================================= -->' + '\n'

    def check_LIQ_PATCH (self, eachRow, TYPE):
        self.LIQUID = 0
        self.PATCH = 0

        if 'liquid' in eachRow.lower() or 'LIQ' in TYPE:
            self.LIQUID = 1
            self.HAS_LIQUID_IN_SECTION = True
        if 'patch' in eachRow.lower() or 'PATCH' in TYPE:
            self.PATCH = 1
            self.HAS_PATCH_IN_SECTION = True

    def check_new_prodname_type (self, NEW_TYPE, TYPE, OTH_PROD_NAME, PRODUCT_NAME, CLASS):
        addType = NEW_TYPE != TYPE
        addOthProdName = OTH_PROD_NAME != PRODUCT_NAME[:3].upper() and 'Sedatives' not in CLASS

        if addType or addOthProdName:
            self.printPage += '<!--' + '\n'
            if addOthProdName:
                self.printPage += 'OTH_PROD_NAME: ' + str(OTH_PROD_NAME) + '\n'
            if addType:
                TYPE = NEW_TYPE
                self.printPage += 'TYPE: ' + str(TYPE) + '\n'
            self.printPage += '-->' + '\n'

        return TYPE

    def get_prodname (self, eachRow):
        if ':' in eachRow:
            PRODUCT_NAME = eachRow.split(':')[0].strip()
        else:
            PRODUCT_NAME = eachRow.strip()
        return PRODUCT_NAME

    def run (self, edit):
        try:
            Selected = self.view.sel()
        
            for sel in Selected:
                inputs = self.view.substr(sel).strip()
                self.printPage = ''

                for eachRow in inputs.splitlines(): 
                    if 'Header:' in eachRow:
                        if self.CURRENT_SUB_SECTION != 0:
                            self.SubBrandsInEachLoop.append(self.CURRENT_SUB_SECTION - 1)

                        self.CURRENT_SECTION += 1
                        self.CURRENT_SUB_SECTION = 1

                        CLASS = eachRow.split(':')[1].strip()
                        API = eachRow.split(':')[2].strip()
                        PRODUCT_NAME = eachRow.split(':')[3].strip()
                        API_NAME = eachRow.split(':')[4].strip().split('_')[0].strip()
                        TYPE = eachRow.split(':')[4].strip().split('_')[2].strip()

                        self.print_class(CLASS, API, API_NAME, TYPE)

                        OTH_PROD_NAME = eachRow.split(':')[4].strip().split('_')[1].strip()

                        self.check_new_prodname_type(TYPE, TYPE, OTH_PROD_NAME, PRODUCT_NAME, CLASS)

                        self.check_LIQ_PATCH(eachRow, TYPE)
                        self.print_looprow(CLASS, API, PRODUCT_NAME)
                        self.CURRENT_SUB_SECTION += 1
                    else:
                        if 'other or unknown' in eachRow:
                            PRODUCT_NAME = self.get_prodname(eachRow)

                            if self.HAS_LIQUID_IN_SECTION:
                                self.LIQUID = 1
                            else:
                                self.LIQUID = 0

                            if self.HAS_PATCH_IN_SECTION:
                                self.PATCH = 1
                            else:
                                self.PATCH = 0

                            self.HAS_LIQUID_IN_SECTION = False
                            self.HAS_PATCH_IN_SECTION = False
                        else:
                            if 'other' in eachRow or 'unknown' in eachRow:
                                PRODUCT_NAME = self.get_prodname(eachRow)
                            else:
                                PRODUCT_NAME = eachRow.split(':')[0].strip()
                                NEW_TYPE = eachRow.split(':')[1].strip().split('_')[2].strip()
                                OTH_PROD_NAME = eachRow.split(':')[1].strip().split('_')[1].strip()

                                TYPE = self.check_new_prodname_type(NEW_TYPE, TYPE, OTH_PROD_NAME, PRODUCT_NAME, CLASS)

                            self.check_LIQ_PATCH(eachRow, TYPE)
                            
                        self.print_looprow(CLASS, API, PRODUCT_NAME)

                        self.CURRENT_SUB_SECTION += 1
                        
                self.view.replace(edit, sel, self.printPage)
        
            self.SubBrandsInEachLoop.append(self.CURRENT_SUB_SECTION - 1)
            print ("SubBrandsInEachLoop = " + str(self.SubBrandsInEachLoop))

        except Exception as e:
            print (e)

class RmpdcLoopNumbering(sublime_plugin.TextCommand):
    def run (self,edit):
        try:
            CURRENT_NUMBER = 0
            CURRENT_SUB_NUMBER = 0
            SubBrandsInEachLoop = []

            Selected = self.view.sel()
        
            for sel in Selected:
                inputs = self.view.substr(sel).strip()
                printPage = ''

                for eachLine in inputs.splitlines(): 

                    if 'CLASS:' in eachLine:
                        if CURRENT_NUMBER != 0:
                            SubBrandsInEachLoop.append(CURRENT_SUB_NUMBER)
                        CURRENT_NUMBER += 1
                        CURRENT_SUB_NUMBER = 0
                    if '<looprow label=' in eachLine:
                        CURRENT_SUB_NUMBER += 1
                        label = eachLine.split('"')[1].split("_")[0]
                        sub_label = eachLine.split('"')[1].split("_")[1]
                        if int(sub_label) != CURRENT_SUB_NUMBER:
                            sub_label = str(CURRENT_SUB_NUMBER)
                        if int(label) != CURRENT_NUMBER:
                            label = str(CURRENT_NUMBER)
                        printPage += '<looprow label="{0}_{1}">'.format(label, sub_label) + '\n'
                    else:
                        printPage += eachLine + '\n'

                self.view.replace(edit, sel, printPage)

            SubBrandsInEachLoop.append(CURRENT_SUB_NUMBER)
            print("SubBrandsInEachLoop = " + str(SubBrandsInEachLoop))

        except Exception as e:
            print (e)

class RmpdcGetAltlabelsB(sublime_plugin.TextCommand):
    IN_VARIABLES = False
    WITHOUT_ROWS = False
    IN_TIME_VARS = False
    Q_ROW_LINES = []
    TIME_ROW_LINES = []
    API_NAME = ''

    printPage = ''

    def clear_vars (self):
        self.Q_ROW_LINES = []
        self.TIME_ROW_LINES = []
        self.IN_VARIABLES = False
        self.WITHOUT_ROWS = False
        self.IN_TIME_VARS = False

    def get_question_label (self, line):
        question_label = ''

        if len(line) > 2:
            if line[0] in ['A','B','C','D']  and line[1].isdigit() and '. ' in line:
                question_label = line.split('. ')[0]
                question_label = question_label.replace('.','_')

        return question_label

    def get_labels (self, question_label):
        row_index = 1

        if len(self.Q_ROW_LINES) > 0 and question_label != '':
            if not self.WITHOUT_ROWS:
                self.printPage += question_label + '\n'

            for row_line in self.Q_ROW_LINES:
                if '\t' in row_line:
                    row_line = row_line.split('\t')[1]

                    self.printPage += question_label + 'r' + str(row_index) + '\t' + row_line + '\n'

                    if 'C5' in question_label and '_' in row_line:
                        self.API_NAME = row_line.split('_')[0]

                    row_index += 1
                elif ('A' in question_label or 'D' in question_label) and ' ' in row_line:
                    row_line = row_line.split(' ')[-1]
                    if '_' in row_line:
                        if self.WITHOUT_ROWS:
                            self.printPage += question_label + '\t' + row_line + '\n'
                        else:
                            self.printPage += question_label + 'r' + str(row_index) + '\t' + row_line + '\n'
                            row_index += 1

            if 'B6' in question_label:
                self.printPage += question_label + 'r' + str(row_index) + '\n'

    def get_time_labels (self):
        row_index = 1

        A_string = 'hTimeSpent_A1_A9'
        B_string = 'hTimeSpent_B1'

        if len(self.TIME_ROW_LINES) > 0:
            for row in self.TIME_ROW_LINES:
                if '\t' in row:
                    q_label = row.split('\t')[0].strip()
                    alt_label = row.split('\t')[1].strip()

                    q_string = ''
                    if 'A' in q_label:
                        q_string = A_string
                    elif 'B' in q_label:
                        q_string = B_string

                    if row_index == 1:
                        self.printPage += q_string + '\n'

                    self.printPage += q_string + 'r' + str(row_index) + '\t' + alt_label + '\n'
                    row_index += 1

    def run (self ,edit):
        try:
            self.printPage = ''
            Selected = self.view.sel()

            question_label = ''

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                for eachLine in inputs.splitlines():
                    eachLine = eachLine.strip()
                    ql = self.get_question_label(eachLine)

                    if ql != '':
                        if self.IN_TIME_VARS:
                            self.get_time_labels()

                        # Clear
                        self.clear_vars()

                        question_label = ql

                        if 'C6' in question_label:
                            self.printPage += question_label + '\t' + self.API_NAME + '_API_OTH_RSNYR_SPFY' + '\n'
                            self.printPage += 'noanswer' + question_label + '_n1' + '\t' + self.API_NAME + '_API_OTH_RSNYR_IDK' + '\n'

                        if 'A' in question_label or 'D' in question_label:
                            if 'Select one.' in eachLine:
                                q_altlabel = eachLine.split('Select one.')[1].strip()
                                self.printPage += question_label + '\t' + q_altlabel + '\n'
                            elif 'Drag the slider to answer the question' in eachLine:
                                self.IN_VARIABLES = True
                                self.WITHOUT_ROWS = True
                            elif '_' in eachLine and ' ' in eachLine:
                                q_altlabel = eachLine.split(' ')[-1].strip()
                                if '_' in q_altlabel:
                                    self.printPage += question_label + '\t' + q_altlabel + '\n'

                    if 'A' in question_label or 'B' in question_label or 'C' in question_label or 'D' in question_label:
                        if ('Variable Name' in eachLine or 'Unchecked' in eachLine) and 'Question\tVariable Name' not in eachLine:
                            self.IN_VARIABLES = True
                        elif (('<Programming>' in eachLine or '<Skip Logic>' in eachLine or '<Responsive Design>' in eachLine) and self.IN_VARIABLES):

                            self.get_labels(question_label)

                            # Clear
                            self.clear_vars()
                            question_label = ''

                        elif self.IN_VARIABLES:
                            if len(eachLine) > 1 and 'Variable Name' not in eachLine and '_' in eachLine:
                                self.Q_ROW_LINES.append(eachLine)
                        elif 'Enter a whole number' in eachLine and '_' in eachLine and 'A' in question_label:
                            self.Q_ROW_LINES.append(eachLine)
                            self.IN_VARIABLES = True
                            self.WITHOUT_ROWS = True

                    if 'Question\tVariable Name' in eachLine:
                        self.IN_TIME_VARS = True
                    elif self.IN_TIME_VARS:
                        self.TIME_ROW_LINES.append(eachLine)

                self.view.replace(edit, sel, self.printPage)


        except Exception as e:
            print (e)
