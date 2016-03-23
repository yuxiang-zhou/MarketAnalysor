'use strict';
/**
 * @ngdoc function
 * @name sbAdminApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the sbAdminApp
 */

angular.module('sbAdminApp').controller(
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
