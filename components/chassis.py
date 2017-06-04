# this is the chassis class, a good example of a component. it is a
# bit special in that it has to take direct numerical input from the
# joystick (which is achieved by changing the 'input' variable, which
# is a list composed of [vx, vy, vz, throttle]) but is a good example
# of what a component should look like.
from ctre import CANTalon
import math
from components.bno055 import BNO055
from wpilib import PIDController


class Chassis:

    bno055 = BNO055
    drive_motor_a = CANTalon
    drive_motor_b = CANTalon
    drive_motor_c = CANTalon
    drive_motor_d = CANTalon

    inches_to_meters = 0.0254
    # some calculations that provide numbers used by the motion profiling
    wheel_circumference = 6 * inches_to_meters * math.pi
    rotations_per_meter = 1 / wheel_circumference
    counts_per_revolution = 1440
    counts_per_meter = counts_per_revolution * rotations_per_meter
    velocity_to_native_units = 0.1 * counts_per_meter

    def __init__(self):
        super().__init__()
        self.inputs = [0.0 for x in range(4)]

    def setup(self):
        """Run just after createObjects.
        Useful if you want to run something after just once after the
        robot code is started, that depends on injected variables"""
        self.motors = [self.drive_motor_a, self.drive_motor_b,
                       self.drive_motor_c, self.drive_motor_d]

    def on_enable(self):
        """Run every time the robot transitions to being enabled"""
        pass

    def on_disable(self):
        """Run every time the robot transitions to being disabled"""
        pass

    def set_pid(self, p, i, d):
        self.drive_motor_a.setControlMode(CANTalon.ControlMode.Position)
        self.drive_motor_b.setControlMode(CANTalon.ControlMode.Follower)
        self.drive_motor_c.setControlMode(CANTalon.ControlMode.Position)
        self.drive_motor_d.setControlMode(CANTalon.ControlMode.Follower)

        for motor in self.motors:
            motor.setPID(p, i, d)

        self.drive_motor_a.setFeedbackDevice(
            CANTalon.FeedbackDevice.QuadEncoder)
        self.drive_motor_c.setFeedbackDevice(
            CANTalon.FeedbackDevice.QuadEncoder)

    def set_point(self, meters):
        for motor in self.motors:
            motor.setPosition(0)

        self.setpoint = self.counts_per_revolution * \
            (self.rotations_per_meter * meters)

        self.drive_motor_a.set(self.setpoint)
        self.drive_motor_b.set(2)
        self.drive_motor_c.set(self.setpoint)
        self.drive_motor_d.set(4)

        return self.setpoint

    def turn(self, radians):
        for motor in self.motors:
            motor.setControlMode(CANTalon.ControlMode.PercentVbus)
        self.controller = PIDController(0.1, 0, 0, self.bno055.getAngle, self.turn_motors)
        self.controller.setInputRange(-math.pi, math.pi)
        self.controller.setTolerance(5)
        self.controller.setOutputRange(-1, 1)

        self.controller.setSetpoint(self.bno055.getAngle() + radians)
        self.controller.enable()

        return self.bno055.getAngle() + radians

    def turn_successful(self):
        if self.controller.onTarget():
            self.controller.disable()

        return self.controller.onTarget()

    def turn_motors(self, PIDOutput):
        # output = max(min(-1, PIDOutput), 1)
        print(self.controller.getError())
        output = PIDOutput
        self.drive_motor_a.set(output)
        self.drive_motor_b.set(output)
        self.drive_motor_c.set(-output)
        self.drive_motor_d.set(-output)

    def get_pos(self):
        return [self.drive_motor_a.getPosition(), self.drive_motor_c.getPosition]
       # return [self.drive_motor_a.getPosition()/self.counts_per_meter,
       #         -(self.drive_motor_c.getPosition()/self.counts_per_meter)]

    def get_velocities(self):
        return [self.drive_motor_a.getEncVelocity() / self.velocity_to_native_units,
                -self.drive_motor_c.getEncVelocity() / self.velocity_to_native_units]

    def get_vel(self):
        return (self.get_velocities()[0] + self.get_velocities()[1]) / 2

    def execute(self):
        """Run at the end of every control loop iteration"""

        # in this loop, we want to turn the list of inputs into
        # signals that we will pass to the motor controllers

        pass
