angular.module('data-tag')
  .controller('HomeController', ['$scope','$http', function ($scope, $http) {

    $scope.tab = {};
    $scope.tab.url = true;
    $scope.tab.text = false;

    $scope.pages = {};
    $scope.showResult = false;
  	$scope.postData = function(text){
        // API target
        var url = 'http://127.0.0.1:5000/api/tagit/v1.0/';
        // Object for data
        textData = {};
        textData.text = text;
        $http.post(url, textData).success(function(data, status){
            console.log("Text Sent!");
            console.log(data);
            // Returned data from API end
            $scope.showResult = true;
            $scope.pages = data;
        }).error(function(data, status){
            console.log(data);
            console.log("Failure");
        })
  	}
    console.log($scope.tab);
    //console.log($scope.tab);
    $scope.navtab = function(value){
        if (value==="url") {
            $scope.tab.text = false;
            $scope.tab.url = true;
            console.log($scope.tab);
        }
        else{
            $scope.tab.text = true;
            $scope.tab.url = false;
            console.log($scope.tab);
        }
    }

}]);
