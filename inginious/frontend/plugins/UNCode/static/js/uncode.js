jQuery(document).ready(function () {

    function updateNavbarLogo(imagePath) {
        let logoElement = $('#wrapper')
            .find('> div.navbar.navbar-default.navbar-static-top > div > div.navbar-header > a');
        const image = logoElement.find("> img").attr("src", imagePath);
        logoElement.text("");
        logoElement.html(image).append(" Code");
    }

    function updateFooter() {
        // Update footer with new information.
        let footer = $('#footer');
        footer.find('> div > div > div > p')
            .html(' &copy; 2017-' + (new Date()).getFullYear() + ' Universidad Nacional de Colombia.');
        footer.find('> div > div > div > div > p')
            .html('<a target="_blank" href="https://github.com/JuezUN/INGInious" class="navbar-link">\n' +
                'UNCode is distributed under AGPL license' +
                '</a>' + ' - <a target="_blank" href="http://www.inginious.org" class="navbar-link">\n' +
                'Powered by INGInious.\n</a>');
    }

    function updatePageIcon(imagePath) {
        $('link[rel="icon"]').attr('href', imagePath);
    }

    function updateTitle() {
        let title = document.title.split("|");
        document.title = title[0] + " |  UNCode";
    }

    function updateTemplate() {
        // This updates all necessary changes in INGInious.
        const imagePath = window.location.origin + "/UNCode/static/images/LogotipoUNAL.png";
        updateNavbarLogo(imagePath);
        updatePageIcon(imagePath);
        updateFooter();
        updateTitle();
    }

    function addTaskContextTemplate() {
        let codeMirror = $('.CodeMirror');
        const defaultTaskContext = $("#default_task_context").text();

        if ($("#context").length !== 0 && codeMirror.length !== 0) {
            let editor = codeMirror[0].CodeMirror;
            if (editor.getDoc().getValue() === "") {
                editor.getDoc().setValue(defaultTaskContext);
            }
        }
    }

    function addTaskContextHelp() {
        let taskContext = $("#context");
        const tipsButton = "<a href='#' type='button' data-toggle='modal' data-target='#task_context_help_modal'>" +
            "<i class='fa fa-question-circle'>  Help.</a>";

        if (taskContext.length !== 0) {
            taskContext.before(tipsButton);
        }
    }

    function addTaskResultLegendButton() {
        let taskAlert = $("#task_alert");
        const legendModalButton = "<a href='#' type='button' data-toggle='modal' data-target='#task_result_legend_modal'>" +
            "<i class='fa fa-question-circle'>  Understand your task result.</a>";
        taskAlert.before(legendModalButton);
    }

    function updateCourseDocumentationLinks() {
        // This section is to update link of "How to create task?" button in course administration.
        // Now redirecting to our documentation.
        let howToCreateTaskElement = $('a[href="http://inginious.readthedocs.org/en/latest/teacher_doc/task_tuto.html"]');
        howToCreateTaskElement.attr("href", "https://github.com/JuezUN/INGInious/wiki/How-to-create-a-task");
        howToCreateTaskElement.attr("target", "_blank");

        // This section is to update link of "Documentation" button in course administration-
        // Now redirecting to our documentation.
        let documentationElement = $('a[href="http://inginious.readthedocs.org/en/latest/teacher_documentation.html"]');
        documentationElement.attr("href", "https://github.com/JuezUN/INGInious/wiki/Course-administration");
        documentationElement.attr("target", "_blank");
    }

    function stopSideBar(){
        $("#sidebar_affix").css('position', 'static');
    }

    updateTemplate();
    addTaskContextTemplate();
    addTaskContextHelp();
    updateCourseDocumentationLinks();
    addTaskResultLegendButton();
    stopSideBar();
});
