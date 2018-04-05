//Displays a custom input run alert in task form
$(function(){
    function displayCustomInputAlert(content)
    {
        displayTaskStudentAlertWithProblems(content,
            "<b>Custom run output:</b>",
            "success", true);
    }

    function runCustomInput (inputId) {
        var runInputCallBack = function (data) {
            if ('status' in data && data['status'] == 'done') {
                if ('result' in data) {
                    if(data['result'] == "failed"){
                        displayTaskStudentErrorAlert(data);
                        unblurTaskForm();
                    }
                    else if(data['result'] == "success") {
                        displayCustomInputAlert(data);
                        unblurTaskForm();
                    }
                }
            }
        }

        blurTaskForm();

        var taskForm = new FormData($('form#task')[0]);
        //taskForm.set("@action", "run_custom_input");

        $.ajax({
                url: taskUrl,
                method: "POST",
                dataType: 'json',
                data: taskForm,
                processData: false,
                contentType: false,
                success: runInputCallBack,
                error: function(er){}
        });
    }

    function uploadfile (inputId) {
        var inputFileId = "filelink-" + inputId;
        var inputFile = $("#"+inputFileId);

        var input = document.getElementById(inputFileId);
        input.addEventListener("change", function(event){
            var reader = new FileReader();
            reader.onload = function(event){
              var contents = event.target.result;
              document.getElementById(inputId).value = contents;
            };
            reader.readAsText(input.files[0]);
          }, false);

        inputFile.click();
    }
})