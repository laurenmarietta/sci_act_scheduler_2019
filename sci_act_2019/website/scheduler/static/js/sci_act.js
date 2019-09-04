function show_availability() {
    // Get the names of the two people
    var user_dropdown = document.getElementById("who_are_you");
    var user = user_dropdown.innerHTML;

    var attendee_dropdown = document.getElementById("who_meet_with")
	var attendee = attendee_dropdown.innerHTML;

    alert(user + attendee);

};


function update_dropdown_text(element, dropdown_id) {
    // Update dropdown menu text
    var value = element.innerHTML;
    var dropdown_button = document.getElementById(dropdown_id);
    dropdown_button.innerHTML = value;
}