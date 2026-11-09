package frc.robot;

import edu.wpi.first.wpilibj2.command.CommandScheduler;
import lib.ironpulse.utils.PhoenixUtils;
import lib.ntext.NTParameterRegistry;
import org.littletonrobotics.junction.LoggedRobot;
import org.littletonrobotics.junction.Logger;
import org.littletonrobotics.junction.networktables.NT4Publisher;

public class Robot extends LoggedRobot {
    private final RobotContainer robotContainer;

    public Robot() {
        super(0.02);
        Logger.addDataReceiver(new NT4Publisher());
        Logger.start();
        robotContainer = new RobotContainer();
    }

    @Override
    public void robotPeriodic() {
        NTParameterRegistry.refresh();
        PhoenixUtils.refreshAll();
        CommandScheduler.getInstance().run();
    }
}
