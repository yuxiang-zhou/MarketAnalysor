'use strict';
/**
 * @ngdoc function
 * @name sbAdminApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the sbAdminApp
 */

angular.module('sbAdminApp').controller(
  'DetailCtrl',
  [
    '$scope', '$http', '$timeout', '$state', '$stateParams', 'getDetail',
    function (
      $scope, $http, $timeout, $state, $stateParams,  getDetail
    ) {
      getDetail($stateParams.symbol, function(data){
        $scope.stockdetail = data[0].fields;
        $scope.host = 'http://localhost:8001/';
        $scope.history_url = $scope.host + 'api/history/stock/' + $scope.stockdetail.Symbol;
        $scope.sector_url = $scope.host + 'api/history/sector/' + $scope.stockdetail.Sector;
        $scope.ftse_url = $scope.host + 'api/history/sector/' + ($scope.stockdetail.Catagory.indexOf('AIM') > -1 ? 'FTAI' : 'FTSE');
      });
    }
  ]
);
