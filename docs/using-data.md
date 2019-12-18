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

package frc.robot.subsystems;

import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj2.command.SubsystemBase;

public class VisionSubsystem extends SubsystemBase {
    /**
    * Represents a detected game object from the Coral
    */
    public class GameObject {
        String name;
        double heading;
        double distance;
        
        /**
        * Holds the data determined by Coral
        * @param name
        * @param heading
        * @param distance
        */
        public GameObject(String name, double heading, double distance) {
            this.name = name;
            this.heading = heading;
            this.distance = distance;
        }
    }
        
    NetworkTable table;
    int totalObjects;
    GameObject[] gameObjects;
    private String[] classes;
    private double[] boxes, box;
    
    public VisionSubsystem() {
        table = NetworkTableInstance.getDefault().getTable("ML");
    }
    
    /**
    * Periodically updates the list of detected objects with the data found on NetworkTables
    */
    @Override
    public void periodic() {
        totalObjects = (int) table.getEntry("nb_objects").getNumber(0);
        gameObjects = new GameObject[totalObjects];
        classes = table.getEntry("object_classes").getStringArray(new String[totalObjects]);
        boxes = table.getEntry("boxes").getDoubleArray(new double[4 * totalObjects]);
        for (int i = 0; i < totalObjects; i += 4) {
            for (int j = 0; j < 4; j++) {
                box[j] = boxes[i + j];
            }
            gameObjects[i] = new GameObject(classes[i], getHeading(box), getDistance(box));
        }
    }
    
    /**
    * Gets the heading of the given object relative to the robot, in degrees
    * @param box the bounding box of a detected object
    * @return the heading of the detected object relative to the robot, in degrees
    */
    private double getHeading(double[] box) {
        return 757.8125 / (Math.pow(Math.abs(box[2] - box[0]), -1.303));
    }
    
    /**
    * Gets the distance of the given object relative to the robot, in inches
    * @param box the bounding box of a detected object
    * @return the distance of the detected object relative to the robot, in inches
    */
    private double getDistance(double[] box) {
        return (((box[0] + box[2]) / 2.0 - 160) / (Math.abs(box[2] - box[0]) / 19.5)) / 12.0;
    }
}
```