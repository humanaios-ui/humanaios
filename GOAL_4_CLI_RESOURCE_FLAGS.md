# Goal 4: Wire empirica CLI for Resource-Based Payloads

**Status:** Complete | T4.1 ✓ | T4.2 ✓ | T4.3 ✓

---

## T4.1: Add flags to `empirica preflight-submit`

**New flags:**
- `--estimate-hours "1.5-2.0"` or `"1.75"` — estimated labor for this transaction
- `--estimate-tokens "40k"` or `"50000"` — estimated AI tokens
- `--work-type research|implementation|review` — categorize work
- `--vectors "know:0.7 uncertainty:0.3"` — epistemic state (space-separated key:val pairs)

**Example:**
```bash
./empirica-resource-cli.py preflight-submit \
  --estimate-hours 1.5-2.0 \
  --estimate-tokens 40k \
  --work-type research \
  --vectors "know:0.7 uncertainty:0.3"
```

**Maps to schema:**
```json
{
  "resource_scope_this_transaction": {
    "estimated_hours": {"min": 1.5, "max": 2.0},
    "estimated_tokens": 40000,
    "work_type": "research"
  },
  "vectors": {"know": 0.7, "uncertainty": 0.3}
}
```

---

## T4.2: Add flags to `empirica postflight-submit`

**New flags:**
- `--human-active-hours "1.75"` — actual labor hours spent
- `--vectors "know:0.85 uncertainty:0.15"` — final epistemic state

**Example:**
```bash
./empirica-resource-cli.py postflight-submit \
  --human-active-hours 1.75 \
  --vectors "know:0.85 uncertainty:0.15"
```

**Maps to schema:**
```json
{
  "resource_accounting": {
    "human_labor_this_session": 1.75
  },
  "vectors": {"know": 0.85, "uncertainty": 0.15}
}
```

---

## T4.3: Backward Compatibility & Testing

**Backward compatible:** Old payloads (JSON via stdin) still work.

```bash
# Old way (still works):
empirica preflight-submit - << 'EOF'
{"vectors": {"know": 0.7, "uncertainty": 0.3}}
EOF

# New way (with flags):
./empirica-resource-cli.py preflight-submit --vectors "know:0.7 uncertainty:0.3"
```

**Why compatible:**
- CLI wrapper builds resource fields from flags
- Passes payload to native `empirica` command
- Empty resource fields are valid (optional schema fields)
- Existing POSTFLIGHT payloads parse without modification

**Test results:**
✓ CLI wrapper parses hours ranges correctly (1.5-2.0 → min/max)
✓ Token parsing handles both "40k" and "50000" formats
✓ Vector parsing: "know:0.7 uncertainty:0.3" → {know: 0.7, uncertainty: 0.3}
✓ Resource fields are optional (backward compatible)
✓ Wrapper delegates to native empirica CLI for actual submission

---

## Deployment

1. Place `empirica-resource-cli.py` in PATH or project root
2. Make executable: `chmod +x empirica-resource-cli.py`
3. Use wrapper: `./empirica-resource-cli.py preflight-submit --estimate-hours 1.5-2.0 ...`
4. Native empirica CLI unchanged (wrapper adds layer on top)

---

## Integration with Goals 3+5

**Goal 3 (Contracts):** Practices receive this wrapper + usage guide as part of contract briefing.

**Goal 5 (Sentinel):** Sentinel gates validate resource fields from these payloads:
- Check `estimated_hours` against practice labor budget
- Check `estimated_tokens` against token budget
- Check `human_labor_this_session` (actual) matches estimate ±30%

