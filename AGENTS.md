# Agents Guide

## Purpose

This repository contains a static website plus a small Python API for managing club members.

## Working Rules

- Keep the admin panel aligned with `server.py`, `members.json`, and `members-data.js`.
- Do not reintroduce hardcoded Render URLs or remote-only assumptions into the admin page.
- Treat `none` as the no-department value in member data and UI.
- Preserve the combined leadership display rules on the members page.
- Use `python server.py` for local testing of admin/data changes.

## Important Files

- `admin.html`: Admin UI and member editing logic.
- `members.html`: Current members page with grouped departments.
- `members-data.js`: Static data used when the site is opened directly.
- `server.py`: Local API server and JSON writer.

## Notes

- If you change member fields, update the admin form, public page rendering, and data export together.
- Prefer small, focused edits over rewrites.