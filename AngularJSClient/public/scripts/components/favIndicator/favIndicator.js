angular.module('sbAdminApp').directive('fav', ['$rootScope', 'isFav', 'addFav', 'removeFav',function($rootScope, isFav, addFav, removeFav) {
  return {
    templateUrl: 'scripts/components/favIndicator/favIndicator.html',
    replace: true,
    restrict: 'E',
    scope: {
      symbol: '='
    },
    link: function($scope, elem, attrs){
      isFav($rootScope.globals.currentUser.username, $scope.symbol, function(response){
        if(response.success) {
          var toggleFavElem = function(val){
            if(val) {
              elem.removeClass("fa-heart-o");
              elem.addClass("fa-heart");
            } else {
              elem.removeClass("fa-heart");
              elem.addClass("fa-heart-o");
            }
          };

          var queryFav = function(){
            isFav($rootScope.globals.currentUser.username, $scope.symbol, function(response){
              $scope.fav = response.result;
            });
          };


          // remove spinner on data recieving
          elem.removeClass("fa-spinner fa-spin");

          // toggole corresponding classes
          $scope.fav = response.result;
          $scope.$watch(function($scope){
            return $scope.fav;
          }, function(newValue, oldValue){
            toggleFavElem(newValue);
          }, true);

          // handle on click events
          elem.click(function(e){
            if($scope.fav) {
              removeFav($rootScope.globals.currentUser.username, $scope.symbol, function(response){
                queryFav();
              });
            } else {
              addFav($rootScope.globals.currentUser.username, $scope.symbol, function(response){
                queryFav();
              });
            }

            $scope.$apply();
          });
        }
      });
    }
  }
}]);
