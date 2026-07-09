/** @odoo-module **/

import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';


var SystrayFullscreenMenu = Widget.extend({
    name: 'fullscreen_menu',
    template: 'odoo_fullscreen.systray.SystrayFullscreenMenu',
    events: {
        'click .o_fullscreen_toggle': '_onFullScreenToggle',
    },

    /**
     * @override
     */
    destroy: function () {
        // Remove the Listener before destroy the widget
        document.removeEventListener("fullscreenchange", this._onKeyEscCompressScreen, false);
        this._super();
    },

    /**
     * Open the browser in fullscreen mode
     * @param event
     */
    openFullscreen: function (event) {
        /* Get the documentElement (<html>) to display the page in fullscreen */
        let elem =  document.documentElement;
        /* Browser compatibility */
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.mozRequestFullScreen) {
            /* Firefox */
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) {
            /* Chrome, Safari & Opera */
            elem.webkitRequestFullscreen();
        } else if (elem.msRequestFullscreen) {
            /* IE/Edge */
            elem.msRequestFullscreen();
        }

        /* Listener that manage fullscreen change and set the proper icon when ESC is pressed */
        document.addEventListener("fullscreenchange", this._onKeyEscCompressScreen, false);
    },

    /**
     * Close the fullscreen mode
     * @param event
     */
    closeFullscreen: function (event) {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
    },

    //------------------------------------------------------------
    // Private
    //------------------------------------------------------------

    /**
     * Event listner.
     * If fullscreenElement is null (so it's disabled) this method set the
     * correct visibility for action buttons
     * @param ev
     * @private
     */
    _onKeyEscCompressScreen: function (ev) {
        if (document.fullscreenElement === null) {
            $('.expand_screen_action').removeClass('o_hide_fullscreen_action');
            $('.compress_screen_action').addClass('o_hide_fullscreen_action');
            document.removeEventListener("fullscreenchange", this._onKeyEscCompressScreen, false);
        }
    },

    //------------------------------------------------------------
    // Handlers
    //------------------------------------------------------------

    /**
     * Click Handler that manage fullscreen toggle action from systray menu
     * @param {*} event
     */
     _onFullScreenToggle: function (event) {
        var self = this;
        var $clickedBtn = $(event.currentTarget);
        if ($clickedBtn.hasClass('expand_screen_action')) {
            self.openFullscreen();
            $('.compress_screen_action').removeClass('o_hide_fullscreen_action');
            $clickedBtn.addClass('o_hide_fullscreen_action');
        } else if ($clickedBtn.hasClass('compress_screen_action')) {
            self.closeFullscreen();
        }
    },
});

// Set it to the right
SystrayFullscreenMenu.prototype.sequence = 30;

SystrayMenu.Items.push(SystrayFullscreenMenu);

export default SystrayFullscreenMenu;
