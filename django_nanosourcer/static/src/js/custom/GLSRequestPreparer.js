function GLSRequestPreparer(gazetteerType, userData) {

    this._params = {};
    this._body = {};
    this._additionalParams = {
        queryParams: {}
    };

    this._sufficientQuereyParams = false;

    if (gazetteerType === "period") {

        this.addParam("gazetteer-id", 2);

        this._collectVarsForPeriodO(userData);

    }

    if (gazetteerType === "place") {

        this.addParam("gazetteer-id", 1);

        this._collectVarsForPleiades(userData);

    }

}

GLSRequestPreparer.prototype = {


    _collectVarsForPeriodO: function(userData) {

        var criteriaCount = 0;

        console.log(userData.searchResults());

        if (this._doesAttributeExist(userData.searchResults()['period']['keyword_str'])) {

            if (userData.searchResults()['period']['keyword_str'].length >= 3) {

                this.addQueryParam('query', userData.searchResults()['period']['keyword_str']);
                criteriaCount = criteriaCount + 1;

            } else {

                console.log("query error");

            }

        }

        if (this._doesAttributeExist(userData.yearMax())) {

            this.addQueryParam('dateMax', userData.yearMax());
            criteriaCount = criteriaCount + 1;

        }

        if (this._doesAttributeExist(userData.yearMin())) {

            this.addQueryParam('dateMin', userData.yearMin());
            criteriaCount = criteriaCount + 1;

        }

        if (this._doesAttributeExist(userData.searchResults()['period']['order_by'])) {

            this.addQueryParam('orderBy', userData.searchResults()['period']['order_by']);

        }

        if (criteriaCount > 0) {

            this._sufficientQuereyParams = true;

        }

    },
    _collectVarsForPleiades: function(userData) {

        var criteriaCount = 0;

        if (this._doesAttributeExist(userData.searchResults()['place']['keyword_str'])) {

            if (userData.searchResults()['place']['keyword_str'].length >= 3) {

                this.addQueryParam('query', userData.searchResults()['place']['keyword_str']);
                criteriaCount = criteriaCount + 1;

            } else {

                console.log("query error");

            }

        }

        var lat_min = this._doesAttributeExist(userData.latitudeMin());
        var lat_max = this._doesAttributeExist(userData.latitudeMax());
        var lng_min = this._doesAttributeExist(userData.longitudeMin());
        var lng_max = this._doesAttributeExist(userData.longitudeMax());

        if (lat_min && lat_max && lng_min && lng_max) {

            lat_min = new Latitude(userData.latitudeMin());
            lat_max = new Latitude(userData.latitudeMax());

            lng_min = new Longitude(userData.longitudeMin());
            lng_max = new Longitude(userData.longitudeMax());

            var bboxString = lat_min.toString() + "," + lng_min.toString() + "," + lat_max.toString() + "," + lng_max.toString();
            this.addQueryParam('bbox', bboxString);
            criteriaCount = criteriaCount + 1;

        }

        if (this._doesAttributeExist(userData.searchResults()['place']['order_by'])) {

            this.addQueryParam('orderBy', userData.searchResults()['place']['order_by']);

        }

        if (criteriaCount > 0) {

            this._sufficientQuereyParams = true;

        }

    },
    _doesAttributeExist: function(value) {

        if ((value !== undefined) && (value !== null) && (value !== "")) {

            return true;

        } else {

            return false;

        }

    },
    params: function(value) {

        if (arguments.length === 0) {

            return this._params;

        } else {

            this._params = value;

        }

    },
    addParam: function(key, value) {

        this._params[key] = value;

    },
    body: function(value) {


        if (arguments.length === 0) {

            return this._body;

        } else {

             this._body = value;

        }

    },
    additionalParams: function(value) {


        if (arguments.length === 0) {

            return this._additionalParams;

        } else {

             this._additionalParams = value;

        }

    },
    queryParams: function(value) {

        if (arguments.length === 0) {

            return this._additionalParams['queryParams'];

        } else {

             this._additionalParams['queryParams'] = value;

        }

    },
    addQueryParam: function(key, value) {

        this._additionalParams['queryParams'][key] = value;

    },
    sufficientQuereyParams: function() {

        return this._sufficientQuereyParams;

    }

};