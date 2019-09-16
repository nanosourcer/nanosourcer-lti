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
        

        console.log(courseConfig);

        showInstructions = readCookie('showInstructions');

        if (showInstructions == null) {

            createCookie('showInstructions', false, 3);
            showInstructions = true;

        } else {

            showInstructions = false;

        }

    };

})();

jQuery(document).ready(function () {

    userData = {

        isSelection: false,
        processStatusID: 1,
        placeSelection: null,
        placeQueryMetadata: null,
        periodSelection: null,
        periodQueryMetadata: null,
        placeKeyword: null,
        periodKeyword: null,
        dateMax: null,
        dateMin: null,
        bboxSelection: {

            northEastLat: null,
            northEastLong: null,
            southWestLat: null,
            southWestLong: null

        }

    };



    spinner = buildSpinner();

    var body = jQuery("body");

    var map = new MapWidget("map-widget", courseConfig);

    var navbar = new Navbar("navbar",
        courseConfig['course_user_info']['user_info'],
        courseConfig['course_search_types']
    );

    body.append(navbar.get());

    var container = jQuery("<div></div>");
    container.attr("class", "container");

    body.append(container);

    var rows = new Container(container);

    var statusCard = buildStatusCard(courseConfig);

    rows.appendStatus(statusCard.get());

    var infoCard = buildInformationCard();
    var imageCard = buildImageViewerCard(

        courseConfig['fedora_image_url'],
        courseConfig['metadata_list'],
        courseConfig['image_dimensions']['image_width'],
        courseConfig['image_dimensions']['image_height']

    );

    var placeCard = buildPlaceSearchCard(map);

    var periodCard = buildPeriodSearchCard();

    rows.appendCards(infoCard.get());
    rows.appendCards(imageCard.get());
    rows.appendCards(placeCard.get());
    rows.appendCards(periodCard.get());


    var startingIndex = 1;

    if (showInstructions) {

        startingIndex = 0;

    }

    cardCarousel = jQuery("#card-container").flickity({

        accessibility: true,
        adaptiveHeight: true,
        autoPlay: false,
        cellAlign: "left",
        cellSelector: ".card",
        contain: true,
        draggable: true,
        dragThreshold: 10,
        freeScroll: false,
        friction: 0.3,
        selectedAttraction: 0.05,
        groupCells: false,
        initialIndex: startingIndex,
        lazyLoad: false,
        percentagePosition: true,
        prevNextButtons: false,
        pageDots: false,
        resize: true,
        rightToLeft: false,
        setGallerySize: true,
        watchCSS: false,
        wrapAround: false

    });

    navbar.build();

    jQuery("#image-thumbnail").viewer({

        fullscreen: true,
        inline: false,
        navbar: false,
        keyboard: true,
        title: false,
        toolbar: true,
        url: courseConfig['fedora_image_url']

    });

    jQuery(".image-viewer-image-container").click(function() {

        jQuery("#image-thumbnail").viewer("show");

    });

    jQuery("#status-search-2").click(function() {

        cardCarousel.flickity('select', 2);

    });

    jQuery("#status-search-3").click(function() {

        cardCarousel.flickity('select', 3);

    });

    jQuery("#status-submit").click(function() {

        var submitModalCardID = "submit-modal-card";
        var submitModalCard = buildSubmitModalCard(submitModalCardID);
        displayModal(submitModalCard.get());

        jQuery("#" + submitModalCardID).css("margin", 0);

    });

    jQuery("#status-skip").click(function() {

        var skipModalCardID = "skip-modal-card";
        var skipModalCard = buildSkipModalCard(skipModalCardID);
        displayModal(skipModalCard.get());

        jQuery("#" + skipModalCardID).css("margin", 0);

    });

    map.build();

    map.getMapObj().on('popupopen', function(e) {

        var px = map.getMapObj().project(e.popup._latlng);
        px.y -= e.popup._container.clientHeight/2;
        map.getMapObj().panTo(map.getMapObj().unproject(px), {animate: true});


    });

    checkGLSHealth(courseConfig);

});

function convertDate(value) {

    if (value < 0) {

        return Math.abs(value) + " BCE"

    } else {

        return value + " CE"

    }

}

