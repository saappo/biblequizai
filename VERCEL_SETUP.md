# Vercel Deployment Setup Guide (Simple - No External Subscriptions!)

## Environment Variables

Set these in your Vercel project dashboard under Settings > Environment Variables:

### Required Variables:
```
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_random_secret_key_here
```

## Simple Storage Options (Only Vercel Pro Features!)

### Option 1: Vercel Blob Storage (Included in Pro Plan) - RECOMMENDED
1. Go to your Vercel project dashboard
2. Click **"Storage"** tab
3. Look for **"Blob"** (file storage)
4. Click **"Add Integration"** and follow the setup wizard
5. Store your SQLite database file in Blob storage

### Option 2: Vercel Edge Config (Included in Pro Plan)
1. Go to **"Storage"** tab
2. Add **"Edge Config"** integration
3. Store configuration and simple data globally
4. Perfect for storing quiz questions

### Option 3: Simple File-Based Storage
- Use the built-in `simple_storage.py` I created
- Works with SQLite files
- No additional services needed

## Marketplace Options (May Require Additional Subscriptions)

### Vercel KV (Marketplace)
- Available in Vercel Marketplace
- Powered by Upstash
- May require additional subscription

### Vercel Postgres (Marketplace)
- Available in Vercel Marketplace
- Powered by Neon
- May require additional subscription

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
4. Set up Vercel Blob (recommended)
5. Test your deployment

## Troubleshooting

- Check Vercel function logs for errors
- Ensure all environment variables are set
- Test locally with the same environment variables

## Vercel Pro Benefits (No Extra Costs!)

As a Vercel Pro user, you have access to:
- **Vercel Blob** (file storage) ✅
- **Vercel Edge Config** (global config) ✅
- Custom domains ✅
- Advanced analytics ✅
- **No external subscriptions needed!** ✅

## Why This Approach is Better:

1. **No additional costs** - Everything is included in your Vercel Pro plan
2. **Simpler setup** - No external database services to manage
3. **Better integration** - Native Vercel services work seamlessly
4. **Easier maintenance** - One platform for everything 