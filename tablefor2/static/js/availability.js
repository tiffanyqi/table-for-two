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

function startEditAvailability() {

}

function confirmEditAvailability() {

}

function cancelEditAvailability() {
    
}

// deletes the availability but first prompts the user
function deleteAvailability(availability_id) {
    // doesn't work
    if (confirm('Are you sure you want to delete this availability?')) {
        $.ajax({
            url: "/availability/delete/%s" % (availability_id),
            type: "POST",
            data: {
                'availability_id': availability_id,
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