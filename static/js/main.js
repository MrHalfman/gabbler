(function () {

    $.material.init();



    $("#notifications_dropdown").on("click", function () {
        $.getJSON("/notifications_read/", function (data) {
           if (data.success) {
               $("#notifications_dropdown").find(".badge").html(0);
               $(".notification-item.unread").removeClass("unread");
           }
        });
    });

    $("#search").on("keydown", function (evt) {
        if (evt.keyCode === 13 && this.value.length >= 2) {
            window.location = "/search/" + this.value;
        }
    });

    $(".regab").on("click", function () {
        var id = $(this).parents(".gab").data('id'),
            $this = $(this);
        $.getJSON("/regab/" + id, function (data) {
           if (data.success) {
               $this.find(".badge").html(data.regabs);
               if (data.regabbed) {
                   $this.removeClass("btn-material-grey-100");
                   $this.addClass("btn-info");
               } else {
                   $this.addClass("btn-material-grey-100");
                   $this.removeClass("btn-info");
               }
           }
        });
    });

    bind_actions();
})();