function buildSpinner() {

    var opts = {

        lines: 13,
        length: 28,
        width: 14,
        radius: 42,
        scale: 1,
        corners: 1,
        color: '#000',
        opacity: 0.25,
        rotate: 0,
        direction: 1,
        speed: 1,
        trail: 60,
        fps: 20,
        zIndex: 2e9,
        className: 'spinner',
        top: '50%',
        left: '50%',
        shadow: false,
        hwaccel: true,
        position: 'absolute'

    };

    return new Spinner().spin();

}

function buildStatusCard(courseConfig) {

    var statusCard = new Card("status-card");

    var statusCardTitle = jQuery("<div></div>");
    statusCardTitle.attr("class", "card-header-title");
    statusCardTitle.text("Selected Metadata");

    var GLSIndicatorText = jQuery("<div></div>");
    GLSIndicatorText.attr("class", "card-header-title");
    GLSIndicatorText.text("GLS Health: ");

    var GLSIndicatorIcon = jQuery("<span></span>");
    GLSIndicatorIcon.attr("id", "gls-indicator");
    GLSIndicatorIcon.attr("class", "gls-red");
    GLSIndicatorIcon.text(" ");

    GLSIndicatorText.append(GLSIndicatorIcon);

    statusCard.appendHeader(statusCardTitle);
    statusCard.appendHeader(GLSIndicatorText);

    var bodyItemContainer = jQuery("<div></div>").attr("class", "col-lg-10 col-md-10 col-sm-10 col-xs-10");

    var index = 2;

    jQuery.each(courseConfig['course_search_types'], function() {

        var bodyItem = new StatusCardBodyItem("status-search-" + index, this);

        bodyItemContainer.append(bodyItem.get());

        index++;

    });

    statusCard.appendBody(bodyItemContainer);

    var thumbnailContainer = jQuery("<div></div>").attr("class", "col-lg-2 col-md-2 col-sm-2 col-xs-2");

    var thumbnail = jQuery("<div></div>").attr("id", "image-thumbnail");

    var thumbnailImg = jQuery("<img>").attr("class", "thumbnail-image").attr("src", courseConfig['fedora_image_url']);

    thumbnail.append(thumbnailImg);

    thumbnailContainer.append(thumbnail);

    statusCard.appendBody(thumbnailContainer);

    var submitBtn = new CardFooterBtn("status-submit", "glyphicon glyphicon-send", "Submit");
    var skipBtn = new CardFooterBtn("status-skip", "glyphicon glyphicon-refresh", "Skip");

    var btnContainerSubmit = jQuery("<div></div>");
    btnContainerSubmit.attr("class", "card-footer-item col-lg-6 col-md-6 col-sm-6 col-xs-6");
    btnContainerSubmit.append(submitBtn.get());

    var btnContainerSkip = jQuery("<div></div>");
    btnContainerSkip.attr("class", "card-footer-item col-lg-6 col-md-6 col-sm-6 col-xs-6");
    btnContainerSkip.append(skipBtn.get());

    statusCard.appendFooter(btnContainerSubmit);
    statusCard.appendFooter(btnContainerSkip);

    return statusCard;

}

function buildImageViewerCard(imageURL, imageMetadataList, width, height) {

    var imageViewerCard = new Card("image-viewer-card");

    var imageViewerCardTitle = jQuery("<div></div>");
    imageViewerCardTitle.attr("class", "card-header-title");
    imageViewerCardTitle.text("Image Viewer");

    imageViewerCard.appendHeader(imageViewerCardTitle);

    imageContainer = jQuery("<div></div>");
    imageContainer.attr("class", "image-viewer-image-container col-lg-6 col-md-6 col-sm-12 col-xs-12");

    var image = jQuery("<img>");
    image.attr("class", "fedora-image");
    image.attr("id", "fedora-image");
    image.attr("src", imageURL);

    imageContainer.append(image);

    metadataContainer = jQuery("<div></div>");
    metadataContainer.attr("class", "metadata-container col-lg-6 col-md-6 col-sm-12 col-xs-12");

    jQuery.each(imageMetadataList, function() {

        var metadataItemContainer = jQuery("<div></div>");
        metadataItemContainer.attr("class", "image-metadata-item-container");

        var type = jQuery("<p></p>");
        type.attr("class", "image-metadata-title");
        type.text(this['type']);

        var label = jQuery("<p></p>");
        label.attr("class", "image-metadata-label");
        label.text(this['label']);

        if (this['label'] !== "") {

            metadataItemContainer.append(type);
            metadataItemContainer.append(label);

            metadataContainer.append(metadataItemContainer);

        }

    });

    var bodyRow = jQuery("<div></div>");
    bodyRow.attr("class", "row card-body-row");

    bodyRow.append(imageContainer, metadataContainer);

    imageViewerCard.appendBody(bodyRow);

    return imageViewerCard;

}

