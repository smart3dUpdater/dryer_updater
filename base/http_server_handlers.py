from base.http_basic import BasicHandler
from tornado.ioloop import IOLoop
import functools
from tornado.escape import json_decode
from tornado import concurrent, gen
from utils import get_interface_connected, get_active, set_active, wifi_connected, scan_wlan, connect_to_wifi, get_my_ips

class HomeHandler(BasicHandler):
    def get(self):
        self.application.where = 'home'
        if self.application.my_board and self.application.board_controller.cycling:
            self.render('drying.html', drying=True)
        else:
            self.render('index.html', drying=self.application.board_controller.cycling, door_open_error=False)

class LoadHandler(BasicHandler):
    def get(self):
        self.application.where = 'load'
        self.render('load.html')

class InfoHandler(BasicHandler):
    def get(self):
        self.application.where = 'info'
        self.render('info.html')

class ConfigHandler(BasicHandler):
    def get(self):
        self.application.where = 'config'
        self.render('config.html')

class AddFilamentHandler(BasicHandler):
    def get(self):
        self.render('add_filament.html')

class DryedMaterialHandler(BasicHandler):
    def get(self):
        self.render('dryed_material.html')

class DryerInfoHandler(BasicHandler):
    def get(self):
        self.render('dryer_info.html')

class LoadFilamentHandler(BasicHandler):
    def get(self):
        materials = self.application.db.get_materials()
        colours = self.application.db.get_colours()
        densities = self.application.db.get_densities()
        diameters = self.application.db.get_diameters()
        self.render('material_form.html', materials=materials, colours=colours,
            densities=densities, diameters=diameters)

class StatusHandler(BasicHandler):
    def get(self):
        (time_formated, cycling, action, remaining_time) = self.application.board_controller.cycle_data()
        data = {
            'temp': self.application.board_controller.get_temperature(),
            'preassure': self.application.board_controller.get_preassure(),
            'time_formated': time_formated,
            'cycling': cycling,
            'action': action,
            'remaining_time': remaining_time,
        }
        self.write(data)

class StartDryingHandler(BasicHandler):
    def get(self):
        if self.application.board_controller.door == '1':
            program = self.application.db.get_custom_program_by_id(get_active())
            self.application.board_controller.set_active(program[4], program[2], program[5], program[3], program[6])
            self.application.board_controller.start_cycle()
            self.render('drying.html', drying=True)
        else:
            self.render('index.html', drying=self.application.board_controller.cycling, door_open_error=True)

class StopHandler(BasicHandler):
    def get(self):
        self.application.board_controller.stop_cycle()
        self.write('ok')

class UpdateHandler(BasicHandler):
    def get(self):
        resp = self.application.updater.make_update()       
        self.write(resp)

class SaveDataHandler(BasicHandler):
    def post(self):
        data = json_decode(self.request.body)
        partial = functools.partial(self.save_data, data['materials'], data['colours'], data['densities'], data['diameters'])
        IOLoop.current().spawn_callback(partial)
        self.write('ok')

    async def save_data(self, materials, colours, densities, diameters):
        if materials:
            self.application.db.save_materials(materials)
        if colours:
            self.application.db.save_colours(colours)
        if densities:
            self.application.db.save_densities(densities)
        if diameters:
            self.application.db.save_diameters(diameters)
        
class SpoolDryedHandler(BasicHandler):
    def get(self):
        self.render('dryed_overlay.html')

class RemainingHandler(BasicHandler):
    def get(self):
        self.render('remaining_material.html')
        
class GeneralStatusHandler(BasicHandler):
    def get(self):
        result = get_interface_connected()
        if result.startswith('wlan'):
            self.write({'conn': 'wlan', 'door': str(self.application.board_controller.door)})
        elif result.startswith('eth'):
            self.write({'conn':'eth', 'door': str(self.application.board_controller.door)})
        else:
            self.write({'conn': '', 'door': str(self.application.board_controller.door)})

