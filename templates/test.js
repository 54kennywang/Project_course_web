function warn(){
	alert('fired');
};


// function hide(id)
// {
// 	alert(id);
// 	$(id).hide();
// }

$(document).ready(function() {
    alert('#haha');
	$('#haha').hide();
});




// var inputs = $("form#myForm input, form#myForm textarea");

// var validateInputs = function validateInputs(inputs) {
//   var validForm = true;
//   inputs.each(function(index) {
//     var input = $(this);
//     if (!input.val() || (input.type === "radio" && !input.is(':checked'))) {
//       $("#subnewtide").attr("disabled", "disabled");
//       validForm = false;
//     }
//   });
//   return validForm;
// }
// inputs.change(function() {
//   if (validateInputs(inputs)) {
//     $("#subnewtide").removeAttr("disabled");
//   }
// });

// var inputs = $("form#login_form input, form#login_form textarea");
var inputs = $("form#login_form input");
var validateInputs = function validateInputs(inputs) {
  var validForm = true;
  inputs.each(function(index) {
    var input = $(this);
    if (!input.val() || (input.type === "radio" && !input.is(':checked'))) {
      $("#login_submit").attr("disabled", "disabled");
      validForm = false;
    }
  });
  return validForm;
}
inputs.change(function() {
  if (validateInputs(inputs)) {
    $("#login_submit").removeAttr("disabled");
  }
});