function buildInformationCard() {

    var informationCard = new Card("information-card");

    var informationCardTitle = jQuery("<div></div>");
    informationCardTitle.attr("class", "card-header-title");
    informationCardTitle.text("Welcome to Nanosourcer!");

    var paragraph0 = jQuery("<p></p>");
    paragraph0.attr("class", "card-body-text col-lg-12 col-md-12 col-sm-12 col-xs-12");
    paragraph0.text( 'Every time you load this page, an image you have not yet tagged will be slected randomly from the collection for this course. The image will appear on the right side of the screen. If your instructor has provided information about the image, it will appear next to the image.');

    var paragraph1 = jQuery("<p></p>");
    paragraph1.attr("class", "card-body-text col-lg-12 col-md-12 col-sm-12 col-xs-12");
    paragraph1.text('Now you’re ready to start tagging. Your instructor will ask you to tag places, periods, or both.');

    var paragraph2 = jQuery("<p></p>");
    paragraph2.attr("class", "card-body-text col-lg-12 col-md-12 col-sm-12 col-xs-12");
    paragraph2.text('For places, if you see a monument or landscape, you should tag it with the place-name that reflects its current location; if you see an object, tag it with the place EITHER where it was created OR where it was found. You may only select one "place" value.');

    var paragraph3 = jQuery("<p></p>");
    paragraph3.attr("class", "card-body-text col-lg-12 col-md-12 col-sm-12 col-xs-12");
    paragraph3.text('To search for a place, draw a box on the map to define the general area where that place is located. Then type a full or partial keyword (for example, the name of a place, like “Athens”) into the “place keyword” field. Select the correct place from the list that appears. If your place name doesn’t appear, scroll down, or redraw a box on the map. When you redraw the box, the selection list will automatically be reset.');

    var paragraph4 = jQuery("<p></p>");
    paragraph4.attr("class", "card-body-text col-lg-12 col-md-12 col-sm-12 col-xs-12");
    paragraph4.text('For periods, if you see a monument or object, you should tag it with the period during which it was created. If you see a monument that you know was used over several periods, you may select multiple values.');

    var paragraph5 = jQuery("<p></p>");
    paragraph5.attr("class", "card-body-text col-lg-12 col-md-12 col-sm-12 col-xs-12");
    paragraph5.text('To search for a period, enter in the “begin year” and “end year” fields the start and end dates that you think will overlap with the period during which you think the object or monument was created and/or in use. Then type a full or partial keyword (for example, the name of a period, like “archaic”) into the “period keyword” field. Select the correct period from the list that appears. You can use the start and end dates of the results and the “spatial label”, which tells you where in space that period applies, to narrow down your choices. You can also change the start and/or end dates to reset the selection list. Remember that AD/CE years should be entered in the form “yyyy”, and BC/BCE years in the form “-yyyy”.');

    var paragraph6 = jQuery("<p></p>");
    paragraph6.attr("class", "card-body-text col-lg-12 col-md-12 col-sm-12 col-xs-12");
    paragraph6.text('You’ll get place results with either a box on the map or a keyword search, but you have to have at least one of them, and if you use them together, they’ll narrow the results. The same is true for periods: you can use either dates or keywords alone, but they work better together.');

    var paragraph7 = jQuery("<p></p>");
    paragraph7.attr("class", "card-body-text col-lg-12 col-md-12 col-sm-12 col-xs-12");
    paragraph7.text('When you are satisfied with your selections, click “Submit Selections” to record them. A new randomly selected image will load. You will never see an image you’ve already tagged again, so don’t click “submit” until you’re sure you’re done with it. If, however, you aren’t sure about an image and you don’t want to submit any tags, just click on “Load a different image” at the top of the page. This will clear out any tags you’ve already selected but haven’t clicked the button to submit.');

    var paragraph8 = jQuery("<p></p>");
    paragraph8.attr("class", "card-body-text col-lg-12 col-md-12 col-sm-12 col-xs-12");
    paragraph8.text('If you load a new image without submitting tags, the image you skipped will go back into your rotation, so it may appear again later. You never have to add tags to an image. It’s better to skip images until you have one you’re sure of than to add tags by guessing.');

    var paragraph9 = jQuery("<p></p>");
    paragraph9.attr("class", "card-body-text col-lg-12 col-md-12 col-sm-12 col-xs-12");
    paragraph9.text('Now you’re ready to go. Have fun tagging!');
    paragraph9.css("font-weight", "bold");

    var textContainer = jQuery("<div></div>");
    textContainer.attr("class", "row");

    textContainer.append(

        paragraph0,
        paragraph1,
        paragraph2,
        paragraph3,
        paragraph4,
        paragraph5,
        paragraph6,
        paragraph7,
        paragraph8,
        paragraph9

    );

    informationCard.appendHeader(informationCardTitle);
    informationCard.appendBody(textContainer);

    return informationCard;

}

