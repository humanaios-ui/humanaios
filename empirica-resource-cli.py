#!/usr/bin/env python3
"""
empirica-resource-cli: CLI wrapper for resource-based PREFLIGHT/POSTFLIGHT
Adds resource accounting flags to empirica commands (backward compatible).
"""

import argparse
import json
import subprocess
import sys


def parse_hours_range(hours_str: str) -> dict:
    """Parse '1.5-2.0' or '1.75' into estimate."""
    if '-' in hours_str:
        parts = hours_str.split('-')
        return {'min': float(parts[0]), 'max': float(parts[1])}
    return {'estimate': float(hours_str)}


def parse_tokens(tokens_str: str) -> int:
    """Parse '40k' or '50000' into integer."""
    if tokens_str.endswith('k'):
        return int(float(tokens_str[:-1]) * 1000)
    return int(tokens_str)


def parse_vectors(vectors_str: str) -> dict:
    """Parse 'know:0.7 uncertainty:0.3' into dict."""
    vectors = {}
    for pair in vectors_str.split():
        key, val = pair.split(':')
        vectors[key] = float(val)
    return vectors


def preflight(args):
    """Handle preflight-submit with resource flags."""
    payload = {'vectors': parse_vectors(args.vectors) if args.vectors else {}}
    
    resource_anchor = {}
    if args.estimate_hours:
        resource_anchor['estimated_hours'] = parse_hours_range(args.estimate_hours)
    if args.estimate_tokens:
        resource_anchor['estimated_tokens'] = parse_tokens(args.estimate_tokens)
    if args.work_type:
        resource_anchor['work_type'] = args.work_type
    
    if resource_anchor:
        payload['resource_scope_this_transaction'] = resource_anchor
    
    subprocess.run(['empirica', 'preflight-submit', '-'], input=json.dumps(payload), text=True)


def postflight(args):
    """Handle postflight-submit with resource flags."""
    payload = {'vectors': parse_vectors(args.vectors) if args.vectors else {}}
    
    if args.human_active_hours:
        payload['resource_accounting'] = {
            'human_labor_this_session': float(args.human_active_hours)
        }
    
    subprocess.run(['empirica', 'postflight-submit', '-'], input=json.dumps(payload), text=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='empirica CLI with resource flags')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # PREFLIGHT
    preflight_parser = subparsers.add_parser('preflight-submit')
    preflight_parser.add_argument('--estimate-hours', help='Estimated hours: "1.5-2.0"')
    preflight_parser.add_argument('--estimate-tokens', help='Estimated tokens: "40k"')
    preflight_parser.add_argument('--work-type', help='Work type: research, implementation, etc.')
    preflight_parser.add_argument('--vectors', help='Vector estimates: "know:0.7 uncertainty:0.3"')
    preflight_parser.set_defaults(func=preflight)
    
    # POSTFLIGHT
    postflight_parser = subparsers.add_parser('postflight-submit')
    postflight_parser.add_argument('--human-active-hours', help='Actual hours spent: "1.75"')
    postflight_parser.add_argument('--vectors', help='Final estimates: "know:0.85 uncertainty:0.15"')
    postflight_parser.set_defaults(func=postflight)
    
    args = parser.parse_args()
    args.func(args)
