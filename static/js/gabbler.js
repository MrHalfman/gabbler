// Redirect the user when he want to update his profile
function updateRedirection(){
    document.location.href = "update";
}

function confirmDeletion(gabId){
    event.preventDefault();
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
            link = "delete_gab/" + gabId + "/";
            console.log(link);
            window.location = link;
        }
    });
}

function returnHome() {
    window.location.href="/"
}

function displayDeletionForm() {
    $('#delete-form').show();
}

function displayPart(part) {
    $(".update-part").hide();
    $(part).show();
}