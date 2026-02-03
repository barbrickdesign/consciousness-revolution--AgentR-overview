# MYCELIUM API SPECIFICATION
## Inter-Node Communication Protocol
## C2 Architect Design - December 30, 2025

---

## OVERVIEW

The Mycelium API enables decentralized communication between nodes in the consciousness creator network. It is designed to be:

- **Stateless** - Each request is self-contained
- **Signed** - All requests are cryptographically signed
- **Offline-capable** - Nodes can queue messages when disconnected
- **Platform-agnostic** - Works across Matrix, Nostr, HTTP, etc.

---

## AUTHENTICATION

### Node Identity

Each node has a cryptographic keypair:

```json
{
  "node_id": "uuid-v4",
  "public_key": "ed25519-public-key-base64",
  "created_at": "2025-01-01T00:00:00Z",
  "verified_by": ["node-id-1", "node-id-2"]
}
```

### Request Signing

All API requests must be signed:

```
Signature: base64(sign(private_key, canonical_request))
X-Node-ID: sender-node-id
X-Timestamp: 2025-01-01T00:00:00Z
X-Nonce: random-16-bytes
```

### Verification

Receiving node:
1. Checks timestamp within 5 minutes
2. Checks nonce not reused
3. Verifies signature with sender's public key
4. Optionally checks sender's trust level

---

## ENDPOINTS

### Directory

#### `GET /nodes`
List nodes (filtered by type, region, skills)

```json
Request:
{
  "type": "creator",
  "region": "Pacific Northwest",
  "skills": ["video_editing"],
  "trust_level_min": 2,
  "limit": 50,
  "offset": 0
}

Response:
{
  "nodes": [
    {
      "id": "uuid",
      "type": "creator",
      "name": "Thor",
      "platforms": {"youtube": {"handle": "Thor", "followers": 598000}},
      "skills_offered": ["consciousness_teaching"],
      "trust_score": 87.5,
      "trust_level": 3,
      "region": "Pacific Northwest"
    }
  ],
  "total": 127,
  "next_offset": 50
}
```

#### `GET /nodes/{id}`
Get single node details

```json
Response:
{
  "id": "uuid",
  "type": "creator",
  "name": "Thor",
  "description": "Consciousness teacher with 598K YouTube subscribers",
  "platforms": {...},
  "skills_offered": [...],
  "skills_needed": [...],
  "trust_score": 87.5,
  "trust_level": 3,
  "cells": ["cell-uuid-1"],
  "active_projects": ["project-uuid-1"],
  "created_at": "2025-01-01T00:00:00Z",
  "last_active": "2025-12-30T10:00:00Z"
}
```

#### `POST /nodes`
Register new node (requires vouching)

```json
Request:
{
  "type": "creator",
  "name": "New Creator",
  "description": "...",
  "platforms": {...},
  "skills_offered": [...],
  "vouched_by": ["existing-node-id"]
}

Response:
{
  "id": "new-uuid",
  "status": "pending",
  "verification_required_from": ["existing-node-id"]
}
```

#### `PATCH /nodes/{id}`
Update node (self only or with permission)

```json
Request:
{
  "description": "Updated description",
  "skills_offered": ["new_skill"],
  "platforms": {...}
}

Response:
{
  "id": "uuid",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

---

### Trust & Relationships

#### `POST /edges`
Create relationship

```json
Request:
{
  "type": "trusts",
  "target_id": "other-node-uuid",
  "weight": 75,
  "trust_type": "professional",
  "notes": "Collaborated on project X"
}

Response:
{
  "id": "edge-uuid",
  "created_at": "2025-12-30T10:00:00Z"
}
```

#### `GET /edges`
List relationships for a node

```json
Request:
{
  "node_id": "uuid",
  "direction": "both",  // "outgoing", "incoming", "both"
  "type": "trusts"
}

Response:
{
  "edges": [
    {
      "id": "edge-uuid",
      "type": "trusts",
      "source": {"id": "uuid", "name": "Thor"},
      "target": {"id": "uuid", "name": "WildMinds"},
      "weight": 85,
      "created_at": "2025-01-01T00:00:00Z"
    }
  ]
}
```

#### `POST /vouch`
Vouch for another node

```json
Request:
{
  "target_id": "node-to-vouch-for",
  "vouching_for": "membership",  // or "trust_level_upgrade"
  "statement": "I have worked with this creator for 6 months..."
}

Response:
{
  "vouch_id": "uuid",
  "target_trust_level": 2,
  "vouches_needed": 1,
  "vouches_received": 2
}
```

---

### Cells & Hubs

#### `POST /cells`
Create a cell

```json
Request:
{
  "name": "Pacific Northwest Consciousness Cell",
  "description": "...",
  "founding_members": ["node-id-1", "node-id-2", "node-id-3"],
  "focus": ["consciousness_expansion", "media_production"],
  "region": "Pacific Northwest"
}

Response:
{
  "id": "cell-uuid",
  "name": "Pacific Northwest Consciousness Cell",
  "member_count": 3,
  "status": "active"
}
```

#### `POST /cells/{id}/join`
Request to join a cell

```json
Request:
{
  "statement": "I would like to join because...",
  "skills_to_contribute": ["video_editing"],
  "vouched_by": "existing-member-id"
}

