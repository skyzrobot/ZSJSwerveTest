package frc.robot.subsystems;

import static edu.wpi.first.units.Units.*;

import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.kinematics.ChassisSpeeds;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import frc.robot.Constants;
import lib.ironpulse.swerve.Swerve;
import lib.ironpulse.swerve.SwerveConfig;
import lib.ironpulse.swerve.mk5n.ImuIOPigeon;
import lib.ironpulse.swerve.mk5n.SwerveMK5NConfig;
import lib.ironpulse.swerve.mk5n.SwerveModuleIOMK5N;

public class SwerveSubsystem extends SubsystemBase {
    private final Swerve swerve;

    public SwerveSubsystem() {
        SwerveMK5NConfig config = buildConfig();

        SwerveModuleIOMK5N[] moduleIOs = new SwerveModuleIOMK5N[config.moduleCount()];
        for (int i = 0; i < moduleIOs.length; i++) {
            moduleIOs[i] = new SwerveModuleIOMK5N(config, i);
        }
        SwerveModuleIOMK5N.startSyncThread();

        swerve = new Swerve(config, new ImuIOPigeon(config, Constants.kPigeonConfig), moduleIOs);
    }

    public void driveFieldRelative(double vxMps, double vyMps, double omegaRadPerSec) {
        swerve.runTwist(
                ChassisSpeeds.fromFieldRelativeSpeeds(
                        vxMps, vyMps, omegaRadPerSec, getRotation()));
    }

    public void driveRobotRelative(ChassisSpeeds speeds) {
        swerve.runTwist(speeds);
    }

    public void stop() {
        swerve.runStop();
    }

    public Pose3d getPose() {
        return swerve.getEstimatedPose();
    }

    public void resetPose(Pose3d pose) {
        swerve.resetEstimatedPose(pose);
    }

    public ChassisSpeeds getChassisSpeeds() {
        return swerve.getChassisSpeeds();
    }

    public Rotation2d getRotation() {
        return swerve.getEstimatedPose().getRotation().toRotation2d();
    }

    public Swerve getSwerve() {
        return swerve;
    }

    private static SwerveMK5NConfig buildConfig() {
        SwerveConfig.SwerveModuleConfig[] moduleConfigs =
                new SwerveConfig.SwerveModuleConfig[Constants.kModules.length];
        for (int i = 0; i < moduleConfigs.length; i++) {
            Constants.ModuleConfig module = Constants.kModules[i];
            moduleConfigs[i] =
                    SwerveConfig.SwerveModuleConfig.builder()
                            .name(module.name())
                            .location(module.location())
                            .driveMotorId(module.driveId())
                            .steerMotorId(module.steerId())
                            .encoderId(module.encoderId())
                            .steerMotorEncoderOffset(module.encoderOffset())
                            .driveInverted(module.driveInverted())
                            .steerInverted(module.steerInverted())
                            .encoderInverted(false)
                            .build();
        }

        return SwerveMK5NConfig.builder()
                .name(Constants.kSwerveName)
                .dtS(Constants.kDtSeconds)
                .wheelDiameter(Constants.kWheelDiameter)
                .driveGearRatio(Constants.kDriveGearRatio)
                .steerGearRatio(Constants.kSteerGearRatio)
                .driveMotorKt(Constants.kDriveMotorKt)
                .driveMass(Constants.kRobotMass)
                .pigeonConfig(Constants.kPigeonConfig)
                .defaultSwerveLimit(Constants.kSwerveLimit)
                .defaultSwerveModuleLimit(Constants.kModuleLimit)
                .moduleConfigs(moduleConfigs)
                .driveStatorCurrentLimit(Constants.kDriveStatorCurrentLimit)
                .steerStatorCurrentLimit(Constants.kSteerStatorCurrentLimit)
                .driveSupplyCurrentLimit(Constants.kDriveSupplyCurrentLimit)
                .steerSupplyCurrentLimit(Constants.kSteerSupplyCurrentLimit)
                .odometryFrequency(Constants.kOdometryFrequency)
                .canivoreCanBus(Constants.kBus)
                .pigeonId(Constants.kPigeon)
                .build();
    }
}
