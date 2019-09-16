function Card(cardID) {

    this._cardObj = jQuery("<div></div>");
    this._cardObj.attr("class", "card");
    this._cardObj.attr("id", cardID);

    this._cardHeaderContainer = jQuery("<div></div>");
    this._cardHeaderContainer.attr("class", "card-header-container");

    this._cardBodyContainer = jQuery("<div></div>");
    this._cardBodyContainer.attr("class", "card-body-container");

    this._cardFooterContainer = jQuery("<div></div>");
    this._cardFooterContainer.attr("class", "card-footer-container");

    this._cardObj.append(this._cardHeaderContainer);
    this._cardObj.append(this._cardBodyContainer);
    this._cardObj.append(this._cardFooterContainer);

}

Card.prototype = {

    appendBody: function(obj) {

        this._cardBodyContainer.append(obj);

    },
    appendFooter: function(obj) {

        this._cardFooterContainer.append(obj);

    },
    appendHeader: function(obj) {

        this._cardHeaderContainer.append(obj);

    },
    get: function() {

        return this._cardObj;

    }

};

function CardFooterBtn(id, iconClass, btnText) {

    this._btnContainer = jQuery("<div></div>");
    this._btnContainer.attr("id", id);
    this._btnContainer.attr("class", "card-footer-btn-container");

    this._btnIcon = jQuery("<span></span>");
    this._btnIcon.attr("class", iconClass + " card-footer-btn-icon");

    this._btnText = jQuery("<span></span>");
    this._btnText.attr("class", "card-footer-btn-text");
    this._btnText.text(btnText);

    this._btnContainer.append(this._btnIcon);
    this._btnContainer.append(this._btnText);

}

CardFooterBtn.prototype = {

    get: function() {

        return this._btnContainer;

    }

};