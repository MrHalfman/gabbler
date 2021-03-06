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

function displayPart(toHide, toShow) {
    $(toHide).hide();
    $(toShow).show();
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
    var form_sending = false;
    var $count = $(".count");
    var $field = $(field);
    $count.text(max); // Add a max value

    valueManager(field, "Say something!", false, content);

    $field.atwho({
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

    $field.keyup(function () {
        // decrements the count
        var preMessage = $(this).text();
        var charCount = max - preMessage.length;
        if ($field.find("br").length > 0) {
            charCount -= $field.find("br").length * 2 - 1;
        }
        $count.text(charCount);

        if(charCount < 0) {
            $(".count").addClass('gab-overflow');
            $(button).prop('disabled', true);
        } else {
            if ($count.hasClass('gab-overflow')) {
                $count.removeClass('gab-overflow');
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
    $field.keypress(function (e) {
        if(e.which === 13 && !e.shiftKey) {
            if (form_sending) {
                return false;
            }
            copyToHiddenField(field, content);
            $(form).submit();
            form_sending = true;
            return false;
        }
    });

    $field.on('paste',function() {
        var $this = $(this);
        setTimeout(function () {
            $this.find('style meta link button img').remove();

            console.log($this.find("div"));
            $this.find("div").replaceWith(function (el) {
                return $(this).text();
            });
            console.log($this.find("div"));
            $this.find("p").replaceWith(function (el) {
                return $(this).text();
            });
            $this.find("a").replaceWith(function (el) {
                return $(this).text();
            });
        }, 100);
    });
}

function bind_actions () {
    $(".like").on("click", function () {
        var id = $(this).parents(".gab").data('id'),
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
        var id = $(this).parents(".gab").data('id'),
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
}