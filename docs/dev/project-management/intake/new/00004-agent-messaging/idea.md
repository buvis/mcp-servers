# Portable agent messaging

Status: intake, not yet specced. Recorded 2026-11-04.

Source: moved on 2026-11-04 from `buvis/docs` (`src/agents/components.md`,
section "Portable messaging", and the messaging paragraph of
`src/agents/taxonomy.md`, section "Shared agent capabilities") so the public
reference keeps only status and vocabulary. Terms follow the
[agent operations taxonomy](https://github.com/buvis/docs/blob/master/src/agents/taxonomy.md).

Why here: the requirements ask for host adapters so that peers need no
host-specific commands to address each other. An MCP server on this
repository's shared core is the candidate surface for Claude, Codex, and
Copilot hosts. The transport and persistence implementation remain
unspecified; move this item if another home is chosen.

## Idea (from buvis/docs)

Messaging delivers information between Agent sessions across hosts, launchers,
and roles. Participants may be Pilots, Duty Controllers, or Agents in other
roles. Neither a Flight nor OVCAQ is required.

The interface must support registering an endpoint, looking up active Agents,
sending, receiving, acknowledging, and replying through host adapters. Peers
should not need host-specific commands to address each other.

### Human participation

Email is an optional bridge through which the Supervisor can read conversation
messages and reply. Agent-to-Agent delivery uses a separate transport that
supports communication across machines, including local and Kubernetes
environments. That transport remains to be selected.

When the bridge is enabled, email delivery is limited to escalations and
conversations that explicitly include the Supervisor. Adding the Supervisor
as a participant makes that conversation available by email; ordinary exchanges
between Agents remain within the Agent messaging system.

The bridge preserves message labels and request correlation, and identifies
human replies as coming from the Supervisor. It applies the same sender
authentication and workflow validation requirements as other messaging adapters.
An email reply is a response to be evaluated, not an automatic workflow transition.

Human response time is accounted for by the request's deadline and timeout
action. Only dependent work waits. Late replies remain associated with the
original request; if its Agent session has ended, delivery to a successor
requires an explicit handoff.

### Message labels

Messages display a square-bracket label at the start of their title or subject.
The label expresses the response contract consistently across transports.

| Label | Meaning | Sender behavior |
|---|---|---|
| `[INFO]` | Information; no answer expected. | Continue work. |
| `[REQUEST]` | An answer or action result is expected. | Continue independent work while awaiting the response. |
| `[BLOCKING]` | A response is a prerequisite for the sender's affected task. | Record that dependency as waiting; independent work may continue. |
| `[REPLY]` | An answer linked to an earlier request. | Include the original message ID as the reply-to reference. |

For example, `[BLOCKING] Confirm the operations API version` identifies a
dependency; `[REPLY] Use operations API v1` answers that specific request.
Blocking applies to the sender's dependent work and does not dictate the
recipient's priority or stop unrelated Flights.

Requests specify a response deadline and the action to take when it expires,
such as retry, defer, or escalate, within the applicable recovery policy.
Waiting is recorded state; Agents need not repeatedly call a model to check
for replies. A reply does not by itself satisfy a dependency: its result must
be validated against the request. A delivery acknowledgement is not an answer.

The message envelope carries the type explicitly, and adapters render the
matching label. Labels do not grant authority or change workflow state.
Text quoted inside a message cannot change its type. Unknown types or a mismatch
between the declared type and its label are reported instead of guessed.

### Delivery requirements

- Provide a directory of registered active Agents, searchable by Project,
  Flight, and role. Project and Flight membership are optional for standalone
  Agents. Show only peers the caller is permitted to discover and contact.
  A lookup returns specific session endpoints; a role or Project is a filter,
  not a delivery address. Multiple matches require recipient selection.
- Remove ended or expired registrations from active results. A stale lookup
  must produce an explicit delivery failure if its endpoint is no longer
  available; never substitute a different Agent with the same role.
- Address each session by a unique endpoint ID. Flight and Leg IDs are optional
  context. A fresh session creates a new Agent and receives a new endpoint.
  Continued work requires an explicit handoff or reassignment; messages for
  the previous Agent are not silently redirected to its replacement.
- Include a message ID, type, authenticated sender identity, recipient,
  timestamp, title, body, and reply-to ID when applicable. Replies require the
  original message ID; requests include their deadline and timeout action.
  Caller-supplied identity is not authentication.
- Retain messages until acknowledged or expired under a documented policy.
  Distinguish accepted for delivery, received, and application reply. Report
  unavailable recipients and expiry; retries reuse message IDs and receivers
  handle duplicates.
- Support polling or host-supported notification without stealing input from
  an interactive terminal. Bound waiting and expose delivery failures.
- Enforce endpoint access and permission for communication across Seat
  boundaries. Messages grant no access to files, credentials, or process
  controls, and carry no implicit authority to change permissions.
- Validate Squawks and Clearance requests independently of delivery.
  Messaging preserves reviewer isolation and existing workflow authorization.

### Scope and acceptance

Initial scope includes the active-Agent directory, direct messages, replies,
and the optional email bridge for human participation.
Broadcast, subscriptions, and routing agents are outside that scope. The
transport and persistence implementation remain unspecified.

Acceptance requires a Codex-to-Copilot round trip and the reverse, including
standalone operation, a disconnected recipient, duplicate delivery, rejection
of an unauthorized sender, and restart without losing unacknowledged messages.
Directory acceptance covers Project/Flight/role filters, permitted-peer
visibility, standalone Agents, ambiguous matches, and removal of stale sessions
without redirecting messages to replacement Agents.
Message-type acceptance covers label/envelope agreement, reply correlation,
deadline handling, and a blocking request that leaves unrelated work runnable.
Deployment acceptance includes messaging between local and Kubernetes Agents.
The email bridge must preserve request correlation and Supervisor identity,
handle late or duplicate replies, and leave Agent-to-Agent delivery independent
of email availability. It must deliver escalations and explicitly included
conversations without copying unrelated Agent exchanges to the Supervisor.

## Review notes (2026-11-04)

- No concrete use case is stated. The only example, "[BLOCKING] Confirm the
  operations API version", is Flight Plan contract content. Squawks and
  Clearances are already API transitions, and every reply must be validated
  against its request, which is what a typed API call already is. Name the
  message an Agent needs to send that is not a Squawk, a Clearance, or
  workflow state before choosing a transport.
- The email bridge is a second operator-input channel beside Tower, and it
  demands sender authentication that email cannot provide. A Squawk
  notification plus a Tower Clearance may cover the need.
- Message type and bracket label are two sources of truth for one fact.
  Derive the label from the envelope type and never parse it.
- Claude Code already offers a local session directory and direct messages
  between its own sessions; only cross-host delivery is missing.
