'use strict';
/**
 * @ngdoc function
 * @name marketApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the marketApp
 */

angular.module('marketApp').controller(
  'TableCtrl',
  [
    '$scope', '$http', '$timeout', '$state', 'getList',
    function ($scope, $http, $timeout, $state, getList) {

      $scope.title = $state.current.title;
      getList($state.current.indices, function(data){
        $scope.ftse = data;
      });
    }
  ]
);
