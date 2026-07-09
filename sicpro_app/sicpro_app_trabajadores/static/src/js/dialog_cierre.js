Dialog.confirm(self, "TEXT", {
    title: _t("TITLE"),
    confirm_callback: function(){
        console.log("Click confirm");
    },
    cancel_callback:function(){
        console.log("Click cancel")
    }
});