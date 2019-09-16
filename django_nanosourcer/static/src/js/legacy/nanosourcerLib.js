function CardManager(parentObj, cardList) {

    var cardMenuContainer = jQuery("<div></div>");
    cardMenuContainer.attr("class", "card-menu");
    cardMenuContainer.attr("id", "card-menu");

    for (var i = 0; i < cardList.length; i ++) {

        var cardContainer = jQuery("<div></div>");
        cardContainer.attr("class", "card-menu-item-container");

        var cardInnerContainer = jQuery("<div></div>");
        cardInnerContainer.attr("class", "card-menu-item-inner-container");

        cardList[i].build();

        cardInnerContainer.append(cardList[i].get());
        cardContainer.append(cardInnerContainer);
        cardMenuContainer.append(cardContainer);

    }

    parentObj.append(cardMenuContainer);

    var parentHeightBefore = parentObj.height();

    // this._flickityObj = new Flickity(".card-menu", {
    //
    //     accessibility: true,
    //     adaptiveHeight: true,
    //     autoPlay: false,
    //     cellAlign: "left",
    //     cellSelector: ".card-menu-item-container",
    //     contain: true,
    //     draggable: true,
    //     dragThreshold: 10,
    //     freeScroll: false,
    //     friction: 0.2,
    //     selectedAttraction: 0.05,
    //     groupCells: false,
    //     initialIndex: 0,
    //     lazyLoad: false,
    //     percentagePosition: true,
    //     prevNextButtons: false,
    //     pageDots: false,
    //     resize: true,
    //     rightToLeft: false,
    //     setGallerySize: true,
    //     watchCSS: false,
    //     wrapAround: false
    //
    // });

    parentObj.height(parentHeightBefore);

}



function Handlers() {

}

