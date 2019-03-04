jQuery(document).ready(function () {

    function addTaskFilesUploadMultipleButton(){
        let uploadFileButton = $('#edit_file_tabs_content').find('a').filter(':contains("Upload a file")');
        const uploadMultipleFilesButton = "&nbsp;<a href='#' class='btn btn-sm btn-info' data-toggle='modal' " +
            "data-target='#task_files_upload_multiple_modal'>Upload multiple files</a>";

        uploadFileButton.after(uploadMultipleFilesButton);
    }

    function uploadMultipleFilesOnChange(){
        $('#upload_multiple_files_input').change(function () {
            let inputFiles = $(this).prop('files');
            let listFilesDiv = $('#list_all_files');
            let listFiles = $.map(inputFiles, function(file) { return file.name; }).join();

            listFilesDiv.find('p[name=list_files]').text(listFiles);
            listFilesDiv.prop("hidden", false);
        });
    }

    function closeModal(){
        // Function to describe the process to follow when the modal is closed.
        $('#task_files_upload_multiple_modal').on('hidden.bs.modal', function () {
                $("#list_all_files").prop("hidden", true);
        });
    }

    function taskFilesUploadMultiple() {
        $("form#upload_multiple_files_form").submit(function (e) {
            e.preventDefault();
            let error = false;
            let resultData = "";
            let filesFailedUpload = [];
            let inputFiles = $("#upload_multiple_files_input").prop('files');

            $('#task_files_upload_multiple_modal').modal('hide');
            $("#submit_multiple_files").prop("disabled", true);
            $.each(inputFiles, function (_, file) {
                let form_data = new FormData();
                form_data.append('action', 'upload');
                form_data.append('path', file.name);
                form_data.append('file', file);
                $.ajax({
                    async:false,
                    url: location.pathname + '/files',
                    type: 'post',
                    data: form_data,
                    contentType: false,
                    cache: false,
                    processData: false,
                    success: function(data) {
                        if(data.search(/alert/i) > 0){
                            error = true;
                            filesFailedUpload.push(file.name);
                        }
                        resultData = data;
                    }
                });
            });
            $("#tab_file_list").replaceWith(resultData);
            addTaskFilesUploadMultipleButton();
            if(error){
                uploadErrorAlert(filesFailedUpload);
            }
        });
    }

    function uploadErrorAlert(filesFailedUpload){
        let tabFileList = $('#tab_file_list');
        let filesAlert = tabFileList.find("div").filter("[role=alert]");
        const message = "<p>There was an error while uploading the files: <strong>" + filesFailedUpload.join() +
            "</strong>. They may be already uploaded.</p>";

        if(filesAlert.length){
            filesAlert.text('');
            filesAlert.append(message)
        } else {
            const alertError = "<div class='alert alert-danger text-center' role='alert'>" + message + "</div>";
            tabFileList.prepend(alertError);
        }
    }

    addTaskFilesUploadMultipleButton();
    uploadMultipleFilesOnChange();
    taskFilesUploadMultiple();
    closeModal();

});