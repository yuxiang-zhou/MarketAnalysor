
###
#  Global Route Configuration
#  Extend/override in reaction/client/routing.coffee
###
Router.configure
  notFoundTemplate: "404"
  loadingTemplate: "blank"

# # we always need to wait on these publications
# Router.waitOn ->
#   @subscribe "stocks"
#   @subscribe "Packages"

# general reaction controller
@StockController = RouteController.extend
  layoutTemplate: "mainLayout"
  onBeforeAction: ->
    Session.set 'active', @url
    @next()
# local ShopController
StockController = @StockController

# Global NaviList

@navElements = []
@navElements.push
  route: 'index'
  path: '/'
  icon: 'fa-dashboard'
  label: 'Dashboard'
  params:
    controller: StockController
    path: "/"
    name: "Dashboard"
    template: "summary"

@navElements.push
  route: 'stock'
  label: 'Stock Details'
  path: '/stock'
  icon: 'fa-table'
  params:
    controller: StockController
    path: "/stock"
    name: "StockDetails"
    template: "stock_table"
    subscriptions: ->
      @subscribe "stocksall"

navElements = @navElements

###
# General Route Declarations
###
Router.map ->
  # default index route, normally overriden parent meteor app
  for nav in navElements
    @route nav.route, nav.params