Handlers.prototype = {

    hamburgerOnClick: function() {

        jQuery('.hamburger-bar-container').on('click', function() {

            var menu = jQuery('#hamburger-menu');

            if (menu.css('display') == 'none') {

                menu.css('display', 'initial');

            } else {

                menu.css('display', 'none');

            }

        });

    },
    customPanelOnClick: function(mapObj) {

        jQuery(".custom-panel-header, .custom-panel-header-pressed").on("click", function() {

            var headerState = jQuery(this).attr("class");

            if (headerState == "custom-panel-header-pressed") {

                jQuery(this).attr("class", "custom-panel-header");

            } else {

                jQuery(this).attr("class", "custom-panel-header-pressed");

            }

            var id = jQuery(this).attr('id');
            id = id.replace('header', 'body');

            var state = jQuery("#" + id).attr("class");

            if (state == "custom-panel-body") {

                jQuery("#" + id).attr("class", "custom-panel-body-open");
                mapObj.invalidateSize();

            } else {

                jQuery("#" + id).attr("class", "custom-panel-body");

            }

        });

    },
    minimumYearFieldOnKeypress: function(field_id, userData) {

        jQuery("#" + field_id).on('keypress', function (ev) {

            if (ev.which == 13) {

                userData.yearMin(ev.currentTarget.value);

            }

        });
    },
    minimumYearFieldOnBlur: function(field_id, userData) {

        jQuery("#" + field_id).on('blur', function (ev) {

            userData.yearMin(ev.currentTarget.value);

        });

    },
    maximumYearFieldOnKeypress: function(field_id, userData) {

        jQuery("#" + field_id).on('keypress', function (ev) {

            if (ev.which == 13) {

                userData.yearMax(ev.currentTarget.value);

            }

        });

    },
    maximumYearFieldOnBlur: function(field_id, userData) {

        jQuery("#" + field_id).on('blur', function (ev) {

            userData.yearMax(ev.currentTarget.value);

        });

    },
    refreshResultsBtnOnClick: function(userData) {

        jQuery('.btnRefreshResults').on('click', function () {

            console.log(userData);

        });
    },
    metadataSearchWidgetOnClick: function(gazetteerSearchKey, userData, GLS, spinnerOptions) {

        jQuery("#" + gazetteerSearchKey + "_search_widget").on('click', function () {

            var q = jQuery("#" + gazetteerSearchKey + "_filter_input").val();
            var result = userData.searchResults();
            result[gazetteerSearchKey] = {'keyword_str': q};
            userData.searchResults(result);

            console.log(userData.searchResults());

            var requestHelper = new GLSRequestPreparer(gazetteerSearchKey, userData);

            if (requestHelper.sufficientQuereyParams()) {

                var container = jQuery('#metadata-results-container-' + gazetteerSearchKey);
                container.empty();

                var spinner = new Spinner(spinnerOptions).spin();
                container.append(spinner.el);

                GLS.gazetteersGazetteerIdSearchGet(

                    requestHelper.params(),
                    requestHelper.body(),
                    requestHelper.additionalParams()

                ).then(function(result) {

                    console.log("SUCCESS");
                    console.log(result);

                    spinner.stop();

                    var metadataResults = new MetadataResults(container, result);

                }).catch(function(result) {


                    console.log("ERROR");
                    console.log(result);

                    spinner.stop();

                });

            } else {

                console.log("INSUFFICIENT QUEREY PARAMS")

            }

        });

    },
    metadataFilterInputOnClick: function(gazetteerSearchKey, userData, GLS, spinnerOptions) {

        jQuery("#" + gazetteerSearchKey + '_filter_input').on('keypress', function (ev) {

            if (ev.which == 13) {

                var result = userData.searchResults();
                result[gazetteerSearchKey] = {'keyword_str': ev.currentTarget.value};
                userData.searchResults(result);

                var requestHelper = new GLSRequestPreparer(gazetteerSearchKey, userData);

                if (requestHelper.sufficientQuereyParams()) {

                    var container = jQuery('#metadata-results-container-' + gazetteerSearchKey);
                    container.empty();

                    var spinner = new Spinner(spinnerOptions).spin();
                    container.append(spinner.el);

                    GLS.gazetteersGazetteerIdSearchGet(

                        requestHelper.params(),
                        requestHelper.body(),
                        requestHelper.additionalParams()

                    ).then(function(result) {

                        console.log("SUCCESS");
                        console.log(result);

                        spinner.stop();

                        var metadataResults = new MetadataResults(gazetteerSearchKey, container, result);

                    }).catch(function(result) {

                        console.log("ERROR");
                        console.log(result);

                        spinner.stop();

                    });

                } else {

                    console.log("INSUFFICIENT QUEREY PARAMS")

                }

            }

        });

    }
    // metadataResultBoxOnClick: function(gazetteerSearchKey) {
    //
    //     jQuery.("#" + gazetteerSearchKey + "_dynamic").click(function (e) {
    //
    //         jQuery.("#" + gazetteerSearchKey + "_results_box").toggle(600, "swing");
    //         e.preventDefault();
    //
    //     });
    //
    // },
    // modalNewImageYesOnClick: function(userData) {
    //
    //     jQuery.("#modal-new-image-yes").on('click', function () {
    //
    //         userData['process_status_id'] = 1;
    //         //transmit_user_selections(userData);
    //
    //     });
    //
    // },
    // modalNewImageNoOnClick: function() {
    //
    //     jQuery.("#modal-new-image-no").on('click', function (e) {
    //
    //         e.preventDefault();
    //
    //     });
    //
    // },
    // loadNewImageConfirmationOnClick: function() {
    //
    //     $("#load_new_image_confirm").on('click', function (e) {
    //
    //         $("#myModalWarning").modal();
    //         e.preventDefault();
    //
    //     });
    //
    // },
    // submitSelectionsBtnOnClick: function(userData) {
    //     $('#btn_submit_selections').on('click', function () {
    //
    //         userData['process_status_id'] = 0;
    //         transmit_user_selections(userData);
    //
    //     });
    // },
    // toggleMetadataLinkOnClick: function() {
    //     $('#toggle_metadata_link').on('click', function (e) {
    //
    //         $('#metadata-toggle-view').toggle(600, "swing");
    //         e.preventDefault();
    //
    //     });
    // },
    // toggleInstructionsLinkOnClick: function() {
    //     $('#toggle_instructions_link').on('click', function (e) {
    //
    //         $('#instructions_panel').toggle(600, "swing");
    //         e.preventDefault();
    //
    //     });
    // },

};

