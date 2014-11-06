angular.module('data-tag')
  .controller('HomeController', ['$scope', function ($scope) {

  	$scope.postData = function(data){
  		alert(data);
  	}

  }]);
