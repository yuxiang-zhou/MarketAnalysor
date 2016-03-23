'use strict';
/**
 * @ngdoc function
 * @name sbAdminApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the sbAdminApp
 */
angular.module('sbAdminApp')
.controller('MainCtrl', ['$scope', '$rootScope', 'getList', 'getFavNews', 'getNT',
function($scope, $rootScope, getList, getFavNews, getNT) {
  $scope.ftse_url = $rootScope.host + 'api/history/sector/FTSE';
  $scope.ftai_url = $rootScope.host + 'api/history/sector/FTAI';
  getFavNews($rootScope.globals.currentUser.username, function(data){
    $scope.newslist = data;
  });

  getNT(function(data){
    $scope.NTStocks = data;
  });

}]);
