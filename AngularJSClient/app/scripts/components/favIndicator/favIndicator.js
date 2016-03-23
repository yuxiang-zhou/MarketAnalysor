angular.module('sbAdminApp').directive('fav', ['$rootScope', 'isFave', function($rootScope, isFave) {
  return {
    templateUrl: 'scripts/components/favIndicator/favIndicator.html',
    replace: true,
    restrict: 'E',
    scope: {
      symbol: '='
    },
    link: function($scope, elem, attrs){
      isFave($rootScope.globals.currentUser.username, $scope.symbol, function(response){
        if(response.success) {
          elem.removeClass("fa-spinner fa-spin");
          if(response.result) {
            elem.removeClass("fa-heart-o");
            elem.addClass("fa-heart");
          } else {
            elem.removeClass("fa-heart");
            elem.addClass("fa-heart-o");
          }
        }
      });
    }
  }
}]);
