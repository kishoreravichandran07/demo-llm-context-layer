# Demo: LLM Context Layer (Synthetic Data)

> **Label:** NEW portfolio work, built November 2026 to demonstrate the design ideas from
> my case study `case-study-multi-llm-context-layer`. It uses only synthetic, invented
> data. It is **not** the original company system and shares no code, data, or design
> assets with it.

## What it demonstrates

Different people export context from different LLM tools in different formats. This demo:

1. **Ingests** two different synthetic export formats (a JSON chat export and a Markdown
   notes export), standing in for "different LLMs".
2. **Extracts** work-relevant context using configurable keyword rules.
3. **Validates** extracted items against a synthetic "internal database" of known
   projects - unverifiable items are quarantined, not shared.
4. **Shares** validated context only with designated coworkers, via a simple access list.

Everything runs offline with the Python standard library only.

## Run it

```bash
python3 context_layer.py
```

Expected output: a per-recipient digest of validated, access-permitted context items,
plus a quarantine report of items that failed validation.

## Layout

- `llm_export_chat.json`, `notes_export.md`, `project_db.json` - synthetic exports and
  the synthetic project database. All invented.
- `context_layer.py` - the whole pipeline, commented.
- `config.py` - keyword rules and the access list, as plain Python to keep the demo
  dependency-free.

## What this is intentionally not

- Not connected to any real LLM API or company system.
- Not a claim about scale; it demonstrates context selection, validation, and access
  control - the parts my case study identifies as the real work.
