# this is the chassis class, a good example of a component. it is a
# bit special in that it has to take direct numerical input from the
# joystick (which is achieved by changing the 'input' variable, which
# is a list composed of [vx, vy, vz, throttle]) but is a good example
# of what a component should look like.
from ctre import CANTalon
import math


class Chassis:

    drive_motor_a = CANTalon
    drive_motor_b = CANTalon
    drive_motor_c = CANTalon
    drive_motor_d = CANTalon
    motors = [drive_motor_a, drive_motor_b, drive_motor_c, drive_motor_d]

    inches_to_meters = 0.0254
    # some calculations that provide numbers used by the motion profiling
    wheel_circumference = 6*inches_to_meters*math.pi
    rotations_per_meter = 1 / wheel_circumference
    counts_per_revolution = 1440
    velocity_to_native_units = 0.1*counts_per_meter


    def __init__(self):
        super().__init__()
        self.inputs = [0.0 for x in range(4)]

    def setup(self):
        """Run just after createObjects.
        Useful if you want to run something after just once after the
        robot code is started, that depends on injected variables"""

    def on_enable(self):
        """Run every time the robot transitions to being enabled"""
        pass

    def on_disable(self):
        """Run every time the robot transitions to being disabled"""
        pass

    def set_pid(self):
        self.drive_motor_a.setControlMode(CANTalon.ControlMode.Position)
        self.drive_motor_b.setControlMode(CANTalon.ControlMode.Follower)
        self.drive_motor_c.setControlMode(CANTalon.ControlMode.Position)
        self.drive_motor_d.setControlMode(CANTalon.ControlMode.Follower)

        for motor in self.motors:
            self.motor.setPID(6, 0.3, 1)

        self.drive_motor_a.setFeedbackDevice(CANTalon.FeedbackDevice.QuadEncoder)
        self.drive_motor_c.setFeedbackDevice(CANTalon.FeedbackDevice.QuadEncoder)

    def set_point(self, meters):
        for motor in self.motors:
            self.motor.setPosition(0)

        self.setpoint = self.counts_per_revolution * (self.rotations_per_meter * meters)

        self.drive_motor_a.set(self.set_point)
        self.drive_motor_b.set(2)
        self.drive_motor_c.set(self.set_point)
        self.drive_motor_d.set(4)

        return self.setpoint

    def get_pos(self):
    return [self.drive_motor_a.getPosition()/self.counts_per_meter,
                -(self.drive_motor_c.getPosition()/self.counts_per_meter)]

    def get_velocities(self):
        return [self.drive_motor_a.getEncVelocity()/self.velocity_to_native_units,
                -self.drive_motor_c.getEncVelocity()/self.velocity_to_native_units]

    def get_vel(self):
        return (self.get_velocities()[0]+self.get_velocities()[1])/2

    def execute(self):
        """Run at the end of every control loop iteration"""

        # in this loop, we want to turn the list of inputs into
        # signals that we will pass to the motor controllers

        pass
