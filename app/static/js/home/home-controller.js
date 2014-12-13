angular.module('data-tag')
  .controller('HomeController', ['$scope','$http', function ($scope, $http) {

    $scope.tab = {};
    $scope.tab.url = true;
    $scope.tab.text = false;

    // Object for data
    $scope.textData = {};
    $scope.textData.type = null;
    $scope.textData.text = null;
    $scope.textData.link = null;

    $scope.pages = {};
    $scope.showResult = false;
  	$scope.postData = function(){
        // API target
        var url = 'http://127.0.0.1:5000/api/tagit/v1.0/';

        if ($scope.textData.link == null){
            $scope.textData.type = "text";
        }else{
            $scope.textData.type = "link";
        }

        console.log($scope.textData);

        $http.post(url, $scope.textData).success(function(data, status){
            console.log("Text Sent!");
            //console.log(data);
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
            console.log($scope.tab);
        }
        else{
            $scope.tab.text = true;
            $scope.tab.url = false;
            console.log($scope.tab);
        }
    }

}]);