function buildSkipModalCard(cardID) {

    var skipModalCard = new Card(cardID);

    var skipModalCardTitle = jQuery("<div></div>");
    skipModalCardTitle.attr("class", "card-header-title");
    skipModalCardTitle.text("Are you sure?");

    skipModalCard.appendHeader(skipModalCardTitle);

     var messageBody = jQuery("<p></p>").attr("class", "popup-text-bold col-lg-12 col-md-12 col-sm-12 col-xs-12");
    messageBody.text("Skipping an image will not remove it from your available image pool. You will have a chance to provide metadata for it again in the future.");

    skipModalCard.appendBody(messageBody);

    var yesBtn = new CardFooterBtn("skip-modal-card-yes-btn", "glyphicon glyphicon-ok", "Yes, Skip It!");

    var yesBtnContainer = jQuery("<div></div>");
    yesBtnContainer.attr("class", "card-footer-item col-lg-6 col-md-6 col-sm-6 col-xs-6");
    yesBtnContainer.append(yesBtn.get());

    var cancelBtn = new CardFooterBtn("skip-modal-card-cancel-btn", "glyphicon glyphicon-remove", "Cancel");

    var cancelBtnContainer = jQuery("<div></div>");
    cancelBtnContainer.attr("class", "card-footer-item col-lg-6 col-md-6 col-sm-6 col-xs-6");
    cancelBtnContainer.append(cancelBtn.get());

    skipModalCard.appendFooter(yesBtnContainer);
    skipModalCard.appendFooter(cancelBtnContainer);

    jQuery(yesBtn.get()).click(function() {

        userData['processStatusID'] = 1;
        var bodyContainer = jQuery("#skip-modal-card > .card-body-container");
        transmitUserData(false, bodyContainer);

    });

    jQuery(cancelBtn.get()).click(function() {

        destroyModal();

    });

    jQuery("html").keyup(function(e) {

        if (e.keyCode == 27) {

            console.log(e.keyCode);
            destroyModal();

        }

    });

    return skipModalCard;

}

