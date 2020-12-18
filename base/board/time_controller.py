
class RemainingTime():

    def __init__(self, cycles, time_temp, time_cycle):
        self.multiplier = 60
        self.total_time = ((cycles * time_temp) + (cycles * time_cycle)) * self.multiplier

    def discount_time(self, time):
        self.total_time -= time

    def set_remaining_time(self, cycles, time_temp, time_cycle):
        self.total_time = ((cycles * time_temp) + (cycles * time_cycle)) * self.multiplier

    def get_remaining_time(self):
        return self.total_time

    def reset_time(self, cycles, time_temp, time_cycle):
        self.total_time = ((cycles * time_temp) + (cycles * time_cycle)) * self.multiplier