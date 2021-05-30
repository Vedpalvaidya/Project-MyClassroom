var editor = ace.edit('target')
editor.getSession().setMode("ace/mode/python");
editor.setOption("showPrintMargin", false)

var mode = document.querySelector("#mode");
if ( mode.textContent === 'Student'){
$(window).on("blur focus", function(e) {
    var prevType = $(this).data("prevType");

    if (prevType != e.type) {   //  reduce double fire issues
        switch (e.type) {
            case "blur":
                window.location = 'compiler';
                break;
        }
    }

    $(this).data("prevType", e.type);
})
}

const cSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/compilation/'
    +'cCompiler'
    +'/'
);

cSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
   document.querySelector('#output').value = data.code;
   $('#load').removeClass('loader');
   console.log('class removed');
};

cSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#code-submit').addEventListener('click', function(){
    const editor_data= editor.getValue();
    const input_data = document.querySelector('#Input').value;
    const code_language = document.querySelector('#navbarDropdown').textContent;
    
    const code  = editor_data;
    console.log(code)

    cSocket.send(JSON.stringify({
        'code' : code,
        'input' : input_data,
        'language':code_language
    }));

});



var flag = 0;

$(document).on('contextmenu',function(e){
    return false;
});

$(window).on('keydown', function(e){
    if (e.ctrlKey && e.keyCode == 86){
        if (flag == 0){
            alert("missed ")
            return false;
        }
        else
        {
            return true;
        }
    }

    if (e.ctrlKey && e.keyCode == 67){
        flag = 1;
    }
})

// $("#target").scroll(function(event) {
//     $(this).prev().height($(this).height());
//     $(this).prev()[0].scrollTop = this.scrollTop;
// });
// $("#target").keyup(function(event) {
//     var elm = $(this);
//     var lines = elm.val().split("\n");
//     var numbers = "";
//     for(var i=0; i<lines.length; i++)
//         numbers += (i+1) + "\n";
//     elm.prev().val(numbers);
//     elm.prev()[0].scrollTop = this.scrollTop;
// });

// $(document).delegate('#target', 'keydown', function(e) {
//     var keyCode = e.keyCode || e.which;
  
//     if (keyCode == 9) {
//       e.preventDefault();
//       var start = this.selectionStart;
//       var end = this.selectionEnd;
  
//       // set textarea value to: text before caret + tab + text after caret
//       $(this).val($(this).val().substring(0, start)
//                   + "\t"
//                   + $(this).val().substring(end));
  
//       // put caret at right position again
//       this.selectionStart =
//       this.selectionEnd = start + 1;
//     }
//   });

$('.theme').click(function(){
    var text_theme = $(this).text()
    if (text_theme == 'Light'){
        editor.setTheme(false);
    }
    else if (text_theme == 'Dark'){
        editor.setTheme("ace/theme/twilight")
    }
})

var code_text = {
    code1 : '#include<stdio.h>\n int main() { \nprintf("start your code from here"); \nreturn 0;\n}',
    code2 : '#include <iostream>\nusing iostream.h\nint main() {\n\t //write your code from here\nreturn 0;\n}',
    code3 : '#start your code from here\n',
    code4 : 'class main {\npublic static void main (String args[])\n{\n//write your code from here\n}\n}'
}




  $('.lan').click(function(){
    var text = $(this).text()
    $('#dropdownName').text(text)

    if(mode.textContent === 'Student'){
    if (text == 'c')
    {
        editor.getSession().setMode("ace/mode/c_cpp");
        editor.setValue(code_text["code1"]);
        editor.getSession().on('change', function() {
            var code_edit1 = editor.getSession().getValue();
            code_text["code1"] = code_edit1
          });
    }
    else if (text == 'c++'){  
        editor.getSession().setMode("ace/mode/c_cpp");
        editor.setValue(code_text["code2"])
        editor.getSession().on('change', function() {
            var code_edit2 = editor.getSession().getValue();
            code_text["code2"] = code_edit2;
          });
    }
    else if (text == 'python'){
        editor.getSession().setMode("ace/mode/python");
        editor.setValue(code_text["code3"])
        flag1 =  0
        if (flag1 == 0){
            editor.getSession().on('change', function() {
                var code_edit3 = editor.getSession().getValue();
                code_text["code3"] = code_edit3;
              });
              flag1 = 1
        }
        
    }
    else if (text == 'java'){
        editor.getSession().setMode("ace/mode/java");
        editor.setValue(code_text["code4"]);
        editor.getSession().on('change', function() {
            var code_edit4 = editor.getSession().getValue();
            code_text["code4"] = code_edit4
          });

   }
 }
});


  

  

$("#reset").click(function(){
    editor.setValue('');
});

$('.alert').click(function(){
    $('.alert').hide(1000);
})

$('#reset_input').click(function(){
    $('#Input').val('')
})
$('#code-submit').click(function(){
    $('#load').addClass('loader');
});

$('#alert_btn').click(function(){
    $('#alert_btn').hide();
    $('#alert').addClass('alert alert-dark').text('If you try to click outside of this page your code will get submitted')
    $('#remove_alert').addClass('btn btn-danger').text('Remove');
})

console.log(code)

$('#remove_alert').click(function(){
    $('#alert').removeClass().text('')
    $('#remove_alert').removeClass().text('')
    $('#alert_btn').show()
});
