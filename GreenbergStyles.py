import sublime
import sublime_plugin

class OpenEndJavaScripts(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
<style name="respview.client.js" mode="after">
<![CDATA[
  <script>
  /* common.js overwrite */
  function populateBuddy(evt) {
      evt = (evt) ? evt : ((event) ? event : null);
      if (evt) {
          var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
          if (elem) {
              if (evt.type === "keypress") {
                  elem.popBuddy.checked = 1;
                  elem.defaultValue = "";
              } else if (evt.type === "blur" && !elem.value.length) {
                  //elem.popBuddy.checked = 0;
              }
              if (window.jQuery) {
                  var $q = $ (elem.popBuddy).closest(".surveyQuestion");
                  $ ('[name="' + elem.popBuddy.name + '"]', $q.length ? $q : document).trigger("change");
              }
          }
      }
  }
  </script>
]]>
</style>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class AutopunchSlider(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
  <style name="question.footer" label="sliderpoints_ac" mode="after" wrap="ready">
  <![CDATA[
var selectionListener = setInterval(function(){
    if($ ('.sliderpoints-legenditem.sliderpoints-selected').length > ($ ('.sq-sliderpoints-container').length) - 1){
        $ ('#btn_continue,#btn_finish').trigger('click');
        clearInterval(selectionListener);
    }

}, 50)
  ]]>
  </style>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class FreezeTitle(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
<style name="question.footer" label="FreezeTitle" mode="after"><![CDATA[
<script>
$ (document).ready( function() {
    "use strict";
    // Change here if you want to freeze something else
    var origTitle = $ ('.question-text');
    var title = origTitle.clone();
    $ ('body').append(title);
    title.css({
      'position': 'fixed',
      'background-color': 'white',
      'top': '0px',
      'padding': '10px 0px',
      'box-shadow': '0px 0px 5px 5px white'
    });

    (function refresh(){
      var titleOffset = parseInt(origTitle.offset().top) - parseInt($ (document).scrollTop())
      title.css({
        'left': parseInt(origTitle.offset().left) - parseInt($ (document).scrollLeft()),
        'width': origTitle.outerWidth()
      });
      if (titleOffset < 0){
        title.show();
      }
      if (titleOffset > 0){
        title.hide();
      }
      setTimeout(refresh, 50);
    })();
});
</script>
<style>
.freeze-title{
    position: fixed;
    top: 0;
    left: 50%;
    max-width: 50%;
    margin-left: -488px;
    background-color: white;
    z-index: 9999;
    padding: 10px;
    border: 1px solid #EFEFEF;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
    box-shadow: 0px 0px 5px 1px #EFEFEF;
    text-align: center;
}
</style>
]]></style>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class FlyInText(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
<!-- The element that we want to fly-in needs to be wrapped around this div tag - <div class="fly-in-container">TEXT</div> -->

<style label="FlyIn" name="question.footer" mode="after">
  <![CDATA[
    <script>
      "use strict";

      $ (document).ready(function(){

        var container = $ ('.fly-in-container');
        var wrapper = $ ('<div>').addClass('fly-in-wrapper');
        var idleTime = 300; // Time before the animation is initiated
        var animationTime = 500; // Animation duration
        var endAnimationTriggered = false;

        container.wrap(wrapper);

        setTimeout(function(){
          container.css({
            visibility: 'visible'
          });
          container.animate({
            right: '0'
          }, animationTime);
        }, idleTime);

        $ ('form').submit(function(){
          if (!endAnimationTriggered) {
            container.animate({
              left: '-100%'
            }, animationTime);
            endAnimationTriggered = true;
            setTimeout(function(){
              $ ('form').submit()
            }, animationTime);
            return false;
          }
        })
      });
    </script>
    <style>
      .fly-in-wrapper {
        position: relative;
        margin: 0;
        padding: 0;
        width: 100%;
        height: auto;
        overflow: hidden;
      }
      .fly-in-container {
        right: -100%; /* Make sure this is present */
        visibility: hidden; /* Make sure this is present */
        position: relative;
        margin: 10px auto;
        padding: 10px;
        width: 80%;
        border: 2px solid black;
        border-radius: 5px;
        box-shadow: 0px 0px 5px 1px gray;
        text-align: center;
      }
    </style>
  ]]>
</style>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

#TODO: Move hover_res and tooltip_style before the selected area
class HoverText(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            tooltip_style = '''
<style name="respview.client.js" mode="after" wrap="ready">
  <![CDATA[
    $ ('.tooltip').tooltip({
      'content': function(){
        return $ (this).attr('title');
      }
    });
  ]]>
</style>
'''
            hover_res = '<res label="Hover"></res>'

            Selected = self.view.sel()

            allcontent = self.view.substr(sublime.Region(0, self.view.size()))
            hasStyle = True if len([line for line in allcontent.splitlines() if "$ ('.tooltip').tooltip({" in line]) > 0 else False

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = ''

                if not hasStyle:
                    printPage = printPage + tooltip_style + '\n\n'

                printPage = printPage + hover_res + '\n\n'

                printPage = printPage + '<span class="tooltip" title="${res.Hover}">' + inputs + '</span>'
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class RadioAutocontinue(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
<style label="AutoContinue" name="question.footer" wrap="ready" mode="after" arg:hideButton="0">
  <![CDATA[
    "use strict";

    var button = $ ('#btn_continue, #btn_finish');
    var inputs = $ ("#question_${this.label} input[type=radio]");
    var radioGroups = [];

    \@if hideButton == '1'
      button.hide();
    \@endif

    inputs.each(function(i, e){
      if ($.inArray($ (e).attr('name'), radioGroups) === -1){
        radioGroups.push($ (e).attr('name'))
      }
    });

    inputs.bind('change', function(){
      if (inputs.filter(":checked").length === radioGroups.length){
        button.show().click();
      }
    });
  ]]>
</style>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class UniversalAutoContinue(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
<style label="UniversalAutoContinue" name="question.footer" wrap="ready" mode="after" arg:hideButton="0">
  <![CDATA[
    "use strict";

    var button = $ ('#btn_continue, #btn_finish');
    var inputs = $ ("#question_${this.label} input[type=radio]");
    var radioGroups = [];

    \@if hideButton == '1'
      button.hide();
    \@endif

    inputs.each(function(i, e){
      if ($.inArray($ (e).attr('name'), radioGroups) === -1){
        radioGroups.push($ (e).attr('name'))
      }
    });

    (function checker(){
      if (inputs.filter(":checked").length === radioGroups.length){
        button.show().click();
      }
      else {
        setTimeout(checker, 50);
      }
    })();

  ]]>
</style>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class RemoveHelpLinks(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
<style name="respview.client.css" mode="after"><![CDATA[
<style type="text/css">
.support-links {
  display: none;
}
</style>
]]></style>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class GeneralStyles(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
<style name="respview.client.css" mode="after">
<![CDATA[
<style>
.comment-text {
    font-family: 'Lato Light', arial, serif;
    color: black;
    font-size: 20px !important;
    line-height: 22px !important;
    font-weight: bold !important;

}
.instruction-text {
    font-family: 'Lato Light', arial, serif !important;
}
.question-text {
    font-family: 'Lato Light', arial, serif;
    color: black;
    font-size: 20px !important;
    line-height: 22px !important;
    font-weight: bold !important;
}
b {
  font-family: 'Lato Regular', arial, serif !important;
}
</style>
]]>
</style>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class CardsortStyleAttributes(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
  cardsort:bucketCSS="height: 100px; width: 160px; padding: 0; border-radius: 10px; background-color: #9dc533; border: 0 none; color: white; font-size: 18px; font-weight: bold; font-family: 'Lato Light';"
  cardsort:cardCSS="width: auto;"
  cardsort:completionCSS="color: rgb( 66, 106, 146 ); font-size: 12px;"
  cardsort:displayCounter="0"
  cardsort:displayNavigation="0"
  cardsort:displayProgress="0"
  cardsort:bucketsPerRow="3"
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class Atm1dStyle(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
<style name="respview.client.css" mode="after">
  <![CDATA[
    <style type="text/css">
/*Make the table as wide as possible based on the theme.css*/
.sq-atm1d-btns{
    width: 100% !important;
}           
/*Adjust the boxes size so that they can fit into the container in three columns*/
.sq-atm1d-btn{
    width: 350px !important;
}
.sq-atm1d-legend .text {
    text-align: center;
}
/* Hide the atm1d flag icon */
.sq-atm1d-flag-icon {
    display: none;
}
/* All atm1d questions */
.sq-atm1d .sq-atm1d-button {
    background-color: transparent;
}
.sq-atm1d .sq-atm1d-hovered {
    background-color: transparent !important;
    border: 2px solid #8CB64F !important;
}
.sq-atm1d .sq-atm1d-legend {
    font-size: 15px;
        color: black;
}
.sq-atm1d-vertical .sq-atm1d-td,.sq-atm1d-vertical .oe {
    text-align: center;
    vertical-align: middle !important;
}
.sq-atm1d-vertical .sq-atm1d-td, .sq-atm1d-vertical .oe {
    text-align: center;
    vertical-align: middle !important;
    padding: 1px !important;
}
.sq-atm1d-content .sq-atm1d-td {
    background-color: #fff;
}
.sq-atm1d .sq-atm1d-table,.sq-atm1d .sq-atm1d-table .sq-atm1d-content {
    height: 100%;
    max-height: none;
    min-height: 47px;
    padding: 0px;
    width: 100%;
    color: black;
}
.table.sq-atm1d-table .img-style img {
    width: 100%;
}
.sq-atm1d .sq-atm1d-selected {
    background-color:  transparent !important;
    border: 4px solid #8CB64F !important;
}
.sq-atm1d .sq-atm1d-button {
    border-radius: 21px;
    margin: 4px !important; 
    min-width: 210px;
    border: 2px solid #BFBEBE;
}
   </style>
  ]]></style>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class SliderStyle(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
<style mode="after" name="respview.client.js" wrap="ready"><![CDATA[
$ (".question-text").attr("title", "");
$ (".instruction-text").attr("title", "");
]]></style>
<style label="slider_text" mode="after" name="respview.client.css"><![CDATA[
<style type="text/css">
.sq-sliderpoints .sliderpoints-legenditem, .sq-sliderpoints .fa-icon-circle {
    font-size: 20px;
}
    </style>
]]></style>
<style label="separateSlider" mode="after" name="respview.client.css"><![CDATA[
<br />
<hr />
<br />
]]></style>
<style label="sliderLegendCSS" mode="after" name="respview.client.css"><![CDATA[
<style>
.sq-sliderpoints-row-legend {
    font-family: 'Lato Light', arial, serif;
    font-weight: bold;
    font-size: 22px !important;
    text-align: center;
}
    </style>
]]></style>

'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class RanksortStyleMobile(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
<style name="question.footer" mode="after" cond="device.mobileDevice">
  <![CDATA[
    <style>
#survey .sq-ranksort-container .sq-ranksort-cards .sq-ranksort-card  {
    height: 100px; 
}
    </style>
  ]]>
</style>
<style name="question.footer" mode="after" cond="not device.mobileDevice">
  <![CDATA[
    <style>
.sq-ranksort-container .sq-ranksort-buckets .sq-ranksort-bucket {
   height: 230px !important;
} 
    </style>
  ]]>
</style>
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)

class RanksortAttributes(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            Selected = self.view.sel()

            for sel in Selected:
                inputs = self.view.substr(sel).strip()

                printPage = '''
  ranksort:uiDraggableHelperCSS="background-color: #8cbb40; color: white; border: 1px solid #8cbb40; border-radius: 5px; height: 250px; width: 500px;"
  ranksort:uiSortablePlaceholderCSS="background-color: #8cbb40; color: white; border: 1px solid #8cbb40; border-radius: 5px;"
  ranksort:uiSortableHelperCSS="background-color: #8cbb40; color: white; border: 1px solid #8cbb40; border-radius: 5px;"
  ranksort:uiDroppableActiveCSS="background-color: #8cbb40; color: white; border: 1px solid #8cbb40; border-radius: 5px;"
  ranksort:uiDroppableHoverCSS="background-color: #8cbb40; color: white; border: 1px solid #8cbb40; border-radius: 5px;"
  ranksort:cardDroppedCSS="background-color: #8cbb40 !important; color: white; border: 1px solid #8cbb40; border-radius: 5px;"
  ranksort:iconAddCSS="color: #8cbb40; display: none;"
  ranksort:iconRemoveCSS="color: #8cbb40; display: none;"
  ranksort:iconRankCSS="color: #8cbb40; display: none;"
  ranksort:bucketCSS="height: 180px;"
  ranksort:bucketsContainerCSS="width: 170px;"
  ranksort:cardCSS="height: 230px;"
  ranksort:cardHoverCSS="background-color: #8cbb40;"
'''
                self.view.replace(edit,sel, printPage)
        except Exception as e:
            print (e)








