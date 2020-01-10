# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import pytest
import logging
from azure.iot.device.iothub.pipeline import mqtt_topic_iothub

logging.basicConfig(level=logging.DEBUG)

# NOTE: All tests (that require it) are parametrized with multiple values for URL encoding.
# This is to show that the URL encoding is done correctly - not all URL encoding encodes
# the '+' character. Thus we must make sure any URL encoded value can encode a '+' specifically,
# in addition to regular encoding.


@pytest.mark.describe(".get_c2d_topic_for_subscribe()")
class TestGetC2DTopicForSubscribe(object):
    @pytest.mark.it("Returns the topic for subscribing to C2D messages from IoTHub")
    @pytest.mark.parametrize(
        "device_id, module_id, expected_topic",
        [
            # Device, no URL Encoding
            pytest.param(
                "my_device",
                None,
                "devices/my_device/messages/devicebound/#",
                id="('my_device', None) ==> 'devices/my_device/messages/devicebound/#'",
            ),
            # Device, with URL Encoding
            pytest.param(
                "my$device",
                None,
                "devices/my%24device/messages/devicebound/#",
                id="('my$device', None) ==> 'devices/my%24device/messages/devicebound/#'",
            ),
            # Device, with URL Encoding (+)
            pytest.param(
                "my+device",
                None,
                "devices/my%2Bdevice/messages/devicebound/#",
                id="('my+device', None) ==> 'devices/my%2Bdevice/messages/devicebound/#'",
            ),
            # Module, no URL Encoding
            pytest.param(
                "my_device",
                "my_module",
                "devices/my_device/modules/my_module/messages/devicebound/#",
                id="('my_device', 'my_module') ==> 'devices/my_device/modules/my_module/messages/devicebound/#'",
            ),
            # Module, with URL Encoding
            pytest.param(
                "my$device",
                "my?module",
                "devices/my%24device/modules/my%3Fmodule/messages/devicebound/#",
                id="('my_device', 'my_module') ==> 'devices/my%24device/modules/my%3Fmodule/messages/devicebound/#'",
            ),
            # Module, with URL Encoding (+)
            pytest.param(
                "my+device",
                "my+module",
                "devices/my%2Bdevice/modules/my%2Bmodule/messages/devicebound/#",
                id="('my_device', 'my_module') ==> 'devices/my%2Bdevice/modules/my%2Bmodule/messages/devicebound/#'",
            ),
        ],
    )
    def test_returns_topic(self, module_id, device_id, expected_topic):
        topic = mqtt_topic_iothub.get_c2d_topic_for_subscribe(device_id, module_id)
        assert topic == expected_topic


@pytest.mark.describe(".get_input_topic_for_subscribe()")
class TestGetInputTopicForSubscribe(object):
    @pytest.mark.it("Returns the topic for subscribing to C2D messages from IoTHub")
    @pytest.mark.parametrize(
        "device_id, module_id, expected_topic",
        [
            # Device, no URL encoding
            pytest.param(
                "my_device",
                None,
                "devices/my_device/inputs/#",
                id="('my_device', None) ==> 'devices/my_device/inputs/#'",
            ),
            # Device, with URL encoding
            pytest.param(
                "my$device",
                None,
                "devices/my%24device/inputs/#",
                id="('my$device', None) ==> 'devices/my%24device/inputs/#'",
            ),
            # Device, with URL encoding (+)
            pytest.param(
                "my+device",
                None,
                "devices/my%2Bdevice/inputs/#",
                id="('my+device', None) ==> 'devices/my%2Bdevice/inputs/#'",
            ),
            # Module, no URL encoding
            pytest.param(
                "my_device",
                "my_module",
                "devices/my_device/modules/my_module/inputs/#",
                id="('my_device', 'my_module') ==> 'devices/my_device/modules/my_module/inputs/#'",
            ),
            # Module, with URL encoding
            pytest.param(
                "my$device",
                "my?module",
                "devices/my%24device/modules/my%3Fmodule/inputs/#",
                id="('my_device', 'my_module') ==> 'devices/my%24device/modules/my%3Fmodule/inputs/#'",
            ),
            # Module, with URL encoding (+)
            pytest.param(
                "my+device",
                "my+module",
                "devices/my%2Bdevice/modules/my%2Bmodule/inputs/#",
                id="('my_device', 'my_module') ==> 'devices/my%2Bdevice/modules/my%2Bmodule/inputs/#'",
            ),
        ],
    )
    def test_returns_topic(self, module_id, device_id, expected_topic):
        topic = mqtt_topic_iothub.get_input_topic_for_subscribe(device_id, module_id)
        assert topic == expected_topic


@pytest.mark.describe(".get_method_topic_for_subscribe()")
class TestGetMethodTopicForSubscribe(object):
    @pytest.mark.it("Returns the topic for subscribing to methods from IoTHub")
    def test_returns_topic(self):
        topic = mqtt_topic_iothub.get_method_topic_for_subscribe()
        assert topic == "$iothub/methods/POST/#"


