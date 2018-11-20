jQuery(document).ready(function() {

    function updateNavbarLogo(imagePath){
        let logoElement = $('#wrapper')
            .find('> div.navbar.navbar-default.navbar-static-top > div > div.navbar-header > a');
        const image = logoElement.find("> img").attr("src", imagePath);
        logoElement.text("");
        logoElement.html(image).append(" Code");
    }

    function updateFooter(){
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

    function updatePageIcon(imagePath){
        $('link[rel="icon"]').attr('href', imagePath);
    }

    function updateTitle(){
         let title = document.title.split("|");
         document.title = title[0] + " |  UNCode";
    }

    function updateTemplate(){
        // This updates all necessary changes in INGInious.
        const imagePath = window.location.origin + "/UN_template/static/images/LogotipoUNAL.png";
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

    updateTemplate();
    addTaskContextTemplate();
});
