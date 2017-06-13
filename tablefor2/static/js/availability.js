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
    var availabilityEdits = document.getElementsByClassName("availability-edit " + availabilityId);
    var availabilityViews = document.getElementsByClassName("availability-view " + availabilityId);
    var availabilityForm = document.getElementById('form-edit-' + availabilityId);

    // if "edit" was pressed, show form
    if (availabilityForm.style.display === 'none' || !availabilityForm.style.display) {
        availabilityForm.style.display = 'table-cell';
        for (var i=0; i < availabilityEdits.length; i++) {
            availabilityEdits[i].style.display = 'table-cell';
            availabilityViews[i].style.display = 'none';
        }
    // if cancelled, hide form
    } else {
        availabilityForm.style.display = 'none';
        for (var j=0; j < availabilityEdits.length; j++) {
            availabilityEdits[j].style.display = 'none';
            availabilityViews[j].style.display = 'table-cell';
        }
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