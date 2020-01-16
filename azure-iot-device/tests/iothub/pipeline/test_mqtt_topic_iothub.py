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


@pytest.mark.describe("get_twin_response_topic_for_subscribe()")
class TestGetTwinResponseTopicForSubscribe(object):
    @pytest.mark.it("Returns the topic for subscribing to twin repsonse from IoTHub")
    def test_returns_topic(self):
        topic = mqtt_topic_iothub.get_twin_response_topic_for_subscribe()
        assert topic == "$iothub/twin/res/#"


@pytest.mark.describe("get_twin_patch_topic_for_subscribe()")
class TestGetTwinPatchTopicForSubscribe(object):
    @pytest.mark.it("Returns the topic for subscribing to twin patches from IoTHub")
    def test_returns_topic(self):
        topic = mqtt_topic_iothub.get_twin_patch_topic_for_subscribe()
        assert topic == "$iothub/twin/PATCH/properties/desired/#"


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
    @pytest.mark.it("URL encodes values (even though any value needing URL encoding is invalid)")
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


@pytest.mark.describe(".get_twin_topic_for_publish()")
class TestGetTwinTopicForPublish(object):
    @pytest.mark.it("Returns topic for sending a twin request to IoTHub")
    @pytest.mark.parametrize(
        "method, resource_location, request_id, expected_topic",
        [
            # Get Twin
            pytest.param(
                "GET",
                "/",
                "3226c2f7-3d30-425c-b83b-0c34335f8220",
                "$iothub/twin/GET/?$rid=3226c2f7-3d30-425c-b83b-0c34335f8220",
                id="('GET', '/', '3226c2f7-3d30-425c-b83b-0c34335f8220') ==> '$iothub/twin/GET/?$rid=3226c2f7-3d30-425c-b83b-0c34335f8220'",
            ),
            # Patch Twin
            pytest.param(
                "POST",
                "/properties/reported/",
                "5002b415-af16-47e9-b89c-8680e01b502f",
                "$iothub/twin/POST/properties/reported/?$rid=5002b415-af16-47e9-b89c-8680e01b502f",
                id="('POST', 'properties/reported', '5002b415-af16-47e9-b89c-8680e01b502f') ==> '$iothub/twin/POST/properties/reported/?$rid=5002b415-af16-47e9-b89c-8680e01b502f'",
            ),
        ],
    )
    def test_returns_topic(self, method, resource_location, request_id, expected_topic):
        # CT-TODO: These first two arguments probably shouldn't have to be provided
        topic = mqtt_topic_iothub.get_twin_topic_for_publish(method, resource_location, request_id)
        assert topic == expected_topic

    # NOTE: request_id should not require URL encoding.
    # There are no valid values for which it would require to be URL encoded.
    # Furthermore, the value is not user supplied, so it should never be NOT already URL encoded.
    # However, for consistency with other methods, and as a sanity check, it is URL encoded anyway.
    @pytest.mark.it(
        "URL encodes 'request_id' parameter (even though any value needing URL encoding is invalid)"
    )
    @pytest.mark.parametrize(
        "method, resource_location, request_id, expected_topic",
        [
            # URL Encode
            pytest.param(
                "GET",
                "/",
                "invalid/request?id",
                "$iothub/twin/GET/?$rid=invalid%2Frequest%3Fid",
                id="Regular URL Encoding",
            ),
            # URL Encode (+)
            pytest.param(
                "POST",
                "/properties/reported/",
                "invalid+request+id",
                "$iothub/twin/POST/properties/reported/?$rid=invalid%2Brequest%2Bid",
                id="URL Encoding of '+' character",
            ),
        ],
    )
    def test_url_encoding_even_when_invalid(
        self, method, resource_location, request_id, expected_topic
    ):
        topic = mqtt_topic_iothub.get_twin_topic_for_publish(method, resource_location, request_id)
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

    @pytest.mark.it("Returns False if the provided topic is not a twin response topic")
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


# CT-TODO: Add these tests. This functionality appears broken? Need to investigate
# @pytest.mark.describe(".is_twin_desired_property_patch_topic()")
# class TestIsTwinDesiredPropertyPatchTopic(object):
#     @pytest.mark.it("Returns True if the provided topic is a desired property patch topic")
#     def test_is_desired_property_patch_topic(self):
#         pass

#     @pytest.mark.it("Returns False if the provided topic is not a desired property patch topic")
#     def test_is_not_desired_property_patch_topic(self):
#         pass


