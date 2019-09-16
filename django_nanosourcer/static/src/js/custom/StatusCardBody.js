function StatusCardBodyItem(id, metadata) {

    this._selectedMetadataItemContainer = jQuery("<div></div>");
    this._selectedMetadataItemContainer.attr("class", "selected-metadata-item-container");
    this._selectedMetadataItemContainer.attr("id", id);

    this._content = null;

    this._buildTitle(metadata['type_name']);
    this._buildMessage(metadata['type_name'], "Nothing Selected");

}

StatusCardBodyItem.prototype = {

    _buildTitle: function(searchType) {

        var title = jQuery("<span></span>");
        title.attr("class", "selected-metadata-item-title");
        title.text(searchType);

        this._selectedMetadataItemContainer.append(title);

    },
    _buildMessage: function(type, messageText) {

        var container = jQuery("<span></span>");
        container.attr("class", "selected-metadata-item-message");

        var infoIcon = jQuery("<span></span>");
        infoIcon.attr("class", "glyphicon glyphicon-info-sign");

        var space = jQuery("<span></span>");
        space.text(" ");

        var message = jQuery("<span></span>");
        message.attr("id", "status-bar-message-" + type);
        message.text(messageText);

        container.append(infoIcon);
        container.append(space);
        container.append(message);

        this._selectedMetadataItemContainer.append(container);

    },
    get: function() {

        return this._selectedMetadataItemContainer;

    },
    updateText: function(update) {


    }
};