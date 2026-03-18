var fs = require("fs");
var http = require('http');
var fichier = "/home/pi/Station_meteo/Mesures_temperatures/mesure.txt";

var server = http.createServer(function (request, response) {
  // Read the file asynchronously on every incoming request for live data
  fs.readFile(fichier, "utf8", function(err, data) {
    if (err) {
      response.writeHead(500, {"Content-Type": "text/plain"});
      response.end("500 Internal Server Error: Cannot read telemetry file.");
      return;
    }
    
    // Force inline display in the browser and define character encoding
    response.writeHead(200, {
        "Content-Type": "text/plain; charset=utf-8",
        "Content-Disposition": "inline",
        "Cache-Control": "no-store, no-cache, must-revalidate",
        "Pragma": "no-cache",
        "X-Content-Type-Options": "nosniff"
    });
    response.end(data);
  });
});

// Listen on port 9000
server.listen(9000);
console.log("Telemetry raw data server running on port 9000");
