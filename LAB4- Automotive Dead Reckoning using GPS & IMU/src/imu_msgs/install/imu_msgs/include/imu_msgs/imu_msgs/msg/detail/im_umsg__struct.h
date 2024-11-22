// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from imu_msgs:msg/IMUmsg.idl
// generated code does not contain a copyright notice

#ifndef IMU_MSGS__MSG__DETAIL__IM_UMSG__STRUCT_H_
#define IMU_MSGS__MSG__DETAIL__IM_UMSG__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'imu'
#include "sensor_msgs/msg/detail/imu__struct.h"
// Member 'mag_field'
#include "sensor_msgs/msg/detail/magnetic_field__struct.h"
// Member 'raw'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/IMUmsg in the package imu_msgs.
typedef struct imu_msgs__msg__IMUmsg
{
  std_msgs__msg__Header header;
  sensor_msgs__msg__Imu imu;
  sensor_msgs__msg__MagneticField mag_field;
  rosidl_runtime_c__String raw;
} imu_msgs__msg__IMUmsg;

// Struct for a sequence of imu_msgs__msg__IMUmsg.
typedef struct imu_msgs__msg__IMUmsg__Sequence
{
  imu_msgs__msg__IMUmsg * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} imu_msgs__msg__IMUmsg__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // IMU_MSGS__MSG__DETAIL__IM_UMSG__STRUCT_H_
