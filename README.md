# NETIC

<div align="center">

[![Django](https://img.shields.io/badge/Django-4.x-092E20?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

**A networking platform built for the ETIC Algarve student community — connect, chat, and build your network.**

[Features](#-features) • [Architecture](#-architecture) • [Installation](#-installation) • [Usage](#-usage) • [Team](#-team)

</div>

---

## Overview

NETIC is a fullstack web platform designed to facilitate meaningful connections between students within the ETIC Algarve community. Users can build and manage their personal network, communicate in real time via integrated chat, and authenticate securely through Google OAuth.

Built as a group project during the Web Programming course at ETIC Algarve, NETIC demonstrates a production-style architecture using Django for backend logic, a dual-database strategy (PostgreSQL + MongoDB), real-time messaging, and full Docker containerization.

---

## Features

- **Student Networking** — Add and remove students from your personal network
- **Real-Time Chat** — Integrated messaging with persistent chat history
- **Google OAuth** — Secure login via Google account, no password required
- **Course-Based Discovery** — Browse and filter students by course
- **Profile Pages** — View and manage your own student profile
- **Containerized Deployment** — Full Docker setup for consistent local and production environments

---

## Architecture

NETIC uses a dual-database architecture to separate concerns by data type:

- **PostgreSQL** handles structured relational data — users, networks, and course relationships — where consistency and foreign key integrity matter
- **MongoDB** handles chat and message history, where a flexible document schema is better suited to variable message structures and high write volume
- **Django** manages routing, authentication, and business logic across both data layers
- **Docker** containerizes the full stack for reproducible environments

```
Client (Browser)
      |
  Django Backend
  /           \
PostgreSQL   MongoDB
(Users,      (Messages,
 Networks,    Chat History)
 Courses)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django, Python, Poetry |
| **Frontend** | HTML, SASS, JavaScript |
| **Databases** | PostgreSQL (relational), MongoDB (chat/messages) |
| **Auth** | Google OAuth |
| **DevOps** | Docker, Docker Compose |

---

## Installation

### Prerequisites

- Docker and Docker Compose
- A Google OAuth client ID and secret

> **Note:** Poetry is only required if you intend to run the backend outside of Docker for local development.

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/maurograndaoramos/NETIC.git
cd NETIC
```

2. **Configure environment variables**

Create a `.env` file in the project root:
```env
# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# PostgreSQL
POSTGRES_DB=netic
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-db-password

# MongoDB
MONGO_URI=mongodb://localhost:27017/netic
```

3. **Run the setup**
```bash
make setup
```

This builds and starts all Docker containers. The application will be available at `http://localhost:8000`.

---

## Usage

1. **Login** — Sign in with your Google account
2. **Discover Students** — Browse by course to find other ETIC students
3. **Build Your Network** — Add students to your personal network
4. **Chat** — Open a conversation with anyone in your network
5. **Manage Your Profile** — View and update your student profile

---

## Screenshots

| Login | Home | Network |
|---|---|---|
| ![Login](/screenShots/login.png) | ![Home](/screenShots/home.png) | ![Network](/screenShots/NetworkPage.png) |

| Student Cards | Chat |
|---|---|
| ![Students](/screenShots/personCard.png) | ![Chat](/screenShots/openChat.png) |

> Additional screenshots (course selection, profile page, empty chat state) are available in the [`screenShots/`](./screenShots) folder.

---

## Team

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/maurograndaoramos">
        <img src="https://github.com/maurograndaoramos.png" width="100px;" alt="Mauro Ramos"/>
        <br />
        <sub><b>Mauro Ramos</b></sub>
      </a>
      <br />
      <sub>Project Lead / Backend Developer</sub>
    </td>
    <td align="center">
      <a href="https://github.com/JoaoCardosoDev">
        <img src="https://github.com/JoaoCardosoDev.png" width="100px;" alt="Joao Cardoso"/>
        <br />
        <sub><b>Joao Cardoso</b></sub>
      </a>
      <br />
      <sub>Frontend Developer</sub>
    </td>
    <td align="center">
      <a href="https://github.com/G00li">
        <img src="https://github.com/G00li.png" width="100px;" alt="Leandro Oliveira"/>
        <br />
        <sub><b>Leandro Oliveira</b></sub>
      </a>
      <br />
      <sub>Frontend Developer</sub>
    </td>
    <td align="center">
      <a href="https://github.com/mccartheney">
        <img src="https://github.com/mccartheney.png" width="100px;" alt="Mccartheney Mendes"/>
        <br />
        <sub><b>Mccartheney Mendes</b></sub>
      </a>
      <br />
      <sub>Backend Developer</sub>
    </td>
    <td align="center">
      <a href="https://github.com/r1ckyjr">
        <img src="https://github.com/r1ckyjr.png" width="100px;" alt="Ricardo Almeida"/>
        <br />
        <sub><b>Ricardo Almeida</b></sub>
      </a>
      <br />
      <sub>Backend Developer</sub>
    </td>
  </tr>
</table>

### Project Details

- **Course**: Programacao Web
- **Institution**: ETIC Algarve
- **Status**: Complete

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built by students, for students @ ETIC Algarve**

[Report Bug](https://github.com/maurograndaoramos/NETIC/issues) • [Request Feature](https://github.com/maurograndaoramos/NETIC/issues)

</div>

