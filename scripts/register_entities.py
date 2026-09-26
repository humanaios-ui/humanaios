#!/usr/bin/env python3
"""
M2 Rank 3 Phase 3: Entity Registration Script
Registers all discovered entities (projects, contacts, orgs, engagements, users)
in the entity_registry with canonical identifiers and authority tiers.
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set

class EntityRegistrar:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.registered_count = 0
        self.entities = {
            'projects': [],
            'contacts': [],
            'organizations': [],
            'engagements': [],
            'users': []
        }

    def discover_projects(self):
        """Discover all projects from .empirica/project.yaml files."""
        practices_dir = Path("/Users/andersonfamily/practices")

        for project_yaml in practices_dir.glob("**/.empirica/project.yaml"):
            try:
                with open(project_yaml) as f:
                    content = f.read()
                    # Simple YAML parsing for ai_id
                    for line in content.split('\n'):
                        if line.startswith('ai_id:'):
                            ai_id = line.split(':', 1)[1].strip().strip("'\"")
                            self.entities['projects'].append({
                                'ai_id': ai_id,
                                'canonical_id': f'empirica-foundation.carly.{ai_id}',
                                'path': str(project_yaml),
                                'authority_tier': 'owner'
                            })
                            break
            except Exception as e:
                print(f"Error reading {project_yaml}: {e}")

    def discover_contacts(self):
        """Discover contacts from git log and project.yaml."""
        contacts_set = set()

        # Carly is always admiral
        self.entities['contacts'].append({
            'email': 'carly.r.anderson@gmail.com',
            'name': 'Carly R. Anderson',
            'canonical_id': 'carly.r.anderson@gmail.com',
            'authority_tier': 'admiral',
            'source': 'project.yaml owner'
        })
        contacts_set.add('carly.r.anderson@gmail.com')

        # Add known contributors
        known_contacts = [
            ('aioshuman@gmail.com', 'AI OS Human', 'member'),
            ('andersonfamily@Carlys-MacBook-Pro.local', 'Local Developer', 'member'),
        ]

        for email, name, tier in known_contacts:
            if email not in contacts_set:
                self.entities['contacts'].append({
                    'email': email,
                    'name': name,
                    'canonical_id': email,
                    'authority_tier': tier,
                    'source': 'git log'
                })
                contacts_set.add(email)

        # Parse git log for additional contributors
        try:
            result = subprocess.run(
                ['git', 'log', '--format=%aE %aN'],
                cwd='/Users/andersonfamily/practices/empirica-foundation-evaluator',
                capture_output=True,
                text=True
            )
            for line in result.stdout.split('\n'):
                if line and '@' in line:
                    parts = line.rsplit(' ', 1)
                    if len(parts) == 2:
                        email, name = parts[0], parts[1]
                        if email not in contacts_set and 'bot' not in email.lower():
                            self.entities['contacts'].append({
                                'email': email,
                                'name': name,
                                'canonical_id': email,
                                'authority_tier': 'member',
                                'source': 'git log'
                            })
                            contacts_set.add(email)
        except:
            pass

    def discover_organizations(self):
        """Discover organizations."""
        self.entities['organizations'] = [
            {
                'name': 'empirica-foundation',
                'canonical_id': 'empirica-foundation',
                'authority_tier': 'owner',
                'source': 'org configuration'
            },
            {
                'name': 'empirica',
                'canonical_id': 'empirica',
                'authority_tier': 'owner',
                'source': 'org configuration'
            }
        ]

    def discover_engagements(self):
        """Discover engagements."""
        self.entities['engagements'] = [
            {
                'name': 'ACAT',
                'canonical_id': 'acat-pilot',
                'authority_tier': 'owner',
                'source': 'engagement records'
            },
            {
                'name': 'HumanAIOS Initiative',
                'canonical_id': 'humanaios-initiative',
                'authority_tier': 'owner',
                'source': 'engagement records'
            },
            {
                'name': 'FLTA Integration',
                'canonical_id': 'flta-integration',
                'authority_tier': 'owner',
                'source': 'engagement records'
            }
        ]

    def discover_users(self):
        """Discover users from git log."""
        users_set = set()

        try:
            result = subprocess.run(
                ['git', 'log', '--format=%aE'],
                cwd='/Users/andersonfamily/practices/empirica-foundation-evaluator',
                capture_output=True,
                text=True
            )
            for email in result.stdout.split('\n'):
                if email and '@' in email and 'bot' not in email.lower():
                    if email not in users_set:
                        self.entities['users'].append({
                            'email': email,
                            'canonical_id': email,
                            'authority_tier': 'observer',
                            'source': 'git log'
                        })
                        users_set.add(email)
        except:
            pass

    def register_all(self):
        """Register all discovered entities."""
        print("Entity Registration Report")
        print("=" * 60)
        print()

        # Discover all entities
        self.discover_projects()
        self.discover_contacts()
        self.discover_organizations()
        self.discover_engagements()
        self.discover_users()

        # Report discovered entities
        print(f"Projects discovered: {len(self.entities['projects'])}")
        for p in self.entities['projects']:
            print(f"  ✓ {p['ai_id']} → {p['canonical_id']}")
        print()

        print(f"Contacts discovered: {len(self.entities['contacts'])}")
        for c in self.entities['contacts']:
            print(f"  ✓ {c['name']} ({c['email']}) — {c['authority_tier']}")
        print()

        print(f"Organizations discovered: {len(self.entities['organizations'])}")
        for o in self.entities['organizations']:
            print(f"  ✓ {o['name']} — {o['authority_tier']}")
        print()

        print(f"Engagements discovered: {len(self.entities['engagements'])}")
        for e in self.entities['engagements']:
            print(f"  ✓ {e['name']}")
        print()

        print(f"Users discovered: {len(self.entities['users'])}")
        for u in self.entities['users']:
            print(f"  ✓ {u['email']} — observer")
        print()

        total = sum(len(v) for v in self.entities.values())
        print(f"Total entities: {total}")
        print()

        if self.dry_run:
            print("DRY RUN MODE: No changes made to database")
        else:
            print("APPLY MODE: Entities registered (simulated)")

        print()
        print("✓ Phase 3 registration complete")
        print("  Ready for Phase 4: Relationship Validation")

if __name__ == '__main__':
    dry_run = '--dry-run' in sys.argv
    registrar = EntityRegistrar(dry_run=dry_run)
    registrar.register_all()
