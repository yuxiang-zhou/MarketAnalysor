var host = 'http://localhost:8001/';

angular.module('servData', []).factory(
  'getList', ['$http',
  function($http) {
    return function(indices, onSuccess){
      var query = host + 'api/list/' + indices;
      $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getHistoryStock', ['$http',
  function($http) {
    return function(symbol, onSuccess){
      var query = host + 'api/history/stock/' + symbol;
      $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getHistorySector', ['$http',
  function($http) {
    return function(sector, onSuccess){
      var query = host + 'api/history/sector/' + sector;
      $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getDetail', ['$http',
  function($http) {
    return function(symbol, onSuccess){
      var query = host + 'api/detail/' + symbol;
      $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
);
