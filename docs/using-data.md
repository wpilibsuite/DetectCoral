
#### Network Tables
- The table containing all inference data is called `ML`.
- The following entries populate that table:
1. `nb_objects`     -> the number (double) of detected objects in the current frame.
2. `object_classes`  -> a string array of the class names of each object. These are in the same order as the coordinates.
3. `boxes`        -> a double array containg the coordinates of every detected object. The coordinates are in the following format: [top_left__x1, top_left_y1, bottom_right_x1, bottom_right_y1, top_left_x2, top_left_y2, ... ]. There are four coordinates per box. A way to parse this array in Java is shown below.
```java
NetworkTable table = NetworkTableInstance.getDefault().getTable("ML");
int totalObjects = (int) table.getEntry("nb_boxes").getDouble(0);
String[] names = table.getEntry("boxes_names").getStringArray(new String[totalObjects]);
double[] boxArray = table.getEntry("boxes").getDoubleArray(new double[totalObjects*4]);
double[][][] objects = new double[totalObjects][2][2]; // array of pairs of coordinates, each pair is an object
for (int i = 0; i < totalObjects; i++) {
    for (int pair = 0; pair < 2; pair++) {
        for (int j = 0; j < 2; j++)
            objects[i][pair][j] = boxArray[totalObjects*4 + pair*2 + j];
    }
}
```

##### Using these values
Here is an example of how to use the bounding box coordinates to determine the angle and distance of the game piece relative to the robot.
```java
String target = "cargo"; // we want to find the first cargo in the array. We recommend sorting the array but width of gamepiece, to find the closest piece.
int index = -1;
for (int i = 0; i < totalObjects; i++) {
    if (names[i].equals(cargo)) {
        index = i;
        break;
    }
}
double angle = 0, distance = 0;
if (index != -1) { // a cargo is detected
    double x1 = objects[index][0][0], x2 = objects[index][1][0];
    /* The following equations were made using a spreadsheet and finding a trendline.
     * They are designed to work with a Microsoft Lifecam 3000 with a 320x240 image output.
     * If you are using different sized images or a different camera, you will/may need to create your own function.
     */
    distance = (((x1 + x2)/2-160)/((x1 - x2)/19.5))/12;
    angle = (9093.75/(Math.pow((x2-x1),Math.log(54/37.41/29))))/12;
}
drivetrain.turnTo(angle);
drivetrain.driveFor(distance);
```