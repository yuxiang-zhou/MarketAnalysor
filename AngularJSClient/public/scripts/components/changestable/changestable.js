angular.module('marketApp').directive('changestable', function(){
  return {
    templateUrl: 'scripts/components/changestable/changestable.html',
    scope: {
      table: '='
    },
    restrict: 'E',
    replace: true
  }
});