function buildSubmitModalCard(cardID) {

    var submitModalCard = new Card(cardID);

    var submitModalCardTitle = jQuery("<div></div>");
    submitModalCardTitle.attr("class", "card-header-title");
    submitModalCardTitle.text("Are you sure?");

    submitModalCard.appendHeader(submitModalCardTitle);

    var messageBody = jQuery("<p></p>").attr("class", "popup-text-bold col-lg-12 col-md-12 col-sm-12 col-xs-12");
    messageBody.text("You are about to submit the following metadata selections for the current image:");

    var metadataRow = jQuery("<div></div>").attr("class", "row");

    var displayButtons = false;

    if (userData['placeSelection'] !== null && userData['periodSelection'] == null) {

        displayButtons = true;

        var placeSection = buildMetadataSelectionDisplay(userData['placeSelection'], 12, 12, 12, 12);

        submitModalCard.appendBody(messageBody);

        metadataRow.append(placeSection);

        submitModalCard.appendBody(metadataRow);

    } else if (userData['placeSelection'] == null && userData['periodSelection'] !== null) {

        displayButtons = true;

        var periodSection = buildMetadataSelectionDisplay(userData['periodSelection'], 12, 12, 12, 12);

        submitModalCard.appendBody(messageBody);

        metadataRow.append(periodSection);

        submitModalCard.appendBody(metadataRow);

    } else if (userData['placeSelection'] !== null && userData['periodSelection'] !== null) {

        displayButtons = true;

        var placeSection = buildMetadataSelectionDisplay(userData['placeSelection'], 6, 6, 12, 12);
        var periodSection = buildMetadataSelectionDisplay(userData['periodSelection'], 6, 6, 12, 12);

        submitModalCard.appendBody(messageBody);

        metadataRow.append(placeSection);
        metadataRow.append(periodSection);

        submitModalCard.appendBody(metadataRow);


    } else {

        var errorMessageContainer = jQuery("<div></div>");
        errorMessageContainer.attr("class", "error-container");
        errorMessageContainer.text("You can't make a submission unless you select at least one piece of metadata.");
        submitModalCard.appendBody(errorMessageContainer);

        setTimeout(function() {

            destroyModal();

        }, 4500);

    }

   if (displayButtons) {

        var yesBtn = new CardFooterBtn("submit-modal-card-yes-btn", "glyphicon glyphicon-ok", "Yes!");

        var yesBtnContainer = jQuery("<div></div>");
        yesBtnContainer.attr("class", "card-footer-item col-lg-6 col-md-6 col-sm-6 col-xs-6");
        yesBtnContainer.append(yesBtn.get());

        var cancelBtn = new CardFooterBtn("submit-modal-card-cancel-btn", "glyphicon glyphicon-remove", "Cancel");

        var cancelBtnContainer = jQuery("<div></div>");
        cancelBtnContainer.attr("class", "card-footer-item col-lg-6 col-md-6 col-sm-6 col-xs-6");
        cancelBtnContainer.append(cancelBtn.get());

        submitModalCard.appendFooter(yesBtnContainer);
        submitModalCard.appendFooter(cancelBtnContainer);

        jQuery(yesBtn.get()).click(function() {

            userData['processStatusID'] = 0;

            var bodyContainer = jQuery("#submit-modal-card > .card-body-container");

            transmitUserData(true, bodyContainer);

        });

        jQuery(cancelBtn.get()).click(function() {

            destroyModal();

        });

   }

    jQuery("html").keyup(function(e) {

        if (e.keyCode == 27) {

            console.log(e.keyCode);
            destroyModal();

        }

    });



    return submitModalCard;

}

function buildMetadataSelectionDisplay(data, colLG, colMD, colSM, colXS) {

    var containerClass = "col-lg-" + colLG + " col-md-" + colMD + " col-sm-" + colSM + " col-xs-" + colXS;
    
    var container = jQuery("<div></div>").attr("class", containerClass);

    var label = jQuery("<span></span>");
    label.attr("class", "popup-text-bold");
    label.text(data['label']);

    var linkContainer = jQuery("<div></div>");

    var linkIcon = jQuery("<span></span>");
    linkIcon.attr("class", "glyphicon glyphicon-link");

    var linkText = jQuery("<a></a>");
    linkText.attr("class", "popup-link-text");
    linkText.attr("href", data['gazetteerURI']);
    linkText.attr("target", "_blank");
    linkText.text(data['gazetteerURI']);

    linkContainer.append(linkIcon, linkText);

    var description = jQuery("<p></p>");
    description.attr("class", "popup-text");
    description.text(data['secondaryLabel']);

    var otherInfoContainer = jQuery("<div></div>");
    otherInfoContainer.attr("class", "row");

    var spatialLabelContainer = jQuery("<div></div>");
    spatialLabelContainer.attr("class", "col-lg-6 col-md-6 col-sm-6 col-xs-6");

    var spatialLabelIcon = jQuery("<span></span>")
        .attr("class", "glyphicon glyphicon-globe");

    var spatialLabelText = jQuery("<span></span>")
        .attr("class", "popup-metadata-text")
        .text(data['spatialLabel']);

    spatialLabelContainer.append(spatialLabelIcon, spatialLabelText);


    var dateContainer = jQuery("<div></div>");
    dateContainer.attr("class", "col-lg-6 col-md-6 col-sm-6 col-xs-6");

    var dateIcon = jQuery("<span></span>")
        .attr("class", "glyphicon glyphicon-calendar");

    var dateText = jQuery("<span></span>")
        .attr("class", "popup-metadata-text")
        .text(convertDate(data['dateMin']) + ' - ' + convertDate(data['dateMax']));

    dateContainer.append(dateIcon, dateText);

    otherInfoContainer.append(spatialLabelContainer, dateContainer);

    container.append(label, linkContainer, description, otherInfoContainer);

    return container;

}

