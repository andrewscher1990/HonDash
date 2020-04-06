var setup = undefined;
var ws = new WebSocket("ws://127.0.0.1:5678/");

ws.onmessage = function(event) {
  var data = JSON.parse(event.data);
  var keys = Object.keys(data);

  // if the setup has not been received
  if (setup === undefined) {
    if (keys[0] == "setup") {
      setup = data["setup"];
      for (var value in setup) {
        for (var option in setup[value]) {
          var method = "set" + option.charAt(0).toUpperCase() + option.slice(1);
          try {
            window[setup[value]["tag"]][method](setup[value][option]);
          } catch (e) {
            // probably it´s not a field for setting up something in the frontend so we can skip it
          }
        }
      }
    }
  } else {
    if (keys[0] == "data") {
      for (var key in data["data"]) {
        // for all values
        try {
          // if it's associated to a frontend tag
          window[setup[key]["tag"]]["refresh"](data["data"][key]);
        } catch (e) {}
      }
    }
  }g
};

// asks for the setup as soon as possible
ws.onopen = function(e) {
  ws.send(JSON.stringify({ action: "setup" }));
};
