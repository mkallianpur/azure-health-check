import pytest
from unittest.mock import patch, MagicMock
from azure_health import health_check


@patch("azure_health.health_check.ComputeManagementClient")
def test_check_vm_status(mock_compute_client):
    mock_vm = MagicMock()
    mock_vm.name = "vm1"

    mock_instance_view = MagicMock()
    mock_instance_view.statuses = [
        MagicMock(code="PowerState/running", display_status="VM running")
    ]

    mock_compute_client.return_value.virtual_machines.list.return_value = [mock_vm]
    mock_compute_client.return_value.virtual_machines.instance_view.return_value = mock_instance_view

    result = health_check.check_vm_status("dummy-sub", "dummy-rg")
    assert result == [("vm1", "VM running")]


@patch("azure_health.health_check.StorageManagementClient")
def test_check_storage_accounts(mock_storage_client):
    mock_account = MagicMock()
    mock_account.name = "storage1"
    mock_account.location = "eastus"

    mock_storage_client.return_value.storage_accounts.list_by_resource_group.return_value = [mock_account]

    result = health_check.check_storage_accounts("dummy-sub", "dummy-rg")
    assert result == [("storage1", "eastus")]


@patch("azure_health.health_check.ServiceBusManagementClient")
def test_check_service_bus(mock_sb_client):
    mock_namespace = MagicMock()
    mock_namespace.name = "ns1"
    mock_namespace.location = "westus"

    mock_sb_client.return_value.namespaces.list_by_resource_group.return_value = [mock_namespace]

    result = health_check.check_service_bus("dummy-sub", "dummy-rg")
    assert result == [("ns1", "westus")]
