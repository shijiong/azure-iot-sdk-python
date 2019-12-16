# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import pytest
import logging
from azure.iot.device.iothub.pipeline import mqtt_topic_iothub

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
            pytest.param(
                "my_device",
                None,
                "devices/my_device/messages/devicebound/#",
                id="('my_device', None) ==> 'devices/my_device/messages/devicebound/#'",
            ),
            pytest.param(
                "my/device",
                None,
                "devices/my%2Fdevice/messages/devicebound/#",
                id="('my/device', None) ==> 'devices/my%2Fdevice/messages/devicebound/#'",
            ),
            pytest.param(
                "my+device",
                None,
                "devices/my%2Bdevice/messages/devicebound/#",
                id="('my+device', None) ==> 'devices/my%2Bdevice/messages/devicebound/#'",
            ),
            pytest.param(
                "my_device",
                "my_module",
                "devices/my_device/modules/my_module/messages/devicebound/#",
                id="('my_device', 'my_module') ==> 'devices/my_device/modules/my_module/messages/devicebound/#'",
            ),
            pytest.param(
                "my/device",
                "my?module",
                "devices/my%2Fdevice/modules/my%3Fmodule/messages/devicebound/#",
                id="('my_device', 'my_module') ==> 'devices/my%2Fdevice/modules/my%3Fmodule/messages/devicebound/#'",
            ),
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
            pytest.param(
                "my_device",
                None,
                "devices/my_device/inputs/#",
                id="('my_device', None) ==> 'devices/my_device/inputs/#'",
            ),
            pytest.param(
                "my/device",
                None,
                "devices/my%2Fdevice/inputs/#",
                id="('my/device', None) ==> 'devices/my%2Fdevice/inputs/#'",
            ),
            pytest.param(
                "my+device",
                None,
                "devices/my%2Bdevice/inputs/#",
                id="('my+device', None) ==> 'devices/my%2Bdevice/inputs/#'",
            ),
            pytest.param(
                "my_device",
                "my_module",
                "devices/my_device/modules/my_module/inputs/#",
                id="('my_device', 'my_module') ==> 'devices/my_device/modules/my_module/inputs/#'",
            ),
            pytest.param(
                "my/device",
                "my?module",
                "devices/my%2Fdevice/modules/my%3Fmodule/inputs/#",
                id="('my_device', 'my_module') ==> 'devices/my%2Fdevice/modules/my%3Fmodule/inputs/#'",
            ),
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


@pytest.mark.describe(".get_telemetry_topic_for_publish()")
class TestGetTelemetryTopicForPublish(object):
    @pytest.mark.it("Returns the topic for sending telemetry to IoTHub")
    @pytest.mark.parametrize(
        "device_id, module_id, expected_topic",
        [
            pytest.param(
                "my_device",
                None,
                "devices/my_device/messages/events/",
                id="('my_device', None) ==> 'devices/my_device/messages/events/'",
            ),
            pytest.param(
                "my/device",
                None,
                "devices/my%2Fdevice/messages/events/",
                id="('my/device', None) ==> 'devices/my%2Fdevice/messages/events/'",
            ),
            pytest.param(
                "my+device",
                None,
                "devices/my%2Bdevice/messages/events/",
                id="('my+device', None) ==> 'devices/my%2Bdevice/messages/events/'",
            ),
            pytest.param(
                "my_device",
                "my_module",
                "devices/my_device/modules/my_module/messages/events/",
                id="('my_device', 'my_module') ==> 'devices/my_device/modules/my_module/messages/events/'",
            ),
            pytest.param(
                "my/device",
                "my?module",
                "devices/my%2Fdevice/modules/my%3Fmodule/messages/events/",
                id="('my_device', 'my_module') ==> 'devices/my%2Fdevice/modules/my%3Fmodule/messages/events/'",
            ),
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


# @pytest.mark.describe(".get_method_topic_for_publish()")
# class TestGetMethodTopicForPublish(object):
#     @pytest.mark.it("Returns the topic for sending a method response to IoTHub")
#     @pytest.mark.parametrize("request_id, status, expected_topic", [
#         pytest.param()
#     ])
