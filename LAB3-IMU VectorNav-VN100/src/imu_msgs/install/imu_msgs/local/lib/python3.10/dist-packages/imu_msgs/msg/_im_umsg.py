# generated from rosidl_generator_py/resource/_idl.py.em
# with input from imu_msgs:msg/IMUmsg.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_IMUmsg(type):
    """Metaclass of message 'IMUmsg'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('imu_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'imu_msgs.msg.IMUmsg')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__im_umsg
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__im_umsg
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__im_umsg
            cls._TYPE_SUPPORT = module.type_support_msg__msg__im_umsg
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__im_umsg

            from sensor_msgs.msg import Imu
            if Imu.__class__._TYPE_SUPPORT is None:
                Imu.__class__.__import_type_support__()

            from sensor_msgs.msg import MagneticField
            if MagneticField.__class__._TYPE_SUPPORT is None:
                MagneticField.__class__.__import_type_support__()

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class IMUmsg(metaclass=Metaclass_IMUmsg):
    """Message class 'IMUmsg'."""

    __slots__ = [
        '_header',
        '_imu',
        '_mag_field',
        '_raw',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'imu': 'sensor_msgs/Imu',
        'mag_field': 'sensor_msgs/MagneticField',
        'raw': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['sensor_msgs', 'msg'], 'Imu'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['sensor_msgs', 'msg'], 'MagneticField'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        from sensor_msgs.msg import Imu
        self.imu = kwargs.get('imu', Imu())
        from sensor_msgs.msg import MagneticField
        self.mag_field = kwargs.get('mag_field', MagneticField())
        self.raw = kwargs.get('raw', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.header != other.header:
            return False
        if self.imu != other.imu:
            return False
        if self.mag_field != other.mag_field:
            return False
        if self.raw != other.raw:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def imu(self):
        """Message field 'imu'."""
        return self._imu

    @imu.setter
    def imu(self, value):
        if __debug__:
            from sensor_msgs.msg import Imu
            assert \
                isinstance(value, Imu), \
                "The 'imu' field must be a sub message of type 'Imu'"
        self._imu = value

    @builtins.property
    def mag_field(self):
        """Message field 'mag_field'."""
        return self._mag_field

    @mag_field.setter
    def mag_field(self, value):
        if __debug__:
            from sensor_msgs.msg import MagneticField
            assert \
                isinstance(value, MagneticField), \
                "The 'mag_field' field must be a sub message of type 'MagneticField'"
        self._mag_field = value

    @builtins.property
    def raw(self):
        """Message field 'raw'."""
        return self._raw

    @raw.setter
    def raw(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'raw' field must be of type 'str'"
        self._raw = value
