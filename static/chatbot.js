$(document).ready(function() {
  $("#user-input").keypress(function(event) {
    if (event.which == 13) {
      event.preventDefault();
      getBotResponse();
    }
  });

  function getBotResponse() {
    var rawText = $("#user-input").val().trim();
    if (rawText === "") {
      return;
    }

    // Create a new div element for the user message
    var userHtml = '<div class="chat-message user-message"><span>' + rawText + '</span></div>';
    $("#user-input").val("");
    $("#chatbox").append(userHtml);

    document.getElementById("user-input").scrollIntoView({block: "start", behavior: "smooth"});

    // show spinner
    $("#loading-spinner").show();

    $.get("/get", {msg: rawText}).done(function(data) {
      // Create a new div element for the chatbot message
      var botHtml = '<div class="chat-message bot-message"><span>' + data + '</span></div>';
      $("#chatbox").append(botHtml);
      document.getElementById("user-input").scrollIntoView({block: "start", behavior: "smooth"});
      // hide spinner
      $("#loading-spinner").hide();
    });
  }
});
