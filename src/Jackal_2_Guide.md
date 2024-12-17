# Jackal-2 connection guide
First connect to the Wi-Fi `jackal-2`:
password: syntheticfastorange
Check connection by typing:
```
ping 10.0.2.3
```
Connect to the robot control using
```
ssh ori@10.0.2.3
```
with the password: puzzle86thikazoo
See the bunch of rostopic here:
```
rostopic list
```
which you will get
```
/bluetooth_teleop/cmd_vel
/bluetooth_teleop/joy
/bluetooth_teleop/joy/set_feedback
/cmd_drive
/cmd_vel
/diagnostics
/diagnostics_agg
/diagnostics_toplevel_state
/e_stop
/feedback
/imu/data
/imu/data_raw
/imu/mag
/imu_filter/parameter_descriptions
/imu_filter/parameter_updates
/jackal_velocity_controller/cmd_vel
/jackal_velocity_controller/odom
/jackal_velocity_controller/parameter_descriptions
/jackal_velocity_controller/parameter_updates
/joint_states
/joy_teleop/cmd_vel
/navsat/fix
/navsat/heading
/navsat/nmea_sentence
/navsat/time_reference
/navsat/vel
/odometry/filtered
/rosout
/rosout_agg
/set_pose
/status
/tf
/tf_static
/twist_marker_server/cmd_vel
/twist_marker_server/feedback
/twist_marker_server/update
/twist_marker_server/update_full
/wifi_connected
```
For example
```
rostopic echo /imu/data_raw
header: 
  seq: 58447
  stamp: 
    secs: 1734434415
    nsecs: 371226487
  frame_id: "imu_link"
orientation: 
  x: 0.0
  y: 0.0
  z: 0.0
  w: 0.0
orientation_covariance: [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
angular_velocity: 
  x: 0.10953202344675951
  y: 0.09542279260863223
  z: -0.3368225936411965
angular_velocity_covariance: [1.218467815533586e-07, 0.0, 0.0, 0.0, 1.218467815533586e-07, 0.0, 0.0, 0.0, 1.218467815533586e-07]
linear_acceleration: 
  x: 0.40587362061531934
  y: 4.920296584126754
  z: 11.31733716301785
linear_acceleration_covariance: [8.661248102725949e-06, 0.0, 0.0, 0.0, 8.661248102725949e-06, 0.0, 0.0, 0.0, 8.661248102725949e-06]
```

Control the robot using the command:
```
rostopic pub /cmd_vel geometry_msgs/Twist "linear:
  x: 0.5
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0" 
```
