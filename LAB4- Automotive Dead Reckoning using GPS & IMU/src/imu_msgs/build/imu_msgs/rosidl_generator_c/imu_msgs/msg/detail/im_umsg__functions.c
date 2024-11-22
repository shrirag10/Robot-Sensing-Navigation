// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from imu_msgs:msg/IMUmsg.idl
// generated code does not contain a copyright notice
#include "imu_msgs/msg/detail/im_umsg__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `imu`
#include "sensor_msgs/msg/detail/imu__functions.h"
// Member `mag_field`
#include "sensor_msgs/msg/detail/magnetic_field__functions.h"
// Member `raw`
#include "rosidl_runtime_c/string_functions.h"

bool
imu_msgs__msg__IMUmsg__init(imu_msgs__msg__IMUmsg * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    imu_msgs__msg__IMUmsg__fini(msg);
    return false;
  }
  // imu
  if (!sensor_msgs__msg__Imu__init(&msg->imu)) {
    imu_msgs__msg__IMUmsg__fini(msg);
    return false;
  }
  // mag_field
  if (!sensor_msgs__msg__MagneticField__init(&msg->mag_field)) {
    imu_msgs__msg__IMUmsg__fini(msg);
    return false;
  }
  // raw
  if (!rosidl_runtime_c__String__init(&msg->raw)) {
    imu_msgs__msg__IMUmsg__fini(msg);
    return false;
  }
  return true;
}

void
imu_msgs__msg__IMUmsg__fini(imu_msgs__msg__IMUmsg * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // imu
  sensor_msgs__msg__Imu__fini(&msg->imu);
  // mag_field
  sensor_msgs__msg__MagneticField__fini(&msg->mag_field);
  // raw
  rosidl_runtime_c__String__fini(&msg->raw);
}

bool
imu_msgs__msg__IMUmsg__are_equal(const imu_msgs__msg__IMUmsg * lhs, const imu_msgs__msg__IMUmsg * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // imu
  if (!sensor_msgs__msg__Imu__are_equal(
      &(lhs->imu), &(rhs->imu)))
  {
    return false;
  }
  // mag_field
  if (!sensor_msgs__msg__MagneticField__are_equal(
      &(lhs->mag_field), &(rhs->mag_field)))
  {
    return false;
  }
  // raw
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->raw), &(rhs->raw)))
  {
    return false;
  }
  return true;
}

bool
imu_msgs__msg__IMUmsg__copy(
  const imu_msgs__msg__IMUmsg * input,
  imu_msgs__msg__IMUmsg * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // imu
  if (!sensor_msgs__msg__Imu__copy(
      &(input->imu), &(output->imu)))
  {
    return false;
  }
  // mag_field
  if (!sensor_msgs__msg__MagneticField__copy(
      &(input->mag_field), &(output->mag_field)))
  {
    return false;
  }
  // raw
  if (!rosidl_runtime_c__String__copy(
      &(input->raw), &(output->raw)))
  {
    return false;
  }
  return true;
}

imu_msgs__msg__IMUmsg *
imu_msgs__msg__IMUmsg__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  imu_msgs__msg__IMUmsg * msg = (imu_msgs__msg__IMUmsg *)allocator.allocate(sizeof(imu_msgs__msg__IMUmsg), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(imu_msgs__msg__IMUmsg));
  bool success = imu_msgs__msg__IMUmsg__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
imu_msgs__msg__IMUmsg__destroy(imu_msgs__msg__IMUmsg * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    imu_msgs__msg__IMUmsg__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
imu_msgs__msg__IMUmsg__Sequence__init(imu_msgs__msg__IMUmsg__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  imu_msgs__msg__IMUmsg * data = NULL;

  if (size) {
    data = (imu_msgs__msg__IMUmsg *)allocator.zero_allocate(size, sizeof(imu_msgs__msg__IMUmsg), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = imu_msgs__msg__IMUmsg__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        imu_msgs__msg__IMUmsg__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
imu_msgs__msg__IMUmsg__Sequence__fini(imu_msgs__msg__IMUmsg__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      imu_msgs__msg__IMUmsg__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

imu_msgs__msg__IMUmsg__Sequence *
imu_msgs__msg__IMUmsg__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  imu_msgs__msg__IMUmsg__Sequence * array = (imu_msgs__msg__IMUmsg__Sequence *)allocator.allocate(sizeof(imu_msgs__msg__IMUmsg__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = imu_msgs__msg__IMUmsg__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
imu_msgs__msg__IMUmsg__Sequence__destroy(imu_msgs__msg__IMUmsg__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    imu_msgs__msg__IMUmsg__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
imu_msgs__msg__IMUmsg__Sequence__are_equal(const imu_msgs__msg__IMUmsg__Sequence * lhs, const imu_msgs__msg__IMUmsg__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!imu_msgs__msg__IMUmsg__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
imu_msgs__msg__IMUmsg__Sequence__copy(
  const imu_msgs__msg__IMUmsg__Sequence * input,
  imu_msgs__msg__IMUmsg__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(imu_msgs__msg__IMUmsg);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    imu_msgs__msg__IMUmsg * data =
      (imu_msgs__msg__IMUmsg *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!imu_msgs__msg__IMUmsg__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          imu_msgs__msg__IMUmsg__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!imu_msgs__msg__IMUmsg__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
