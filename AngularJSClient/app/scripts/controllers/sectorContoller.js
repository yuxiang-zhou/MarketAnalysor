'use strict';
/**
 * @ngdoc function
 * @name sbAdminApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the sbAdminApp
 */

angular.module('sbAdminApp').controller(
  'SectorCtrl',
  [
    '$scope', '$rootScope', '$http', '$timeout', '$state', 'getSectorList',
    function ($scope, $rootScope, $http, $timeout, $state, getSectorList) {
      getSectorList(function(data){
        $scope.sectors = [];

        data.forEach(function(elem, index, arr){
          $scope.sectors.push({
            'title': elem,
            'id': elem,
            'url': $rootScope.host + 'api/history/sector/' + elem
          });
        });
      });
    }
  ]
);
