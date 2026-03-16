# Quantum Crafters - IT Club DPS Ranchi

Welcome to the official repository for **Quantum Crafters**, the IT Club of Delhi Public School (DPS) Ranchi!

Quantum Crafters is a student-led club dedicated to innovation, tech learning, and hands-on experience in fields like AI, coding, and IoT to empower students to become future-ready innovators, problem solvers, and leaders in the field of technology.

## 🚀 Features

- **Modern & Responsive UI**: Built with Tailwind CSS and designed with sleek, dynamic styles.
- **Dynamic Member Management**: Includes a custom-built Admin Panel to easily add, update, and manage current and past members.
- **REST API Backend**: A lightweight Python HTTP server (`server.py`) powers the API endpoints to fetch and update member data dynamically.
- **Interactive Pages**: Explore our home, about, events, contact, and dedicated member directories.

## 🛠️ Tech Stack

- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript, jQuery, Lucide Icons
- **Backend**: Python 3 (Standard `http.server` module)
- **Data Storage**: Local JSON storage (`members.json`) bundled into static JS generation for high performance.

## 📂 Project Structure

- `index.html`: The main landing page.
- `about.html`, `contact.html`, `events.html`: Pages providing details about the club's aims, activities, and contact info.
- `members.html`, `past-members.html`, `founding-committee.html`: Member directories showing cards of IT Club members.
- `admin.html`: Secure admin panel interface for updating the club's membership roster visually.
- `server.py`: The backend Python script handling API requests and file uploads.
- `members.json` & `members-data.js`: The JSON database and its exported JavaScript equivalent to feed the dynamic client pages.
- `public/`: Directory containing uploaded images and static assets (e.g., logos).
- `*.py` Helpers: Extra automation and maintenance scripts used during development (e.g., `update_admin_dynamic.py`, `update_footers.py`).

## 🏃‍♂️ How to Run Locally

To get the website running fully on your local machine with the API server active:

1. Ensure you have **Python 3** installed on your system.
2. Open a terminal and navigate to the project directory:
   ```bash
   cd path/to/Quantum-Crafters/website
   ```
3. Start the backend server:
   ```bash
   python server.py
   ```
4. The server will launch on port `8000`. Open your web browser and visit:
   ```text
   http://localhost:8000/index.html
   ```

*(Note: While you can open the HTML files directly in a browser, running the Python server is necessary for the API endpoints—like fetching and updating members via the Admin Panel—to function properly.)*

## 📱 Contact

- **Email**: [quantumcrafters6@gmail.com](mailto:quantumcrafters6@gmail.com)
- **Instagram**: [@quantum.crafters](https://www.instagram.com/quantum.crafters)
