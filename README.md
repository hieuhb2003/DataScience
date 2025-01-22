# Data Science Project

This project requires Python 3.8+ and Docker to run.

## Setup Instructions

1. **Download Data**

```bash
python download_data.py
```

2. **Set up Groq API Key**
   - Create an account at [Groq Cloud](https://console.groq.com/)
   - Get your API key from the dashboard
   - Create a `.env` file and add:

```bash
GROQ_API_KEY=your_api_key_here
```

3. **Run with Docker**

```bash
docker-compose up -d
```

## Project Structure

- `data/`: Contains datasets
- `src/`: Source code
- `docker/`: Docker configuration

## Troubleshooting

- If you get API errors, verify your Groq API key
- If data download fails, check your internet connection
- For Docker issues, ensure Docker is running
