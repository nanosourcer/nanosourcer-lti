function MetadataItem(metadata) {

    this._metadataItemContainer = jQuery("<div></div>");
    this._metadataItemContainer.attr("class", "metadata-item-container");

    if (this._metadataObj === null) {

        var noSelectionMessage = jQuery("<div></div>");
        noSelectionMessage.attr("class", "metadata-item-message");
        noSelectionMessage.text("Nothing Selected");
        this._metadataItemContainer.append(noSelectionMessage);

    } else {

        this._buildLabelRow(metadata['label']);
        this._buildSecondaryLabeRow(metadata['secondaryLabel']);
        this._buildSpatialLabeRow(metadata['spatialLabel']);
        this._buildGPSCoordinatesRow(metadata['lat'], metadata['long']);
        this._buildDataRow(metadata['dateMax'], metadata['dateMin']);
        this._buildGazetteerURIRow(metadata['gazetteerURI']);

    }

}

MetadataItem.prototype = {

    _appendDateSuffix: function(date) {

        if (date <= -1) {

            return Math.abs(date) + " BCE"

        } else {

            return date + " CE"

        }

    },
    _buildGazetteerURIRow: function(gazetteerURI) {

        if (this._checkForValue(gazetteerURI)) {

            var rowContainer = jQuery("<div></div>");
            rowContainer.attr("class", "metadata-item-row");

            var linkGlyphicon = jQuery("<span></span>");
            linkGlyphicon.attr("class", "glyphicon glyphicon-link metadata-item-row-icon");

            var rowText = jQuery("<span></span>");
            rowText.attr("class", "metadata-item-row-text");
            rowText.text(gazetteerURI);

            rowContainer.append(linkGlyphicon);
            rowContainer.append(rowText);

            this._metadataItemContainer.append(rowContainer);

        }

    },
    _buildDataRow: function(dateMax, dateMin) {

        var rowContainer = jQuery("<div></div>");
        rowContainer.attr("class", "metadata-item-row");

        var calendarGlyphicon = jQuery("<span></span>");
        calendarGlyphicon.attr("class", "glyphicon glyphicon-calendar metadata-item-row-icon");

        var rowText = jQuery("<span></span>");
        rowText.attr("class", "metadata-item-row-text");

        var dateText = this._buildDateText(dateMax, dateMin);

        rowText.text(dateText);

        rowContainer.append(calendarGlyphicon);
        rowContainer.append(rowText);

        this._metadataItemContainer.append(rowContainer);

    },
    _buildDateText: function(max, min) {


        if (this._checkForValue(max) && this._checkForValue(min)) {

            return this._appendDateSuffix(min) + " - " + this._appendDateSuffix(max);

        } else {

            if (this._checkForValue(max)) {

                return "< " + this._appendDateSuffix(max);

            } else {

                return "> " + this._appendDateSuffix(min);

            }

        }


    },
    _buildGPSCoordinatesRow: function(lat, long) {

        if (this._checkForValue(lat) && this._checkForValue(long)) {

            var rowContainer = jQuery("<div></div>");
            rowContainer.attr("class", "metadata-item-row");

            var mapMarkGlyphicon = jQuery("<span></span>");
            mapMarkGlyphicon.attr("class", "glyphicon glyphicon-map-marker metadata-item-row-icon");

            var rowText = jQuery("<span></span>");
            rowText.attr("class", "metadata-item-row-text");

            var gpsCoordinateText = lat + ", " + long;

            rowText.text(gpsCoordinateText);

            rowContainer.append(mapMarkGlyphicon);
            rowContainer.append(rowText);

            this._metadataItemContainer.append(rowContainer);

        }
        
    },
    _buildLabelRow: function(label) {

        if (this._checkForValue(label)) {

            var rowContainer = jQuery("<div></div>");
            rowContainer.attr("class", "metadata-item-row");

            var rowText = jQuery("<span></span>");
            rowText.attr("class", "metadata-item-row-text");
            rowText.text(label);

            rowContainer.append(rowText);

            this._metadataItemContainer.append(rowContainer);

        }

    },
    _buildSecondaryLabeRow: function(secondaryLabel) {

        if (this._checkForValue(secondaryLabel)) {

            var rowContainer = jQuery("<div></div>");
            rowContainer.attr("class", "metadata-item-row");

            var rowText = jQuery("<span></span>");
            rowText.attr("class", "metadata-item-row-text");
            rowText.text(secondaryLabel);

            rowContainer.append(rowText);

            this._metadataItemContainer.append(rowContainer);

        }

    },
    _buildSpatialLabeRow: function(spaitalLabel) {

        if (this._checkForValue(spaitalLabel)) {

            var rowContainer = jQuery("<div></div>");
            rowContainer.attr("class", "metadata-item-row");

            var globeGlyphicon = jQuery("<span></span>");
            globeGlyphicon.attr("class", "glyphicon glyphicon-globe metadata-item-row-icon");

            var rowText = jQuery("<span></span>");
            rowText.attr("class", "metadata-item-row-text");
            rowText.text(spaitalLabel);

            rowContainer.append(globeGlyphicon);
            rowContainer.append(rowText);

            this._metadataItemContainer.append(rowContainer);

        }

    },
    _checkForValue: function(value) {

        if (value!== null || value !== undefined || value !== "None") {

            return true;

        } else {

            return false;

        }

    },
    get: function() {

       return this._metadataItemContainer;

   }

};