function Latitude(value) {

    this._value = value;
    this._validate();

}

Latitude.prototype = {

    valueOf: function() {

        return this._value;

    },
    toString: function() {

        return this._value.toString();

    },
    _validate: function() {

        if ((this._value !== undefined) && (this._value !== null)) {

            if ((this._value > 90.0) || (this._value < -90.0)) {

                throw "Input value out of range"

            }

                this._value = parseFloat(this._value);

        } else {

            throw "Invalid parameter"

        }

    },
    value: function(value) {

        if (arguments.length === 0) {

            return this._value;

        } else {

            this._value = value;
            this._validate()

        }

    }

};

function Longitude(value) {

    this._value = value;
    this._validate();

}

Longitude.prototype = {

    valueOf: function() {

        return this._value;

    },
    toString: function() {

        return this._value.toString();

    },
    _validate: function() {

        if ((this._value !== undefined) && (this._value !== null)) {

            if ((this._value > 180.0) || (this._value < -180.0)) {

                throw "Input value out of range"

            }

                this._value = parseFloat(this._value);

        } else {

            throw "Invalid parameter"

        }

    },
    value: function(value) {

        if (arguments.length === 0) {

            return this._value;

        } else {

            this._value = value;
            this._validate()

        }

    }

};

function MetadataResults(gazetteerSearchKey, container, metadata) {

    container.empty();

    var results = metadata['data']['response']['items'];

    var even = false;

    var containerForm = jQuery('<form></form>');

    for (var i = 0; i < results.length; i++) {

        var row = new MetadataResultsRow(gazetteerSearchKey, containerForm, results[i], even);

        if (even) {
            even = false;
        } else {
            even = true;
        }

    }

    container.append(containerForm);

}

MetadataResults.prototype = {

};

