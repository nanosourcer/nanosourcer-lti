function MapWidget(mapWidgetID, courseConfig) {

    this._showCoordinateMarkers = false;

    this._mapWidgetID = mapWidgetID;
    this._courseConfig = courseConfig;
    this._mapWidget = jQuery("<div></div>");
    this._mapWidget.attr("id", mapWidgetID);

    this._mapObj = null;
    this._coordinatesWindow = null;

    this._bbox_nw_lat = null;
    this._bbox_nw_lng = null;
    this._bbox_se_lat = null;
    this._bbox_se_lng = null;

    this._markerFeatureGroup = L.featureGroup();

    this._bboxParam = null;
    this._keywordParam = null;

    this._glsClient = apigClientFactory.newClient({

        apiKey: courseConfig['gazetteer_api_key']

    });

    this._glsParams = {

        "gazetteer-id": 1

    };
    this._glsBody = {};
    this._glsAdditionalParams = {
        queryParams: {}
    };

}

MapWidget.prototype = {

    _addMarkersToMap: function(markerList, queryMetadata) {

        this._mapObj.removeLayer(this._markerFeatureGroup);

        var features = [];

        if (jQuery(window).width() > 1315) {

            var maxWidth = 200;

        } else {

            var maxWidth = 350;

        }

        for (var i = 0; i < markerList.length; i++) {

            var latLng = new L.latLng(markerList[i]['lat'], markerList[i]['long']);

            var circle = new L.circle(latLng, 1500, {

                color: 'red',
                fillColor: 'red',
                fillOpacity: 1.0,
                className: "leaflet-clickable " + "place-" + i

            }).bindPopup(this._buildPopup(markerList[i], i, queryMetadata)[0],{

                maxWidth: maxWidth

            });



            features.push(circle);

        }

        this._markerFeatureGroup = new L.featureGroup(features).addTo(this._mapObj);

    },
    _addResultRows: function(markerList, queryMetadata) {

        var container = jQuery("#map-results-container");

        container.empty();

        for (var i = 0; i < markerList.length; i++) {

            var row = this._buildResultRow(markerList[i], i, queryMetadata);
            container.append(row);

        }

    },
    _buildResultRow: function(data, number, queryMetadata) {


        var markerContainer = jQuery("<div></div>");
        markerContainer.attr("class", "metadata-row col-lg-1 col-md-1 col-sm-1 col-xs-1");

        var markerBox = jQuery("<div></div>");
        markerBox.attr("class", "marker-box-place");

        var markerRing = jQuery("<div></div>");
        markerRing.attr("class", "matadata-row-marker-place");
        markerRing.attr("name", "place-" + number);

        var markerDot = jQuery("<div></div>");
        markerDot.attr("class", "metadata-row-marker-dot-place");

        markerRing.append(markerDot);

        markerRing.click(function() {

            jQuery(".active-meta-marker-place").each(function() {

                jQuery(this).attr("class", "matadata-row-marker-place");

            });

            jQuery(this).attr("class", "matadata-row-marker-place active-meta-marker-place");

            jQuery("path").attr("stroke", "red").attr("fill", "red");

            var selected = jQuery(".place-" + number).attr("fill", "green").attr("stroke", "green");

            if (jQuery(".leaflet-popup-close-button").length > 0) {

                jQuery(".leaflet-popup-close-button")[0].click();

            }
            
            userData['placeSelection'] = data;
            userData['placeQueryMetadata'] = queryMetadata;

            jQuery("#status-bar-message-Place").text(data['label']);

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
        return metadataRowContainer;


    },
    _buildPopup: function(data, number, queryMetadata) {

        var container = jQuery("<div></div>");
        container.attr("class", "popup-container");

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

        var locationContainer = jQuery("<div></div>");
        locationContainer.attr("class", "col-lg-6 col-md-6 col-sm-6 col-xs-6");

        var locationIcon = jQuery("<span></span>")
            .attr("class", "glyphicon glyphicon-map-marker");

        var locationText = jQuery("<span></span>")
            .attr("class", "popup-metadata-text")
            .text(data['lat'] + ', ' + data['long']);

        locationContainer.append(locationIcon, locationText);

        var dateContainer = jQuery("<div></div>");
        dateContainer.attr("class", "col-lg-6 col-md-6 col-sm-6 col-xs-6");

        var dateIcon = jQuery("<span></span>")
            .attr("class", "glyphicon glyphicon-calendar");

        var dateText = jQuery("<span></span>")
            .attr("class", "popup-metadata-text")
            .text(this._convertDate(data['dateMin']) + ' - ' + this._convertDate(data['dateMax']));

        dateContainer.append(dateIcon, dateText);

        otherInfoContainer.append(spatialLabelContainer, locationContainer, dateContainer);

        var buttonRow = jQuery("<div></div>");
        buttonRow.attr("class", "row");
        buttonRow.css("margin-top", "10px");

        var buttonContainer = jQuery("<div></div>");
        buttonContainer.attr("class", "col-lg-12 col-md-12 col-sm-12 col-xs-12");
        buttonContainer.css("text-align", "center");

        var selectBtn = jQuery("<button></button>");
        selectBtn.attr("class", "btn btn-default");
        selectBtn.text("Select this URI");
        selectBtn.click(function() {

            jQuery("#map-results-container").scrollTop(0);

            userData['placeSelection'] = data;
            userData['placeQueryMetadata'] = queryMetadata;
            userData['isSelection'] = true;

            jQuery("#status-bar-message-Place").text(data['label']);

            jQuery(".active-meta-marker-place").each(function() {

                jQuery(this).attr("class", "matadata-row-marker-place");

            });

            var selector = 'place-' + number;

            var row = jQuery('[name="' + selector + '"]');
            row.attr("class", "matadata-row-marker-place active-meta-marker-place");

            jQuery("path").attr("stroke", "red").attr("fill", "red");
            jQuery(".place-" + number).attr("fill", "green").attr("stroke", "green");

            var position = jQuery(jQuery(row.parent()).parent()).position();


            jQuery("#map-results-container").scrollTop(Math.abs(position['top']));

        });

        buttonContainer.append(selectBtn[0]);

        buttonRow.append(buttonContainer);

        container.append(linkContainer, description, otherInfoContainer, buttonRow);

        return container;

    },
    _clear_bbox_coordiantes: function() {

        this._bbox_nw_lat = null;
        this._bbox_nw_lng = null;
        this._bbox_se_lat = null;
        this._bbox_se_lng = null;

        this._bboxParam = null;

        if (this._showCoordinateMarkers) {

            jQuery("#north-west-coordinate").text("Undefined");
            jQuery("#south-east-coordinate").text("Undefined");

        }

    },
    _convertDate: function(value) {

        if (value < 0) {

            return Math.abs(value) + " BCE"

        } else {

            return value + " CE"

        }

    },
    _queryAPI: function(advanced) {

        var self = this;

        this._keywordParam = jQuery("#place-keyword-input").val();

        userData['placeKeyword'] = this._keywordParam;

        this._glsAdditionalParams = {
            queryParams: {}
        };

        var sufficient = false;

        if (this._keywordParam.length > 2) {

            this._glsAdditionalParams['queryParams']['query'] = this._keywordParam;
            sufficient = true;

        }

        if (this._bboxParam != null) {

            this._glsAdditionalParams['queryParams']['bbox'] = this._bboxParam;
            sufficient = true;

        }

        if (advanced) {

            this._glsAdditionalParams['queryParams']['advanced'] = "true";

        }

        if (sufficient) {

            var target = document.getElementById("map-results-container");
            var jTarget = jQuery("#map-results-container");
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

            if (jQuery(window).width() > 1315) {

                jTarget.css("height", "451px");

            } else {

                jTarget.css("height", "200px");

            }


            this._glsClient.gazetteersGazetteerIdSearchGet(this._glsParams, this._glsBody, this._glsAdditionalParams)
                .then(function (result) {

                    var items = result['data']['response']['items'];
                    var queryMetadata = result['data']['response']['queryMetadata'];

                    spinner.stop();

                    self._addMarkersToMap(items, queryMetadata);
                    self._addResultRows(items, queryMetadata);

                    jTarget.css("height", "auto");
                    jQuery("#card-container").flickity("reloadCells");

                }).catch(function(result) {

                    spinner.stop();
                    jTarget.css("height", "auto");
                    var errorMessageContainer = jQuery("<div></div>");
                    errorMessageContainer.attr("class", "error-container");
                    errorMessageContainer.text("Too many results. Try narrowing your search criteria.");

                    jQuery("#map-results-container").append(errorMessageContainer);

                    jQuery("#card-container").flickity("reloadCells");

                });
        }

    },
    _update_bbox_coordinates: function(bounds) {

        this._bbox_nw_lat = bounds._northEast.lat;
        this._bbox_nw_lng = bounds._southWest.lng;
        this._bbox_se_lat = bounds._southWest.lat;
        this._bbox_se_lng = bounds._northEast.lng;

        if (this._showCoordinateMarkers) {

            jQuery("#north-west-coordinate").text(parseFloat(this._bbox_nw_lat).toFixed(7) + ', ' + parseFloat(this._bbox_nw_lng).toFixed(7));
            jQuery("#south-east-coordinate").text(parseFloat(this._bbox_se_lat).toFixed(7) + ', ' + parseFloat(this._bbox_se_lng).toFixed(7));

        }

        this._bboxParam = bounds._northEast.lat + "," + bounds._southWest.lng + "," + bounds._southWest.lat + "," + bounds._northEast.lng;

        userData['bboxSelection'] = {

            northEastLat:   this._bbox_nw_lat,
            northEastLong:  this._bbox_nw_lng,
            southWestLat:   this._bbox_se_lat,
            southWestLong:   this._bbox_se_lng

        };

    },
    build: function() {

        var self = this;

        this._mapObj = L.map(this._mapWidgetID, {scrollWheelZoom: false});

        var osmUrl = this._courseConfig['mapbox_leaflet_url'];
        var osmAttrib = 'Tiles Courtesy of <a href="https://www.mapbox.com/about/maps/">© Mapbox</a> <a href="http://www.openstreetmap.org/copyright">© OpenStreetMap</a>';
        var osm = new L.TileLayer(osmUrl, {
            minZoom: 2,
            maxZoom: 12,
            attribution: osmAttrib,
            attributionControl: {compact: true},
            type: 'map',
            ext: 'svg',
            subdomains: '1'
        });

        this._mapObj.setView(

            new L.LatLng(

                this._courseConfig['start_lat'],
                this._courseConfig['start_lng']

            ),

            this._courseConfig['start_zoom']

        );

        // Add it to the map
        this._mapObj.addLayer(osm);

        var locationFilter = new L.LocationFilter();
        locationFilter.addTo(this._mapObj);

        var self = this;

        locationFilter.on("change", function() {

            self._update_bbox_coordinates(this.getBounds());

        });

        locationFilter.on("enabled", function() {

            self._update_bbox_coordinates(this.getBounds());

        });

        locationFilter.on("disabled", function() {

            self._clear_bbox_coordiantes();

        });

    },
    getContainer: function() {

        var container = jQuery("<div></div>");
        container.attr("class", "map-container col-lg-6 col-md-6 col-sm-12 col-xs-12");
        container.append(this._mapWidget);

        return container;

    },
    getResultsContainer: function() {

        var container = jQuery("<div></div>");
        container.attr("id", "map-results-container");
        container.attr("class", "map-results-container col-lg-6 col-md-6 col-sm-12 col-xs-12");

        return container;

    },
    getCoordinatesWindow: function(mapObj) {

        var self = this;

        this._windowObj = jQuery("<div></div>");
        this._windowObj.attr("class", "window-container col-lg-12 col-md-12 col-sm-12 col-xs-12");

        if (this._showCoordinateMarkers) {

            this._coordinateRowContainer = jQuery("<div></div>");
            this._coordinateRowContainer.attr("class", "row");

            var northWestContainer = jQuery("<div></div>");
            northWestContainer.attr("class", "coordinate-container col-lg-6 col-md-6 col-sm-12 col-xs-12");

            var northWestIcon = jQuery("<span></span>");
            northWestIcon.attr("class", "red-dot glyphicon glyphicon-map-marker");

            var northWestSpan = jQuery("<span></span>");
            northWestSpan.attr("id", "north-west-coordinate");
            northWestSpan.attr("class", "coordinate-text");
            northWestSpan.text("Undefined");

            northWestContainer.append(northWestIcon, northWestSpan);

            var southEastContainer = jQuery("<div></div>");
            southEastContainer.attr("class", "coordinate-container col-lg-6 col-md-6 col-sm-12 col-xs-12");

            var southEastIcon = jQuery("<span></span>");
            southEastIcon.attr("class", "green-dot glyphicon glyphicon-map-marker");

            var southEastSpan = jQuery("<span></span>");
            southEastSpan.attr("id", "south-east-coordinate");
            southEastSpan.attr("class", "coordinate-text");
            southEastSpan.text("Undefined");

            southEastContainer.append(southEastIcon, southEastSpan);

            this._coordinateRowContainer.append(
                northWestContainer,
                southEastContainer
            );

        }


        this._inputObjContainer = jQuery("<div></div>");
        this._inputObjContainer.attr("class", "row");

        var placeSearchInputContainer = jQuery("<div></div>");
        placeSearchInputContainer.attr("class", "col-lg-12 col-md-12 col-sm-12 col-xs-12");

        var placeInputGroup = jQuery("<div></div>");
        placeInputGroup.attr("class", "input-group");

        var placeInputSpanFront = jQuery("<div></div>");
        placeInputSpanFront.attr("class", "input-group-btn");

        var placeInputSpanBack = jQuery("<div></div>");
        placeInputSpanBack.attr("class", "input-group-btn");

        var placeInputSpanIcon = jQuery("<button></button>");
        placeInputSpanIcon.attr("class", "btn btn-default glyphicon glyphicon-search");
        placeInputSpanIcon.css("top", 0);

        var placeInputAdvancedSpanIcon = jQuery("<button></button>");
        placeInputAdvancedSpanIcon.attr("class", "btn btn-default");
        placeInputAdvancedSpanIcon.css("top", 0);
        placeInputAdvancedSpanIcon.css("background-color", "#BF5700 ");
        placeInputAdvancedSpanIcon.css("border-color", "#BF5700 ");
        placeInputAdvancedSpanIcon.text(" Advanced Search");

        placeInputSpanIcon.click(function() {

             self._queryAPI();

        });

        placeInputAdvancedSpanIcon.click(function() {

             self._queryAPI(advanced=true);

        });

        placeInputSpanFront.append(placeInputSpanIcon);
        placeInputSpanBack.append(placeInputAdvancedSpanIcon);

        var placeInputInput = jQuery("<input>");
        placeInputInput.attr("id", "place-keyword-input");
        placeInputInput.attr("type", "text");
        placeInputInput.attr("class", "form-control");

        placeInputInput.keyup(function(e) {

            if (e.keyCode == 13) {

                self._queryAPI();

            }

        });

        placeInputGroup.append(placeInputSpanFront, placeInputInput, placeInputSpanBack);
        placeSearchInputContainer.append(placeInputGroup);

        this._inputObjContainer.append(placeSearchInputContainer);

        this._resultContainer = jQuery("<div></div>");
        this._resultContainer.attr("class", "row");

        this._resultBody = jQuery("<div></div>");
        this._resultBody.attr("class", "col-lg-12 col-md-12 col-sm-12 col-xs-12");

        this._resultBodyMessage = jQuery("<span></span>");
        this._resultBodyMessage.attr("id", "place-result-message");
        this._resultBodyMessage.attr("class", "result-message");

        this._resultBody.append(this._resultBodyMessage);
        this._resultContainer.append(this._resultBody);

        if (this._showCoordinateMarkers) {

            this._windowObj.append(
                this._coordinateRowContainer,
                this._inputObjContainer,
                this._resultContainer
            );

        } else {

            this._windowObj.append(
                this._inputObjContainer,
                this._resultContainer
            );

        }

        return this._windowObj;

    },
    getMapObj: function() {

        return this._mapObj;

    }

};