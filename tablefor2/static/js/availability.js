$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip({
    container : 'body'
  });
  if ($('h1').text() === 'Edit Your Recurring Availability') {
    toggleSelected();
    populateTimes();
  }

  // makes an AJAX request to send recurring over to django
  $('#availability-btn').click(function() {
    $.ajax({
      type: 'POST',
      url: '/availability/save/',
      data: {
        'recurring_availabilities[]': newAvailabilities,
        'csrfmiddlewaretoken': getCookie('csrftoken')
      }
    });
  });
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

// executes highlighting, http://jsfiddle.net/few5E/
function toggleSelected() {
  var isMouseDown = false;
  $("#availability-table-edit td")
    .mousedown(function () {
      isMouseDown = true;
      $(this).toggleClass("highlighted");
      distinguishHighlighted(this);
      return false; // prevent text selection
    })
    .mouseover(function () {
      if (isMouseDown) {
        $(this).toggleClass("highlighted");
        distinguishHighlighted(this);
      }
    });

  $(document)
    .mouseup(function () {
      isMouseDown = false;
    });
}

// adds or removes highlighting from list
function distinguishHighlighted(element) {
  if ($(element).hasClass("highlighted")) {
    newAvailabilities.push(element.id);

  } else {
    newAvailabilities.push(element.id + '-deleted');
  }
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
