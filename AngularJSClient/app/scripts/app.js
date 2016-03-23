'use strict';
/**
 * @ngdoc overview
 * @name sbAdminApp
 * @description
 * # sbAdminApp
 *
 * Main module of the application.
 */
var app = angular
  .module('sbAdminApp', [
    'oc.lazyLoad',
    'ui.router',
    'ngAnimate',
    'ui.bootstrap',
    'angular-loading-bar',
    'Authentication',
    'servData',
    'ngCookies'
  ])
  .config([ '$stateProvider','$urlRouterProvider','$ocLazyLoadProvider',function ($stateProvider,$urlRouterProvider,$ocLazyLoadProvider) {


    $ocLazyLoadProvider.config({
      debug:false,
      events:true,
    });

    $urlRouterProvider.when('', '/dashboard/home');
    $urlRouterProvider.when('/index', '/dashboard/home');
    $urlRouterProvider.otherwise('/dashboard/notfound');

    $stateProvider
      .state('login',{
        templateUrl:'views/pages/login.html',
        url:'/login',
        controller:'LoginCtrl',
        resolve: {
          loadMyFile:function($ocLazyLoad) {
            return $ocLazyLoad.load({
                name:'sbAdminApp',
                files:['scripts/controllers/authenContoller.js']
            })
          }
        }
      })
      .state('dashboard', {
        url:'/dashboard',
        templateUrl: 'views/template.html',
        resolve: {
            loadMyDirectives:function($ocLazyLoad){
                return $ocLazyLoad.load(
                {
                    name:'sbAdminApp',
                    files:[
                    'scripts/directives/header/header.js',
                    'scripts/directives/header/header-notification/header-notification.js',
                    'scripts/directives/sidebar/sidebar.js',
                    'scripts/directives/sidebar/sidebar-search/sidebar-search.js'
                    ]
                }),
                $ocLazyLoad.load(
                {
                   name:'toggle-switch',
                   files:["bower_components/angular-toggle-switch/angular-toggle-switch.min.js",
                          "bower_components/angular-toggle-switch/angular-toggle-switch.css"
                      ]
                }),
                $ocLazyLoad.load(
                {
                  name:'sbAdminApp',
                  files:['scripts/components/stocktable/stocktable.js']
                }),
                $ocLazyLoad.load(
                {
                  name:'sbAdminApp',
                  files:['scripts/components/annotativechart/annochart.js']
                }),
                $ocLazyLoad.load(
                {
                  name:'sbAdminApp',
                  files:['scripts/components/favIndicator/favIndicator.js']
                })
                // $ocLazyLoad.load(
                // {
                //   name:'ngResource',
                //   files:['bower_components/angular-resource/angular-resource.js']
                // })
                // $ocLazyLoad.load(
                // {
                //   name:'ngSanitize',
                //   files:['bower_components/angular-sanitize/angular-sanitize.js']
                // })
                // $ocLazyLoad.load(
                // {
                //   name:'ngTouch',
                //   files:['bower_components/angular-touch/angular-touch.js']
                // })
            }
        }
      }).state('dashboard.home',{
        url:'/home',
        controller: 'MainCtrl',
        templateUrl:'views/dashboard.html',
        resolve: {
          loadMyFiles:function($ocLazyLoad) {
            return $ocLazyLoad.load({
              name:'sbAdminApp',
              files:[
              'scripts/controllers/dashboardController.js',
              'scripts/directives/timeline/timeline.js',
              'scripts/directives/notifications/notifications.js',
              'scripts/directives/chat/chat.js',
              'scripts/directives/dashboard/stats/stats.js'
              ]
            })
          }
        }
      }).state('dashboard.table',{
        abstract: true,
        template:'<ui-view />',
        url:'/table',
        resolve: {
          loadCtrl:function($ocLazyLoad) {
            return $ocLazyLoad.load({
                name:'sbAdminApp',
                files:['scripts/controllers/tableContoller.js']
            })
          }
        }
      }).state('dashboard.table.all',{
        templateUrl:'views/table.html',
        url:'/all',
        title:'FTSE ALL (including AIM) Shares',
        indices: 'all',
        controller:'TableCtrl',
      }).state('dashboard.table.ftse',{
        templateUrl:'views/table.html',
        url:'/ftse',
        title:'FTSE ALL Shares',
        indices: 'ftse',
        controller:'TableCtrl',
      }).state('dashboard.table.ftai',{
        templateUrl:'views/table.html',
        url:'/ftai',
        title:'FTSE AIM ALL Shares',
        indices: 'ftai',
        controller:'TableCtrl',
      }).state('dashboard.detail',{
        templateUrl:'views/detail.html',
        url:'/detail/:symbol',
        controller:'DetailCtrl',
        resolve: {
          loadCtrl:function($ocLazyLoad) {
            return $ocLazyLoad.load({
                name:'sbAdminApp',
                files:['scripts/controllers/detailContoller.js']
            })
          }
        }
      }).state('dashboard.sectors',{
        templateUrl:'views/sector.html',
        url:'/sectors',
        controller:'SectorCtrl',
        resolve: {
          loadMyFile:function($ocLazyLoad) {
            return $ocLazyLoad.load({
                name:'sbAdminApp',
                files:['scripts/controllers/sectorContoller.js']
            })
          }
        }
      }).state('dashboard.fav',{
        templateUrl:'views/fav.html',
        url:'/fav',
        controller:'FavCtrl',
        resolve: {
          loadMyFile:function($ocLazyLoad) {
            return $ocLazyLoad.load({
                name:'sbAdminApp',
                files:['scripts/controllers/favContoller.js']
            })
          }
        }
      }).state('dashboard.news',{
        templateUrl:'views/news.html',
        url:'/news',
        controller:'NewsCtrl',
        resolve: {
          loadMyFile:function($ocLazyLoad) {
            return $ocLazyLoad.load({
                name:'sbAdminApp',
                files:['scripts/controllers/newsContoller.js']
            })
          }
        }
      })
  }])

.run(['$rootScope', '$location', '$cookieStore', '$http',
  function ($rootScope, $location, $cookieStore, $http) {
    $rootScope.host = 'http://localhost:8001/';
    // keep user logged in after page refresh
    $rootScope.globals = $cookieStore.get('globals') || {};
    $rootScope.navigator = $location.url();
    if ($rootScope.globals.currentUser) {
      $http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata; // jshint ignore:line
    }

    $rootScope.$on('$locationChangeStart', function (event, next, current) {

      $rootScope.navigator = $location.url();

      // redirect to login page if not logged in
      if ($location.path() !== '/login' && !$rootScope.globals.currentUser) {
          $location.path('/login');
      }
    });
  }]);
