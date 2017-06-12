function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// toggles the time available slot
function editAvailability(availabilityId) {
    var availabilityBtnCancel = document.getElementById('btn-cancel-' + availabilityId);
    var availabilityBtnEdit = document.getElementById('btn-edit-' + availabilityId);
    var availabilityBtnDelete = document.getElementById('btn-delete-' + availabilityId);
    var availabilityForm = document.getElementById('form-edit-' + availabilityId);
    if (availabilityForm.style.display === 'none' || !availabilityForm.style.display) {
        availabilityForm.style.display = 'block';
        availabilityBtnCancel.style.display = 'inline';
        availabilityBtnDelete.style.display = 'none';
        availabilityBtnEdit.style.display = 'none';
    } else {
        availabilityForm.style.display = 'none';
        availabilityBtnCancel.style.display = 'none';
        availabilityBtnDelete.style.display = 'inline';
        availabilityBtnEdit.style.display = 'inline';
    }

}

function confirmEditAvailability() {

}

// deletes the availability but first prompts the user
function deleteAvailability(availabilityId) {
    // doesn't work
    if (confirm('Are you sure you want to delete this availability?')) {
        $.ajax({
            url: "/availability/delete/%s" % (availabilityId),
            type: "POST",
            data: {
                'availability_id': availabilityId,
                'csrfmiddlewaretoken': getCookie('csrftoken')
            },
            success: function(response){
                alert('Availability deleted!');
            },
            error: function(response){
                alert('error; '+ eval(error));
            }
        });

    } else {
        alert('Ok, availability not deleted.');
    }
    return false;
}