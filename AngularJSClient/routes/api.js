var express = require('express');
var router = express.Router();
var http = require("http");

function getJson(options, onSuccess, onError){
  var req = http.request(options, function(res)
  {
      var output = '';
      res.setEncoding('utf8');

      res.on('data', function (chunk) {
          output += chunk;
      });

      res.on('end', function() {
          var obj = JSON.parse(output);
          onSuccess(obj);
      });
  });

  req.on('error', function(err) {
    onError({'error': err.message});
  });

  req.end();
}


/* GET home page. */
router.get('/', function(req, res, next) {
  res.send('API Ducumentation');
});

router.get('/*?', function(req, res, next) {
    var options = {
      host: 'localhost',
      port: 8001,
      path: escape('/api/' + req.params[0]),
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    };

    getJson(options, function(data){
      res.send(data);
    }, function(err){
      res.send(err);
    });

});

module.exports = router;
