from magicbot.state_machine import AutonomousStateMachine
from magicbot import state
from components.chassis import Chassis
import math


class Autonomous(AutonomousStateMachine):
    MODE_NAME = "Test"
    chassis = Chassis
    loop = 1

    # @state(first=True, must_finish=True)
    # def move_forward(self):
    #     self.chassis.set_pid(0.5, 0, 15)
    #     self.set_point = self.chassis.set_point(3)
    #     self.next_state("reach_destination")

    # @state(must_finish=True)
    # def reach_destination(self):
    #     print(self.chassis.get_pos()[0])
    #     if self.chassis.get_pos()[0] > self.set_point - 100 and self.chassis.get_pos()[0] < self.set_point + 100:
    #         # if self.chassis.get_vel() < 100:
    #         self.chassis.set_point(0)
    #         self.next_state("turn")

    @state(first=True, must_finish=True)
    def turn(self):
        self.chassis.turn(math.pi/2)
        self.set_point = self.next_state("finish_turn")

    @state(must_finish=True)
    def finish_turn(self):
        if self.chassis.turn_successful():
            # if self.loop >= 2:
            #     self.loop += 1
            #     self.next_state("move_forward")
            # else:
            #     self.done()
            self.done()