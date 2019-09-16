function Container(parent) {

    this._navigationBodySection = jQuery("<div></div>");
    this._navigationBodySection.attr("class", "row");

    this._statusBodySection = jQuery("<div></div>");
    this._statusBodySection.attr("class", "row");

    this._cardBodySection = jQuery("<div></div>");
    this._cardBodySection.attr("id", "card-container");
    this._cardBodySection.attr("class", "row");

    parent.append(

        this._navigationBodySection,
        this._statusBodySection,
        this._cardBodySection

    );

}

Container.prototype = {

    appendNavigation: function(navigationObj) {

        this._navigationBodySection.append(navigationObj);

    },
    appendStatus: function(statusObj) {

        this._statusBodySection.append(statusObj);

    },
    appendCards: function(cardsObj) {

        this._cardBodySection.append(cardsObj);

    }

};