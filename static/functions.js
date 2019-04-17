

// $(document).ready(function() {
// 	alert('yesssssssssssssss');
// });

function request_success(){
	alert("Remark submitted!");
};

function change_success(){
	alert("Change committed!");
};

function feedback_success(){
	alert("Feedback sent!");
};

function reply_success(){
	alert("Feedback replied!");
};

function warn(){
	alert('fired');
};

function display(id){
	var x = document.getElementById(id);
	x.style.display = 'block';
};

function hide(id)
{
	$(id).hide();
}

$(document).ready(function() {
	$('#new_requests').hide();
	$('#all_requests').hide();
	$('#student_request').hide();
	$('#request_history').hide();
	$('#feedback_history').hide();
	$('#my_new_feedback').hide();
	$('#feedback_reply').hide();
	$('#reply_from_prof').hide();
	$('#all_feedback').hide();
});



// https://stackoverflow.com/questions/31762447/force-user-to-fill-all-fields-before-enabling-form-submit
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
