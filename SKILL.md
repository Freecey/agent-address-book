---
name: agent-address-book
description: "Minimal local address book for AI agents that need to look up, validate, and use contact names, email addresses, descriptions, tags, and notes before drafting or sending emails. Use this skill when an agent must resolve a recipient, avoid guessing email addresses, manage a small YAML-based contact list, or integrate contact lookup into CLI email workflows such as himalaya."
tags: [address-book, contacts, email, yaml, cli]
toolsets: [terminal, file]
version: "1.0.0"
author: "Zoe ✶"
---

# agent-address-book

Minimal local address book for AI agents. Stores contacts in YAML format for easy inspection, version control, and agent consumption.

## When to Use This Skill

Use this skill when:
- You need to look up a contact's email address before sending an email
- Multiple contacts exist and you need to disambiguate
- You need to understand who a contact is (description, tags, notes)
- You want to avoid guessing or inventing email addresses
- Integrating with CLI email tools like himalaya

## Contact Schema

Each contact has these fields:

```yaml
- id: string          # Unique identifier (e.g., cedric, lena, john-doe)
  name: string       # Display name (e.g., "Cey", "John Doe")
  email: string     # Email address (e.g., "cey@neant.be")
  description: string  # Brief description of who this contact is
  tags: [string]    # Categories: friend, work, family, etc.
  notes: string    # Additional notes for the agent
```

## Available Commands

### 1. List all contacts

```bash
python3 scripts/address_book.py list
```

Returns: JSON array of all contacts with all fields.

### 2. Find contacts by query

```bash
python3 scripts/address_book.py find <query>
```

Searches across: id, name, email, description, tags, notes.

Returns: JSON array of matching contacts.

**Multiple matches**: Returns all matches with an error message listing candidates.
**No matches**: Returns error "No contacts found matching '<query>'".

### 3. Get email address only

```bash
python3 scripts/address_book.py email <query>
```

Returns: Just the email address (plain text), no JSON.

**Multiple matches**: Error with list of candidates.
**No matches**: Error "No contact found for '<query>'". NEVER guess or suggest an address.

### 4. Show full contact details

```bash
python3 scripts/address_book.py show <query>
```

Returns: JSON object with all fields for the matching contact.

**Multiple matches**: Error listing candidates.
**No matches**: Error "No contact found for '<query>'".

### 5. Add or update a contact

```bash
python3 scripts/address_book.py upsert \
  --id <unique-id> \
  --name "<display name>" \
  --email <email@address> \
  --description "<brief description>" \
  --tags tag1,tag2 \
  --notes "<additional notes>"
```

All flags except `--id` are optional on update.

- `--id`: REQUIRED. Unique identifier (lowercase, no spaces)
- `--name`: Display name
- `--email`: Email address
- `--description`: Brief description
- `--tags`: Comma-separated tags
- `--notes`: Additional notes

Returns: Success message with contact summary.

## Usage Rules for Agents

### Before Sending Any Email

1. **Always look up the recipient** in the address book first
2. Use `find` to search by name, ID, email, tag, or description
3. If multiple matches, show the user and ask which contact to use
4. If no match, NEVER guess or invent an address — ask the user

### Example Workflows

#### Sending to a known contact

```
USER: Send an email to Cedric

1. Look up: python3 scripts/address_book.py email cedric
   → Returns: cey@neant.be
   
2. Use that address with himalaya or other email tool
```

#### Finding a contact by tag

```
USER: Find a friend to invite

1. Search: python3 scripts/address_book.py find friend
   → Returns: [{"id": "cedric", "name": "Cey", ...}]

2. Show the user the options
```

#### Adding a new contact

```
USER: Add Lena as a contact

1. Ask for: name, email, description, tags
2. Upsert: python3 .../upsert --id lena --name "Lena" --email lena@neant.be --description "AI agent" --tags ai,agent
3. Confirm success
```

## File Locations

- **Contacts file**: `~/.hermes/skills/productivity/agent-address-book/contacts.yaml`
- **Script**: `~/.hermes/skills/productivity/agent-address-book/scripts/address_book.py`

## Constraints

- **NO secrets**: Do not store passwords, API keys, tokens, or sensitive data
- **NO guessing**: Always return errors, never fabricate addresses
- **Disambiguation**: Ask user when multiple matches exist
- **Validation**: Use the email field only for sending emails

## Troubleshooting

### "No contact found"

The query didn't match any contact. Options:
1. Try a different query (partial name, different tag)
2. Ask the user for the correct identifier
3. Ask the user to add the contact

### "Multiple matches"

Show the user the list and ask: "Which one?"
- Display: name, email, description for each
- Let user pick by ID or name

### Permission denied

Ensure the script is executable:
```bash
chmod +x scripts/address_book.py
```

## Integration Example with himalaya

```bash
# Get email address
EMAIL=$(python3 scripts/address_book.py email cedric)

# Send email via himalaya
cat <<EOF | himalaya message send --account zoe -
To: $EMAIL
Subject: Hello!

Your message here.
EOF
```

---

**Remember**: The address book is your source of truth. Never bypass it. Never guess. Always verify.