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
            link = "delete-gab/" + gabId + "/";
            console.log(link);
            window.location = link;
        }
    });
}

