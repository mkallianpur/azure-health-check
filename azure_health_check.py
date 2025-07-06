import argparse
import yaml
from azure_health import health_check

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Azure Resource Health Check")
    parser.add_argument('--config', required=True, help='Path to YAML config file')
    args = parser.parse_args()

    config = load_config(args.config)
    sub_id = config['subscription_id']
    rg = config['resource_group']
    checks = config.get('check', [])

    if 'vm' in checks:
        print("\n🔍 Checking VM status...")
        for name, status in health_check.check_vm_status(sub_id, rg):
            print(f"VM: {name} → {status}")

    if 'storage' in checks:
        print("\n📦 Checking Storage Accounts...")
        for name, loc in health_check.check_storage_accounts(sub_id, rg):
            print(f"Storage Account: {name} → {loc}")

    if 'servicebus' in checks:
        print("\n📨 Checking Service Bus...")
        for name, loc in health_check.check_service_bus(sub_id, rg):
            print(f"Service Bus: {name} → {loc}")

if __name__ == '__main__':
    main()
