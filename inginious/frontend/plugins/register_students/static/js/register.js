jQuery(document).ready(function () {

    let register_succeeded = false;

    function displayRegisterStudentsAlertError(data) {
        let alert_element = $("#register_students_alert");
        alert_element.prop("class", "alert alert-danger");
        alert_element.text(data);
        alert_element.prop("hidden", false);
    }

    function runRegisterStudents(data) {
        // Function executed when the Ajax request success.
        if ("status" in data && data["status"] === "error") {
            displayRegisterStudentsAlertError(data["text"]);
        } else if ("status" in data && data["status"] === "success") {
            let alert_element = $("#register_students_alert");
            register_succeeded = true;
            $("#students_file").val('');
            alert_element.prop("class", "alert alert-success");
            alert_element.text(data["text"]);
            alert_element.prop("hidden", false);
            setTimeout(function () {
                alert_element.prop("hidden", true);
            }, 10000)
        } else {
            displayRegisterStudentsAlertError("An error occurred while registering. Please try again.");
        }
    }

    function getCourseId(){
        return window.location.href.split("/")[4]; // Get the course id using the current URL.
    }

    function submitRegisterStudents() {
        $("form#upload_students_file").submit(function (e) {
            e.preventDefault();
            let file = $("#students_file").prop('files')[0];
            const file_extensions = /(\.csv)$/i;
            console.log(file);
            if (file === undefined) {
                displayRegisterStudentsAlertError("Please select a file before submitting it.");
            } else if (!file_extensions.exec(file.name)) {
                displayRegisterStudentsAlertError("The inserted file should be a .csv file.");
            } else {
                let formData = new FormData();
                formData.append("file", file);
                formData.append("course", getCourseId());
                $.ajax({
                    url: '/api/addStudents/',
                    method: "POST",
                    dataType: 'json',
                    data: formData,
                    mimeType: "multipart/form-data",
                    async: false,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        runRegisterStudents(data);
                    },
                    error: function (data) {
                        displayRegisterStudentsAlertError(data);
                    }
                });
            }
        });
    }

    function appendRegisterStudentsButton() {
        // Function intended for appending the button to open the modal in the 'students' page.
        const html = "<br><button class='btn btn-success' data-toggle='modal' data-target='#register_students_modal'>" +
            "<i class='fa fa-users'></i> Register students</button>";
        let tab_students = $('#tab_students');
        tab_students.append(html);
    }

    function closeModal(){
        // Function to describe the process to follow when the modal is closed.
        $('#register_students_modal').on('hidden.bs.modal', function () {
            if(register_succeeded){
                window.location.replace(window.location.href);
            } else {
                $("#students_file").val('');
                $("#register_students_alert").prop("hidden", true);
            }
        });
    }

    closeModal();
    appendRegisterStudentsButton();
    submitRegisterStudents();
});
