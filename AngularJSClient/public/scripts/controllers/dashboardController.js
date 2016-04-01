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

  $scope.predicateMap = [
    {'id':'fields.weekly_change','title':'Weekly'},
    {'id':'fields.monthly_change','title':'Monthly'},
    {'id':'fields.seasonally_change','title':'Seasonally'},
    {'id':'fields.halfyearly_change','title':'Half-yearly'},
    {'id':'fields.yearly_change','title':'Yearly'}
  ]

  getList('all', function(data){
    $scope.stocks = data;
    $scope.predicate = $scope.predicateMap[0];
    $scope.reverse = true;
  });


  $scope.order = function(predicate) {
    $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : false;
    $scope.predicate = predicate;
  };
  getFavNews($rootScope.globals.currentUser.username, function(data){
    $scope.newslist = data;
  });

  getNT(function(data){
    $scope.NTStocks = data;
  });

}]);
