angular.module('marketApp').directive('newstable', function(){
  return {
    templateUrl: 'scripts/components/newstable/newstable.html',
    scope: {
      newslist: '='
    },
    restrict: 'E',
    replace: true
  }
});
