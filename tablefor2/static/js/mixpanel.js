// mixpanel.identify(profile.distinct_id);
mixpanel.track('Page Viewed');
// make the page name properties

// makes an AJAX request to send recurring over to django
function getDistinctId() {
  $.ajax({
    type: 'POST',
    url: '/profile/save/',
    data: {
      'distinctId': mixpanel.get_distinct_id(),
      'csrfmiddlewaretoken': getCookie('csrftoken'),
      'hi': 'hi'
    }
  });
}