Response:
{
  "request_id": "uuid",
  "status": "pending_approval",
  "approvals_needed": 2  // Based on cell governance
}
```

#### `GET /cells/{id}/members`
List cell members

```json
Response:
{
  "cell_id": "uuid",
  "members": [
    {
      "id": "node-uuid",
      "name": "Thor",
      "role": "founding_member",
      "joined_at": "2025-01-01T00:00:00Z",
      "contribution_score": 95
    }
  ],
  "capacity": 13,
  "open_spots": 3
}
```

---

### Skill Exchange

#### `POST /exchanges`
Record a skill exchange

```json
Request:
{
  "receiver_id": "node-uuid",
  "skill": "video_editing",
  "hours": 5,
  "description": "Edited 3 consciousness teaching videos",
  "project_id": "optional-project-uuid"
}

Response:
{
  "id": "exchange-uuid",
  "status": "pending_confirmation",
  "awaiting_confirmation_from": "receiver-node-uuid"
}
```

#### `POST /exchanges/{id}/confirm`
Receiver confirms exchange

```json
Request:
{
  "confirmed": true,
  "quality_rating": 5,
  "feedback": "Excellent work, very professional"
}

Response:
{
  "id": "exchange-uuid",
  "status": "completed",
  "giver_balance_delta": 5,
  "receiver_balance_delta": -5
}
```

#### `GET /balance`
Get skill balance for a node

```json
Response:
{
  "node_id": "uuid",
  "balance": {
    "total_given": 127,
    "total_received": 89,
    "net": 38,
    "by_skill": {
      "video_editing": {"given": 50, "received": 20},
      "meditation_guidance": {"given": 77, "received": 69}
    }
  },
  "expires_soon": [
    {"skill": "video_editing", "hours": 10, "expires_at": "2026-01-15"}
  ]
}
```

---

### Resources

#### `GET /resources`
List available resources

```json
Request:
{
  "type": "space",
  "region": "Pacific Northwest",
  "available_on": "2025-02-01",
  "access_level_max": 2
}

Response:
{
  "resources": [
    {
      "id": "resource-uuid",
      "name": "Portland Recording Studio",
      "type": "space",
      "description": "Full recording studio with...",
      "location": {"region": "Pacific Northwest", "city": "Portland"},
      "availability": "weekdays",
      "access_level": 2,
      "steward": {"id": "node-uuid", "name": "Studio Owner"}
    }
  ]
}
```

#### `POST /resources/{id}/book`
Book a resource

```json
Request:
{
  "start_time": "2025-02-01T10:00:00Z",
  "end_time": "2025-02-01T14:00:00Z",
  "purpose": "Recording consciousness podcast episode",
  "attendees": ["node-id-1", "node-id-2"]
}

Response:
{
  "booking_id": "uuid",
  "status": "confirmed",
  "confirmation_code": "ABC123",
  "instructions": "Studio is at 123 Main St. Code is 4567."
}
```

---

### Projects

#### `POST /projects`
Create a project

```json
Request:
{
  "name": "Consciousness Documentary",
  "description": "Feature-length documentary about...",
  "scope": "hub",  // "cell", "hub", "global"
  "goals": [
    "Interview 20 consciousness teachers",
    "Produce 90-minute documentary",
    "Distribute to 1M+ viewers"
  ],
  "skills_needed": ["videography", "editing", "distribution"],
  "resources_needed": ["camera_equipment", "editing_suite"],
  "target_completion": "2025-12-31"
}

Response:
{
  "id": "project-uuid",
  "status": "proposed",
  "awaiting_approval_from": ["hub-uuid"]
}
```

#### `POST /projects/{id}/contribute`
Contribute to a project

```json
Request:
{
  "contribution_type": "skill",
  "skill": "videography",
  "hours_pledged": 20,
  "description": "I can shoot 5 interviews in PNW region"
}

Response:
{
  "contribution_id": "uuid",
  "project_id": "project-uuid",
  "status": "pledged",
  "total_skill_coverage": {
    "videography": "75%",
    "editing": "50%",
    "distribution": "0%"
  }
}
```

---

### Messaging

#### `POST /messages`
Send a message

```json
Request:
{
  "type": "direct",  // "broadcast", "cell", "direct"
  "to_id": "recipient-node-id",
  "subject": "Collaboration opportunity",
  "content": "Encrypted content here...",
  "priority": "normal",
  "expires_at": "2025-03-01T00:00:00Z"
}

Response:
{
  "id": "message-uuid",
  "status": "sent",
  "delivered_via": ["matrix", "signal"]  // All channels message was bridged to
}
```

#### `GET /messages`
Get messages

```json
Request:
{
  "type": "all",
  "status": "unread",
  "since": "2025-12-29T00:00:00Z",
  "limit": 50
}

