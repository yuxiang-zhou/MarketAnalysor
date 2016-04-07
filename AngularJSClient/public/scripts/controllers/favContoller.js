'use strict';
/**
 * @ngdoc function
 * @name marketApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the marketApp
 */

angular.module('marketApp').controller(
  'FavCtrl',
  [
    '$scope', '$rootScope', '$http', '$timeout', '$state', 'getFavNews', 'getFavList',
    function ($scope, $rootScope, $http, $timeout, $state, getFavNews, getFavList) {

      getFavList($rootScope.globals.currentUser.username, function(data){
        $scope.favstock = data;
      });

      getFavNews($rootScope.globals.currentUser.username, function(data){
        $scope.newslist = data;
      });
    }
  ]
);
