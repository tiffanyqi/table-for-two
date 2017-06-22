// highlights table for availability
// source: http://jsfiddle.net/few5E/
$(function () {
  var isMouseDown = false;
  $("#availability-table-edit td")
    .mousedown(function () {
      isMouseDown = true;
      console.log(this);
      $(this).toggleClass("highlighted");
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