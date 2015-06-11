// Redirect the user when he want to update his profile
function updateRedirection(){
    document.location.href = "update";
}

function confirmDeletion(evt){
    var $this = $(this);
    evt.preventDefault();
    swal({
        title: "Are you sure to delete your gab?",
        text: "You will not be able to recover it!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it forever!",
        cancelButtonText: "No, I miss click!",
        closeOnConfirm: false
    },
    function(isConfirm){
        if (isConfirm) {
            window.location = $this.attr("href");
        }
    });
}

function returnHome() {
    event.preventDefault();
    window.location.href="/";
}

function displayDeletionForm() {
    $('#delete-form').show();
}

function displayPart(part) {
    $(".update-part").hide();
    $(part).show();
}


/* ------- DIV INSTEAD OF THE TEXTAREA PART ----------- */

// Check if they are some text in the field (if not, disable the button)
function emptyText(max, field, button) {
    if(max - $(field).text().length == max) {
        $(button).prop('disabled', true);
    }
    else {
        $(button).prop('disabled', false);
    }
}

// Copy the text in the div and set it into an hidden field
function copyToHiddenField(field, hiddenField) {
    var $field = $(field).clone();

    $field.find("div").replaceWith(function (n) {
       return (n === 0 ? "\n" : "") + $(this).text() + "\n";
    });

    $field.find("p").replaceWith(function (n) {
       return (n === 0 ? "\n" : "") + $(this).text() + "\n";
    });

    $field.find("br").replaceWith(function () {
       return "\n";
    });

    $field.find(".userlink").replaceWith(function () {
       return "@" + $(this).data("username");
    });

    $(hiddenField).val($field.text());
}

function addHint(field, hintText, isContent) {
    if (!isContent){
        $(field).html(hintText);
        return false;
    }
    return true;
}

/**
 * Add or remove CSS class when we focus or not
 * Save the content from the div to an hidden field
 */
function valueManager(field, hint, isContent, hiddenField) {
    var hintText = "<span class=\"help-text\">" + hint + "</span>";
    isContent = addHint(field, hintText, isContent);

    $(field).focusin(function() {
        $(this).addClass("on-hover-gab");
        if(!isContent) {
            $(this).text("");
        }
    });

    $(field).focusout(function() {
        $(this).removeClass("on-hover-gab");
        var isText = $(this).text() != "";
        isContent = addHint(this, hintText, isText);

        if (!isText) {
            $(hiddenField).val("");
        }
        else {
            copyToHiddenField(field, hiddenField)
        }
    });
}

function manageBlock(form, field, content, button, max) {

    $(".count").text(max); // Add a max value

    valueManager(field, "Say something!", false, content);

    $(field).atwho({
        at: "@",
        searchKey: "username",
        callbacks: {
            remoteFilter: function (query, callback) {
                if (query === "") {
                    return [];
                }
                $.getJSON("/api/users/", {search: query},  function (data) {
                    callback(data);
                });
            }
        },
        displayTpl: "<li>${username}</li>",
        insertTpl: "<span class='label label-primary userlink' data-username='${username}'>${username}</span>"
    });

    $(field).keyup(function () {
        // decrements the count
        var preMessage = $(this).text();
        var that = this;
        var charCount = max - preMessage.length;
        $(".count").text(charCount);

        if(charCount < 0) {
            $(".count").addClass('gab-overflow');
            $(button).prop('disabled', true);
            isUnderZero = true;
        }
        else {
            if ($(".count").hasClass('gab-overflow')) {
                $(".count").removeClass('gab-overflow');
                $(button).prop('disabled', false);
            }

            var re = /\S/; // Match if they are only non-visible char
            if(re.test(preMessage) || charCount == max) {
                $(button).prop('disabled', true);
                emptyText(max, field, button);
            }
            else if ($(button).isDisabled) {
                $(button).prop('disabled', false);
            }
        }
    });

    // Send the message when we press enter
    $(field).keypress(function (e) {
        if(e.which === 13 && !e.shiftKey) {
            copyToHiddenField(field, content);
            $(form).submit();
            return false;
        }
    });
}