angular.module('sbAdminApp').directive('stocktable', function(){
  return {
    templateUrl: 'scripts/components/stocktable/stocktable.html',
    scope: {
      ftse: '='
    },
    restrict: 'E',
    replace: true
  }
});
