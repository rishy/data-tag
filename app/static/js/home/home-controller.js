angular.module('data-tag')
  .controller('HomeController', ['$scope','$http', function ($scope, $http) {

    $scope.tab = {};
    $scope.tab.url = true;
    $scope.tab.text = false;

    // Object for data
    $scope.input = {};
    $scope.input.type = null;
    $scope.input.text = null;
    $scope.input.link = null;

    $scope.pages = {};
    $scope.showResult = false;
  	$scope.postData = function(){
        // API target
        var url = 'http://127.0.0.1:5000/api/tagit/v1.0/';

        if ($scope.input.link == undefined || $scope.input.link == ""){
            $scope.input.type = "text";
        }else{
            $scope.input.type = "link";
        }

        console.log($scope.input);

        $http.post(url, $scope.input).success(function(data, status){
            console.log("Text Sent!");
            console.log(data);
            // Returned data from API end
            $scope.showResult = true;
            $scope.pages = data;
        }).error(function(data, status){
            //console.log(data);
            console.log("Failure");
        })
  	}

    $scope.navtab = function(value){
        if (value==="url") {
            $scope.tab.text = false;
            $scope.tab.url = true;
        }
        else{
            $scope.tab.text = true;
            $scope.tab.url = false;
        }
    }

}]);
