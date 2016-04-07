angular.module('servData', []).factory(
  'getList', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(indices, onSuccess){
      var query = $rootScope.host + 'api/list/' + indices;
      $http.get(query, { cache: true }).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getHistoryStock', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(symbol, onSuccess){
      var query = $rootScope.host + 'api/history/stock/' + symbol;
      $http.get(query, { cache: true }).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getHistorySector', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(sector, onSuccess){
      var query = $rootScope.host + 'api/history/sector/' + sector;
      $http.get(query, { cache: true }).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getDetail', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(symbol, onSuccess){
      var query = $rootScope.host + 'api/detail/' + symbol;
      $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getSectorList', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(onSuccess){
      var query = $rootScope.host + 'api/sector/list/';
      $http.get(query, { cache: true }).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getNews', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(userid, onSuccess){
      var query = $rootScope.host + 'api/news/' + userid;
      $http.get(query, { cache: true }).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getFavList', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(userid, onSuccess){
      var query = $rootScope.host + 'api/favlist/' + userid;
      $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getFavNews', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(userid, onSuccess){
      var query = $rootScope.host + 'api/favnews/' + userid;
      $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getNT', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(onSuccess){
      var query = $rootScope.host + 'api/nt/';
      $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'search', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(text, onSuccess){
      var query = $rootScope.host + 'api/search/' + text;
      $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'isFav', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(username, symbol, onSuccess){
      var query = $rootScope.host + 'api/isfav/' + username + '/' + symbol;
      $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'addFav', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(username, symbol, onSuccess){
      var query = $rootScope.host + 'api/favlike/' + username + '/' + symbol;
      $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'removeFav', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(username, symbol, onSuccess){
      var query = $rootScope.host + 'api/favdislike/' + username + '/' + symbol;
      $http.get(query).success(function(data){
        onSuccess(data);
      });
    }
  }]
);
