'use strict';
/**
 * @ngdoc overview
 * @name marketApp
 * @description
 * # marketApp
 *
 * Main module of the application.
 */
var app = angular
  .module('marketApp', [
    'oc.lazyLoad',
    'ui.router',
    'ui.bootstrap',
    'angular-loading-bar',
    'Authentication',
    'servData',
    'ngCookies',
    'ngAnimate',
  ])
  .config([ '$stateProvider','$urlRouterProvider','$ocLazyLoadProvider',function ($stateProvider,$urlRouterProvider,$ocLazyLoadProvider) {


    $ocLazyLoadProvider.config({
      debug:false,
      events:true,
    });

    $urlRouterProvider.when('', '/dashboard/home');
    $urlRouterProvider.when('/index', '/dashboard/home');
    $urlRouterProvider.when('/dashboard', '/dashboard/home');
    $urlRouterProvider.otherwise('/dashboard/notfound');

    $stateProvider
      .state('login',{
        templateUrl:'views/pages/login.html',
        url:'/login',
        controller:'LoginCtrl',
        resolve: {
          loadMyFile:function($ocLazyLoad) {
            return $ocLazyLoad.load({
                name:'marketApp',
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
                    name:'marketApp',
                    files:[
                    'scripts/directives/header/header.js',
                    'scripts/directives/header/header-notification/header-notification.js',
                    'scripts/directives/sidebar/sidebar.js',
                    'scripts/directives/sidebar/sidebar-search/sidebar-search.js'
                    ]
                }),
                $ocLazyLoad.load(
                {
                  name:'marketApp',
                  files:['scripts/components/stocktable/stocktable.js']
                }),
                $ocLazyLoad.load(
                {
                  name:'marketApp',
                  files:['scripts/components/newstable/newstable.js']
                }),
                $ocLazyLoad.load(
                {
                  name:'marketApp',
                  files:['scripts/components/stockchart/stockchart.js']
                }),
                $ocLazyLoad.load(
                {
                  name:'marketApp',
                  files:['scripts/components/favIndicator/favIndicator.js']
                })
                // $ocLazyLoad.load(
                // {
                //    name:'ngAnimate',
                //    files:["bower_components/angular-animate/angular-animate.js"]
                // }),
                // $ocLazyLoad.load(
                // {
                //    name:'toggle-switch',
                //    files:["bower_components/angular-toggle-switch/angular-toggle-switch.min.js",
                //           "bower_components/angular-toggle-switch/angular-toggle-switch.css"
                //       ]
                // }),
                // $ocLazyLoad.load(
                // {
                //   name:'marketApp',
                //   files:['scripts/components/annotativechart/annochart.js']
                // }),
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
              name:'marketApp',
              files:[
                'scripts/controllers/dashboardController.js',
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
                name:'marketApp',
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
                name:'marketApp',
                files:['scripts/controllers/detailContoller.js']
            })
          }
        }
      }).state('dashboard.search',{
        templateUrl:'views/search.html',
        url:'/search/:searchText',
        controller:'SearchCtrl',
        resolve: {
          loadCtrl:function($ocLazyLoad) {
            return $ocLazyLoad.load({
                name:'marketApp',
                files:['scripts/controllers/searchContoller.js']
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
                name:'marketApp',
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
                name:'marketApp',
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
                name:'marketApp',
                files:['scripts/controllers/newsContoller.js']
            })
          }
        }
      }).state('dashboard.notfound',{
        templateUrl:'views/pages/notfound.html',
        url:'/notfound',
      }).state('dashboard.chart',{
        templateUrl:'views/charts.html',
        url:'/chart',
        controller:'ChartCtrl',
        resolve: {
          loadMyFile:function($ocLazyLoad) {
            return $ocLazyLoad.load({
              name:'chart.js',
              files:[
                'bower_components/angular-chart.js/dist/angular-chart.min.js',
                'bower_components/angular-chart.js/dist/angular-chart.css'
              ]
            }),
            $ocLazyLoad.load({
                name:'marketApp',
                files:['scripts/controllers/chartContoller.js']
            })
          }
        }
      })
  }])

.run(['$rootScope', '$location', '$cookieStore', '$http', '$state', '$stateParams', 'AuthenticationService',
  function ($rootScope, $location, $cookieStore, $http, $state, $stateParams, AuthenticationService) {
    $rootScope.host = '/';
    // keep user logged in after page refresh
    $rootScope.globals = $cookieStore.get('globals') || {};
    $rootScope.navigator = $location.url();

    if ($rootScope.globals.currentUser) {
      $http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata;
    }

    $rootScope.$on('$locationChangeStart', function (event, next, current) {
      var navStack = [];
      var navBase = "#";
      var path = $location.url().split('/');
      for(var i = 1; i < path.length; ++i) {
        navBase = navBase + '/' + path[i]
        navStack.push({
          url: navBase,
          name: path[i]
        });
      }

      $rootScope.navigator = navStack;

      // redirect to login page if not logged in
      if ($location.path() !== '/login' && !AuthenticationService.isAuthenticated()) {
        $rootScope.lastvisit = next.split('#')[1];
        $location.path('login');
      }
    });
  }]);