function MetadataResultsRow(gazetteerSearchKey, container, rowData, even) {

    this._url = rowData['gazetteerURI'];
    this._label = rowData['label'];
    this._secondaryLabel = rowData['secondaryLabel'];
    this._spatialLabel = rowData['spatialLabel'];
    this._dateMax = rowData['dateMax'];
    this._dateMin = rowData['dateMin'];
    this._latitude = rowData['lat'];
    this._longitude = rowData['long'];


    this._row = jQuery('<div></div>');
    this._row.attr('class', 'metadata-results-row');

    this._radioContainer = jQuery('<div></div>');
    this._radioContainer.attr('class', 'col-lg-1 col-md-1 col-sm-1 col-xs-1');
    this._radioFlex = jQuery('<div></div>');
    this._radioFlex.attr('class', 'metadata-row-section-container');

    this._radioButton = jQuery('<input type="radio">');
    this._radioButton.attr('class', 'metadata-row-radio-btn');

    var theRowLabel = this._label;

    this._radioButton.on('click', function() {

        jQuery.each(container.children(), function() {

           jQuery(this).children().find('.metadata-row-radio-btn').prop("checked", false);

        });

        jQuery(this).prop("checked", true);
        var message = jQuery(jQuery(jQuery(container.parent()).parent()).children()[0]);
        var span = jQuery(message).children()[0];
        message.empty();

        message.append(span);
        message.text(" " + theRowLabel);

        var panelMessageID = "#panel-header-uri-selection-" + gazetteerSearchKey.substr(0,1).toUpperCase() + gazetteerSearchKey.substr(1, gazetteerSearchKey.length);

        var panelHeaderMessage = jQuery(panelMessageID);
        panelHeaderMessage.append(span);
        panelHeaderMessage.text(" " + theRowLabel);
        panelHeaderMessage.attr("style", "display: block");


    });

    this._radioFlex.append(this._radioButton);

    this._radioContainer.append(this._radioFlex);

    this._bodyContainer = jQuery('<div></div>');
    this._bodyContainer.attr('class', 'col-lg-12 col-md-6 col-sm-11 col-xs-11');
    this._bodyFlex = jQuery('<div></div>');

    this._bodyFlex.attr('class', 'metadata-row-section-container');

    this._labelField = jQuery('<p></p>');
    this._labelField.attr('class', 'metadata-row-section-container-title');
    this._labelField.text(this._label);

    this._labelField.append(this._labelFieldBold);

    this._descriptionField = jQuery('<p></p>');
    this._descriptionField.text(this._secondaryLabel);

    this._bodyFlex.append(this._labelField);
    this._bodyFlex.append(this._descriptionField);

    this._bodyContainer.append(this._bodyFlex);

    this._locationContainer = jQuery('<div></div>');
    this._locationContainer.attr('class', 'col-lg-12 col-md-5 col-sm-12 col-xs-12');
    this._locationFlex = jQuery('<div></div>');

    this._locationFlex.attr('class', 'metadata-row-section-container');

    if (this._doesAttributeExist(this._spatialLabel)) {

        this._globeIcon = jQuery('<span></span>');
        this._globeIcon.attr('class', 'glyphicon glyphicon-globe center-glypicon');

        this._locationTextSpace = jQuery('<span>&nbsp;</span>');

        this._locationText = jQuery('<span></span>');
        this._locationText.text(this._spatialLabel);

        this._locationTextContainer = jQuery('<p></p>');
        this._locationTextContainer.append(this._globeIcon);
        this._locationTextContainer.append(this._locationTextSpace);
        this._locationTextContainer.append(this._locationText);

        this._locationFlex.append(this._locationTextContainer);

    }

    if (this._doesAttributeExist(this._latitude) && this._doesAttributeExist(this._longitude))  {

        this._latLongContainer = jQuery('<p></p>');
        this._latLongIcon = jQuery('<span></span>');
        this._latLongIcon.attr('class', 'glyphicon glyphicon-map-marker center-glypicon');
        this._latLongSpace = jQuery('<span>&nbsp;</span>');
        this._latLongText = jQuery('<span></span>');
        this._latLongText.text(this._latitude + '°, ' + this._longitude + '°');

        this._latLongContainer.append(this._latLongIcon);
        this._latLongContainer.append(this._latLongSpace);
        this._latLongContainer.append(this._latLongText);

        this._locationFlex.append(this._latLongContainer);

    }

    if (this._doesAttributeExist(this._dateMin) && this._doesAttributeExist(this._dateMax)) {

        this._timeContainer = jQuery('<p></p>');
        this._calIcon = jQuery('<span></span>');
        this._calIcon.attr('class', 'glyphicon glyphicon-calendar center-glypicon');
        this._timeSpace = jQuery('<span>&nbsp;</span>');
        this._timeText = jQuery('<span></span>');
        this._timeText.text(this._dateMin + ' - ' + this._dateMax);

        this._timeContainer.append(this._calIcon);
        this._timeContainer.append(this._timeSpace);
        this._timeContainer.append(this._timeText);

        this._locationFlex.append(this._timeContainer);

    }

    if (this._doesAttributeExist(this._url)) {

        this._urlContainer = jQuery('<p></p>');
        this._urlIcon = jQuery('<span></span>');
        this._urlIcon.attr('class', 'glyphicon glyphicon-link center-glypicon');
        this._urlSpance = jQuery('<span>&nbsp;</span>');
        this._urlText = jQuery('<span></span>');
        this._urlText.text(this._url);

        this._urlContainer.append(this._urlIcon);
        this._urlContainer.append(this._urlSpance);
        this._urlContainer.append(this._urlText);

        this._locationFlex.append(this._urlContainer);


    }

    this._locationContainer.append(this._locationFlex);

    this._row.append(this._radioContainer);
    this._row.append(this._bodyContainer);
    this._row.append(this._locationContainer);

    container.append(this._row);

}

MetadataResultsRow.prototype = {

    _insertLabel: function() {

        label = jQuery('<p></p>');
        label.text(this._label);
        return label;

    },
    _doesAttributeExist: function(value) {

        if ((value !== undefined) && (value !== null) && (value !== "")) {

            return true;

        } else {

            return false;

        }

    }

};

