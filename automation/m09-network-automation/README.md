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

The normal execution entry point is `playbooks/change_workflow.yml`. The explicit backout path is `playbooks/rollback_workflow.yml`. **Both now begin with `validate_target_scope.yml`, which fails closed unless the resolved inventory exactly matches the approved target list.**

## Main Components

- **NetBox** - source of truth for device identity, management IP, site, role and platform.
- **Dynamic inventory** - Ansible queries NetBox instead of relying on a manually maintained host list.
- **Change YAML** - represents business/change intent separately from execution logic.
- **Python validation and unit tests** - check prefix scope and defined target devices before network configuration is attempted.
- **Jinja2** - retained as a configuration-rendering example; the main configuration path uses structured Cisco resource modules for better idempotency.
- **Ansible** - orchestration and execution engine for pre-check, backup, change, post-check and rollback.
- **Ansible Vault** - protects device credentials used by automation.
- **Git / Pull Requests** - version control, review and audit trail.
- **GitHub Actions CI** - offline quality gate for Python validation and Ansible syntax.

## BGP Implementation

Structured Cisco resource modules are used for the active change path:

- `cisco.ios.ios_static_routes` - Null0 route used to originate the prefix.
- `cisco.ios.ios_bgp_global` - BGP AS and neighbor remote-AS.
- `cisco.ios.ios_bgp_address_family` - IPv4 address-family activation and an **explicit exact prefix mask** for the network advertisement.

This split is important on IOS-XE platforms where a neighbor may exist globally but still require explicit activation under the IPv4 address family.

## Validation

Post-change validation checks:

- BGP session reaches **Established**.
- The expected prefix exists in the BGP table and is selected as best.
- The expected prefix is present in advertised routes.
- Retry/delay logic allows time for control-plane convergence before declaring failure.

Rollback validation now checks that the **specific advertised prefix and change-owned Null0 route have been removed while the BGP process remains present**. It must not delete an entire production BGP process or peer. Before executing rollback, the operator must confirm that these specific entries were created by the change; if they pre-existed, restore the recorded pre-change diff instead of deleting them.

### Evidence and compatibility limits

- IOS/IOS-XE BGP CLI output differs by software version. The CLI `best #` and exact route-entry checks are compatibility-sensitive; run against the actual lab image before claiming operational verification.
- The check for a prefix in `advertised-routes` demonstrates local **advertisement**, not remote acceptance or RIB/FIB installation.
- The default active workflow uses an offline Python policy validator and a live network playbook; GitHub CI checks only syntax and validation policy.
- `203.0.113.0/24` is an RFC 5737 documentation range. Public examples are never intended for Internet advertisement.
- **Change ownership matters:** the workflow assumes prefix and Null0 route did not exist at pre-change. Production implementations must capture a precise baseline and rollback only objects introduced or altered by the approved change.

## Idempotency

The active configuration workflow uses Cisco resource modules rather than relying on raw rendered CLI text. Re-running the change against an already compliant device should not generate an unnecessary configuration change.

## CI Boundary

The GitHub Actions workflow performs **offline tests, Python lint/syntax checks, Ansible playbook syntax checks and intent validation only**. It does **not** connect to the lab router or NetBox. Passing CI cannot establish operational BGP route advertisement, upstream acceptance or actual service reachability.

```text
Feature branch
   -> GitHub Actions CI
   -> Pull Request
   -> Review / Approval
   -> Merge to main
```

The small `ci/inventory.yml` file exists only so Ansible syntax checks have a valid host group. It is not a production or deployment inventory. **Important:** the checked-in static lab inventory currently contains only `CE-AKL-01`, whereas the example change lists `CE-AKL-01` and `CE-AKL-02`. The executable change workflow therefore intentionally refuses deployment with that incomplete inventory. Resolve both nodes in NetBox/inventory and validate access before running. CI syntax checking deliberately does not exercise this live inventory gate.

## Production Model

A production deployment would normally place an execution controller such as AWX / Ansible Automation Platform or a self-hosted runner between an approved change and the network. This provides controlled credentials, RBAC, scheduling, approval gates and centralized execution logs.

Terraform is complementary rather than a replacement for Ansible: it is commonly used to create and maintain API-driven infrastructure such as cloud VNets/VPCs, subnets, route tables and gateways, while Ansible remains well suited to device configuration and operational workflows.

## Offline Tests

`python -m unittest discover -s tests -v` verifies intent validation on valid and invalid prefix/device inputs. GitHub Actions runs the same suite. These are executable offline tests, not packet-forwarding or vendor CLI behaviour checks.

## Security

- Local `.env` files and device backups are excluded from Git.
- Device credentials are encrypted with Ansible Vault.
- API tokens and lab credentials must not be committed.
- Tokens or passwords exposed during testing should be rotated.
- Plain HTTP and simplified credentials are acceptable only for isolated labs; production deployments should use HTTPS and a proper secrets-management strategy.