function buildPlaceSearchCard(mapWidget) {

    var placeSearchCard = new Card("period-search-card");

    var placeSearchCardTitle = jQuery("<div></div>");
    placeSearchCardTitle.attr("class", "card-header-title");
    placeSearchCardTitle.text("Place Search");

    placeSearchCard.appendHeader(placeSearchCardTitle);

    var bodyRow = jQuery("<div></div>");
    bodyRow.attr("class", "row card-body-row");

    bodyRow.append(mapWidget.getContainer());
    bodyRow.append(mapWidget.getResultsContainer());
    bodyRow.append(mapWidget.getCoordinatesWindow());

    placeSearchCard.appendBody(bodyRow);

    return placeSearchCard;

}

function buildPeriodSearchCard() {

    var periodSearchCard = new Card("period-search-card");

    var periodWidget = new PeriodWidget();

    var periodSearchCardTitle = jQuery("<div></div>");
    periodSearchCardTitle.attr("class", "card-header-title");
    periodSearchCardTitle.text("Period Search");

    periodSearchCard.appendHeader(periodSearchCardTitle);

    var bodyRow = jQuery("<div></div>");
    bodyRow.attr("class", "row card-body-row");

    bodyRow.append(periodWidget.get());

    periodSearchCard.appendBody(bodyRow);

    return periodSearchCard;

}

function destroyModal() {

    jQuery(".modal-background-shadow").css("animation", "modal-fade-out 1s ease-in-out 0s 1 normal");
    jQuery(".modal-background-shadow").css("opacity", "0.0");
    
    setTimeout(function() {
        
        jQuery(".modal-background-shadow").remove();
        
    }, 2500);

    jQuery("body").css("overflow", "initial");

    jQuery("html").off("keyup");

}

function displayModal(modalCard) {

    var background = jQuery("<div></div>").attr("class", "modal-background-shadow");

    background.append(modalCard);

    jQuery("body").append(background).css("overflow", "hidden");

}

