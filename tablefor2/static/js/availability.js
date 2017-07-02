// TODOs:
// figure out if users drag, it should be saved too

$(function () {
  toggleSelected();
  populateTimes();
});

var newAvailabilities = [];

// highlights existing recurring
function populateTimes() {
  var existing = document.getElementById("recurring-availabilities").value || [];
  if (existing != '[]') {
    var recurringAvailabilities = existing.split("', u'"); // some fiddling to remove weird format string
    for (var i=0; i < recurringAvailabilities.length; i++) {
      var rec = recurringAvailabilities[i];
      if (i === 0) {
        rec = rec.substring(3);
      }
      if (i == recurringAvailabilities.length-1) {
        rec = rec.slice(0, -2);
      }
      var recElement = document.getElementById(rec);
      $(recElement).addClass("highlighted");
      newAvailabilities.push(rec);
    }
  }
}


// makes the highlighted portions toggle, http://jsfiddle.net/few5E/
function toggleSelected() {
  var isMouseDown = false;
  $("#availability-table-edit td")
    .mousedown(function () {
      isMouseDown = true;
      $(this).toggleClass("highlighted");

      // add newly highlighted
      if ($(this).hasClass("highlighted")) {
        newAvailabilities.push(this.id);

      // remove not highlighted
      } else {
        var index = newAvailabilities.indexOf(this.id);
        newAvailabilities.splice(index, 1);
        newAvailabilities.push(this.id + '-deleted');
      }
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
}


// makes an AJAX request to send recurring over to django
function saveRecurringAvailabilities() {
  $.ajax({
    type: 'POST',
    url: '/availability/save/',
    data: {
      'recurring_availabilities[]': newAvailabilities,
      'csrfmiddlewaretoken': getCookie('csrftoken')
    }
  });
}


// Helper function to grab cookies, mostly for csrf
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