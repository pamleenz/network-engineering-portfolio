# Portfolio Audit — 2026-10-15

**Repository:** [network-engineering-portfolio](../)  
**Audit scope:** Complete default-branch directory inventory, root README, all existing module README files, M10/M12 publication, representative automation/security/reference configs. This is a **documentation and sample-config review**, **not** exhaustive line-by-line runtime validation of all device configs or a vulnerability assessment.

## Status

**Repository structure: COMPLETE for the documented study programme.** Previously missing M10 and M12 module directories and links have been added. M12 learner assessment remains pending. No production acceptance or non-Check-Point M10 vendor lab tests are claimed.

## Findings

| ID | Priority | Observation | Recommendation / Disposition |
|---|---|---|---|
| F01 | Resolved | Root README marked M10 Current and M12 Planned | Updated learning state, module paths and evidence distinctions |
| F02 | Resolved | M10/M12 missing from GitHub | Published per-module README plus GitHub-friendly Markdown study/handover guides |
| F03 | Informational | Check Point old ICMP checks were taken with temporary diagnostic rules; later removed | M10/M12 clearly describe these as historical evidence; recheck final installed policy before claiming current acceptance |
| F04 | Informational | Palo Alto/Junos/F5/Arista content is architecture, reference config and simulated incidents | Explicit DESIGN / NO VM VALIDATION across new module documentation |
| F05 | Follow-up | M09 GitHub Actions checks Python, schema/change intent and Ansible playbook syntax, not device reachability or production BGP/FIB/customer traffic | Describe as CI validation, not live deployment; add controlled integration tests only when supported test gear is available |
| F06 | Follow-up | M09 example `postcheck_from_data.yml` greps free-form CLI output (including `'best'`), which can be platform/format fragile; validate a `network` advertisement with exact prefix/mask on actual IOS/IOS-XE variant | Use structured parsed outputs or explicit `show bgp`/neighbor advertised-routes matched to full prefix and desired origin; test rollback independently |
| F07 | Documented limitation | FortiGate FortiOS evaluation build constrained IPsec proposal to DES and some HA/management features were only designed | Keep DES labelled LAB ONLY; production migration must use approved strong cryptography and subscriptions |
| F08 | Documented limitation | Nexus configs mapped from FRR/Linux EVPN lab; not all Cisco N9Kv syntax/hardware feature behaviour actually tested | Keep NX-OS snippets as REFERENCE and verify platform before reuse |
| F09 | Follow-up | M12 target migration, application tests, HA/failover, synthetic monitoring and signed service acceptance are not executed | Keep M12 service acceptance Pending; obtain real test evidence before operational sign-off |
| F10 | Follow-up | Some reference configuration examples may not constitute full deployable configurations (e.g. VRF, MLAG, VPN, BGP, management access) | Preserve explicit snippet/reference labels and add device/version-specific prechecks before reuse |
| F11 | Follow-up | Public project contains an encrypted Ansible Vault file and reference configurations | Encrypted does not remove credential rotation/access-review obligations; ensure no real reusable secrets or identity data are tracked, including Git history |
| F12 | Review limitation | This review did not execute every config or rerun CI/test suites | “All files verified correct” would overstate the audit; deep code/test verification requires runtime and a test environment |

## Link and structure check

- The tree now contains all documented top-level study areas and M10/M12 entry files.
- Root README references valid directory paths; GitHub resolves directory links even when the tree API lists directory names without trailing slashes.
- M10/M12 module README references are relative to their proper subdirectories.
- Review check did not establish the technical correctness of every legacy scenario output or all undocumented runtime dependencies.

## Next improvements, by priority

1. Complete and grade M12 independent scenario only after the learner provides an answer.
2. Capture updated Check Point final-policy and application-test evidence and an actual backup/restore rehearsal.
3. Strengthen M09 BGP assertions and add isolated integration-test examples that explicitly separate CI from deployed changes.
4. Verify representative FortiGate/M09 configuration against actual platform syntax, licenses and secure-production baselines.
5. Where vendor evaluation environments become available, add true Junos/PAN-OS/BIG-IP/EOS test artifacts rather than rewriting design notes as observed outputs.

**Audit outcome:** Portfolio content and indexing are coherent and suitable as an educational network-engineering portfolio, with the listed limitations. They should **not** be represented as a wholly lab-validated, production-ready multi-vendor network.

## 2026-10-15 Remediation Addendum

The later full-config pass reviewed **57 current configuration/YAML/shell/reference files** for obvious inline shared secrets and suspicious credential strings, plus all 14 module/root README files and their 44 internal relative Markdown links. No broken internal README links were found. This was a **static review**, not a penetration test or line-by-line vendor-device replay.

### Direct GitHub changes completed

- **M09 rollback blast radius:** Replaced the prior `no router bgp <AS>` whole-process deletion with scoped removal of a change-owned IPv4 BGP network statement and its Null0 route. Updated rollback verification to ensure the BGP AS remains configured. Historical pre-change ownership must still be proven before any live rollback.
- **M09 prefix accuracy:** Added explicit BGP network mask to `ios_bgp_address_family` example, aligned rollback with the IPv4 address-family, and repaired Jinja2 output directory creation.
- **M09 post-check:** Removed brittle fixed attribute-word-order checks. Added checks of route entry/best-path and advertisement with clear IOS-CLI-version limitations. These prove local control-plane assertions only, not remote acceptance or FIB/packet forwarding.
- **M09 intent checks:** Refactored `scripts/validate_change.py` to reject default/multicast/too-specific prefix and undefined or duplicated targets. Added offline `unittest` cases and enabled them in GitHub Actions.
- **M09 approved-target scope:** Added `validate_target_scope.yml` to both change and rollback workflows. The repository's static inventory lists only CE-AKL-01 although the sample change intends CE-AKL-01 and CE-AKL-02, so the live workflow now intentionally **fails closed** until the approved inventory is complete. CI syntax success does not run this gate against actual devices.
- **Wireless/NAC secret hygiene:** Redacted literal RADIUS shared-secret/CoA-secret strings from `enterprise-wireless-nac/configs/hostapd-corp.conf`. The historical Git version still exists. If either old value was ever a real or reused credential, rotate it. No claim is made that Git history was erased.
- **Documentation:** Updated M09 module README with explicit CI bounds, workflow safety conditions and inventory discrepancy. M10 and M12 technical documentation remains explicitly design/simulation-labelled where applicable.

### Test evidence and unresolved runtime checks

- The GitHub Actions runs invoked after these changes verify **Python offline unit tests, intent validation and Ansible playbook syntax**. Refer to the [M09 Actions history](https://github.com/pamleenz/network-engineering-portfolio/actions/workflows/m09-network-automation-ci.yml) for exact commit-specific outcomes; never equate Success with an IOS/NetBox integration test.
- The complete M09 BGP postcheck/rollback must still be validated on the target IOS/IOS-XE software release using known device output. It may need a model-driven or parsed-output check rather than CLI text grep.
- Actual Check Point final Security Policy after diagnostic-rule cleanup, external application tests, Palo Alto/Juniper/F5/Arista VM tests, HA/failover and M12 final independent scenario scoring cannot be completed from the GitHub repository.
- Historical credentials in older Git commits and encrypted Vault contents cannot be declared secure solely by inspecting current text. Confirm old secrets are test-only or rotate them, and keep new secrets external to this public repository.

**Post-remediation disposition:** Documentation coverage, internal README links and identified high-impact static workflow issues are corrected. **Production functional verification and final M12 individual assessment remain pending.**
