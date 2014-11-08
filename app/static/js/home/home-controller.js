angular.module('data-tag')
  .controller('HomeController', ['$scope','$http', function ($scope, $http) {

    $scope.resultData = {};
  	$scope.postData = function(text){
        // API target
        var url = 'http://localhost:5000/api/tagit/v1.0/';
        // Object for data
        textData = {};
        textData.text = text;
        $http.post(url, textData).success(function(data, status){
            console.log("Text Sent!");
            console.log(data.text);
            // Returned data from API end
            $scope.resultData = data;
        }).error(function(data, status){
            console.log("Failure");
        })

  	}

  }]);
