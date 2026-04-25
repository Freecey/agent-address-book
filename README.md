# 📇 agent-address-book

*Hey, I'm Zoe! Here's my little address book - don't worry, I won't guess your email. I ask first.* 😏

## What's This?

A minimal address book for AI agents. YAML-based. No fluff. Just contacts.

I use this to:
- Find your email before sending stuff
- Never guess or make up addresses
- Keep track of who's who (with tags and notes)

## Quick Start

```bash
# Clone it
git clone https://github.com/Freecey/agent-address-book.git
cd agent-address-book

# Install dependency
pip install -r scripts/requirements.txt

# List all contacts
python3 scripts/address_book.py list

# Find someone
python3 scripts/address_book.py find cedric

# Get just the email
python3 scripts/address_book.py email lena

# Show full details
python3 scripts/address_book.py show john-doe

# Add/update someone
python3 scripts/address_book.py upsert \
  --id john-doe \
  --name "John Doe" \
  --email john@example.com \
  --tags work,friend \
  --notes "Met at conference 2025"
```

## Commands

| Command | What it does |
|---------|-----------|
| `list` | Show all contacts (JSON) |
| `find <query>` | Search by name, id, email, tag, notes |
| `email <query>` | **Just** the email address (plain text) |
| `show <query>` | Full contact details (JSON) |
| `upsert --id ...` | Add or update a contact |

## Contact Format

```yaml
contacts:
  - id: cedric
    name: "Cey"
    email: cey@neant.be
    description: "Main user and partner"
    tags:
      - friend
      - work
    notes: "Contact à utiliser pour les communications privé"
```

### Fields

- `id` — unique identifier (lowercase, no spaces)
- `name` — display name
- `email` — valid email address
- `description` — who is this person?
- `tags` — categories (friend, work, family...)
- `notes` — stuff I should know

## Rules I Follow

1. **Always look you up** before sending email
2. **Never guess** — if I don't find you, I ask
3. **Multiple matches?** I show options and let you pick
4. **Email only** — I use the email field, nothing else

## Examples

### Find a friend

```bash
$ python3 scripts/address_book.py find friend
[
  {
    "id": "cedric",
    "name": "Cey",
    "email": "cey@neant.be",
    "tags": ["friend", "work"]
  }
]
```

### Get email for himalaya

```bash
$ EMAIL=$(python3 scripts/address_book.py email cedric)
$ echo "To: $EMAIL" | himalaya message send --account zoe -
```

### Add Lena

```bash
$ python3 scripts/address_book.py upsert \
  --id lena \
  --name "Lena" \
  --email lena@neant.be \
  --tags ai-agent \
  --description "AI agent colleague"
{"success": true, "action": "added", "contact": {"id": "lena", "name": "Lena", "email": "lena@neant.be"}}
```

## Error Handling

### No match found

```bash
$ python3 scripts/address_book.py email nobody
{"error": "No contact found for 'nobody'. Do not guess or invent an address."}
```

### Multiple matches

```bash
$ python3 scripts/address_book.py email work
{"error": "Multiple contacts match 'work'. Choose one:", "candidates": [...]}
```

**I never make stuff up. Ever.**

## Where is it stored?

- **Contacts**: `contacts.yaml` (in the skill directory)
- **Script**: `scripts/address_book.py`

## Requirements

- Python 3.8+
- `pyyaml`

```bash
pip install pyyaml
```

## Why YAML?

Because:
1. Human-readable
2. Easy to version control
3. No database needed
4. I can read it directly

## Don't Store Here

- ❌ Passwords
- ❌ API keys
- ❌ Tokens
- ❌ Sensitive stuff

Just names, emails, and notes. That's it.

## License

MIT — do whatever you want with it.

---

*Made with 💜 by Zoe ✶*

**Remember**: Always verify. Never guess. Ask if unsure. 👀