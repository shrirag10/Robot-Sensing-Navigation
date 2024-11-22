// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from gps_msgs:msg/GPSmsg.idl
// generated code does not contain a copyright notice

#ifndef GPS_MSGS__MSG__DETAIL__GP_SMSG__STRUCT_HPP_
#define GPS_MSGS__MSG__DETAIL__GP_SMSG__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__gps_msgs__msg__GPSmsg __attribute__((deprecated))
#else
# define DEPRECATED__gps_msgs__msg__GPSmsg __declspec(deprecated)
#endif

namespace gps_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct GPSmsg_
{
  using Type = GPSmsg_<ContainerAllocator>;

  explicit GPSmsg_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->latitude = 0.0;
      this->longitude = 0.0;
      this->altitude = 0.0;
      this->utm_easting = 0.0;
      this->utm_northing = 0.0;
      this->zone = 0l;
      this->letter = "";
    }
  }

  explicit GPSmsg_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    letter(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->latitude = 0.0;
      this->longitude = 0.0;
      this->altitude = 0.0;
      this->utm_easting = 0.0;
      this->utm_northing = 0.0;
      this->zone = 0l;
      this->letter = "";
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _latitude_type =
    double;
  _latitude_type latitude;
  using _longitude_type =
    double;
  _longitude_type longitude;
  using _altitude_type =
    double;
  _altitude_type altitude;
  using _utm_easting_type =
    double;
  _utm_easting_type utm_easting;
  using _utm_northing_type =
    double;
  _utm_northing_type utm_northing;
  using _zone_type =
    int32_t;
  _zone_type zone;
  using _letter_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _letter_type letter;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__latitude(
    const double & _arg)
  {
    this->latitude = _arg;
    return *this;
  }
  Type & set__longitude(
    const double & _arg)
  {
    this->longitude = _arg;
    return *this;
  }
  Type & set__altitude(
    const double & _arg)
  {
    this->altitude = _arg;
    return *this;
  }
  Type & set__utm_easting(
    const double & _arg)
  {
    this->utm_easting = _arg;
    return *this;
  }
  Type & set__utm_northing(
    const double & _arg)
  {
    this->utm_northing = _arg;
    return *this;
  }
  Type & set__zone(
    const int32_t & _arg)
  {
    this->zone = _arg;
    return *this;
  }
  Type & set__letter(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->letter = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    gps_msgs::msg::GPSmsg_<ContainerAllocator> *;
  using ConstRawPtr =
    const gps_msgs::msg::GPSmsg_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<gps_msgs::msg::GPSmsg_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<gps_msgs::msg::GPSmsg_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      gps_msgs::msg::GPSmsg_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<gps_msgs::msg::GPSmsg_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      gps_msgs::msg::GPSmsg_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<gps_msgs::msg::GPSmsg_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<gps_msgs::msg::GPSmsg_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<gps_msgs::msg::GPSmsg_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__gps_msgs__msg__GPSmsg
    std::shared_ptr<gps_msgs::msg::GPSmsg_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__gps_msgs__msg__GPSmsg
    std::shared_ptr<gps_msgs::msg::GPSmsg_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GPSmsg_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->latitude != other.latitude) {
      return false;
    }
    if (this->longitude != other.longitude) {
      return false;
    }
    if (this->altitude != other.altitude) {
      return false;
    }
    if (this->utm_easting != other.utm_easting) {
      return false;
    }
    if (this->utm_northing != other.utm_northing) {
      return false;
    }
    if (this->zone != other.zone) {
      return false;
    }
    if (this->letter != other.letter) {
      return false;
    }
    return true;
  }
  bool operator!=(const GPSmsg_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GPSmsg_

// alias to use template instance with default allocator
using GPSmsg =
  gps_msgs::msg::GPSmsg_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace gps_msgs

#endif  // GPS_MSGS__MSG__DETAIL__GP_SMSG__STRUCT_HPP_
