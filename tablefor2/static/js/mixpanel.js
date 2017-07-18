// mixpanel.identify(profile.distinct_id);
mixpanel.track('Page Viewed', {
  'Page': $('h1').text()
});

if ($('h1').text() == 'Welcome to Table for Two!') {
  mixpanel.reset();
}

// set the distinct_id to save in back-end
function setProperties() {
  document.getElementById("id_distinct_id").value = mixpanel.get_distinct_id();
  document.getElementById("id_initial_referrer").value = mixpanel.get_property('$initial_referrer');
  document.getElementById("id_initial_referring_domain").value = mixpanel.get_property('$initial_referring_domain');
}