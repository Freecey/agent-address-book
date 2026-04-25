#!/usr/bin/env python3
"""
agent-address-book - Minimal CLI address book for AI agents.

Usage:
    python3 address_book.py list
    python3 address_book.py find <query>
    python3 address_book.py email <query>
    python3 address_book.py show <query>
    python3 address_book.py upsert --id <id> --name <name> --email <email> ...
"""

import argparse
import json
import os
import sys
import yaml
from pathlib import Path

# Configuration
SKILL_DIR = Path(__file__).parent.parent
CONTACTS_FILE = SKILL_DIR / "contacts.yaml"


def load_contacts() -> list:
    """Load contacts from YAML file."""
    if not CONTACTS_FILE.exists():
        return []
    
    with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
        return data.get("contacts", [])


def save_contacts(contacts: list) -> None:
    """Save contacts to YAML file."""
    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        yaml.dump({"contacts": contacts}, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def find_contacts(contacts: list, query: str) -> list:
    """Find contacts matching query across all fields."""
    query_lower = query.lower()
    matches = []
    
    for contact in contacts:
        # Search in all fields
        searchable = " ".join([
            contact.get("id", ""),
            contact.get("name", ""),
            contact.get("email", ""),
            contact.get("description", ""),
            contact.get("notes", ""),
            " ".join(contact.get("tags", []))
        ]).lower()
        
        if query_lower in searchable:
            matches.append(contact)
    
    return matches


def cmd_list(contacts: list) -> None:
    """List all contacts."""
    # Output as JSON for agent consumption
    print(json.dumps(contacts, indent=2, ensure_ascii=False))


def cmd_find(contacts: list, query: str) -> None:
    """Find contacts matching query."""
    query = query.strip()
    if not query:
        print(json.dumps({"error": "Query cannot be empty"}), file=sys.stderr)
        sys.exit(1)
    
    matches = find_contacts(contacts, query)
    
    if not matches:
        print(json.dumps({"error": f"No contacts found matching '{query}'"}), file=sys.stderr)
        sys.exit(1)
    
    print(json.dumps(matches, indent=2, ensure_ascii=False))


def cmd_email(contacts: list, query: str) -> None:
    """Get email address only for matching contact."""
    query = query.strip()
    if not query:
        print(json.dumps({"error": "Query cannot be empty"}), file=sys.stderr)
        sys.exit(1)
    
    matches = find_contacts(contacts, query)
    
    if not matches:
        print(json.dumps({"error": f"No contact found for '{query}'. Do not guess or invent an address."}), file=sys.stderr)
        sys.exit(1)
    
    if len(matches) > 1:
        # Multiple matches - show candidates
        candidates = [{"id": c.get("id"), "name": c.get("name"), "email": c.get("email")} for c in matches]
        print(json.dumps({"error": f"Multiple contacts match '{query}'. Choose one:", "candidates": candidates}), file=sys.stderr)
        sys.exit(1)
    
    # Single match - return just email
    email = matches[0].get("email", "")
    if not email:
        print(json.dumps({"error": f"Contact found but no email address for '{query}'"}), file=sys.stderr)
        sys.exit(1)
    
    print(email)


def cmd_show(contacts: list, query: str) -> None:
    """Show full contact details."""
    query = query.strip()
    if not query:
        print(json.dumps({"error": "Query cannot be empty"}), file=sys.stderr)
        sys.exit(1)
    
    matches = find_contacts(contacts, query)
    
    if not matches:
        print(json.dumps({"error": f"No contact found for '{query}'"}), file=sys.stderr)
        sys.exit(1)
    
    if len(matches) > 1:
        candidates = [{"id": c.get("id"), "name": c.get("name")} for c in matches]
        print(json.dumps({"error": f"Multiple contacts match '{query}':", "candidates": candidates}), file=sys.stderr)
        sys.exit(1)
    
    print(json.dumps(matches[0], indent=2, ensure_ascii=False))


def cmd_upsert(contacts: list, args: argparse.Namespace) -> None:
    """Add or update a contact."""
    # Validate required fields
    if not args.id:
        print(json.dumps({"error": "--id is required"}), file=sys.stderr)
        sys.exit(1)
    
    if not args.email:
        print(json.dumps({"error": "--email is required"}), file=sys.stderr)
        sys.exit(1)
    
    # Check for existing contact
    existing_idx = None
    for i, c in enumerate(contacts):
        if c.get("id") == args.id:
            existing_idx = i
            break
    
    # Build contact object
    contact = {
        "id": args.id,
        "name": args.name or (existing_idx is not None and contacts[existing_idx].get("name", "")) or "",
        "email": args.email,
        "description": args.description or (existing_idx is not None and contacts[existing_idx].get("description", "")) or "",
        "tags": args.tags.split(",") if args.tags else (existing_idx is not None and contacts[existing_idx].get("tags", [])) or [],
        "notes": args.notes or (existing_idx is not None and contacts[existing_idx].get("notes", "")) or ""
    }
    
    # Clean empty tags
    if contact["tags"]:
        contact["tags"] = [t.strip() for t in contact["tags"] if t]
    else:
        contact["tags"] = []
    
    # Update or add
    if existing_idx is not None:
        contacts[existing_idx] = contact
        action = "updated"
    else:
        contacts.append(contact)
        action = "added"
    
    save_contacts(contacts)
    
    print(json.dumps({
        "success": True,
        "action": action,
        "contact": {
            "id": contact["id"],
            "name": contact["name"],
            "email": contact["email"]
        }
    }, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="agent-address-book: Minimal CLI address book for AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 address_book.py list
    python3 address_book.py find cedric
    python3 address_book.py email cedric
    python3 address_book.py show lena
    python3 address_book.py upsert --id john --name "John Doe" --email john@example.com --tags work,friend
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # list command
    subparsers.add_parser("list", help="List all contacts")
    
    # find command
    find_parser = subparsers.add_parser("find", help="Find contacts by query")
    find_parser.add_argument("query", help="Search query")
    
    # email command
    email_parser = subparsers.add_parser("email", help="Get email address only")
    email_parser.add_argument("query", help="Search query")
    
    # show command
    show_parser = subparsers.add_parser("show", help="Show full contact details")
    show_parser.add_argument("query", help="Search query")
    
    # upsert command
    upsert_parser = subparsers.add_parser("upsert", help="Add or update a contact")
    upsert_parser.add_argument("--id", required=True, help="Unique contact ID")
    upsert_parser.add_argument("--name", help="Display name")
    upsert_parser.add_argument("--email", required=True, help="Email address")
    upsert_parser.add_argument("--description", help="Brief description")
    upsert_parser.add_argument("--tags", help="Comma-separated tags")
    upsert_parser.add_argument("--notes", help="Additional notes")
    
    args = parser.parse_args()
    
    # Load contacts
    contacts = load_contacts()
    
    # Execute command
    if args.command == "list":
        cmd_list(contacts)
    elif args.command == "find":
        cmd_find(contacts, args.query)
    elif args.command == "email":
        cmd_email(contacts, args.query)
    elif args.command == "show":
        cmd_show(contacts, args.query)
    elif args.command == "upsert":
        cmd_upsert(contacts, args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()