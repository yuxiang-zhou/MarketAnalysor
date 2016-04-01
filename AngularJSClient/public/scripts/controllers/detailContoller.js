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
    '$scope', '$rootScope', '$http', '$timeout', '$state', '$stateParams', 'getDetail', 'getNews',
    function (
      $scope, $rootScope, $http, $timeout, $state, $stateParams,  getDetail, getNews
    ) {
      getDetail($stateParams.symbol, function(data){
        $scope.stockdetail = data[0].fields;
        $scope.history_url = $rootScope.host + 'api/history/stock/' + $scope.stockdetail.Symbol;
        $scope.sector_url = $rootScope.host + 'api/history/sector/' + $scope.stockdetail.Sector;
        $scope.ftse_url = $rootScope.host + 'api/history/sector/' + ($scope.stockdetail.Catagory.indexOf('AIM') > -1 ? 'FTAI' : 'FTSE');

        getNews($scope.stockdetail.Symbol, function(data){
          $scope.newslist = data;
        });
      });
    }
  ]
);
