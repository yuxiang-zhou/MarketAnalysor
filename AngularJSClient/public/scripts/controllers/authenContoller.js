'use strict';

angular.module('marketApp')

.controller('LoginCtrl',
    ['$scope', '$rootScope', '$location', 'AuthenticationService',
    function ($scope, $rootScope, $location, AuthenticationService) {
        // reset login status
        AuthenticationService.ClearCredentials();

        $scope.login = function () {

          $scope.dataLoading = true;
          AuthenticationService.Login($scope.username, $scope.password, function(response) {

            if(response.data.success) {
              AuthenticationService.SetCredentials($scope.username, $scope.password);

              if($rootScope.lastvisit){
                var url = $rootScope.lastvisit;
                $rootScope.lastvisit = undefined;
                $location.path(url);
              } else {
                $location.path('/index');
              }
            } else {
              $scope.error = response.data.message;
              $scope.dataLoading = false;
            }
          });
        };
    }]);