function UserData() {

    this._latitude_min = null;
    this._latitude_max = null;
    this._longitude_min = null;
    this._longitude_max = null;
    this._date_min = null;
    this._date_max = null;
    this._search_results = {};
    this._is_gaz_selected = 0;
    this._image_dimensions = null;
    this._course_search_types = null;
    this._metadata_list = null;
    this._image_title = null;
    this._collection_pid = null;
    this._image_pid = null;
    this._lti_user_id = null;
    this._lti_course_id = null;
    this._course_round_id = null;
    this._gazetteerConfigs = [];

    if (this._checkSesssionStorage('lti_session_key')) {

        this._lti_session_key = sessionStorage.getItem('lti_session_key');

    } else {

        this._lti_session_key = null;

    }

}

UserData.prototype = {

    _checkSesssionStorage: function(key) {

        if (sessionStorage.getItem(key) === null) {

            return false;

        } else {

            return true;

        }

    },
    latitudeMin: function(value) {

        if (arguments.length === 0) {

            return this._latitude_min

        } else {

            this._latitude_min = value;

        }

    },
    latitudeMax: function(value) {

        if (arguments.length === 0) {

            return this._latitude_max

        } else {

            this._latitude_max = value;

        }

    },
    longitudeMin: function(value) {

        if (arguments.length === 0) {

            return this._longitude_min;

        } else {

            this._longitude_min = value;

        }

    },
    longitudeMax: function(value) {

        if (arguments.length === 0) {

            return this._longitude_max;

        } else {

            this._longitude_max = value;

        }

    },
    yearMin: function(value) {

        if (arguments.length === 0) {

            return this._date_min;

        } else {

            this._date_min = value;

        }

    },
    yearMax: function(value) {

        if (arguments.length === 0) {

            return this._date_max;

        } else {

            this._date_max = value;

        }

    },
    searchResults: function(value) {

        if (arguments.length === 0) {

            return this._search_results;

        } else {

            this._search_results = value;

        }

    },
    isGazetteerSelected: function(value) {

        if (arguments.length === 0) {

            return this._is_gaz_selected;

        } else {

            this._is_gaz_selected = value;

        }

    },
    imageDimensions: function(value) {

        if (arguments.length === 0) {

            return this._image_dimensions;

        } else {

            this._image_dimensions = value;

        }

    },
    courseSearchType: function(value) {

        if (arguments.length === 0) {

            return this._course_search_types;

        } else {

            this._course_search_types = value;

        }

    },
    metadataList: function(value) {

        if (arguments.length === 0) {

            return this._metadata_list;

        } else {

            this._metadata_list = value;

        }

    },
    imageTitle: function(value) {

        if (arguments.length === 0) {

            return this._image_title;

        } else {

            this._image_title = value;

        }

    },
    collectionPID: function(value) {

        if (arguments.length === 0) {

            return this._collection_pid;

        } else {

            this._collection_pid = value;

        }

    },
    imagePID: function(value) {

        if (arguments.length === 0) {

            return this._image_pid;

        } else {

            this._image_pid = value;

        }

    },
    LTICourseID: function(value) {

        if (arguments.length === 0) {

            return this._lti_course_id;

        } else {

            this._lti_course_id = value;

        }

    },
    LTIUserID: function(value) {

        if (arguments.length === 0) {

            return this._lti_user_id;

        } else {

            this._lti_user_id = value;

        }

    },
    LTISessionKey: function(value) {

        if (arguments.length === 0) {

            return this._lti_session_key;

        } else {

            this._lti_session_key = value;

        }

    },
    courseRoundID: function(value) {

        if (arguments.length === 0) {

            return this._course_round_id;

        } else {

            this._course_round_id = value;

        }

    },
    gazetteerConfigs: function(value) {

        if (arguments.length === 0) {

            return this._gazetteerConfigs;

        } else {

            this._gazetteerConfigs.push(value);

        }

    }


};


