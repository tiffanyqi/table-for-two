if (document.getElementById("distinct-id")) {
    var distinctId = document.getElementById("distinct-id").value;
    if (distinctId) {
        mixpanel.identify(distinctId);
    }
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

// reset mixpanel distinct_id
function reset() {
  mixpanel.reset();
}