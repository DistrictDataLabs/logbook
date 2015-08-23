/*
 * main.js
 * Main javascript function that should be run first thing in the Logbook App.
 *
 * Author:  Benjamin Bengfort <bbengfort@districtdatalabs.com>
 * Created: Sun Aug 23 09:58:00 2015 -0500
 *
 * Dependencies:
 *  - jquery
 *  - underscore
 */

(function() {

  // Do the CSRf AJAX Modification
  var csrfToken   = $('input[name="csrfmiddlewaretoken"]').val();
  $.ajaxSetup({headers: {"X-CSRFToken": csrfToken}});

  console.log("Logbook App is started and ready");

})();
