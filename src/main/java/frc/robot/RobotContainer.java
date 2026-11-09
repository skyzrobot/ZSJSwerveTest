package frc.robot;

import static edu.wpi.first.units.Units.*;

import edu.wpi.first.wpilibj2.command.Commands;
import edu.wpi.first.wpilibj2.command.button.CommandXboxController;
import frc.robot.subsystems.SwerveSubsystem;

public class RobotContainer {
    private final SwerveSubsystem swerve = new SwerveSubsystem();
    private final CommandXboxController controller =
            new CommandXboxController(Constants.kDriverControllerPort);

    public RobotContainer() {
        swerve.setDefaultCommand(Commands.run(this::driveWithJoystick, swerve));
    }

    private void driveWithJoystick() {
        double maxSpeed = Constants.kSwerveLimit.maxLinearVelocity().in(MetersPerSecond);
        double maxOmega = Constants.kSwerveLimit.maxAngularVelocity().in(RadiansPerSecond);
        double x = -controller.getLeftY() * maxSpeed;
        double y = -controller.getLeftX() * maxSpeed;
        double omega = -controller.getRightX() * maxOmega;
        swerve.driveFieldRelative(x, y, omega);
    }

    public SwerveSubsystem getSwerve() {
        return swerve;
    }
}
