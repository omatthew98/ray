import sys

import pytest

from ray.serve._private.common import DeploymentHandleSource, RequestProtocol
from ray.serve._private.utils import DEFAULT
from ray.serve.handle import _DynamicHandleOptions, _InitHandleOptions


def test_dynamic_handle_options():
    default_options = _DynamicHandleOptions()
    assert default_options.method_name == "__call__"
    assert default_options.multiplexed_model_id == ""
    assert default_options.stream is False
    assert default_options._request_protocol == RequestProtocol.UNDEFINED

    # Test setting method name.
    only_set_method = default_options.copy_and_update(method_name="hi")
    assert only_set_method.method_name == "hi"
    assert only_set_method.multiplexed_model_id == ""
    assert only_set_method.stream is False
    assert default_options._request_protocol == RequestProtocol.UNDEFINED

    # Existing options should be unmodified.
    assert default_options.method_name == "__call__"
    assert default_options.multiplexed_model_id == ""
    assert default_options.stream is False
    assert default_options._request_protocol == RequestProtocol.UNDEFINED

    # Test setting model ID.
    only_set_model_id = default_options.copy_and_update(multiplexed_model_id="hi")
    assert only_set_model_id.method_name == "__call__"
    assert only_set_model_id.multiplexed_model_id == "hi"
    assert only_set_model_id.stream is False
    assert default_options._request_protocol == RequestProtocol.UNDEFINED

    # Existing options should be unmodified.
    assert default_options.method_name == "__call__"
    assert default_options.multiplexed_model_id == ""
    assert default_options.stream is False
    assert default_options._request_protocol == RequestProtocol.UNDEFINED

    # Test setting stream.
    only_set_stream = default_options.copy_and_update(stream=True)
    assert only_set_stream.method_name == "__call__"
    assert only_set_stream.multiplexed_model_id == ""
    assert only_set_stream.stream is True
    assert default_options._request_protocol == RequestProtocol.UNDEFINED

    # Existing options should be unmodified.
    assert default_options.method_name == "__call__"
    assert default_options.multiplexed_model_id == ""
    assert default_options.stream is False
    assert default_options._request_protocol == RequestProtocol.UNDEFINED

    # Test setting multiple.
    set_multiple = default_options.copy_and_update(method_name="hi", stream=True)
    assert set_multiple.method_name == "hi"
    assert set_multiple.multiplexed_model_id == ""
    assert set_multiple.stream is True
    assert default_options._request_protocol == RequestProtocol.UNDEFINED


def test_init_handle_options():
    default_options = _InitHandleOptions.create()
    assert default_options._prefer_local_routing is False
    assert default_options._source == DeploymentHandleSource.UNKNOWN

    default1 = _InitHandleOptions.create(_prefer_local_routing=DEFAULT.VALUE)
    assert default1._prefer_local_routing is False
    assert default1._source == DeploymentHandleSource.UNKNOWN

    default2 = _InitHandleOptions.create(_source=DEFAULT.VALUE)
    assert default2._prefer_local_routing is False
    assert default2._source == DeploymentHandleSource.UNKNOWN

    prefer_local = _InitHandleOptions.create(
        _prefer_local_routing=True, _source=DEFAULT.VALUE
    )
    assert prefer_local._prefer_local_routing is True
    assert prefer_local._source == DeploymentHandleSource.UNKNOWN

    proxy_options = _InitHandleOptions.create(_source=DeploymentHandleSource.PROXY)
    assert proxy_options._prefer_local_routing is False
    assert proxy_options._source == DeploymentHandleSource.PROXY


if __name__ == "__main__":
    sys.exit(pytest.main(["-v", "-s", __file__]))