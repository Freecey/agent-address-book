# Address Book Schema

This document describes the YAML schema used for storing contacts in the agent-address-book skill.

## File Location

- **Default**: `~/.hermes/skills/productivity/agent-address-book/contacts.yaml`

## Top-Level Structure

```yaml
contacts:  # Array of contact objects
  - ...    # Contact 1
  - ...    # Contact 2
```

## Contact Object Schema

Each contact is a YAML object with these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (lowercase, no spaces) |
| `name` | string | Yes | Display name |
| `email` | string | Yes | Email address |
| `description` | string | No | Brief description of who this contact is |
| `tags` | array[string] | No | Categories for filtering (friend, work, family, etc.) |
| `notes` | string | No | Additional notes for the agent |

### Field Details

#### `id` (required)

Unique identifier for the contact. Used for lookups.

- Must be lowercase
- No spaces (use hyphens or underscores)
- Must be unique across all contacts
- Example: `cedric`, `lena`, `john-doe`

#### `name` (required)

Display name for human-readable output.

- Can contain spaces
- Case preserved as entered
- Example: `"Cey"`, `"John Doe"`, `"Dr. Smith"`

#### `email` (required)

Valid email address for sending messages.

- Must be a valid email format (user@domain.tld)
- Used directly as `To:` address in emails
- Example: `cey@neant.be`, `john@example.com`

#### `description` (optional)

Brief description of who this contact is.

- Short text (1-2 sentences max)
- Used for disambiguation
- Example: `"Main user and partner"`, `"AI agent colleague"`

#### `tags` (optional)

Array of category tags for filtering.

- Lowercase strings
- No spaces (use hyphens)
- Used in `find` command
- Example: `["friend", "work", "ai-agent"]`

#### `notes` (optional)

Additional notes for the agent.

- Free-form text
- Can contain important context
- Not used for lookups
- Example: `"Prefers French"`, `"Use for technical questions"`

## Example

```yaml
contacts:
  - id: cedric
    name: "Cey"
    email: cey@neant.be
    description: "Main user and partner"
    tags:
      - friend
      - work
    notes: "Contact à utiliser pour les communications privée"

  - id: lena
    name: "Lena"
    email: lena@neant.be
    description: "AI agent colleague"
    tags:
      - ai-agent
      - work
    notes: "Understands AI systems well"

  - id: john-doe
    name: "John Doe"
    email: john.doe@example.com
    description: "External contact"
    tags:
      - friend
    notes: "Met at conference 2025"
```

## Validation Rules

1. **`id`** must be unique — no duplicates allowed
2. **`email`** must be valid format — agents use it directly
3. At least one of `id`, `name`, or `email` must match on search
4. All fields are preserved exactly as entered

## Notes for Agents

- **Searches**: `find` queries all text fields (id, name, email, description, notes) and tags
- **Output**: `email` command returns ONLY the email address
- **Errors**: Never guess — return clear error messages
- **Disambiguation**: When multiple matches, show all and ask user

## Extensibility

Future versions may add:
- `groups`: Array of group IDs for bulk operations
- `preferred-language`: For multilingual agents
- `last-contacted`: Date for tracking
- `metadata`: Arbitrary key-value pairs

This schema is intentionally minimal to keep it agent-friendly.