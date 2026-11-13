# Demo: LLM Context Layer (Synthetic Data)

> **Label:** Illustrative demo built with an AI assistant (Instinct) in November 2026,
> specifically for this portfolio. It uses only synthetic, invented data. It demonstrates
> design ideas from the case study `case-study-multi-llm-context-layer`. It is **not**
> the original company system, shares no code, data, or design assets with it, and is
> not presented as evidence of the profile owner's own programming.

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

## Tests

```bash
python3 -m unittest test_context_layer.py -v
```

The tests cover the work-relevance filter, the validation/quarantine split, and the
access-control separation (who may receive whose context), plus a check that no
secret-looking strings appear in the shipped files.

## Limitations

- The access list is a local, illustrative filter. It is not production authentication,
  network isolation, or the firewall controls referenced in the case study.
- Validation only checks that a mentioned project name exists in the synthetic database.
  It does not check whether the statement about that project is accurate.
- All data is invented for demonstration.

## Layout

- `llm_export_chat.json`, `notes_export.md`, `project_db.json` - synthetic exports and
  the synthetic project database. All invented.
- `context_layer.py` - the whole pipeline, commented.
- `config.py` - keyword rules and the access list, as plain Python to keep the demo
  dependency-free.
- `test_context_layer.py` - unit tests for the pipeline.

## What this is intentionally not

- Not connected to any real LLM API or company system.
- Not a claim about scale; it demonstrates context selection, validation, and access
  control - the parts the case study focuses on.
