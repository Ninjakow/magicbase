import magicbot
import wpilib

from ctre import CANTalon
from components.chassis import Chassis
from components.bno055 import BNO055

from networktables import NetworkTable

import logging

import math


class Robot(magicbot.MagicRobot):

    chassis = Chassis

    def createObjects(self):
        '''Create motors and stuff here'''

        self.drive_motor_a = CANTalon(2)
        self.drive_motor_b = CANTalon(5)
        self.drive_motor_c = CANTalon(4)
        self.drive_motor_d = CANTalon(3)

        self.drive_motor_c.setInverted(True)
        self.drive_motor_d.setInverted(True)

        # Objects that are created here are shared with all classes
        # that declare them. For example, if I had:
        # self.elevator_motor = wpilib.TalonSRX(2)
        # here, then I could have
        # class Elevator:
        #     elevator_motor = wpilib.TalonSRX
        # and that variable would be available to both the MyRobot
        # class and the Elevator class. This "variable injection"
        # is especially useful if you want to certain objects with
        # multiple different classes.

        # create the imu object
        self.bno055 = BNO055()

        # the "logger" - allows you to print to the logging screen
        # of the control computer
        self.logger = logging.getLogger("robot")
        # the SmartDashboard network table allows you to send
        # information to a html dashboard. useful for data display
        # for drivers, and also for plotting variables over time
        # while debugging
        self.sd = NetworkTable.getTable('SmartDashboard')

        # boilerplate setup for the joystick
        self.joystick = wpilib.Joystick(0)
        self.gamepad = wpilib.Joystick(1)
        self.pressed_buttons_js = set()
        self.pressed_buttons_gp = set()
        self.spin_rate = 0.3

    def putData(self):
        # update the data on the smart dashboard
        # put the inputs to the dashboard
        self.sd.putNumber("i_x", self.chassis.inputs[0])
        self.sd.putNumber("i_y", self.chassis.inputs[1])
        self.sd.putNumber("i_z", self.chassis.inputs[2])
        self.sd.putNumber("i_t", self.chassis.inputs[3])
        self.sd.putNumber("heading", self.bno055.getHeading())

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        self.putData()

        # if you want to get access to the buttons, you should be doing it like so:
        try:
            if self.debounce(1):
                # perform some action
                pass
        except:
            self.onException()

        # or with the gamepad
        try:
            if self.debounce(1, gamepad=True):
                #perform some action
                pass
        except:
            self.onException()

        # this is where the joystick inputs get converted to numbers that are sent
        # to the chassis component. we rescale them using the rescale_js function,
        # in order to make their response exponential, and to set a dead zone -
        # which just means if it is under a certain value a 0 will be sent
        # TODO: Tune these constants for whatever robot they are on
        self.chassis.inputs = [-rescale_js(self.joystick.getY(), deadzone=0.05, exponential=1.2),
                               - rescale_js(self.joystick.getX(), deadzone=0.05, exponential=1.2),
                               - rescale_js(self.joystick.getZ(), deadzone=0.2, exponential=15.0,
                                            rate=self.spin_rate),
                               (self.joystick.getThrottle() - 1.0) / -2.0
                               ]

    # the 'debounce' function keeps tracks of which buttons have been pressed
    def debounce(self, button, gamepad=False):
        device = None
        if gamepad:
            pressed_buttons = self.pressed_buttons_gp
            device = self.gamepad
        else:
            pressed_buttons = self.pressed_buttons_js
            device = self.joystick
        if device.getRawButton(button):
            if button in pressed_buttons:
                return False
            else:
                pressed_buttons.add(button)
                return True
        else:
            pressed_buttons.discard(button)
            return False


# see comment in teleopPeriodic for information
def rescale_js(value, deadzone=0.0, exponential=0.0, rate=1.0):
    value_negative = 1.0
    if value < 0:
        value_negative = -1.0
        value = -value
    # Cap to be +/-1
    if abs(value) > 1.0:
        value /= abs(value)
    # Apply deadzone
    if abs(value) < deadzone:
        return 0.0
    elif exponential == 0.0:
        value = (value - deadzone) / (1 - deadzone)
    else:
        a = math.log(exponential + 1) / (1 - deadzone)
        value = (math.exp(a * (value - deadzone)) - 1) / exponential
    return value * value_negative * rate


if __name__ == '__main__':
    wpilib.run(Robot)
