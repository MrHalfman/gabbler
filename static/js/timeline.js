(function () {
    var actual_page = 1,
        loading_gabs = false;

    function update() {
        if (document.hidden) {
            window.setTimeout(update, 2000);
            return;
        }

        $.get("/gabs_list/0/", function (resp) {
            if (resp) {
                var $resp = $(resp),
                    last_gabs = $resp.find(".gab"),
                    $list = $("#gabs_list");

                for (var i = 0; i < last_gabs.length; i++) {
                    var $last_gab = $(last_gabs[i]),
                        id = $(last_gabs[i]).data("id"),
                        selected_gab = $list.find(".gab[data-id='" + id + "']");
                    if (selected_gab.length < 1) {
                        $list.prepend($last_gab.parent());
                    } else {
                        selected_gab.find(".bottom-action-buttons").replaceWith($last_gab.find(".bottom-action-buttons"));
                        selected_gab.find(".dislike .badge").html($last_gab.find(".dislike .badge").html());
                    }
                }

                var actual_gabs = $list.find(".gab");
                for (var j = 0; j < actual_gabs.length; j++) {
                    var $gab = $(actual_gabs[j]);
                    if ($resp.find("[data-id='" + $gab.data("id") + "']").length < 1) {
                        $gab.remove();
                    }
                }
                bind_actions();
            }
            window.setTimeout(update, 2000);
        });
    }

    update();
    function loadMoreGabs() {
        if (loading_gabs) {
            return false;
        }
        loading_gabs = true;

        $.get("/gabs_list/" + actual_page, function (resp) {
            $("#gabs_list").append(resp);
            actual_page++;
            loading_gabs = false;
        });
    }

    $(window).scroll(function () {
        var $window = $(window),
            $document = $(document),
            px_tobottom = ($document.height() - $window.height()) - $window.scrollTop();

        if (px_tobottom < 150) {
            loadMoreGabs();
        }
    });
})();
