#
# Copyright (c) 2019 by Delphix. All rights reserved.
#

import pytest
from dlpx.virtualization.common._common_classes import RemoteEnvironment, RemoteHost
from dlpx.virtualization.common.exceptions import IncorrectTypeError
from dlpx.virtualization.platform import Mount
from dlpx.virtualization.platform import OwnershipSpecification
from dlpx.virtualization.platform import MountSpecification


@pytest.fixture
def remote_host():
    return RemoteHost("host", "host-reference", "binary_path", "scratch_path")


@pytest.fixture
def remote_environment(remote_host):
    return RemoteEnvironment("environment",
                             "environment-reference",
                             remote_host)


class TestPluginClasses:
    @staticmethod
    def test_init_mount_success(remote_environment):
        Mount(remote_environment, 'mount_path', 'shared_path')

    @staticmethod
    def test_init_mount_bad_remote_env():
        with pytest.raises(IncorrectTypeError) as err_info:
            Mount('bad string', 'mount_path', 'shared_path')
        assert err_info.value.message == (
            "Mount's parameter 'remote_environment' was type 'str' but"
            " should be of"
            " class 'dlpx.virtualization.common._common_classes.RemoteEnvironment'.")

    @staticmethod
    def test_init_mount_bad_mount_path(remote_environment):
        with pytest.raises(IncorrectTypeError) as err_info:
            Mount(remote_environment, 10000, 'shared_path')
        assert err_info.value.message == (
            "Mount's parameter 'mount_path' was type 'int' but should"
            " be of type 'basestring'.")

    @staticmethod
    def test_init_mount_bad_shared_path(remote_environment):
        with pytest.raises(IncorrectTypeError) as err_info:
            Mount(remote_environment, 'mount_path', 10000)
        assert err_info.value.message == (
            "Mount's parameter 'shared_path' was type 'int' but should"
            " be of type 'basestring' if defined.")

    @staticmethod
    def test_init_ownership_spec():
        OwnershipSpecification(10, 10)

    @staticmethod
    def test_init_ownership_spec_bad_uid():
        with pytest.raises(IncorrectTypeError) as err_info:
            OwnershipSpecification('10', 10)
        assert err_info.value.message == (
            "OwnershipSpecification's parameter 'uid' was type 'str' but"
            " should be of type 'int'.")

    @staticmethod
    def test_init_ownership_spec_bad_gid():
        with pytest.raises(IncorrectTypeError) as err_info:
            OwnershipSpecification(10, '10')
        assert err_info.value.message == (
            "OwnershipSpecification's parameter 'gid' was type 'str' but"
            " should be of type 'int'.")

    @staticmethod
    def test_init_mount_spec(remote_environment):
        mount = Mount(remote_environment, 'mount_path', 'shared_path')
        MountSpecification([mount], OwnershipSpecification(10, 10))

    @staticmethod
    def test_init_mount_spec_mounts_not_list():
        with pytest.raises(IncorrectTypeError) as err_info:
            MountSpecification('string', OwnershipSpecification(10, 10))
        assert err_info.value.message == (
            "MountSpecification's parameter 'mounts' was type 'str' but"
            " should be of type 'list of dlpx.virtualization.platform"
            "._plugin_classes.Mount'.")

    @staticmethod
    def test_init_mount_spec_bad_mounts():
        with pytest.raises(IncorrectTypeError) as err_info:
            MountSpecification(['string'], OwnershipSpecification(10, 10))
        assert err_info.value.message == (
            "MountSpecification's parameter 'mounts' was a list of"
            " [type 'str'] but should be of type 'list of dlpx.virtualization"
            ".platform._plugin_classes.Mount'.")

    @staticmethod
    def test_init_mount_spec_bad_owner_spec(remote_environment):
        mount = Mount(remote_environment, 'mount_path', 'shared_path')

        with pytest.raises(IncorrectTypeError) as err_info:
            MountSpecification([mount], 'string')
        assert err_info.value.message == (
            "MountSpecification's parameter 'ownership_specification' was"
            " type 'str' but should be of class 'dlpx.virtualization"
            ".platform._plugin_classes.OwnershipSpecification'"
            " if defined.")
