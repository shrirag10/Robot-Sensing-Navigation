// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from imu_msgs:msg/IMUmsg.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "imu_msgs/msg/detail/im_umsg__rosidl_typesupport_introspection_c.h"
#include "imu_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "imu_msgs/msg/detail/im_umsg__functions.h"
#include "imu_msgs/msg/detail/im_umsg__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `imu`
#include "sensor_msgs/msg/imu.h"
// Member `imu`
#include "sensor_msgs/msg/detail/imu__rosidl_typesupport_introspection_c.h"
// Member `mag_field`
#include "sensor_msgs/msg/magnetic_field.h"
// Member `mag_field`
#include "sensor_msgs/msg/detail/magnetic_field__rosidl_typesupport_introspection_c.h"
// Member `raw`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  imu_msgs__msg__IMUmsg__init(message_memory);
}

void imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_fini_function(void * message_memory)
{
  imu_msgs__msg__IMUmsg__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_message_member_array[4] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(imu_msgs__msg__IMUmsg, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "imu",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(imu_msgs__msg__IMUmsg, imu),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "mag_field",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(imu_msgs__msg__IMUmsg, mag_field),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "raw",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(imu_msgs__msg__IMUmsg, raw),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_message_members = {
  "imu_msgs__msg",  // message namespace
  "IMUmsg",  // message name
  4,  // number of fields
  sizeof(imu_msgs__msg__IMUmsg),
  imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_message_member_array,  // message members
  imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_init_function,  // function to initialize message memory (memory has to be allocated)
  imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_message_type_support_handle = {
  0,
  &imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_imu_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, imu_msgs, msg, IMUmsg)() {
  imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, Imu)();
  imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, MagneticField)();
  if (!imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_message_type_support_handle.typesupport_identifier) {
    imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &imu_msgs__msg__IMUmsg__rosidl_typesupport_introspection_c__IMUmsg_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
