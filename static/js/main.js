(function () {
    var actual_page = 1,
        loading_gabs = false;

    $.material.init();

    $(".like").on("click", function () {
        var id = $(this).data('id'),
            $this = $(this);
        $.getJSON("/like/" + id, function (data) {
           if (data.success) {
               $this.find(".badge").html(data.likes);
               $this.parent().find(".dislike .badge").html(data.dislikes);
               if (data.liking) {
                   $this.parent().find(".dislike").removeClass("btn-danger");
                   $this.removeClass("btn-material-grey-100");
                   $this.addClass("btn-success");
               } else {
                   $this.removeClass("btn-success");
                   $this.addClass("btn-material-grey-100");
               }
           }
        });
    });

    $(".dislike").on("click", function () {
        var id = $(this).data('id'),
            $this = $(this);
        $.getJSON("/dislike/" + id, function (data) {
           if (data.success) {
               $this.find(".badge").html(data.dislikes);
               $this.parent().find(".like .badge").html(data.likes);
               if (data.disliking) {
                   $this.parent().find(".like").removeClass("btn-success");
                   $this.removeClass("btn-material-grey-100");
                   $this.addClass("btn-danger");
               } else {
                   $this.removeClass("btn-danger");
                   $this.addClass("btn-material-grey-100");
               }
           }
        });
    });

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

})();