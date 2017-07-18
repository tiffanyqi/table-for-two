// mixpanel.identify(profile.distinct_id);
mixpanel.track('Page Viewed');
// make the page name properties


// makes an AJAX request to send recurring over to django
function setDistinctId() {
  document.getElementById("id_distinct_id").value = mixpanel.get_distinct_id();
}