# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import pytest
import logging
from azure.iot.device.provisioning.pipeline import mqtt_topic_provisioning

logging.basicConfig(level=logging.DEBUG)

# NOTE: All tests (that require it) are parametrized with multiple values for URL encoding.
# This is to show that the URL encoding is done correctly - not all URL encoding encodes
# the '+' character. Thus we must make sure any URL encoded value can encode a '+' specifically,
# in addition to standard URL encoding.


@pytest.mark.describe(".get_register_topic_for_subscribe()")
class TestGetRegisterTopicForSubscribe(object):
    @pytest.mark.it("Returns the topic for subscribing to registration responses from DPS")
    def test_returns_topic(self):
        topic = mqtt_topic_provisioning.get_register_topic_for_subscribe()
        assert topic == "$dps/registrations/res/#"


# @pytest.mark.describe(".get_register_topic_for_publish()")
# class TestGetRegisterTopicForPublish(object):
#     @pytest.mark.it("Returns the topic for publishing registration requests to DPS")
#     @pytest.mark.parametrize("request_id, expected_topic", [
#         # UUID
#         pytest.param("3226c2f7-3d30-425c-b83b-0c34335f8220", "$dps/registrations/PUT/iotdps-register/?$rid=3226c2f7-3d30-425c-b83b-0c34335f8220", id="'3226c2f7-3d30-425c-b83b-0c34335f8220' ==> '$dps/registrations/PUT/iotdps-register/?$rid=3226c2f7-3d30-425c-b83b-0c34335f8220'"),
#         pytest.param()
#     ])
#     def test_returns_topic(self):
