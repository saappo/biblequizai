# Vercel Deployment Setup Guide

## Environment Variables

Set these in your Vercel project dashboard under Settings > Environment Variables:

### Required Variables:
```
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_random_secret_key_here
```

### Database Variables (if using Vercel Postgres):
```
DATABASE_URL=postgresql://username:password@host:port/database
```

## Database Setup

### Option 1: Vercel Postgres (Neon-powered) - RECOMMENDED
1. Go to your Vercel project dashboard
2. Click **"Storage"** tab
3. Look for **"Postgres"** in the marketplace integrations
4. Click **"Add Integration"** or **"Connect"**
5. Follow the setup wizard
6. Copy the connection string to your environment variables

### Option 2: Vercel Marketplace Postgres
1. Go to **"Marketplace"** in your Vercel dashboard
2. Search for **"Postgres"** or **"Neon"**
3. Click on the Postgres integration
4. Follow the setup wizard

### Option 3: External Database
- Use services like Supabase, Railway, or PlanetScale
- Add the connection string to your environment variables

## Vercel Cron Jobs (for scheduled tasks)

Since APScheduler doesn't work on serverless, use Vercel Cron Jobs:

1. Create a new file: `api/cron/generate-questions.py`
2. Add this to your `vercel.json`:
```json
{
  "crons": [
    {
      "path": "/api/cron/generate-questions",
      "schedule": "0 1 * * *"
    }
  ]
}
```

## Deployment Steps

1. Push your code to GitHub
2. Vercel will automatically deploy
3. Set up environment variables
4. Set up database
5. Test your deployment

## Troubleshooting

- Check Vercel function logs for errors
- Ensure all environment variables are set
- Verify database connection
- Test locally with the same environment variables

## Vercel Pro Benefits

As a Vercel Pro user, you have access to:
- Vercel Postgres (Neon-powered)
- Vercel KV (Redis-powered)
- Vercel Blob (file storage)
- Vercel Edge Config
- Custom domains
- Advanced analytics 