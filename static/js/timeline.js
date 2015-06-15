
function update() {
    if (document.hidden) {
        window.setTimeout(update, 2000);
        return;
    }

    $.get("/gabs_list/0/", function (resp) {
        if (resp) {
            var last_gabs = $(resp).find(".gab"),
                $list = $("#gabs_list");

            for (var i = 0; i < last_gabs.length; i++) {
                var $last_gab = $(last_gabs[i]),
                    id = $(last_gabs[i]).data("id");
                if ($list.find(".gab[data-id='" + id + "']").length < 1) {
                    $list.prepend($last_gab.parent());
                }
            }
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
