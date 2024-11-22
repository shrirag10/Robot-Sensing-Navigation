// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from imu_msgs:msg/IMUmsg.idl
// generated code does not contain a copyright notice

#ifndef IMU_MSGS__MSG__DETAIL__IM_UMSG__TRAITS_HPP_
#define IMU_MSGS__MSG__DETAIL__IM_UMSG__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "imu_msgs/msg/detail/im_umsg__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'imu'
#include "sensor_msgs/msg/detail/imu__traits.hpp"
// Member 'mag_field'
#include "sensor_msgs/msg/detail/magnetic_field__traits.hpp"

namespace imu_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const IMUmsg & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: imu
  {
    out << "imu: ";
    to_flow_style_yaml(msg.imu, out);
    out << ", ";
  }

  // member: mag_field
  {
    out << "mag_field: ";
    to_flow_style_yaml(msg.mag_field, out);
    out << ", ";
  }

  // member: raw
  {
    out << "raw: ";
    rosidl_generator_traits::value_to_yaml(msg.raw, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const IMUmsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: imu
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "imu:\n";
    to_block_style_yaml(msg.imu, out, indentation + 2);
  }

  // member: mag_field
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mag_field:\n";
    to_block_style_yaml(msg.mag_field, out, indentation + 2);
  }

  // member: raw
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "raw: ";
    rosidl_generator_traits::value_to_yaml(msg.raw, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const IMUmsg & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace imu_msgs

namespace rosidl_generator_traits
{

[[deprecated("use imu_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const imu_msgs::msg::IMUmsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  imu_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use imu_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const imu_msgs::msg::IMUmsg & msg)
{
  return imu_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<imu_msgs::msg::IMUmsg>()
{
  return "imu_msgs::msg::IMUmsg";
}

template<>
inline const char * name<imu_msgs::msg::IMUmsg>()
{
  return "imu_msgs/msg/IMUmsg";
}

template<>
struct has_fixed_size<imu_msgs::msg::IMUmsg>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<imu_msgs::msg::IMUmsg>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<imu_msgs::msg::IMUmsg>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // IMU_MSGS__MSG__DETAIL__IM_UMSG__TRAITS_HPP_
