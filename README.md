# TBOO - AI-based Asian Fortune Telling 🍀

TBOO.AI is a consumer-centric decentralized application (DApp) that combines traditional Asian fortune-telling with AI technology to facilitate the transition from Web2 to Web3.

## What is Saju (Four Pillars of Destiny)?

Saju is a destiny interpretation system based on Oriental philosophy, composed of four pillars representing the year, month, day, and time of birth. Each pillar consists of a combination of Heavenly Stems (天干) and Earthly Branches (地支), which are used to analyze an individual's innate personality and flow of destiny.

## TBOO API Usage Guide

### API Endpoint

```bash
GET http://localhost:8000/api/saju/
```

### Request Headers
```
Content-Type: application/json
X-API-KEY: your_api_key
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| birthdate | string | Required | Date of birth (YYYY-MM-DD) |
| birthtime | string | Required | Time of birth (HH:mm) |
| gender | string | Required | Gender (male/female) |

### Request Example

```bash
curl -X GET "http://localhost:8000/api/saju/?birthdate=1990-01-01&birthtime=12:00&gender=male" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_api_key" \
  -d '{
    "status": "success",
    "data": {
      "character": { ... },
      "saju": { ... },
      "il_ju": { ... },
      "oheang_rate": { ... },
      "luck_score": { ... },
      "saju_score": { ... },
      "dae_won_su": 9
    }
  }'
```

### Response Format

```json
{
  "status": "success",
  "data": {
    "character": { ... },
    "saju": { ... },
    "il_ju": { ... },
    "oheang_rate": {
        "ground": 33.2,
        "fire": 15.9,
        "water": 6.8,
        "wood": 32.7,
        "gold": 11.4
    },
    "luck_score": {
        "love": 44,
        "wealth": 62,
        "study": 72,
        "health": 13
    },
    "saju_score": {
        "sang-gwan": 8.5,
        "ski-sin": 5.5,
        "jeong-jae": 16.0,
        "pyeon-jae": 3.5,
        "jeong-gwan": 11.2,
        "pyeon-gwan": 22.3,
        "jeong-in": 13.1,
        "pyeon-in": 14.0,
        "geop-jae": 0.0,
        "bi-gyeon": 6.0
    },
    "dae_won_su": 9
  }
}
```

- `character`
    - Contains character information, representing the Day Pillar (日柱) information from the Saju.
- `saju`
    - Contains information about personality traits based on your character and dominant elements.
- `il_ju`
    - Contains interpretation of your Day Pillar.
- `oheang_rate`
    - Contains the ratio of the Five Elements in your entire Saju, consisting of ground, fire, water, wood, and gold.
- `luck_score`
    - Contains fortune scores in four categories: love, wealth, study, and health.
- `saju_score`
    - Contains Saju scores in ten categories: Sang-gwan, Sik-sin, Jeong-jae, Pyeon-jae, Jeong-gwan, Pyeon-gwan, Jeong-in, Pyeon-in, Geop-jae, and Bi-gyeon.
- `dae_won_su`
    - Contains your Major Number (大元數), which is determined by the combination of Heavenly Stems and Earthly Branches in your Saju.

## Running Locally

```bash
pip install -r requirements.txt
python manage.py runserver
```

Once the server is running, you can test the API at `http://localhost:8000`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
