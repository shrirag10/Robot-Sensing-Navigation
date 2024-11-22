// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from gps_msgs:msg/GPSmsg.idl
// generated code does not contain a copyright notice

#ifndef GPS_MSGS__MSG__DETAIL__GP_SMSG__BUILDER_HPP_
#define GPS_MSGS__MSG__DETAIL__GP_SMSG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "gps_msgs/msg/detail/gp_smsg__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace gps_msgs
{

namespace msg
{

namespace builder
{

class Init_GPSmsg_letter
{
public:
  explicit Init_GPSmsg_letter(::gps_msgs::msg::GPSmsg & msg)
  : msg_(msg)
  {}
  ::gps_msgs::msg::GPSmsg letter(::gps_msgs::msg::GPSmsg::_letter_type arg)
  {
    msg_.letter = std::move(arg);
    return std::move(msg_);
  }

private:
  ::gps_msgs::msg::GPSmsg msg_;
};

class Init_GPSmsg_zone
{
public:
  explicit Init_GPSmsg_zone(::gps_msgs::msg::GPSmsg & msg)
  : msg_(msg)
  {}
  Init_GPSmsg_letter zone(::gps_msgs::msg::GPSmsg::_zone_type arg)
  {
    msg_.zone = std::move(arg);
    return Init_GPSmsg_letter(msg_);
  }

private:
  ::gps_msgs::msg::GPSmsg msg_;
};

class Init_GPSmsg_utm_northing
{
public:
  explicit Init_GPSmsg_utm_northing(::gps_msgs::msg::GPSmsg & msg)
  : msg_(msg)
  {}
  Init_GPSmsg_zone utm_northing(::gps_msgs::msg::GPSmsg::_utm_northing_type arg)
  {
    msg_.utm_northing = std::move(arg);
    return Init_GPSmsg_zone(msg_);
  }

private:
  ::gps_msgs::msg::GPSmsg msg_;
};

class Init_GPSmsg_utm_easting
{
public:
  explicit Init_GPSmsg_utm_easting(::gps_msgs::msg::GPSmsg & msg)
  : msg_(msg)
  {}
  Init_GPSmsg_utm_northing utm_easting(::gps_msgs::msg::GPSmsg::_utm_easting_type arg)
  {
    msg_.utm_easting = std::move(arg);
    return Init_GPSmsg_utm_northing(msg_);
  }

private:
  ::gps_msgs::msg::GPSmsg msg_;
};

class Init_GPSmsg_altitude
{
public:
  explicit Init_GPSmsg_altitude(::gps_msgs::msg::GPSmsg & msg)
  : msg_(msg)
  {}
  Init_GPSmsg_utm_easting altitude(::gps_msgs::msg::GPSmsg::_altitude_type arg)
  {
    msg_.altitude = std::move(arg);
    return Init_GPSmsg_utm_easting(msg_);
  }

private:
  ::gps_msgs::msg::GPSmsg msg_;
};

class Init_GPSmsg_longitude
{
public:
  explicit Init_GPSmsg_longitude(::gps_msgs::msg::GPSmsg & msg)
  : msg_(msg)
  {}
  Init_GPSmsg_altitude longitude(::gps_msgs::msg::GPSmsg::_longitude_type arg)
  {
    msg_.longitude = std::move(arg);
    return Init_GPSmsg_altitude(msg_);
  }

private:
  ::gps_msgs::msg::GPSmsg msg_;
};

class Init_GPSmsg_latitude
{
public:
  explicit Init_GPSmsg_latitude(::gps_msgs::msg::GPSmsg & msg)
  : msg_(msg)
  {}
  Init_GPSmsg_longitude latitude(::gps_msgs::msg::GPSmsg::_latitude_type arg)
  {
    msg_.latitude = std::move(arg);
    return Init_GPSmsg_longitude(msg_);
  }

private:
  ::gps_msgs::msg::GPSmsg msg_;
};

class Init_GPSmsg_header
{
public:
  Init_GPSmsg_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GPSmsg_latitude header(::gps_msgs::msg::GPSmsg::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_GPSmsg_latitude(msg_);
  }

private:
  ::gps_msgs::msg::GPSmsg msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::gps_msgs::msg::GPSmsg>()
{
  return gps_msgs::msg::builder::Init_GPSmsg_header();
}

}  // namespace gps_msgs

#endif  // GPS_MSGS__MSG__DETAIL__GP_SMSG__BUILDER_HPP_
