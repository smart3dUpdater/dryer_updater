from base.http_serial_handlers import *
from base.http_server_handlers import *
from tornado import web

serial_handlers = [
    (r"/ciclado-on/([0-9]+)", CicladoOnHandler),
    (r"/ciclado-off", CicladoOffHandler),
    (r"/first-status", FirstStatusHandler),
]

web_handlers = [
    (r"/", HomeHandler),
    (r"/load", LoadHandler),
    (r"/info", InfoHandler),
    (r"/config", ConfigHandler),
    (r"/start-drying", StartDryingHandler),
    (r"/add-filament", AddFilamentHandler),
    (r"/dryed-material", DryedMaterialHandler),
    (r"/dryer-info", DryerInfoHandler),
    (r"/update", UpdateHandler),
    (r"/stop", StopHandler),
    (r"/status", StatusHandler),
    (r"/load-filament", LoadFilamentHandler),
    (r"/save-data", SaveDataHandler),
    (r"/spool-dryed", SpoolDryedHandler),
    (r"/remaining", RemainingHandler),
    (r"/general-status", GeneralStatusHandler),
    (r"/drying-programs", DryingProgramsHandler),
    (r"/custom-program", CustomProgramHandler),
    (r"/save-custom-program", CustomProgramHandler),
    (r"/edit-program/([0-9]+)", EditProgramHandler),
    (r"/non-editable-program/([0-9])+", NonEditableProgram),
    (r"/activate", ActivateSaveProgramHandler),
    (r"/activate/([0-9]+)", ActivateEditProgramHandler),
    (r"/network", NetworkHandler),
    (r"/get-wifi-connection", WifiConnectionHandler),
    (r"/wifi-connection", ToWifiConnectionHandler),
    (r"/disconnect-wifi", DisconnectWifiHandler),
    (r"/icons/(.*)", web.StaticFileHandler, {"path": "/home/pi/software/static/icons"}),
    (r"/css/(.*)", web.StaticFileHandler, {"path": "/home/pi/software/static/css"}),
    (r"/js/(.*)", web.StaticFileHandler, {"path": "/home/pi/software/static/js"}),
    (r"/Keyboard-master/(.*)", web.StaticFileHandler, {"path": "/home/pi/software/static/Keyboard-master"})
]
