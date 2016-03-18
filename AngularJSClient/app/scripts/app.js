'use strict';
/**
 * @ngdoc overview
 * @name sbAdminApp
 * @description
 * # sbAdminApp
 *
 * Main module of the application.
 */
angular
  .module('sbAdminApp', [
    'oc.lazyLoad',
    'ui.router',
    'ui.bootstrap',
    'angular-loading-bar',
  ])
  .config(['$stateProvider','$urlRouterProvider','$ocLazyLoadProvider',function ($stateProvider,$urlRouterProvider,$ocLazyLoadProvider) {

    $ocLazyLoadProvider.config({
      debug:false,
      events:true,
    });

    $urlRouterProvider.when('', '/dashboard/home');
    $urlRouterProvider.when('/index', '/dashboard/home');
    $urlRouterProvider.otherwise('/dashboard/notfound');

    $stateProvider
      .state('dashboard', {
        url:'/dashboard',
        templateUrl: 'views/dashboard/main.html',
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
                  name:'ngAnimate',
                  files:['bower_components/angular-animate/angular-animate.js']
                }),
                $ocLazyLoad.load(
                {
                  name:'servData',
                  files:['scripts/services/dataService.js']
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
                })
                // $ocLazyLoad.load(
                // {
                //   name:'ngCookies',
                //   files:['bower_components/angular-cookies/angular-cookies.js']
                // })
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
        templateUrl:'views/dashboard/home.html',
        resolve: {
          loadMyFiles:function($ocLazyLoad) {
            return $ocLazyLoad.load({
              name:'sbAdminApp',
              files:[
              'scripts/controllers/main.js',
              'scripts/directives/timeline/timeline.js',
              'scripts/directives/notifications/notifications.js',
              'scripts/directives/chat/chat.js',
              'scripts/directives/dashboard/stats/stats.js'
              ]
            })
          }
        }
      }).state('dashboard.form',{
        templateUrl:'views/form.html',
        url:'/form'
      }).state('dashboard.blank',{
        templateUrl:'views/pages/blank.html',
        url:'/blank'
      }).state('login',{
        templateUrl:'views/pages/login.html',
        url:'/login'
      }).state('dashboard.notfound',{
        templateUrl:'views/pages/notfound.html',
        url:'/notfound',
        resolve: {
          loadCSS:function($ocLazyLoad){
            return $ocLazyLoad.load(
            {
              name:'sbAdminApp',
              files:[
                "styles/notfound.css"
              ]
            })
          }
        }
      }).state('dashboard.chart',{
        templateUrl:'views/chart.html',
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
                name:'sbAdminApp',
                files:['scripts/controllers/chartContoller.js']
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
      }).state('dashboard.panels-wells',{
        templateUrl:'views/ui-elements/panels-wells.html',
        url:'/panels-wells'
      }).state('dashboard.buttons',{
        templateUrl:'views/ui-elements/buttons.html',
        url:'/buttons'
      }).state('dashboard.notifications',{
        templateUrl:'views/ui-elements/notifications.html',
        url:'/notifications'
      }).state('dashboard.typography',{
        templateUrl:'views/ui-elements/typography.html',
        url:'/typography'
      }).state('dashboard.icons',{
        templateUrl:'views/ui-elements/icons.html',
        url:'/icons'
      }).state('dashboard.grid',{
        templateUrl:'views/ui-elements/grid.html',
        url:'/grid'
      })
  }]);