// function refreshApiData(search_scope) {
    //
    //     min_criteria = [];
    //
    //     search_results = userData['search_results'];
    //
    //     for (var st_key in search_results) {
    //
    //
    //         var additionalParams = {};
    //         additionalParams['queryParams'] = {};
    //
    //         if (!search_results.hasOwnProperty(st_key)) {
    //             continue;
    //         }
    //
    //         if (!(search_scope === 'global')) {
    //             if (!(search_scope === st_key)) {
    //                 continue;
    //             }
    //         }
    //
    //         min_criteria[st_key] = 0;
    //
    //         var gaz_dict = gaz_config[st_key]['gaz_dict'];
    //
    //         var gaz_param = $.map(gaz_dict, function (gaz_info) {
    //             return gaz_info['gaz_name'];
    //         }).join(',');
    //
    //         var keyword_str = userData['search_results'][st_key]['keyword_str'];
    //
    //         if (keyword_str) {
    //             min_criteria[st_key] += 1;
    //             additionalParams['queryParams']['query'] = keyword_str;
    //         }
    //
    //     }
    //
    //     var nw_lat = userData['bbox_nw_lat'];
    //     var nw_lng = userData['bbox_nw_lng'];
    //     var se_lat = userData['bbox_se_lat'];
    //     var se_lng = userData['bbox_se_lng'];
    //
    //     var dt_begin = userData['year_min'];
    //     var dt_end = userData['year_max'];
    //
    //     var order_by = userData['search_results'][st_key]['order_by'];
    //
    //     if (nw_lat != null && nw_lng != null && se_lat != null && se_lng != null) {
    //         additionalParams['queryParams']['bbox'] = nw_lat + "," + nw_lng + "," + se_lat + "," + se_lng;
    //         min_criteria[st_key] += 1;
    //     }
    //
    //     if (st_key != 'place') {
    //
    //         if (!is_empty(dt_begin)) {
    //             additionalParams['queryParams']['dateMin'] = dt_begin;
    //             min_criteria[st_key] += 1;
    //         }
    //
    //         if (!is_empty(dt_end)) {
    //             additionalParams['queryParams']['dateMax'] = dt_end;
    //             min_criteria[st_key] += 1;
    //         }
    //     }
    //
    //     if (!is_empty(order_by)) {
    //         additionalParams['queryParams']['orderBy'] = order_by;
    //         // Reset order_by to null with each call.
    //         userData['search_results'][st_key]['order_by'] = null;
    //     }
    //
    //     gazData[st_key] = [];
    //     if (min_criteria[st_key] < 1) {
    //         $("#" + st_key + "_results_table_body").html('<div class="results_error_box">' +
    //             'At least one criteria is required to search the ' +
    //             st_key +
    //             ' Gazetteer.' +
    //             '<br/>Select at least one of: geo bounding box area, begin year, end year, or keyword.' +
    //             '</div>');
    //     } else {
    //         is_err_notified = 0;
    //         pull_gazetteer_results(st_key, 1, additionalParams);
    //     }
    //
    // }
    //
    // function prepare_keyword(q) {
    //     final_str = q.replace(/\s+/g, '+');
    //     return final_str;
    //
    // }
    //
    // function validate_year(year) {
    //     if (is_empty(year)) {
    //         return true;
    //     }
    //     return (year.match(/^[0-9\-]+$/));
    //
    // }



    //
    // function pull_gazetteer_results(search_type, gazetteerID, queryParams) {
    //
    //
    //
    //
    //
    //     gazetteerAPI.gazetteersGazetteerIdSearchGet(params, body, queryParams)
    //         .then(function(result) {
    //
    //             results = result.data.response;
    //
    //             console.log(results);
    //
    //             spinner.stop();
    //
    //         }).catch(function(result) {
    //
    //             console.log(result);
    //
    //             spinner.stop();
    //             if (is_err_notified != 1) {
    //                 is_err_notified = 1;
    //                 alert('Unable to retrieve Gazetteer results. Please wait a few minutes and try again.')
    //             }
    //             $(tbody_id).empty();
    //             $(tbody_id).html('<div class="results_error_box">Unable to retrieve Gazetteer results for ' + search_type + '</div>');
    //
    //         });
    //
    // }
    //
    // function mark_gaz_selection(search_type, idx) {
    //
    //     var gaz_item = gazData[search_type][idx];
    //     userData['is_gaz_selected'] = 1;
    //     userData['search_results'][search_type]['user_selections'] = gaz_item;
    //     selected_id = "#select_" + search_type + "_dynamic";
    //     var sel_text = gaz_item['label'];
    //     $(selected_id).html(sel_text);
    //
    // }
