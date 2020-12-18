from base.board.board_controller import ArduinoController
import unittest
import time

class ZmqSenderMock:

    def __init__(self):
        self.command = None

    def on(self):
        self.command = 'on'

    def off(self):
        self.command = 'off'

    def temp(self):
        self.command = 'temp'


class ArduinoSimulator:

    def __init__(self, zmq_zender, arduino_controller):
        self.zmq_zender = zmq_zender
        self.arduino_controller = arduino_controller
        self.in_program = True
        self.temperature = "43.0"
        self.preassure = "1000.0"
        self.humidity = 20
        self.door = 'abierta'
        self.cycle = 'off'
        self.error = ''
        self.board_data = "<T:{},P:{},H:{},D:{},C:{},E:{}>"

    def loop(self):
        while self.in_program:
            data = self.board_data.format(
                self.temperature,
                self.preassure,
                self.humidity,
                self.door,
                self.cycle,
                self.error
            )
            self.arduino_controller.set_status(data)
            if self.zmq_zender.command == 'on':
                self.preassure = "500.0"
            elif self.zmq_zender.command == 'off':
                self.preassure = "1000.0"
                self.temperature = "43.0"
            elif self.zmq_zender.command == 'temp':
                self.temperature = "45"
            time.sleep(5)
            if len(self.arduino_controller.cycles) == 0:
                self.terminate()

    def terminate(self):
        self.in_program = False
        self.zmq_zender.off() 
        self.zmq_zender.temp(45)
        # Setear la presion off y la temperatura a 45 cuando termine el ultimo ciclo del secado

class TestSum(unittest.TestCase):
    def test_logic(self):
        """
        Test that it can sum a list of integers
        """
        zmq = ZmqSenderMock()
        ard = ArduinoController(zmq, True)
        cont = ArduinoSimulator(zmq, ard)
        ard.start_cycle()
        start = time.time()
        cont.loop()
        end = time.time()
        result = int(end - start)
        print("result {}".format(result))
        self.assertGreaterEqual(result, 540)

    def test_logic_repeated(self):
        """
        Test that it can sum a list of integers
        """
        zmq = ZmqSenderMock()
        ard = ArduinoController(zmq, True)
        cont = ArduinoSimulator(zmq, ard)
        ard.start_cycle()
        first_start = time.time()
        cont.loop()
        first_end = time.time()
        first_result = int(first_end - first_start)
        print("first_result {}".format(first_result))
        cont.in_program = True
        ard.start_cycle()
        sec_start = time.time()
        cont.loop()
        sec_end = time.time()
        sec_result = int(sec_end - sec_start)
        print("sec_result {}".format(sec_result))
        result = first_result + sec_result
        self.assertGreaterEqual(result, 1080)

if __name__ == '__main__':
    unittest.main()