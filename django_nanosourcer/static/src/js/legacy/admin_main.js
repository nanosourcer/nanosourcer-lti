var adminConfig = {};

(function () {

    // For on page load initialization. Custom configuration settings selected by admin/teacher.
    window.init_page_session = function (initAdminConfig) {

        adminConfig = initAdminConfig;

    };

})();

$(document).ready(function () {
    
    lti_session_key = sessionStorage.getItem('lti_session_key');
    
    $("#load_new_image_confirm").on('click', function (e) {
        $("#myModal").modal();
        e.preventDefault();
    });

    $("#modal-new-image-no").on('click', function (e) {
        e.preventDefault();
    });

    $("#modal-new-image-yes").on('click', function (e) {
        userData['process_status_id'] = 1;
        transmit_user_selections(userData);
    });

    $(".hamburger-bars-container").on("click", function() {

        if ($("#hamburger-menu").css('display') == 'none') {

            $("#hamburger-menu").css('display', 'initial');

        } else {

            $("#hamburger-menu").css('display', 'none');

        }

    });


});


