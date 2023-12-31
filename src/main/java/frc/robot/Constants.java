package frc.robot;

public final class Constants {
    public static final class JoystickContants {
        public static final int kJoystick = 0;
    }

    public static final class LiftConstants {
        public static final int kMotor = 1;

        public static final double kCircumferenceOfWheelInMeters = 6.0;
        public static final double kGearRatio = 1 / 4;
        public static final double kRotationsToMeters = kCircumferenceOfWheelInMeters * kGearRatio;
        
        public static final double kMaxHeight = 1.5;
        public static final double kMinHeight = 0.0;
        public static final class LiftPidConstants {
            public static final double kMaxVelocity = 1.75;
            public static final double kMaxAcceleration = 0.75;

            public static final double kP = 1.3;
            public static final double kI = 0.0;
            public static final double kD = 0.7;
        }
    }
}
