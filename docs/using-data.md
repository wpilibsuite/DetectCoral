# Using the Data

The Raspberry Pi writes all detection information to NetworkTables, which can be used by your robot code. Below is a Java example for parsing and using this data.
#### Network Tables Format
- The table containing all inference data is called `ML`.
- The following entries populate that table:
    1. `nb_objects`     -> the number (double) of detected objects in the current frame.
    2. `object_classes`  -> a string array of the class names of each object. These are in the same order as the coordinates.
    3. `boxes`        -> a double array containg the coordinates of every detected object. The coordinates are in the following format: [top_left__x1, top_left_y1, bottom_right_x1, bottom_right_y1, top_left_x2, top_left_y2, ... ]. There are four coordinates per box. A way to parse this array in Java is shown below.

The below `VisionSubsystem` Java class parses the data from NetworkTables and stores it in a usable way.

```java
/*----------------------------------------------------------------------------*/
/* Copyright (c) 2018 FIRST. All Rights Reserved.                             */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/

/*----------------------------------------------------------------------------*/
/* Copyright (c) 2018 FIRST. All Rights Reserved.                             */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/

/*----------------------------------------------------------------------------*/
/* Copyright (c) 2018 FIRST. All Rights Reserved.                             */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/

package frc.robot.subsystems;

import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj2.command.SubsystemBase;

public class VisionSubsystem extends SubsystemBase {
  private NetworkTable table;
  private int totalObjects = 0;
  public Cargo[] cargo = new Cargo[0];
  public Hatch[] hatches = new Hatch[0];
  public int totalCargo, totalHatches;
  private String[] classes;
  private double[] boxes, box;

  private abstract class Gamepiece {
    public double distance;
    public double xOffset;

    /**
     * Gets the relative angle of the game piece in radians
     * @return the angle
     */
    public double getAngle() {
      return Math.atan(xOffset / distance);
    }
  }

  /**
   * Represents a detected cargo from the Coral
   */
  public class Cargo extends Gamepiece{

    /**
     * Holds the data determined by Coral
     *
     * @param box the array of points
     */
    public Cargo(double[] box) {
      this.distance = 231.13 * Math.pow(box[3] - box[1], -1.303);
      this.xOffset = (160 - ((box[0] + box[2]) / 2)) / (((box[3] - box[1]) / 13.0) * 39.37);
    }
  }

  /**
   * Represents a detected hatch from the Coral
   */
  public class Hatch extends Gamepiece{

    /**
     * Holds the data determined by Coral
     *
     * @param box the array of points
     */
    public Hatch(double[] box) {
      this.distance = 289.67 * Math.pow(box[3] - box[1], -1.131);
      this.xOffset = (160 - ((box[0] + box[2]) / 2)) / (((box[3] - box[1]) / 19.5) * 39.37);
    }
  }

  public VisionSubsystem() {
    table = NetworkTableInstance.getDefault().getTable("ML");
  }

  /**
   * Periodically updates the list of detected objects with the data found on NetworkTables
   * Also creates array of cargo and their relative position.
   */
  @Override
  public void periodic() {
    totalCargo = 0;
    totalHatches = 0;
    totalObjects = (int) table.getEntry("nb_objects").getDouble(0);
    classes = table.getEntry("object_classes").getStringArray(new String[totalObjects]);
    boxes = table.getEntry("boxes").getDoubleArray(new double[4 * totalObjects]);
    // Count up number of cargo and hatches
    for (String s : classes) {
      if (s.equals("Cargo"))
        totalCargo++;
      if (s.equals("Hatchcover"))
        totalHatches++;
    }

    cargo = new Cargo[totalCargo];
    hatches = new Hatch[totalHatches];
    int cargoIndex = 0;
    int hatchIndex = 0;

    // Generate arrays of Cargo and Hatch objects
    for (int i = 0; i < totalObjects; i += 4) {
      box = new double[4];
      for (int j = 0; j < 4; j++) {
        box[j] = boxes[i + j];
      }
      if (classes[i].equals("Cargo")) {
        cargo[cargoIndex] = new Cargo(box);
        cargoIndex++;
      }
      if (classes[i].equals("Hatchcover")) {
        hatches[hatchIndex] = new Hatch(box);
        hatchIndex++;
      }
    }
  }
}
```

Using the arrays created by the `VisionSubsystem`, one can make a simple command to turn to face a game piece. In this example, a hatch is used. One thing to note is the ~15fps of inference attained by a Google Coral is not fast enough for PID input directly, however calculating the relative heading of a game piece and then turning to that heading works accurately.
```java
package frc.robot.commands;

import edu.wpi.first.wpilibj.controller.PIDController;
import edu.wpi.first.wpilibj2.command.PIDCommand;
import frc.robot.subsystems.DriveSubsystem;
import frc.robot.subsystems.VisionSubsystem;

/**
 * Command that turns the robot to face the first detected hatch
 */
public class TurnToHatchCommand extends PIDCommand {
  private VisionSubsystem visionSubsystem;
  private DriveSubsystem driveSubsystem;

  /**
   * PIDCommand uses relative hatch angle at time of initialization, not construction.
   * Turn is based on gyro.
   * @param driveSubsystem the drive subsystem
   * @param visionSubsystem the vision subsystem
   */
  public TurnToHatchCommand(DriveSubsystem driveSubsystem, VisionSubsystem visionSubsystem) {
    super(
        // Tune these values for your chassis
        new PIDController(1, 0, 0),
        // Gets the heading of the robot in radians as PID input
        () -> driveSubsystem.getGyroAngle().getRadians(),
        // 0 setpoint at construction, immediately overwritten at time of init
        0,
        // Turns with output
        (double value) -> driveSubsystem.drive(0, value, true),
        // Required subsystems
        driveSubsystem,
        visionSubsystem
    );
    this.driveSubsystem = driveSubsystem;
    this.visionSubsystem = visionSubsystem;
    // Set tolerance for PID
    getController().setTolerance(10, 5);
    // Using gyro heading in Radians, so continuous input
    getController().enableContinuousInput(-Math.PI, Math.PI);
  }

  /**
   * Sets setpoint at init
   */
  @Override
  public void initialize() {
    super.initialize();
    getController().setSetpoint(getHatchAngle());
  }

  @Override
  public boolean isFinished() {
    return getController().atSetpoint();
  }

  /**
   * Gets the angle of the hatch if there is one
   * @return angle of hatch
   */
  public double getHatchAngle() {
    if (visionSubsystem.totalHatches > 0) {
      return visionSubsystem.hatches[0].getAngle();
    }
    // return current drivetrain angle if no hatch detected, so no turning
    return driveSubsystem.getGyroAngle().getRadians();
  }
}
```