class DryingProgramsHandler(BasicHandler):
    def get(self):
        programs = self.application.db.get_all_custom_program()
        if len(programs) < 12:
            for x in range(len(programs), 12):
                programs.append([0])
        self.render('drying_programs.html', programs=programs, active=get_active())

class CustomProgramHandler(BasicHandler):
    def get(self):
        self.render('custom_program.html')

    def post(self):
        data = json_decode(self.request.body)
        partial = functools.partial(self.save_data, data['name'], data['pressure'], data['duration'],
                    data['temperature'], data['preheating'], data['subcicles'])
        IOLoop.current().spawn_callback(partial)
        self.write('ok')

    async def save_data(self, name, pressure, duration, temperature, preheating, subcicles):
        self.application.db.save_custom_program(name, pressure, duration, temperature, preheating, subcicles)

class NonEditableProgram(BasicHandler):
    def get(self, id_program):
        program = self.application.db.get_custom_program_by_id(id_program)
        self.render('non_editable_program.html', program=program)

class EditProgramHandler(BasicHandler):
    def get(self, id_program):
        program = self.application.db.get_custom_program_by_id(id_program)
        self.render('edit_program.html', program=program)

    def post(self, id_program):
        data = json_decode(self.request.body)
        program = self.application.db.get_custom_program_by_id(id_program)
        if program[7] == 'yes':
            partial = functools.partial(self.save_data, id_program, data['name'], data['pressure'], data['duration'],
                                        data['temperature'], data['preheating'], data['subcicles'])
            IOLoop.current().spawn_callback(partial)
            self.write('ok')
        else:
            self.send_error(403)

    async def save_data(self, id_program, name, pressure, duration, temperature, preheating, subcicles):
        self.application.db.edit_custom_program(id_program, name, pressure, duration, temperature, preheating, subcicles)

class ActivateEditProgramHandler(BasicHandler):
    def post(self, id_program):
        data = json_decode(self.request.body)
        partial = functools.partial(self.save_data, id_program, data['name'], data['pressure'], data['duration'],
                    data['temperature'], data['preheating'], data['subcicles'])
        IOLoop.current().spawn_callback(partial)
        set_active(id_program)
        self.write('ok')

    async def save_data(self, id_program, name, pressure, duration, temperature, preheating, subcicles):
        self.application.db.edit_custom_program(id_program, name, pressure, duration, temperature, preheating, subcicles)

class ActivateSaveProgramHandler(BasicHandler):
    def post(self):
        #TODO: activate con el json
        data = json_decode(self.request.body)
        partial = functools.partial(self.save_data, data['name'], data['pressure'], data['duration'],
                    data['temperature'], data['preheating'], data['subcicles'])
        IOLoop.current().spawn_callback(partial)
        self.write('ok')

    async def save_data(self, name, pressure, duration, temperature, preheating, subcicles):
        self.application.db.save_custom_program(name, pressure, duration, temperature, preheating, subcicles)
        set_active(self.application.db.cursor.lastrowid)

class WifiConnectionHandler(BasicHandler):

    @concurrent.run_on_executor
    def get(self):
        wifi_list = scan_wlan()
        selected = wifi_connected()
        self.write({"wifi_list": wifi_list, 'selected': selected})

class ToWifiConnectionHandler(BasicHandler):

    @gen.coroutine
    def post(self):
        network_name = self.get_body_argument("network_name")
        password = self.get_body_argument("password", default=None)
        result = yield connect_to_wifi(network_name, password)
        if not result or network_name != result:
            result = 'Connection error'
        self.write(result)

class NetworkHandler(BasicHandler):
    def get(self):
        (ip_wifi, ip_eth) = get_my_ips()
        try:
            selected = wifi_connected()
        except:
            selected = ''
        self.render('network_info.html', ip_wifi=ip_wifi, ip_eth=ip_eth, selected=selected)

class DisconnectWifiHandler(BasicHandler):
    @gen.coroutine
    def get(self):
        result = yield connect_to_wifi('fake', '1234')
        self.write('ok')