function transformUserData(data, courseConfig) {

    var gazetteerInfo = courseConfig['gaz_config'];

    var transformedData = {};

    if (data['bboxSelection']['northEastLat'] !== null) {

        transformedData['bbox_nw_lat'] = data['bboxSelection']['northEastLat'];
        transformedData['bbow_nw_lng'] = data['bboxSelection']['northEastLong'];
        transformedData['bbox_se_lat'] = data['bboxSelection']['southWestLat'];
        transformedData['bbow_se_lng'] = data['bboxSelection']['southWestLong'];

    }

    transformedData['year_min'] = data['dateMin'];
    transformedData['year_max'] = data['dateMax'];
    transformedData['course_search_types'] = courseConfig['course_search_types'];

    transformedData['image_dimensions'] = courseConfig['image_dimensions'];
    transformedData['image_title'] = courseConfig['image_title'];
    transformedData['collection_pid'] = courseConfig['collection_pid'];
    transformedData['image_pid'] = courseConfig['image_pid'];
    transformedData['course_round_id'] = courseConfig['course_round_id'];
    transformedData['lti_user_id'] = courseConfig['lti_user_id'];
    transformedData['lti_course_id'] = courseConfig['lti_course_id'];
    transformedData['process_status_id'] = data['processStatusID'];
    transformedData['is_gaz_selected'] = false;


    if (userData['placeSelection'] !== null) {

        transformedData['search_results'] = {};
        transformedData['search_results']['place'] = {};

        transformedData['search_results']['place']['keyword_str'] = userData['placeKeyword'];
        transformedData['search_results']['place']['order_by'] = "relevance";
        transformedData['search_results']['place']['gaz_key'] = "place";

        var pleiadesInfo = gazetteerInfo['place']['gaz_dict']['pleiades'];

        transformedData['search_results']['place']['gaz_name'] = pleiadesInfo['gaz_name'];
        transformedData['search_results']['place']['gaz_url'] = pleiadesInfo['gaz_url'];
        transformedData['search_results']['place']['columns'] = gazetteerInfo['place']['columns'];
        transformedData['search_results']['place']['result_count'] = data['placeQueryMetadata']['count'];
        transformedData['search_results']['place']['user_selections'] = userData['placeSelection'];

        transformedData['is_gaz_selected'] = true;

    }

    if (userData['periodSelection'] !== null) {

        transformedData['search_results'] = {};
        transformedData['search_results']['period'] = {};

        transformedData['search_results']['period']['keyword_str'] = userData['periodKeyword'];
        transformedData['search_results']['period']['order_by'] = "relevance";
        transformedData['search_results']['period']['gaz_key'] = "period";

        var periodoInfo = gazetteerInfo['period']['gaz_dict']['periodo'];

        transformedData['search_results']['period']['gaz_name'] = periodoInfo['gaz_name'];
        transformedData['search_results']['period']['gaz_url'] = periodoInfo['gaz_url'];
        transformedData['search_results']['period']['columns'] = gazetteerInfo['period']['columns'];
        transformedData['search_results']['period']['result_count'] = data['periodQueryMetadata']['count'];
        transformedData['search_results']['period']['user_selections'] = userData['periodSelection'];

        transformedData['is_gaz_selected'] = true;

    }

    return transformedData;

}

function transmitUserData(verbose, messageContainer) {

    var dataToBeTransmitted = transformUserData(userData, courseConfig);

    saveData = {

        'userData': JSON.stringify(dataToBeTransmitted),
        'lk': courseConfig['lti_session_key']

    };

    jQuery.ajax({

        url: '/student-selections/',
        type: 'post',
        data: saveData

    }).done(function (data, textStatus, xhr) {

        if (verbose) {

            var successMessageContainer = jQuery("<div></div>");
            successMessageContainer.attr("class", "success-container");
            successMessageContainer.text("Metadata Saved!");

            messageContainer.empty();
            messageContainer.append(successMessageContainer);

            setTimeout(function() {

                document.location = "/main/?lk=" + courseConfig['lti_session_key'];

            }, 2500);

        } else {

            setTimeout(function() {

                document.location = "/main/?lk=" + courseConfig['lti_session_key'];

            }, 500);

        }



    }).fail(function (data) {

        if (data.responseJSON) {

            info = data.responseJSON.info;

        } else if (data.responseText) {

            info = data.responseText

        } else {

            info = "Unable to save your selections.";

        }

        var errorMessageContainer = jQuery("<div></div>");
        errorMessageContainer.attr("class", "error-container");
        errorMessageContainer.text(info);

        messageContainer.empty();
        messageContainer.append(errorMessageContainer);

    });

}

function createCookie(name,value,days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    }
    else var expires = "";
    document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name,"",-1);
}

function checkGLSHealth(courseConfig) {

    var client = apigClientFactory.newClient({

        apiKey: courseConfig['gazetteer_api_key']

    });

    var glsParams = {};
    var glsBody = {};
    var glsAdditionalParams = {
        queryParams: {}
    };

    client.gazetteersGet(glsParams, glsBody, glsAdditionalParams)
        .then(function(result) {
            jQuery("#gls-indicator").attr("class", "gls-green");
        })
        .catch(function(result) {
            jQuery("#gls-indicator").attr("class", "gls-red");
            while(jQuery("#gls-indicator").hasClass("gls-red")) {

                client.gazetteersGet(glsParams, glsBody, glsAdditionalParams)
                    .then(function(result) {
                        jQuery("#gls-indicator").attr("class", "gls-green");
                    })

            }
        });


}

