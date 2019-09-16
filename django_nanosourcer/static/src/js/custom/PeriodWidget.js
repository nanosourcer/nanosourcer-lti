function PeriodWidget() {

    this._container = jQuery("<div></div>");
    this._container.attr("class", "period-container col-lg-12 col-md-12 col-sm-12 col-xs-12");

    this._keywordParam = null;
    this._dateMax = null;
    this._dateMin = null;


    this._glsClient = apigClientFactory.newClient({

        apiKey: courseConfig['gazetteer_api_key']

    });

    this._glsParams = {

        "gazetteer-id": 2

    };
    this._glsBody = {};
    this._glsAdditionalParams = {
        queryParams: {}
    };

    this._build();

}

PeriodWidget.prototype = {

    _build: function() {

        var self = this;

        var periodSearchInputContainer = jQuery("<div></div>");
        periodSearchInputContainer.attr("class", "col-lg-12 col-md-12 col-sm-12 col-xs-12");

        var periodInputGroup = jQuery("<div></div>");
        periodInputGroup.attr("class", "input-group");

        var periodInputSpan = jQuery("<div></div>");
        periodInputSpan.attr("class", "input-group-btn");

        var periodInputSpanIcon = jQuery("<button></button>");
        periodInputSpanIcon.attr("class", "btn btn-default glyphicon glyphicon-search");
        periodInputSpanIcon.css("top", 0);

        periodInputSpanIcon.click(function() {

             self._queryAPI();

        });

        periodInputSpan.append(periodInputSpanIcon);

        var periodInputInput = jQuery("<input>");
        periodInputInput.attr("id", "period-keyword-input");
        periodInputInput.attr("type", "text");
        periodInputInput.attr("class", "form-control");

        periodInputInput.keyup(function(e) {

            if (e.keyCode == 13) {

                self._queryAPI();

            }

        });

        var periodSearchMinDateContainer = jQuery("<div></div>");
        periodSearchMinDateContainer.attr("class", "col-lg-6 col-md-6 col-sm-6 col-xs-6");

        var periodMinDateInputGroup = jQuery("<div></div>");
        periodMinDateInputGroup.attr("class", "input-group");

        var periodMinDateSpan = jQuery("<span></span>");
        periodMinDateSpan.attr("class", "input-group-addon");
        periodMinDateSpan.text("Period Start");

        var periodMinDateInput = jQuery("<input>");
        periodMinDateInput.attr("id", "period-date-min");
        periodMinDateInput.attr("class", "form-control");
        periodMinDateInput.attr("type", "number");

        periodMinDateInput.keyup(function(e) {

            if (e.keyCode == 13) {

                self._queryAPI();

            }

        });

        periodMinDateInputGroup.append(periodMinDateSpan, periodMinDateInput);
        periodSearchMinDateContainer.append(periodMinDateInputGroup);

        var periodSearchMaxDateContainer = jQuery("<div></div>");
        periodSearchMaxDateContainer.attr("class", "col-lg-6 col-md-6 col-sm-6 col-xs-6");

        var periodMaxDateInputGroup = jQuery("<div></div>");
        periodMaxDateInputGroup.attr("class", "input-group");

        var periodMaxDateSpan = jQuery("<span></span>");
        periodMaxDateSpan.attr("class", "input-group-addon");
        periodMaxDateSpan.text("Period End");

        var periodMaxDateInput = jQuery("<input>");
        periodMaxDateInput.attr("id", "period-date-max");
        periodMaxDateInput.attr("class", "form-control");
        periodMaxDateInput.attr("type", "number");

        periodMaxDateInput.keyup(function(e) {

            if (e.keyCode == 13) {

                self._queryAPI();

            }

        });

        periodMaxDateInputGroup.append(periodMaxDateSpan, periodMaxDateInput);
        periodSearchMaxDateContainer.append(periodMaxDateInputGroup);


        periodInputGroup.append(periodInputSpan, periodInputInput);

        periodSearchInputContainer.append(periodInputGroup);

        //results

        var periodResultsContainer = jQuery("<div></div>");
        periodResultsContainer.attr("class", "col-lg-12 col-md-12 col-sm-12 col-xs-12");

        var periodResults = jQuery("<div></div>");
        periodResults.attr("id", "period-results-container");
        periodResults.attr("class", "period-results-container");

        periodResultsContainer.append(periodResults);

        var periodSearchInputRow = jQuery("<div></div>");
        periodSearchInputRow.attr("class", "row");

        periodSearchInputRow.append(periodSearchInputContainer);

        var periodDateInputsRow = jQuery("<div></div>");
        periodDateInputsRow.attr("class", "row");
        periodDateInputsRow.css("margin-top", "5px");

        periodDateInputsRow.append(periodSearchMinDateContainer, periodSearchMaxDateContainer);

        var periodResultsRow = jQuery("<div></div>");
        periodResultsRow.attr("class", "row");

        periodResultsRow.append(periodResultsContainer);

        this._container.append(periodSearchInputRow, periodDateInputsRow, periodResultsRow);

    },
    _buildResultRow: function(containerRow, data) {

        var markerContainer = jQuery("<div></div>");
        markerContainer.attr("class", "metadata-row col-lg-1 col-md-1 col-sm-1 col-xs-1");

        var markerBox = jQuery("<div></div>");
        markerBox.attr("class", "marker-box");

        var markerRing = jQuery("<div></div>");
        markerRing.attr("class", "metadata-row-marker");

        var markerDot = jQuery("<div></div>");
        markerDot.attr("class", "metadata-row-marker-dot");

        markerRing.append(markerDot);

        markerRing.click(function() {

            jQuery(".active-meta-marker").each(function() {

                jQuery(this).attr("class", "metadata-row-marker");

            });

            jQuery(this).attr("class", "metadata-row-marker active-meta-marker");

            userData['periodSelection'] = data;
            userData['isSelection'] = true;

            jQuery("#status-bar-message-Period").text(data['label']);

        });

        markerBox.append(markerRing);
        markerContainer.append(markerBox);

        var container = jQuery("<div></div>");
        container.attr("class", "metadata-row col-lg-11 col-md-11 col-sm-11 col-xs-11");

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

        linkContainer.append(label, linkIcon, linkText);

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
            .text(this._convertDate(data['dateMin']) + ' - ' + this._convertDate(data['dateMax']));

        dateContainer.append(dateIcon, dateText);

        otherInfoContainer.append(spatialLabelContainer, dateContainer);

        container.append(linkContainer, description, otherInfoContainer);

        var metadataRowContainer = jQuery("<div></div>");
        metadataRowContainer.attr("class", "metadata-row-container");

        metadataRowContainer.append(markerContainer, container);

        containerRow.append(metadataRowContainer);

    },
    _convertDate: function(value) {

        if (value < 0) {

            return Math.abs(value) + " BCE"

        } else {

            return value + " CE"

        }

    },
    _queryAPI: function() {

        var self = this;

        this._keywordParam = jQuery("#period-keyword-input").val();
        this._dateMin = jQuery("#period-date-min").val();
        this._dateMax = jQuery("#period-date-max").val();



        this._glsAdditionalParams = {
            queryParams: {}
        };

        var sufficient = false;

        if (this._keywordParam.length > 2) {

            this._glsAdditionalParams['queryParams']['query'] = this._keywordParam;
            sufficient = true;
            userData['periodKeyword'] = this._keywordParam;

        }

        if (this._dateMax != "") {

            this._glsAdditionalParams['queryParams']['dateMax'] = this._dateMax;
            sufficient = true;
            userData['dateMax'] = this._dateMax;

        }

        if (this._dateMin != "") {

            this._glsAdditionalParams['queryParams']['dateMin'] = this._dateMin;
            sufficient = true;
            userData['dateMin'] = this._dateMin;

        }

        if (sufficient) {

            var target = document.getElementById("period-results-container");
            var jTarget = jQuery("#period-results-container");
            jTarget.empty();

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

            var spinner = new Spinner(opts).spin(target);

            this._glsClient.gazetteersGazetteerIdSearchGet(this._glsParams, this._glsBody, this._glsAdditionalParams)
                .then(function (result) {

                    var items = result['data']['response']['items'];
                    var queryMetadata = result['data']['response']['queryMetadata'];

                    userData['periodQueryMetadata'] = queryMetadata;

                    spinner.stop();

                    jQuery("#period-results-container").css("margin-top", "10px");

                    if (items.length > 0) {

                        for (var i = 0; i < items.length; i++) {


                            self._buildResultRow(jQuery("#period-results-container"), items[i], queryMetadata);

                        }



                    } else {

                        var errorMessageContainer = jQuery("<div></div>");
                        errorMessageContainer.attr("class", "warning-container");
                        errorMessageContainer.text("Unable to find a match. Try narrowing or modifying your search criteria.");

                        jQuery("#period-results-container").append(errorMessageContainer);

                    }

                    jQuery("#card-container").flickity("reloadCells");

                }).catch(function(result) {

                    spinner.stop();
                    jTarget.css("height", "auto");
                    var errorMessageContainer = jQuery("<div></div>");
                    errorMessageContainer.attr("class", "error-container");
                    errorMessageContainer.text("Invalid Inputs. Modify your search criteria and try again.");

                    jQuery("#period-results-container").append(errorMessageContainer);

                    jQuery("#card-container").flickity("reloadCells");

                });
        }


    },
    get: function() {

        return this._container;

    }

};