@pytest.mark.describe(".get_telemetry_topic_for_publish()")
class TestGetTelemetryTopicForPublish(object):
    @pytest.mark.it("Returns the topic for sending telemetry to IoTHub")
    @pytest.mark.parametrize(
        "device_id, module_id, expected_topic",
        [
            # Device, no URL encoding
            pytest.param(
                "my_device",
                None,
                "devices/my_device/messages/events/",
                id="('my_device', None) ==> 'devices/my_device/messages/events/'",
            ),
            # Device, with URL encoding
            pytest.param(
                "my$device",
                None,
                "devices/my%24device/messages/events/",
                id="('my$device', None) ==> 'devices/my%24device/messages/events/'",
            ),
            # Device, with URL encoding (+)
            pytest.param(
                "my+device",
                None,
                "devices/my%2Bdevice/messages/events/",
                id="('my+device', None) ==> 'devices/my%2Bdevice/messages/events/'",
            ),
            # Module, no URL encoding
            pytest.param(
                "my_device",
                "my_module",
                "devices/my_device/modules/my_module/messages/events/",
                id="('my_device', 'my_module') ==> 'devices/my_device/modules/my_module/messages/events/'",
            ),
            # Module, with URL encoding
            pytest.param(
                "my$device",
                "my?module",
                "devices/my%24device/modules/my%3Fmodule/messages/events/",
                id="('my_device', 'my_module') ==> 'devices/my%24device/modules/my%3Fmodule/messages/events/'",
            ),
            # Module, with URL encoding (+)
            pytest.param(
                "my+device",
                "my+module",
                "devices/my%2Bdevice/modules/my%2Bmodule/messages/events/",
                id="('my_device', 'my_module') ==> 'devices/my%2Bdevice/modules/my%2Bmodule/messages/events/'",
            ),
        ],
    )
    def test_returns_topic(self, module_id, device_id, expected_topic):
        topic = mqtt_topic_iothub.get_telemetry_topic_for_publish(device_id, module_id)
        assert topic == expected_topic


@pytest.mark.describe(".get_method_topic_for_publish()")
class TestGetMethodTopicForPublish(object):
    @pytest.mark.it("Returns the topic for sending a method response to IoTHub")
    @pytest.mark.parametrize(
        "request_id, status, expected_topic",
        [
            # Successful result
            pytest.param(
                "1",
                "200",
                "$iothub/methods/res/200/?$rid=1",
                id="('1', '200') ==> '$iothub/methods/res/200/?$rid=1'",
            ),
            # Fail result
            pytest.param(
                "475764",
                "500",
                "$iothub/methods/res/500/?$rid=475764",
                id="('475764', '500') ==> '$iothub/methods/res/500/?$rid=475764",
            ),
        ],
    )
    def test_returns_topic(self, request_id, status, expected_topic):
        topic = mqtt_topic_iothub.get_method_topic_for_publish(request_id, status)
        assert topic == expected_topic

    # NOTE: Neither request_id nor status should require URL encoding.
    # There are no valid values for which they would require to be URL encoded.
    # However, because they are directly user provided, we encode them anyway for safety.
    # PLEASE NOTE THAT ALL OF THESE TEST CASES ARE INVALID AS A RESULT.
    @pytest.mark.it("URL encodes values (even though any URL encoded value is invalid)")
    @pytest.mark.parametrize(
        "request_id, status, expected_topic",
        [
            # URL Encode
            pytest.param(
                "invalid/request?id",
                "invalid$status",
                "$iothub/methods/res/invalid%24status/?$rid=invalid%2Frequest%3Fid",
                id="Regular URL Encoding",
            ),
            # URL Encode (+)
            pytest.param(
                "invalid+request+id",
                "invalid+status",
                "$iothub/methods/res/invalid%2Bstatus/?$rid=invalid%2Brequest%2Bid",
                id="URL Encoding of '+' character",
            ),
        ],
    )
    def test_url_encoding_even_when_invalid(self, request_id, status, expected_topic):
        topic = mqtt_topic_iothub.get_method_topic_for_publish(request_id, status)
        assert topic == expected_topic


