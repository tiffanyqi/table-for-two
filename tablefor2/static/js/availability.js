// highlights table for availability
// source: http://jsfiddle.net/few5E/


// Helper function to grab cookies, mostly for csrf
// Use like this:
// var csrftoken = getCookie('csrftoken');
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
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

var recurringAvailabilities = [];

// TODOs:
// figure out how to show these green parts again
// figure out if users drag, it should be saved too

$(function () {
  var isMouseDown = false;
  $("#availability-table-edit td")
    .mousedown(function () {
      isMouseDown = true;
      $(this).toggleClass("highlighted");

      if ($(this).hasClass("highlighted")) {
        recurringAvailabilities.push(this.id);
      } else {
        var index = recurringAvailabilities.indexOf(this.id);
        recurringAvailabilities.splice(index, 1);
      }
      console.log(recurringAvailabilities);
      return false; // prevent text selection
    })
    .mouseover(function () {
      if (isMouseDown) {
        $(this).toggleClass("highlighted");
      }
    });
  
  $(document)
    .mouseup(function () {
      isMouseDown = false;
    });
});

// i'm figuring this out
function saveRecurringAvailabilities() {
  $.ajax({
    type: 'POST',
    url: '/availability/save/',
    data: {
      'recurring_availabilities[]': recurringAvailabilities,
      'csrfmiddlewaretoken': getCookie('csrftoken')
    }
  });
}