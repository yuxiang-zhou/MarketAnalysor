'use strict';

/**
 * @ngdoc directive
 * @name izzyposWebApp.directive:adminPosHeader
 * @description
 * # adminPosHeader
 */

angular.module('marketApp')
  .directive('sidebarSearch',function() {
    return {
      templateUrl:'scripts/directives/sidebar/sidebar-search/sidebar-search.html',
      restrict: 'E',
      replace: true,
      scope: {
      },
      controller:function($scope, $location){
        $scope.selectedMenu = 'home';
        $scope.goSearch = function(){
          $location.path('dashboard/search/' + $scope.searchText);
        };
      }
    }
  });
