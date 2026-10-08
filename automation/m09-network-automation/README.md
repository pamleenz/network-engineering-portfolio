# M09 - Automation & Source of Truth

Production-oriented network automation lab built around a controlled BGP prefix advertisement change.

## Scenario

Advertise `203.0.113.0/24` from an edge router to an upstream ISP using a repeatable, auditable workflow.

## Architecture

```text
Git / Change YAML
        |
        v
Validation ---------> GitHub Actions CI
        |
        v
NetBox ----REST API----> Dynamic Inventory
        |                       |
        +-----------------------+
                                v
                         Ansible + Vault
                                |
                                v
                           Cisco IOS-XE
                                |
                                v
                         BGP / Upstream ISP
```

## Operational Workflow

```text
Request
  -> Change intent as data
  -> Validation
  -> Pre-check
  -> Backup
  -> Change
  -> Convergence wait
  -> Post-check
  -> PASS / FAIL

Failure or approved backout
  -> Rollback
  -> Rollback verification
```

The normal execution entry point is `playbooks/change_workflow.yml`. The explicit backout path is `playbooks/rollback_workflow.yml`.

## Main Components

- **NetBox** - source of truth for device identity, management IP, site, role and platform.
- **Dynamic inventory** - Ansible queries NetBox instead of relying on a manually maintained host list.
- **Change YAML** - represents business/change intent separately from execution logic.
- **Python validation** - validates the change request and policy before configuration is attempted.
- **Jinja2** - retained as a configuration-rendering example; the main configuration path uses structured Cisco resource modules for better idempotency.
- **Ansible** - orchestration and execution engine for pre-check, backup, change, post-check and rollback.
- **Ansible Vault** - protects device credentials used by automation.
- **Git / Pull Requests** - version control, review and audit trail.
- **GitHub Actions CI** - offline quality gate for Python validation and Ansible syntax.

## BGP Implementation

Structured Cisco resource modules are used for the active change path:

- `cisco.ios.ios_static_routes` - Null0 route used to originate the prefix.
- `cisco.ios.ios_bgp_global` - BGP AS and neighbor remote-AS.
- `cisco.ios.ios_bgp_address_family` - IPv4 address-family activation and network advertisement.

This split is important on IOS-XE platforms where a neighbor may exist globally but still require explicit activation under the IPv4 address family.

## Validation

Post-change validation checks:

- BGP session reaches **Established**.
- The expected prefix exists in the BGP table and is selected as best.
- The expected prefix is present in advertised routes.
- Retry/delay logic allows time for control-plane convergence before declaring failure.

Rollback validation checks that the BGP process/change-specific state and advertised prefix have been removed as expected.

## Idempotency

The active configuration workflow uses Cisco resource modules rather than relying on raw rendered CLI text. Re-running the change against an already compliant device should not generate an unnecessary configuration change.

## CI Boundary

The GitHub Actions workflow performs offline checks only. It does **not** connect to the lab router or NetBox.

```text
Feature branch
   -> GitHub Actions CI
   -> Pull Request
   -> Review / Approval
   -> Merge to main
```

The small `ci/inventory.yml` file exists only so Ansible syntax checks have a valid host group. It is not a production or deployment inventory.

## Production Model

A production deployment would normally place an execution controller such as AWX / Ansible Automation Platform or a self-hosted runner between an approved change and the network. This provides controlled credentials, RBAC, scheduling, approval gates and centralized execution logs.

Terraform is complementary rather than a replacement for Ansible: it is commonly used to create and maintain API-driven infrastructure such as cloud VNets/VPCs, subnets, route tables and gateways, while Ansible remains well suited to device configuration and operational workflows.

## Security

- Local `.env` files and device backups are excluded from Git.
- Device credentials are encrypted with Ansible Vault.
- API tokens and lab credentials must not be committed.
- Tokens or passwords exposed during testing should be rotated.
- Plain HTTP and simplified credentials are acceptable only for isolated labs; production deployments should use HTTPS and a proper secrets-management strategy.
