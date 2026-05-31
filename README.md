# Global Critical Resource Intelligence Network (GCRIN)

An autonomous, AI-powered intelligence platform designed to monitor, analyze, and visualize global risks affecting critical resources and supply chains in real-time.

## Overview

GCRIN acts as an automated intelligence agency for supply chain monitoring. It continuously ingests global news data from the GDELT DOC 2.0 API, processes the raw intelligence through an advanced Natural Language Processing (NLP) pipeline, and visualizes the calculated risks on a premium, interactive 3D dashboard.

The system requires zero routine human intervention after initial setup.

## Key Features

- **Autonomous Intelligence Gathering**: A FastAPI background scheduler polls global event databases (GDELT) every 30 minutes for keywords related to critical commodities (Semiconductors, Lithium, Copper, etc.).
- **AI-Powered Analysis**: 
  - Uses `spaCy` for Named Entity Recognition (NER) to extract involved organizations and regions.
  - Utilizes `VADER Sentiment Analysis` to calculate the severity of the disruption and assign a risk score.
- **Interactive 3D Dashboard**: A luxurious, typography-driven Next.js frontend featuring a WebGL interactive particle data-node network built with React Three Fiber.
- **Scrollytelling UI**: Buttery-smooth, scroll-driven UI transitions powered by `framer-motion` to elegantly reveal critical data.

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, APScheduler
- **AI/NLP**: spaCy, VADER Sentiment, langdetect, deep-translator
- **Database**: PostgreSQL
- **Frontend**: Next.js 15 (App Router), React, Tailwind CSS, Framer Motion
- **3D Rendering**: Three.js, React Three Fiber, React Three Drei

## Running Locally

1. **Prerequisites**: Ensure you have Python 3.12+, Node.js, and a local instance of PostgreSQL running.
2. **Setup**: Run `scripts\setup.bat` to automatically install all Python dependencies, download the NLP models, and install Node.js modules.
3. **Execute**: Run `scripts\run.bat` to concurrently start the FastAPI backend and the Next.js development server.

## License
MIT License
