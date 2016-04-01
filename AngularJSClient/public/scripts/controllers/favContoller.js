'use strict';
/**
 * @ngdoc function
 * @name sbAdminApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the sbAdminApp
 */

angular.module('sbAdminApp').controller(
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
