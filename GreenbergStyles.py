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




