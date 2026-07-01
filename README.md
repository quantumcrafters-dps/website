# Quantum Crafters

Official website for Quantum Crafters, the IT Club of Delhi Public School, Ranchi.

## Overview

The site is a static front end with a lightweight Python API for member data. The admin panel edits the club roster, and the public pages render the current and past members from the generated data file.

## Tech Stack

- HTML5
- Tailwind CSS
- Vanilla JavaScript
- jQuery
- Lucide Icons
- Python 3 `http.server`

## Key Files

- `index.html`: Homepage.
- `about.html`, `contact.html`, `events.html`: Informational pages.
- `members.html`, `past-members.html`, `founding-committee.html`: Member listings.
- `admin.html`: Admin panel for editing club members.
- `server.py`: Local API server for `/api/members` and `/api/upload`.
- `members.json`: Source data store.
- `members-data.js`: Static data exported for file-based viewing.
- `public/`: Static assets and uploaded images.

## Run Locally

1. Install Python 3.
2. Open a terminal in the `website` folder.
3. Run `python server.py`.
4. Open `http://localhost:8000/index.html`.

## Contact

- Email: [quantumcrafters6@gmail.com](mailto:quantumcrafters6@gmail.com)
- Instagram: [@quantum.crafters](https://www.instagram.com/quantum.crafters)
