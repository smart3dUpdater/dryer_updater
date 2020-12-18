import time
from base.board.time_controller import RemainingTime
from utils import get_active
import logging

class ArduinoController:

    PH = 'PH'
    STB = 'STB'
    DRY = 'DRY'
    CL = 'CL'

    def __init__(self, zmq_sender, test=False):
        self.logger = logging.getLogger('server_logger')
        self.temperature = 0
        self.preassure = None
        self.humidity = None
        self.door = None
        self.cycle = None
        self.error = None
        self.zmq_sender = zmq_sender
        self.cycle_current = 1
        #Cantidad de subciclos
        self.cycle_target = 3
        #Presion objetivo al prender
        self.preassure_target_on = 550
        #Presion objetivo para volver a prender en caso de que todavía haya subciclos
        self.preassure_target_off = 950
        #temperatura objetivo
        self.temp_target = 45
        # Minutes
        if test:
            #Para test
            self.time_target = 2
        else:
            #Tiempo objetivo de espera una vez que se llega a la presión deseada
            self.time_target = 30
        # Seconds
        if test:
            #Para test
            self.time_after_temp = 1
        else:
            #Tiempo objetivo de espera una vez que se llega a la temperatura deseada
            self.time_after_temp = 10
        self.time_multiplier = 60
        self.cycling = False
        self.in_cycle = False
        self.first_temp_reached = False
        self.is_wait_temp_reached = False
        self.timer = 0
        self.total_drying_time = 0
        #self.wait_temp_reached = 10
        self.wait_temp_reached = 0
        self.status_timeout = 5
        #new
        self.time_cycle = 0
        self.time_temp = 0
        self.is_in_my_cycle = False
        self.cycles = []
        self.start_conteo = False
        self.action = self.PH
        self.remaining_controller = RemainingTime(self.cycle_target, self.time_after_temp, self.time_target)

    #Se setea el activo desde la DB al realizar start
    def set_active(self, pressure, duration, temperature, preheating, subcicles):
        self.logger.info('Given set active params: subcicles: {}, pressure: {}, temperature: {}, duration: {}, preheating: {}'.format(
            subcicles, pressure, temperature, duration, preheating
        ))
        self.cycle_target = subcicles
        self.preassure_target_on = pressure
        self.temp_target = temperature
        self.time_target = duration
        self.time_after_temp = preheating
        self.logger.info('Set active confirmed: subcicles: {}, pressure: {}, temperature: {}, duration: {}, preheating: {}'.format(
            self.cycle_target, self.preassure_target_on, self.temp_target, self.time_target, self.time_after_temp
        ))
        self.remaining_controller.set_remaining_time(self.cycle_target, self.time_after_temp, self.time_target)
    
    def set_status(self, board_data):
        #Recibo el status de la arduino y seteo las variables
        dict_data = dict(item.split(":") for item in board_data[1:-1].split(","))
        self.temperature = int(dict_data['T'].split('.')[0])
        self.preassure = dict_data['P'].split('.')[0]
        self.humidity = dict_data['H']
        self.door = dict_data['D']
        self.cycle = dict_data['C']
        self.error = dict_data['E']
        if self.cycling:
            self.check_cycle_status()

    def get_temperature(self):
        if self.temperature:
            return self.temperature
        else:
            return '00'
    
    def get_preassure(self):
        if self.preassure:
            return self.preassure
        else:
            return '00'
    
    def start_cycle(self):
        self.zmq_sender.temp(self.temp_target)
        self.cycling = True
        self.first_temp_reached = False
        self.total_drying_time = 0
        self.wait_temp_reached = 0
        #Genero todos los subciclos, es decir pór cada subciclo coloco un metodo check que realiza todas las verificaciones
        self.cycles = [[self.check, False] for i in range(0, self.cycle_target)]
        self.start_conteo = False
        self.action = self.PH

    def stop_cycle(self):
        #Vuelvo todas las variables a 0
        self.zmq_sender.off()
        self.zmq_sender.temp(self.temp_target)
        self.cycling = False
        self.in_cycle = False
        self.first_temp_reached = False
        self.is_wait_temp_reached = False
        self.cycle_current = 1
        self.wait_temp_reached = 0
        self.cycles = []
        self.start_conteo = False
        self.is_in_my_cycle = False
        self.time_temp = 0
        self.remaining_controller.reset_time(self.cycle_target, self.time_after_temp, self.time_target)
        self.action = self.PH

    def check_cycle_status(self):
        self.total_drying_time += self.status_timeout
        #Verifico los ciclados que estan en False, por lo tanto los que faltan correr
        until_cycles = [x for x in self.cycles if not x[1]]
        if until_cycles:
            if not self.start_conteo:
                #realizo los checkeos del metodo check
                resp = until_cycles[0][0]()
                if resp:
                    self.start_conteo = True
                    until_cycles[0][1] = resp
            #Espero a llegar a la presion off
            if self.start_conteo and int(self.preassure) >= self.preassure_target_off:
                self.action = self.PH
                self.zmq_sender.temp(self.temp_target)
                self.start_conteo = False
        else:
            self.stop_cycle()
            

    def check(self):
        self.time_temp += self.status_timeout
        #Se realiza el conteo del tiempo restante
        self.check_remaining()
        if self.in_cycle:
            self.time_cycle += self.status_timeout
        #espero a llegar a la temperatura objetivo
        if not self.first_temp_reached and self.temperature >= self.temp_target:
            self.first_temp_reached = True
            self.time_temp = 0
            self.action = self.STB
        #Espero a llegar al tiempo seteado con la temperatura
        calc = self.time_after_temp * self.time_multiplier
        if self.first_temp_reached and self.time_temp >= calc and not self.is_in_my_cycle:
            #Prendo bomba porque llegue a tiempo con la temperatura
            if not self.is_wait_temp_reached:
                self.action = self.DRY
                self.zmq_sender.on(self.preassure_target_on)
                self.is_wait_temp_reached = True
                self.is_in_my_cycle = True
        #Espero a llegar al tiempo de ciclado
        if int(self.preassure) <= self.preassure_target_on and not self.in_cycle:
            self.time_cycle = 0
            self.in_cycle = True
        if self.time_cycle >= self.time_target * self.time_multiplier:
            #Termino el ciclado y retorno True indicando que lo termine
            self.action = self.CL
            self.zmq_sender.off()
            self.time_cycle = 0
            self.time_temp = 0
            self.is_wait_temp_reached = False
            self.is_in_my_cycle = False
            self.first_temp_reached = False
            self.in_cycle = False
            return True
        else:
            return False

    def check_remaining(self):
        #Solo se cuenta el tiempo restante en base a estos estados
        if self.action == self.STB or (self.action == self.DRY and self.in_cycle):
            self.remaining_controller.discount_time(self.status_timeout)

    def cycle_data(self):
        time_formated = time.strftime("%H:%M", time.gmtime(self.total_drying_time))
        remaining_time = time.strftime("%H:%M", time.gmtime(self.remaining_controller.get_remaining_time()))
        return (time_formated, self.cycling, self.action, remaining_time)

