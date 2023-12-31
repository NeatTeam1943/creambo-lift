package frc.robot.subsystems;

import com.revrobotics.CANSparkMax;
import com.revrobotics.RelativeEncoder;
import com.revrobotics.CANSparkMaxLowLevel.MotorType;

import edu.wpi.first.math.controller.ProfiledPIDController;
import edu.wpi.first.math.trajectory.TrapezoidProfile;
import edu.wpi.first.wpilibj.XboxController;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import frc.robot.LiftUtils;
import frc.robot.Constants.JoystickContants;
import frc.robot.Constants.LiftConstants;
import frc.robot.Constants.LiftConstants.LiftPidConstants;

public class Lift extends SubsystemBase {
  private CANSparkMax m_motor;
  private RelativeEncoder m_encoder;

  private TrapezoidProfile.Constraints m_constraints;
  private final ProfiledPIDController m_controller;

  private XboxController m_joystick;

  public Lift() {
    m_joystick = new XboxController(JoystickContants.kJoystick);

    m_motor = new CANSparkMax(LiftConstants.kMotor, MotorType.kBrushless);
    m_encoder = m_motor.getEncoder();

    LiftUtils.ResetEncoder(m_encoder);
    m_encoder.setPositionConversionFactor(LiftConstants.kRotationsToMeters);

    m_constraints = new TrapezoidProfile.Constraints(LiftPidConstants.kMaxVelocity, LiftPidConstants.kMaxAcceleration);

    m_controller = new ProfiledPIDController(LiftPidConstants.kP, LiftPidConstants.kI, LiftPidConstants.kD,
        m_constraints);
  }

  @Override
  public void periodic() {
    if (m_joystick.getRightBumper()){
      m_controller.setGoal(LiftConstants.kMaxHeight);
    }
    
    else if (m_joystick.getLeftBumper()){
      m_controller.setGoal(LiftConstants.kMinHeight);
    }

    m_motor.set(m_controller.calculate(m_encoder.getPosition()));
  }
}