@pytest.mark.describe(".get_input_name_from_topic()")
class TestGetInputNameFromTopic(object):
    @pytest.mark.it("Returns the input name from an input topic")
    def test_valid_input_topic(self):
        topic = "devices/fake_device/modules/fake_module/inputs/fake_input"
        expected_input_name = "fake_input"

        assert mqtt_topic_iothub.get_input_name_from_topic(topic) == expected_input_name

    @pytest.mark.it("Raises a ValueError if the provided topic is not an input name topic")
    @pytest.mark.parametrize(
        "topic",
        [
            pytest.param("not a topic", id="Not a topic"),
            pytest.param("$iothub/methods/POST/fake_method/?$rid=1", id="Topic of wrong type"),
            pytest.param("devices/fake_device/inputs/fake_input", id="Malformed topic"),
        ],
    )
    def test_invalid_input_topic(self, topic):
        with pytest.raises(ValueError):
            mqtt_topic_iothub.get_input_name_from_topic(topic)


@pytest.mark.describe(".get_method_name_from_topic()")
class TestGetMethodNameFromTopic(object):
    @pytest.mark.it("Returns the method name from a method topic")
    def test_valid_method_topic(self):
        topic = "$iothub/methods/POST/fake_method/?$rid=1"
        expected_method_name = "fake_method"

        assert mqtt_topic_iothub.get_method_name_from_topic(topic) == expected_method_name

    @pytest.mark.it("Raises a ValueError if the provided topic is not a method topic")
    @pytest.mark.parametrize(
        "topic",
        [
            pytest.param("not a topic", id="Not a topic"),
            pytest.param(
                "devices/fake_device/modules/fake_module/inputs/fake_input",
                id="Topic of wrong type",
            ),
            pytest.param("$iothub/methdos/POST/fake_method/?$rid=1", id="Malformed topic"),
        ],
    )
    def test_invalid_method_topic(self, topic):
        with pytest.raises(ValueError):
            mqtt_topic_iothub.get_method_name_from_topic(topic)


@pytest.mark.describe(".get_method_request_id_from_topic()")
class TestGetMethodRequestIdFromTopic(object):
    @pytest.mark.it("Returns the request id from a method topic")
    def test_valid_method_topic(self):
        topic = "$iothub/methods/POST/fake_method/?$rid=1"
        expected_request_id = "1"

        assert mqtt_topic_iothub.get_method_request_id_from_topic(topic) == expected_request_id

    @pytest.mark.it("Raises a ValueError if the provided topic is not a method topic")
    @pytest.mark.parametrize(
        "topic",
        [
            pytest.param("not a topic", id="Not a topic"),
            pytest.param(
                "devices/fake_device/modules/fake_module/inputs/fake_input",
                id="Topic of wrong type",
            ),
            pytest.param("$iothub/methdos/POST/fake_method/?$rid=1", id="Malformed topic"),
        ],
    )
    def test_invalid_method_topic(self, topic):
        with pytest.raises(ValueError):
            mqtt_topic_iothub.get_method_request_id_from_topic(topic)


@pytest.mark.describe(".get_twin_request_id_from_topic()")
class TestGetTwinRequestIdFromTopic(object):
    @pytest.mark.it("Returns the request id from a twin response topic")
    def test_valid_twin_response_topic(self):
        topic = "$iothub/twin/res/200/?rid=1"
        expected_request_id = "1"

        assert mqtt_topic_iothub.get_twin_request_id_from_topic(topic) == expected_request_id

    @pytest.mark.it("Raises a ValueError if the provided topic is not a twin response topic")
    @pytest.mark.parametrize(
        "topic",
        [
            pytest.param("not a topic", id="Not a topic"),
            pytest.param(
                "devices/fake_device/modules/fake_module/inputs/fake_input",
                id="Topic of wrong type",
            ),
            pytest.param("$iothub/twn/res/200?rid=1", id="Malformed topic"),
        ],
    )
    def test_invalid_twin_response_topic(self, topic):
        with pytest.raises(ValueError):
            mqtt_topic_iothub.get_twin_request_id_from_topic(topic)


@pytest.mark.describe("get_twin_status_code_from_topic()")
class TestGetTwinStatusCodeFromTopic(object):
    @pytest.mark.it("Returns the status from a twin response topic")
    def test_valid_twin_response_topic(self):
        topic = "$iothub/twin/res/200/?rid=1"
        expected_status = "200"

        assert mqtt_topic_iothub.get_twin_status_code_from_topic(topic) == expected_status

    @pytest.mark.it("Raises a ValueError if the provided topic is not a twin response topic")
    @pytest.mark.parametrize(
        "topic",
        [
            pytest.param("not a topic", id="Not a topic"),
            pytest.param(
                "devices/fake_device/modules/fake_module/inputs/fake_input",
                id="Topic of wrong type",
            ),
            pytest.param("$iothub/twn/res/200?rid=1", id="Malformed topic"),
        ],
    )
    def test_invalid_twin_response_topic(self, topic):
        with pytest.raises(ValueError):
            mqtt_topic_iothub.get_twin_request_id_from_topic(topic)


# CT-TODO: message extraction/encoding tests
