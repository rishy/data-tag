angular.module('data-tag')
  .controller('HomeController', ['$scope','$http','$interval',
    '$timeout', function ($scope, $http, $interval, $timeout) {

    $scope.tab = {};
    $scope.tab.url = true;
    $scope.tab.text = false;

    // Object for data
    $scope.input = {};
    $scope.input.type = null;
    $scope.input.text = null;
    $scope.input.link = null;
    $scope.processing = false;

    $scope.tab = {};
    $scope.tab.url = true;
    $scope.tab.text = false;

    $scope.pages = {};
    $scope.showResult = false;
    $scope.showNoun = new Array(18);
    var load_interval;
    var blink_interval;

    $scope.result = {};

  	$scope.postData = function(){

        $scope.processing = true;
        blinkProcessing();
        $scope.result.pages = [];

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
            $scope.nouns = data.all_nouns;
            $scope.processing = false;
            // Show loader nouns
            startLoading();

            $scope.result = data;
            //  here result object has three properties
            //  result.id => job key
            //  result.all_nouns => all nouns extracted from text
            //  result.status => status of job(pending, started, finished)

        }).error(function(data, status){
            //console.log(data);
            console.log("Failure");
        })

        var interval = $interval( function(){
            if($scope.result){
                req = { 'id': $scope.result.id };
                $http.post(url2, req).success(function(data, status){
                    console.log("Text Sent!");
                    console.log(data);
                    // Remove $interval once tags have been fetched
                    if(data.status == 'finished'){
                        $interval.cancel(interval);
                        $interval.cancel(load_interval);
                        $interval.cancel(blink_interval);
                        $scope.result = data;
                        // show the tags section with wikipedia summary
                        $scope.showResult = true;
                    }
                    //  here result object has three properties
                    //  result.id => job key
                    //  result.status => status of job(pending, started, finished)
                    //  result.pages => a list of result pages
                }).error(function(data, status){
                    //console.log(data);
                    console.log("Failure");
                })
            }
        }, 500);

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

<<<<<<< HEAD
    $scope.navtab = function(value){
        if (value==="url") {
            $scope.tab.text = false;
            $scope.tab.url = true;
            $scope.input.text = "";
        }
        else{
            $scope.tab.text = true;
            $scope.tab.url = false;
            $scope.input.link = "";
        }
    }

    startLoading = function(){

        load_interval = $interval(function(){

            // Number of nouns to show( <= 6)
            var k = Math.ceil(12 * Math.random());

            // Show each of the selected nouns after 50 millisecs
            for(var i = 0; i < k; i++){
                var idx = Math.ceil(18 * Math.random());
                    $scope.showNoun[idx] = true;
            }

            // Hide all the nouns again
            $timeout(function(){
                $scope.showNoun = new Array(18);
            }, 900);

            // Shuffle the nouns
            $scope.nouns = shuffle($scope.nouns);

        }, 1000);

    }

    blinkProcessing = function(){

        blink_interval = $interval(function(){
            // Blink processing
            $scope.processing = !$scope.processing;
        }, 900);

    }

    //+ Jonas Raoni Soares Silva
    //@ http://jsfromhell.com/array/shuffle [v1.0]
    function shuffle(o){ //v1.0
        for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
        return o;
    }

=======
>>>>>>> feat(ui): input url field added along with navigation
}]);
