package frc.robot;

import lib.ntext.NTParameter;

@NTParameter(tableName = "Params/SwerveModule")
public final class SwerveModuleParams {
    public static final class Drive {
        static final double kP = 6.0;
        static final double kI = 0.0;
        static final double kD = 0.0;
        static final double kS = 0.0;
        static final double kV = 0.0;
        static final double kA = 0.0;
    }

    public static final class Steer {
        static final double kP = 0.0;
        static final double kI = 0.0;
        static final double kD = 0.0;
        static final double kS = 0.0;
    }
}
