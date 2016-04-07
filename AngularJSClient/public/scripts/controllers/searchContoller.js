'use strict';
/**
 * @ngdoc function
 * @name marketApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the marketApp
 */

angular.module('marketApp').controller(
  'SearchCtrl',
  [
    '$scope', '$rootScope', '$http', '$state', '$stateParams', 'search',
    function (
      $scope, $rootScope, $http, $state, $stateParams, search
    ) {
      $scope.searchText = $stateParams.searchText;
      search($scope.searchText, function(data){
        $scope.ftse = data;
      });
    }
  ]
);
