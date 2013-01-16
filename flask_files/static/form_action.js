// experimenting with javascript!

var form = document.forms.action_form;
var action_field = form.elements.action;
form.elements.send.onclick = function() {
    var action = action_field.value;
    if (action) {
        var response_tag = document.createElement("p");
        var response_text = document.createTextNode(action);
        response_tag.appendChild(response_text);
        document.body.appendChild(response_tag);
    }
    else {
        alert("You must enter an action.");
    }
};

// console.log(document.body.innerHTML);



