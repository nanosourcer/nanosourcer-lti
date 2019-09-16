function Navbar(containerID, userInfo, searchTypes) {

    this._userFirstName = userInfo['firstName'];
    this._userLastName = userInfo['lastName'];
    this._userSISID = userInfo['sisID'];
    this._courseSearchTypes = searchTypes;
    this._currentIndex = 0;

    this._containerObj = jQuery("<div></div>");
    this._containerObj.attr("id", containerID);
    this._containerObj.attr("class", "navbar-container");

    this._buildNavbarHeader();
    this._buildNavbarMenu();

}

Navbar.prototype = {

    _buildNavbarMenuItem: function (key, text) {

        var container = jQuery("<div></div>");
        container.attr("id", "menu-item-container-" + key);
        container.attr("class", "navbar-menu-item-container");

        var item = jQuery("<span></span>");
        item.attr("id", "menu-item-" + key);
        item.attr("class", "navbar-menu-item");
        item.text(text);

        var indicator = jQuery("<div></div>");
        indicator.attr("id", "menu-item-indicator-" + key);
        indicator.attr("class", "navbar-menu-item-indicator");

        container.append(item);
        container.append(indicator);

        return container;

    },
    _buildNavbarHeader: function () {

        var navbarHeaderContainer = jQuery("<div></div>");
        navbarHeaderContainer.attr("id", "navbar-header-container");
        navbarHeaderContainer.attr("class", "navbar-header-container");

        var titleText = jQuery("<span></span>");
        titleText.attr("id", "navbar-header-title-text");
        titleText.attr("class", "navbar-header-title-text");
        titleText.text("Nanosourcer");

        navbarHeaderContainer.append(titleText);

        this._containerObj.append(navbarHeaderContainer);

    },
    _buildNavbarMenu: function() {

        var self = this;

        var menuContainer = jQuery("<div></div>");
        menuContainer.attr("id", "navbar-menu-container");
        menuContainer.attr("class", "navbar-menu-container");

        var menu = jQuery("<div></div>");
        menu.attr("id", "navbar-menu");
        menu.attr("class", "navbar-menu");

        var information = self._buildNavbarMenuItem("information", "Information");
        menu.append(information);
        var imageViewer = self._buildNavbarMenuItem("image-viewer", "Image Viewer");
        menu.append(imageViewer);

        jQuery.each(self._courseSearchTypes, function() {

            var searchType = self._buildNavbarMenuItem(this['type_name'], this['type_name'] + " Search");
            menu.append(searchType);

        });

        menuContainer.append(menu);

        this._containerObj.append(menuContainer);

    },
    get: function() {
        return this._containerObj;
    },
    currentIndex: function() {

        return this._currentIndex;

    },
    build: function() {

        var containers = jQuery(".navbar-menu-item-container");

        var numOfContainers = containers.length;

        widthValue = 100.0 / numOfContainers;

        containers.each(function() {

            jQuery(this).css("width", widthValue + "%")
                .css("min-width", "200px");

        });

        var draggableThreshold = 10;

        if ((numOfContainers * 200) < jQuery(window).width()) {

            draggableThreshold = 1000;

        }

        this._flickityMenu = new Flickity(".navbar-menu", {

            accessibility: true,
            adaptiveHeight: true,
            autoPlay: false,
            cellAlign: "left",
            cellSelector: ".navbar-menu-item-container",
            contain: true,
            draggable: true,
            dragThreshold: draggableThreshold,
            freeScroll: false,
            friction: 0.3,
            selectedAttraction: 0.05,
            groupCells: false,
            initialIndex: 0,
            lazyLoad: false,
            percentagePosition: true,
            prevNextButtons: false,
            pageDots: false,
            resize: false,
            rightToLeft: false,
            setGallerySize: false,
            watchCSS: false,
            wrapAround: false,
            asNavFor: "#card-container"

        });

        var self = this;

        this._flickityMenu.on("staticClick", function(event, pointer, cellElement, cellIndex) {

            self._currentIndex = cellIndex;

            self._flickityMenu.select(self._currentIndex);

        });

    }

};