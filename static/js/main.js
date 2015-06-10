(function () {
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
})();