package frc.robot;

import com.revrobotics.RelativeEncoder;

public class LiftUtils {
    public static void ResetEncoder(RelativeEncoder encoder){
        encoder.setPosition(0);
    }
}