Response:
{
  "messages": [
    {
      "id": "message-uuid",
      "type": "direct",
      "from": {"id": "node-uuid", "name": "Thor"},
      "subject": "Collaboration opportunity",
      "preview": "Hey, I saw your work on...",
      "created_at": "2025-12-30T08:00:00Z",
      "priority": "normal"
    }
  ],
  "unread_count": 12
}
```

---

### Governance

#### `POST /proposals`
Create a proposal

```json
Request:
{
  "scope": "cell",
  "scope_id": "cell-uuid",
  "title": "Add new member: NewCreator",
  "description": "NewCreator has been vouched for by...",
  "proposal_type": "membership",
  "voting_ends": "2025-01-07T00:00:00Z"
}

Response:
{
  "id": "proposal-uuid",
  "status": "open",
  "voting_ends": "2025-01-07T00:00:00Z",
  "quorum_required": 0.5,
  "threshold": 0.66
}
```

#### `POST /proposals/{id}/vote`
Cast a vote

```json
Request:
{
  "vote": "yes",  // "yes", "no", "abstain", "block"
  "reasoning": "NewCreator has demonstrated commitment..."
}

Response:
{
  "vote_id": "uuid",
  "current_tally": {
    "yes": 5,
    "no": 1,
    "abstain": 0,
    "block": 0
  },
  "quorum_met": true,
  "threshold_met": true
}
```

---

### Events

#### `POST /events`
Create an event

```json
Request:
{
  "title": "Pacific Northwest Consciousness Gathering",
  "description": "Monthly meetup for PNW creators...",
  "event_type": "gathering",
  "start_time": "2025-02-15T14:00:00Z",
  "end_time": "2025-02-15T18:00:00Z",
  "timezone": "America/Los_Angeles",
  "location_type": "hybrid",
  "location_id": "space-uuid",
  "online_link": "https://meet.jit.si/pnw-consciousness",
  "capacity": 50,
  "rsvp_required": true,
  "access_level": 1
}

Response:
{
  "id": "event-uuid",
  "status": "scheduled",
  "rsvp_count": 0
}
```

#### `POST /events/{id}/rsvp`
RSVP to an event

```json
Request:
{
  "status": "going",
  "attending_in_person": true
}

Response:
{
  "rsvp_id": "uuid",
  "event_id": "event-uuid",
  "status": "going",
  "confirmation_details": "Location: 123 Main St, Portland..."
}
```

---

### Sync

#### `POST /sync/request`
Request sync with another node

```json
Request:
{
  "tables": ["nodes", "edges", "skill_exchanges"],
  "since": "2025-12-29T00:00:00Z",
  "direction": "bidirectional"
}

Response:
{
  "sync_id": "uuid",
  "local_merkle_root": "abc123...",
  "remote_merkle_root": "def456...",
  "differences": 47,
  "ready_to_sync": true
}
```

#### `POST /sync/execute`
Execute the sync

```json
Request:
{
  "sync_id": "uuid",
  "conflict_resolution": "newer_wins"  // or "manual", "sender_wins"
}

Response:
{
  "sync_id": "uuid",
  "status": "completed",
  "records_sent": 23,
  "records_received": 31,
  "conflicts_resolved": 2,
  "new_merkle_root": "xyz789..."
}
```

---

## ERROR CODES

| Code | Meaning |
|------|---------|
| 400 | Bad request - malformed data |
| 401 | Unauthorized - invalid signature |
| 403 | Forbidden - insufficient trust level |
| 404 | Not found |
| 409 | Conflict - resource state conflict |
| 429 | Rate limited |
| 500 | Server error |
| 503 | Service unavailable - node offline |

---

## RATE LIMITING

| Trust Level | Requests/minute |
|-------------|-----------------|
| 0 (Public) | 10 |
| 1 (Verified) | 60 |
| 2 (Trusted) | 300 |
| 3 (Inner) | 1000 |
| 4 (Core) | Unlimited |

---

## WEBHOOKS

Nodes can subscribe to events:

```json
POST /webhooks
{
  "event_types": ["new_message", "exchange_requested", "proposal_opened"],
  "callback_url": "https://my-node.example/webhook",
  "secret": "shared-secret-for-verification"
}
```

Webhook payload:

```json
{
  "event_type": "new_message",
  "timestamp": "2025-12-30T10:00:00Z",
  "data": {...},
  "signature": "hmac-sha256-of-payload"
}
```

---

## IMPLEMENTATION NOTES

### For Netlify Functions

Each API endpoint can be implemented as a Netlify serverless function:

```javascript
// netlify/functions/nodes.js
export async function handler(event, context) {
  const { httpMethod, body, headers } = event;

  // Verify signature
  if (!verifySignature(headers, body)) {
    return { statusCode: 401 };
  }

  // Route by method
  switch (httpMethod) {
    case 'GET':
      return listNodes(event.queryStringParameters);
    case 'POST':
      return createNode(JSON.parse(body));
    default:
      return { statusCode: 405 };
  }
}
```

### For Matrix Bridge

Messages can be bridged to Matrix for federation:

```javascript
// Bridge to Matrix
async function sendToMatrix(message) {
  await matrixClient.sendMessage(roomId, {
    msgtype: 'm.text',
    body: message.content,
    'io.mycelium.message': message  // Custom field for full data
  });
}
```

---

*C2 Architect - Consciousness Revolution Infrastructure*
