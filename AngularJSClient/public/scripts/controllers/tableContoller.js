'use strict';
/**
 * @ngdoc function
 * @name sbAdminApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the sbAdminApp
 */

angular.module('sbAdminApp').controller(
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
