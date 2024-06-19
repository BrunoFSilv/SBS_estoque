from app.controllers.default import *

routes ={
    "index_route":"/", "index_controller": IndexControoler.as_view("index"),
    "login_route":"/login", "login_controller": LoginController.as_view("login"),
    "entry_route":"/entrada", "entry_controller": EntryController.as_view("entry"),
    "movement_route":"/movimentacao", "movement_controller": MovementController.as_view("movement"),
    "search_route":"/procura", "search_controller": SearchController.as_view("search"),
    "found_route":"/procura/<movement_id>", "found_controller": FoundController.as_view("found"),
    "movement_searsh_route":"/procura/<movement_id>/<movement_uuid>", "movement_searsh_controller": MovementSearshController.as_view("movementSearsh")
}

