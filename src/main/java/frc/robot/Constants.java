package frc.robot;

import static edu.wpi.first.units.Units.*;

import com.ctre.phoenix6.CANBus;
import edu.wpi.first.math.geometry.Translation2d;
import edu.wpi.first.units.measure.Angle;
import edu.wpi.first.units.measure.Current;
import edu.wpi.first.units.measure.Distance;
import edu.wpi.first.units.measure.Frequency;
import edu.wpi.first.units.measure.Mass;
import lib.ironpulse.swerve.ImuPigeonConfig;
import lib.ironpulse.swerve.SwerveLimit;
import lib.ironpulse.swerve.SwerveModuleLimit;

public final class Constants {
    private Constants() {}

    public static final String kSwerveName = "Swerve";

    public static final int kDriverControllerPort = 0;

    public static final int kFrontLeftDrive = 0;
    public static final int kFrontLeftSteer = 1;
    public static final int kFrontRightDrive = 2;
    public static final int kFrontRightSteer = 3;
    public static final int kBackLeftDrive = 4;
    public static final int kBackLeftSteer = 5;
    public static final int kBackRightDrive = 6;
    public static final int kBackRightSteer = 7;

    public static final int kFrontLeftEncoder = 8;
    public static final int kFrontRightEncoder = 9;
    public static final int kBackLeftEncoder = 10;
    public static final int kBackRightEncoder = 11;

    public static final int kPigeon = 20;
    public static final CANBus kBus = CANBus.roboRIO();

    public static final double kDtSeconds = 0.02;
    public static final Frequency kOdometryFrequency = Hertz.of(100.0);

    public static final Distance kWheelDiameter = Inches.of(4.0);
    public static final double kDriveGearRatio = 6.03;
    public static final double kSteerGearRatio = 26.09;
    public static final double kDriveMotorKt = 0.0194;
    public static final Mass kRobotMass = Kilograms.of(60.0);

    public static final double kHalfWheelBaseMeters = 0.30;
    public static final double kHalfTrackWidthMeters = 0.30;

    public static final Current kDriveStatorCurrentLimit = Amps.of(80.0);
    public static final Current kDriveSupplyCurrentLimit = Amps.of(60.0);
    public static final Current kSteerStatorCurrentLimit = Amps.of(40.0);
    public static final Current kSteerSupplyCurrentLimit = Amps.of(30.0);

    public static final ImuPigeonConfig kPigeonConfig = ImuPigeonConfig.builder().build();

    public static final SwerveLimit kSwerveLimit =
            SwerveLimit.builder()
                    .maxLinearVelocity(MetersPerSecond.of(4.6))
                    .maxSkidAcceleration(MetersPerSecondPerSecond.of(12.0))
                    .maxBrakeAcceleration(MetersPerSecondPerSecond.of(14.0))
                    .maxAngularVelocity(RadiansPerSecond.of(9.0))
                    .maxAngularAcceleration(RadiansPerSecondPerSecond.of(36.0))
                    .build();

    public static final SwerveModuleLimit kModuleLimit =
            SwerveModuleLimit.builder()
                    .maxDriveVelocity(MetersPerSecond.of(5.0))
                    .maxDriveAcceleration(MetersPerSecondPerSecond.of(30.0))
                    .maxDriveDeceleration(MetersPerSecondPerSecond.of(35.0))
                    .maxSteerAngularVelocity(RadiansPerSecond.of(24.0))
                    .maxSteerAngularAcceleration(RadiansPerSecondPerSecond.of(240.0))
                    .build();

    public record ModuleConfig(
            String name,
            Translation2d location,
            int driveId,
            int steerId,
            int encoderId,
            Angle encoderOffset,
            boolean driveInverted,
            boolean steerInverted) {}

    public static final ModuleConfig kFrontLeftModule =
            new ModuleConfig(
                    "FrontLeft",
                    new Translation2d(kHalfWheelBaseMeters, kHalfTrackWidthMeters),
                    kFrontLeftDrive,
                    kFrontLeftSteer,
                    kFrontLeftEncoder,
                    Rotations.of(0.0),
                    false,
                    false);

    public static final ModuleConfig kFrontRightModule =
            new ModuleConfig(
                    "FrontRight",
                    new Translation2d(kHalfWheelBaseMeters, -kHalfTrackWidthMeters),
                    kFrontRightDrive,
                    kFrontRightSteer,
                    kFrontRightEncoder,
                    Rotations.of(0.0),
                    false,
                    false);

    public static final ModuleConfig kBackLeftModule =
            new ModuleConfig(
                    "BackLeft",
                    new Translation2d(-kHalfWheelBaseMeters, kHalfTrackWidthMeters),
                    kBackLeftDrive,
                    kBackLeftSteer,
                    kBackLeftEncoder,
                    Rotations.of(0.0),
                    false,
                    false);

    public static final ModuleConfig kBackRightModule =
            new ModuleConfig(
                    "BackRight",
                    new Translation2d(-kHalfWheelBaseMeters, -kHalfTrackWidthMeters),
                    kBackRightDrive,
                    kBackRightSteer,
                    kBackRightEncoder,
                    Rotations.of(0.0),
                    false,
                    false);

    public static final ModuleConfig[] kModules = {
        kFrontLeftModule, kFrontRightModule, kBackLeftModule, kBackRightModule
    };
}
