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

    $scope.result = {};

  	$scope.postData = function(){
        // API target
        var url1 = 'http://127.0.0.1:5000/api/tagit/v1.0/';
        var url2 = 'http://127.0.0.1:5000/api/tagit/v1.0/result/';

        if ($scope.input.link == undefined || $scope.input.link == ""){
            $scope.input.type = "text";
        }else{
            $scope.input.type = "link";
        }

        console.log($scope.input);

        $http.post(url1, $scope.input).success(function(data, status){
            console.log("Text Sent!");
            console.log(data);
            // Returned data from API end
            $scope.showResult = true;
            $scope.pages = data;
            $scope.result = data;
            //  here result object has three properties
            //  result.id => job key
            //  result.all_nouns => all nouns extracted from text
            //  result.status => status of job(pending, started, finished)

        }).error(function(data, status){
            //console.log(data);
            console.log("Failure");
        })

        // add settimeout() function to send the http resquest for url2
        // untill you get the result.status=finished
        $http.post(url2, $scope.input).success(function($scope.result, status){
            console.log("Text Sent!");
            console.log(data);
            // Returned data from API end
            $scope.showResult = true;
            $scope.result.pages = data;
            //  here result object has three properties
            //  result.id => job key
            //  result.status => status of job(pending, started, finished)
            //  result.pages => a list of result pages
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
