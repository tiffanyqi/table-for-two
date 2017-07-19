if ($('h1').text() == 'Welcome to Table for Two!') {
  mixpanel.reset();
} else if ($('h1').text() == 'Table for Two Dashboard') {
  var distinctId = document.getElementById("distinct-id").value;
  mixpanel.identify(distinctId);
}
setTimeout(function() {
  mixpanel.track('Page Viewed', {
    'Page': $('h1').text()
  });
}, 1000);

// set the distinct_id to save in back-end
function setProperties() {
  document.getElementById("id_distinct_id").value = mixpanel.get_distinct_id();
}