/**
 * Created by msl656 on 6/30/16.
 */
var courseConfig = {};
var userData = {};
var gazData = {};
var gazConfig;
var is_err_notified;

(function () {

    // For on page load initialization. Custom configuration settings selected by admin/teacher.
    window.init_page_session = function (initCourseConfig) {

        courseConfig = initCourseConfig;
        gazConfig = courseConfig['gaz_config'];

    };

})();

$(document).ready(function() {

    var map = new mapboxgl.Map({

        container: 'mapbox-container'

    })

});