@pytest.mark.describe(".is_c2d_topic()")
class TestIsC2DTopic(object):
    @pytest.mark.it(
        "Returns True if the provided topic is a C2D topic and matches the provided device id"
    )
    @pytest.mark.parametrize(
        "topic, device_id",
        [
            pytest.param(
                "devices/fake_device/messages/devicebound/%24.mid=6b822696-f75a-46f5-8b02-0680db65abf5&%24.to=%2Fdevices%2Ffake_device%2Fmessages%2FdeviceBound&iothub-ack=full",
                "fake_device",
                id="No URL encoding required for device_id",
            )
            # CT-TODO: Add test cases for URL encoding scenarios when requirements are learned
        ],
    )
    def test_is_c2d_topic(self, topic, device_id):
        assert mqtt_topic_iothub.is_c2d_topic(topic, device_id)

    @pytest.mark.it("Returns False if the provided topic is not a C2D topic")
    @pytest.mark.parametrize(
        "topic, device_id",
        [
            pytest.param("not a topic", "fake_device", id="Not a topic"),
            pytest.param(
                "devices/fake_device/modules/fake_module/inputs/fake_input/%24.mid=6b822696-f75a-46f5-8b02-0680db65abf5&%24.to=%2Fdevices%2Ffake_device%2Fmessages%2FdeviceBound&iothub-ack=full",
                "fake_device",
                id="Topic of wrong type",
            ),
            pytest.param(
                "devices/fake_device/msgs/devicebound/%24.mid=6b822696-f75a-46f5-8b02-0680db65abf5&%24.to=%2Fdevices%2Ffake_device%2Fmessages%2FdeviceBound&iothub-ack=full",
                "fake_device",
                id="Malformed topic",
            ),
        ],
    )
    def test_is_not_c2d_topic(self, topic, device_id):
        assert not mqtt_topic_iothub.is_c2d_topic(topic, device_id)

    @pytest.mark.it(
        "Returns False if the provided topic is a C2D topic, but does not match the provided device id"
    )
    # CT-TODO: Add test cases for various URL encoding scenarios / matching
    def test_is_c2d_topic_but_wrong_device_id(self):
        topic = (
            "devices/fake_device/messages/devicebound/%24.mid=6b822696-f75a-46f5-8b02-0680db65abf5&%24.to=%2Fdevices%2Ffake_device%2Fmessages%2FdeviceBound&iothub-ack=full",
        )
        device_id = "VERY_fake_device"
        assert not mqtt_topic_iothub.is_c2d_topic(topic, device_id)


# CT-TODO: What does an input topic look like?
# @pytest.mark.describe(".is_input_topic()")
# class TestIsInputTopic(object):
#     @pytest.mark.it("Returns True if the provided topic is an input topic and matches the provided device id and module id")
#     @pytest.mark.parametrize("topic, device_id, module_id", [
#         pytest.param("devices/fake_device/modules/fake_module/inputs/", "fake_device", "fake_module", id="No URL encoding required for ids")
#     ])
#     def test_is_input_topic(self, topic, device_id, module_id):
#         assert mqtt_topic_iothub.is_input_topic(topic, device_id, module_id)

#     @pytest.mark.it("Returns False if the provided topic is not an input topic")
#     def test_is_not_input_topic(self):
#         pass

#     @pytest.mark.it("Returns False if the provided topic is an input topic, but does match the provided device id and/or module_id")
#     def test_is_input_topic_but_wrong_id(self):
#         pass


@pytest.mark.describe(".is_method_topic()")
class TestIsMethodTopic(object):
    @pytest.mark.it("Returns True if the provided topic is a method topic")
    def test_is_method_topic(self):
        topic = "$iothub/methods/POST/fake_method/?$rid=1"
        assert mqtt_topic_iothub.is_method_topic(topic)

    @pytest.mark.it("Returns False if the provided topic is not a method topic")
    @pytest.mark.parametrize(
        "topic",
        [
            pytest.param("not a topic", id="Not a topic"),
            pytest.param(
                "devices/fake_device/messages/devicebound/%24.mid=6b822696-f75a-46f5-8b02-0680db65abf5&%24.to=%2Fdevices%2Ffake_device%2Fmessages%2FdeviceBound&iothub-ack=full",
                id="Topic of wrong type",
            ),
            pytest.param("$iothub/mthds/POST/fake_method/?$rid=1", id="Malformed topic"),
        ],
    )
    def test_is_not_method_topic(self, topic):
        assert not mqtt_topic_iothub.is_method_topic(topic)


@pytest.mark.describe(".is_twin_response_topic()")
class TestIsTwinResponseTopic(object):
    @pytest.mark.it("Returns True if the provided topic is a twin response topic")
    def test_is_twin_response_topic(self):
        topic = "$iothub/twin/res/200/?$rid=d9d7ce4d-3be9-498b-abde-913b81b880e5"
        assert mqtt_topic_iothub.is_twin_response_topic(topic)

    @pytest.mark.it("Returns False if the provided topic is not a method topic")
    @pytest.mark.parametrize(
        "topic",
        [
            pytest.param("not a topic", id="Not a topic"),
            pytest.param("$iothub/methods/POST/fake_method/?$rid=1", id="Topic of wrong type"),
            pytest.param(
                "$iothub/twin/rs/200/?$rid=d9d7ce4d-3be9-498b-abde-913b81b880e5",
                id="Malformed topic",
            ),
        ],
    )
    def test_is_not_twin_response_topic(self, topic):
        assert not mqtt_topic_iothub.is_twin_response_topic(topic)


# @pytest.mark.describe(".is_twin_desired_property_patch_topic()")
# class TestIsTwinDesiredPropertyPatchTopic(object):
