'use strict';
/**
 * @ngdoc function
 * @name marketApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the marketApp
 */

angular.module('marketApp').controller(
  'NewsCtrl',
  [
    '$scope', '$http', '$timeout', '$state', 'getNews',
    function ($scope, $http, $timeout, $state, getNews) {
      getNews('all', function(data){
        $scope.newslist = data;
      });
    }
  ]
);
