// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from imu_msgs:msg/IMUmsg.idl
// generated code does not contain a copyright notice

#ifndef IMU_MSGS__MSG__DETAIL__IM_UMSG__BUILDER_HPP_
#define IMU_MSGS__MSG__DETAIL__IM_UMSG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "imu_msgs/msg/detail/im_umsg__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace imu_msgs
{

namespace msg
{

namespace builder
{

class Init_IMUmsg_raw
{
public:
  explicit Init_IMUmsg_raw(::imu_msgs::msg::IMUmsg & msg)
  : msg_(msg)
  {}
  ::imu_msgs::msg::IMUmsg raw(::imu_msgs::msg::IMUmsg::_raw_type arg)
  {
    msg_.raw = std::move(arg);
    return std::move(msg_);
  }

private:
  ::imu_msgs::msg::IMUmsg msg_;
};

class Init_IMUmsg_mag_field
{
public:
  explicit Init_IMUmsg_mag_field(::imu_msgs::msg::IMUmsg & msg)
  : msg_(msg)
  {}
  Init_IMUmsg_raw mag_field(::imu_msgs::msg::IMUmsg::_mag_field_type arg)
  {
    msg_.mag_field = std::move(arg);
    return Init_IMUmsg_raw(msg_);
  }

private:
  ::imu_msgs::msg::IMUmsg msg_;
};

class Init_IMUmsg_imu
{
public:
  explicit Init_IMUmsg_imu(::imu_msgs::msg::IMUmsg & msg)
  : msg_(msg)
  {}
  Init_IMUmsg_mag_field imu(::imu_msgs::msg::IMUmsg::_imu_type arg)
  {
    msg_.imu = std::move(arg);
    return Init_IMUmsg_mag_field(msg_);
  }

private:
  ::imu_msgs::msg::IMUmsg msg_;
};

class Init_IMUmsg_header
{
public:
  Init_IMUmsg_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_IMUmsg_imu header(::imu_msgs::msg::IMUmsg::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_IMUmsg_imu(msg_);
  }

private:
  ::imu_msgs::msg::IMUmsg msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::imu_msgs::msg::IMUmsg>()
{
  return imu_msgs::msg::builder::Init_IMUmsg_header();
}

}  // namespace imu_msgs

#endif  // IMU_MSGS__MSG__DETAIL__IM_UMSG__BUILDER_HPP_
