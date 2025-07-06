from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.servicebus import ServiceBusManagementClient
from azure.mgmt.storage import StorageManagementClient


def check_vm_status(subscription_id, resource_group):
    compute_client = ComputeManagementClient(DefaultAzureCredential(), subscription_id)
    vms = compute_client.virtual_machines.list(resource_group)
    status_report = []
    for vm in vms:
        instance_view = compute_client.virtual_machines.instance_view(resource_group, vm.name)
        statuses = instance_view.statuses
        state = [s.display_status for s in statuses if s.code.startswith('PowerState/')]
        status_report.append((vm.name, state[0] if state else 'Unknown'))
    return status_report


def check_storage_accounts(subscription_id, resource_group):
    storage_client = StorageManagementClient(DefaultAzureCredential(), subscription_id)
    accounts = storage_client.storage_accounts.list_by_resource_group(resource_group)
    return [(acct.name, acct.location) for acct in accounts]


def check_service_bus(subscription_id, resource_group):
    sb_client = ServiceBusManagementClient(DefaultAzureCredential(), subscription_id)
    namespaces = sb_client.namespaces.list_by_resource_group(resource_group)
    return [(ns.name, ns.location) for ns in namespaces]
