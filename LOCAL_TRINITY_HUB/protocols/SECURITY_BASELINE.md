# SECURITY BASELINE
## Minimum Security Requirements

---

## PRINCIPLE

Security is not optional.
Security is not an afterthought.
Security is the foundation everything else stands on.

**If it's not secure, it doesn't ship.**

---

## MINIMUM REQUIREMENTS

### Authentication
- [ ] All systems require authentication
- [ ] No default passwords
- [ ] Multi-factor where possible
- [ ] Session timeouts enforced
- [ ] Failed attempt lockouts

### Authorization
- [ ] Principle of least privilege
- [ ] Role-based access control
- [ ] No shared accounts
- [ ] Access regularly audited
- [ ] Permissions documented

### Encryption
- [ ] Data encrypted at rest
- [ ] Data encrypted in transit
- [ ] Strong encryption standards (AES-256, TLS 1.3)
- [ ] Keys properly managed
- [ ] No hardcoded secrets

### Logging
- [ ] All access logged
- [ ] All changes logged
- [ ] Logs tamper-protected
- [ ] Logs regularly reviewed
- [ ] Alerts on anomalies

---

## CREDENTIAL MANAGEMENT

### Storage
- Never in code
- Never in plain text
- Environment variables or vault
- Encrypted at rest
- Access logged

### Rotation
- API keys: Every 90 days
- Passwords: Every 180 days
- Certificates: Before expiration
- After any suspected compromise: Immediately

### Sharing
- Never via email
- Never via chat
- Use secure vault or encrypted channel
- Temporary access when possible
- Revoke when no longer needed

---

## ACCESS CONTROL

### Commander Level
- Full system access
- All credentials
- All environments
- All nodes

### Terminal Instance Level (C1, C2, C3)
- Working directory access
- Assigned credentials only
- Execution permissions
- No credential management

### Worker Level
- Task-specific access only
- No persistent access
- Results returned to parent
- Terminated after task

### Network Node Level
- Syncthing sync access
- Local system access
- Network communication
- Shared credential subset

---

## NETWORK SECURITY

### Firewall Rules
- Default deny inbound
- Allow only required ports
- Document all open ports
- Regular rule review

### Required Ports
| Port | Service | Access |
|------|---------|--------|
| 22 | SSH | Internal only |
| 443 | HTTPS | As needed |
| 22000 | Syncthing | Internal only |
| 41641 | Tailscale | VPN only |

### Network Segmentation
- Development network isolated
- Production network isolated
- Management network isolated
- No cross-network access without explicit rule

---

## CODE SECURITY

### Before Commit
- [ ] No secrets in code
- [ ] No API keys hardcoded
- [ ] Dependencies scanned
- [ ] Input validation present
- [ ] Output encoding present

### OWASP Top 10 Coverage
- [ ] Injection prevention
- [ ] Authentication checks
- [ ] Sensitive data protection
- [ ] XXE prevention
- [ ] Access control
- [ ] Security misconfiguration review
- [ ] XSS prevention
- [ ] Deserialization checks
- [ ] Component vulnerability check
- [ ] Logging and monitoring

### Dependency Management
- Known vulnerabilities scanned
- Outdated packages flagged
- Automatic security updates
- License compliance checked

---

## DATA SECURITY

### Classification
| Level | Description | Handling |
|-------|-------------|----------|
| PUBLIC | Can be shared | Standard |
| INTERNAL | Team only | Encrypted at rest |
| CONFIDENTIAL | Need-to-know | Encrypted + access logged |
| SECRET | Commander only | Maximum protection |

### Handling Requirements
- PUBLIC: No special requirements
- INTERNAL: Encrypted storage, team access
- CONFIDENTIAL: Encrypted, logged, audited
- SECRET: Encrypted, MFA, audit trail, Commander only

### Data Disposal
- Secure delete (not just delete)
- Multiple overwrites for sensitive
- Verify deletion
- Log disposal

---

## BACKUP SECURITY

### Backup Requirements
- Encrypted before storage
- Encrypted in transit
- Stored in multiple locations
- Tested regularly
- Access logged

### Backup Access
- Commander only for full restore
- Verified before restoration
- Logged when accessed
- Decryption keys secured separately

---

## INCIDENT RESPONSE

### Detection
- Monitor logs for anomalies
- Alert on suspicious patterns
- Regular security scans
- Threat intelligence feeds

### Response Steps
1. **Detect** - Identify the incident
2. **Contain** - Stop the spread
3. **Eradicate** - Remove the threat
4. **Recover** - Restore operations
5. **Learn** - Document and improve

### Severity Levels
| Level | Description | Response Time |
|-------|-------------|---------------|
| CRITICAL | Active breach | Immediate |
| HIGH | Confirmed vulnerability | < 4 hours |
| MEDIUM | Potential vulnerability | < 24 hours |
| LOW | Minor issue | < 7 days |

---

## SECURITY MONITORING

### Daily Checks
- Failed login attempts
- Unusual access patterns
- Error rate spikes
- Resource anomalies

### Weekly Checks
- Log review
- Access audit
- Vulnerability scan
- Backup verification

### Monthly Checks
- Full security audit
- Penetration test (if resources allow)
- Policy review
- Training refresh

### Quarterly Checks
- Full credential rotation
- Access recertification
- Disaster recovery test
- Security architecture review

---

## SECURITY TOOLS

### Required
- Password manager / Vault
- Encryption tools
- Log aggregation
- Backup system

### Recommended
- Vulnerability scanner
- Intrusion detection
- SIEM (Security Information and Event Management)
- Threat intelligence

---

## COMPLIANCE

### Audit Trail
- All security events logged
- Logs retained 1 year minimum
- Logs searchable and exportable
- Regular audit review

### Documentation
- Security policies documented
- Procedures documented
- Exceptions documented
- Changes documented

---

## SECURITY CULTURE

### Principles
- Security is everyone's job
- Report suspicious activity
- Ask if unsure
- Better safe than compromised

### Training
- Security awareness (ongoing)
- Phishing recognition
- Incident reporting
- Secure coding practices

### Accountability
- Security violations documented
- Patterns addressed
- Improvements implemented
- No blame, just fixes

---

## QUICK REFERENCE CHECKLIST

### Before Deploying Anything
- [ ] Secrets externalized
- [ ] Authentication required
- [ ] Authorization checked
- [ ] Encryption enabled
- [ ] Logging configured
- [ ] Input validated
- [ ] Output encoded
- [ ] Dependencies scanned
- [ ] Access documented

### After Any Security Incident
- [ ] Incident documented
- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Prevention added
- [ ] Protocol updated
- [ ] Team informed

---

## THE BASELINE GUARANTEE

Every system in this network will:
1. Authenticate users
2. Authorize actions
3. Encrypt data
4. Log access
5. Alert on anomalies

**No exceptions. No shortcuts. No excuses.**

Security is the price of autonomy.
Without security, there is no sovereignty.
The baseline is the minimum. Exceed it.

**Secure the system. Protect the mission.**
