# Gloval Route Class def

class Navigation

  getStruct: ->
    return @struct

  constructor: (route,path,icon,label,params) ->
    @struct = {}
    @struct.route = route
    @struct.path = path
    @struct.icon = icon
    @struct.label = label
    @struct.params = params
    @struct.params.path = path
    @struct.params.name = label.replace(" ", "");
    @struct.children=[]

  addChild: (instNavi) ->
    @struct.children.push(instNavi.getStruct())
    return this
@Navigation = Navigation



###
#  Global Route Configuration
#  Extend/override in reaction/client/routing.coffee
###
Router.configure
  notFoundTemplate: "404"
  loadingTemplate: "blank"

# # we always need to wait on these publications
# Router.waitOn ->
#   @subscribe "stocksall"
#   @subscribe "stocksFTSE"
#   @subscribe "stocksFTSEAIM"
#   @subscribe "Packages"

# general reaction controller
@PageController = RouteController.extend
  layoutTemplate: "mainLayout"
  onBeforeAction: ->
    Session.set 'active', @url
    @next()
# local ShopController
PageController = @PageController


# Global NaviList
@navElements = []
@navElements.push(
    new Navigation('index','/','fa-dashboard','Dashboard',{controller: PageController, template: "summary"}).getStruct()
  )
@navElements.push(
    new Navigation('stock','/stock','fa-table','Stock Details',{controller: PageController, template: "stock_table", waitOn:-> return @subscribe 'stocksall'}).addChild(
      new Navigation('stock','/stock-ftse','fa-table','FTSE ALL Share',{controller: PageController, template: "stock_table", waitOn:-> return @subscribe 'stocksFTSE'})
    ).addChild(
      new Navigation('stock','/stock-aim','fa-table','FTSE AIM ALL Share',{controller: PageController, template: "stock_table", waitOn:-> return @subscribe 'stocksFTSEAIM'})
    ).getStruct()
  )

navElements = @navElements

###
# General Route Declarations
###
Router.map ->
  # default index route, normally overriden parent meteor app
  that = this
  addNavigation = (navs) ->
    for nav in navs
      that.route nav.route, nav.params
      addNavigation(nav.children)

  addNavigation(navElements)

  # Router for displaying details stock information
  @route 'stockdetail',
    controller: PageController
    path: "/stockdetail/:symbol"
    name: "stockdetail"
    template: "stockdetail"
    waitOn:->
      return @subscribe 'stocksall'
    data: ->
      return StockDB.findOne({"symbol":@params.symbol})

  @route '/api/history/:symbol', (->
      data = StockDBHist.find({"symbol":@params.symbol}).fetch()
      @response.end JSON.stringify(data)
    ), {where: 'server'}
