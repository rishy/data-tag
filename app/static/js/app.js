// Declare app level module which depends on filters, and services
var datatag = angular.module('data-tag', ['ngResource', 'ngRoute', 'ui.bootstrap', 'ui.date']);

datatag.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/home/home.html',
        controller: 'HomeController'})
      .otherwise({redirectTo: '/'});
}]);
