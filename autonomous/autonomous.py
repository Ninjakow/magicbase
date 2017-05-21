from magicbot.state_machine import AutonomousStateMachine
from magicbot import state
from components.chassis import Chassis


class Autonomous(AutonomousStateMachine):
    MODE_NAME = "Test"
    chassis = Chassis

    @state(first=True, must_finish=True)
    def move_forward(self):
        self.chassis.set_pid()
        self.set_point = self.chassis.set_point(3, 3)
        self.set_point = self.set_point[0]
        self.next_state("reach_destination")

    @state(must_finish=True)
    def reach_destination(self):
        if self.chassis.get_pos()[0] > self.set_point-100 and self.chassis.get_pos()[0] < self.set_point+100:
            if self.chassis.get_vel() < 100:
                self.chassis.set_point(0, 0)
                self.next_state("turn")

    @state(must_finish=True)
    def turn(self):
        self.chassis.set_point(1, -1)
        self.done()
