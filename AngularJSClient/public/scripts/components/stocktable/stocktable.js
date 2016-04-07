angular.module('marketApp').directive('stocktable', function(){
  return {
    templateUrl: 'scripts/components/stocktable/stocktable.html',
    scope: {
      ftse: '='
    },
    restrict: 'E',
    replace: true,
    controller: function($scope){
      $scope.predicate = 'fields.Symbol';
      $scope.reverse = true;

      $scope.order = function(predicate) {
        $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : true;
        $scope.predicate = predicate;
      };
    }
  }
});
