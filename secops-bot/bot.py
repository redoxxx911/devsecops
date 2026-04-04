import os
import json
import logging
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import gitlab
from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load env vars
load_dotenv()

# Configure Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize API Clients
llm_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
es = Elasticsearch(os.getenv("ELASTICSEARCH_URL"))
gl = gitlab.Gitlab(os.getenv("GITLAB_URL"), private_token=os.getenv("GITLAB_TOKEN"))

# Global chat ID for background alerting
ALERT_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# The AI Model Fallback Chain
MODELS = [
    "qwen/qwen3.6-plus-preview:free",
    "qwen/qwen3.6-plus:free",
    "qwen/qwen3-235b-a22b:free",
    "qwen/qwen3-coder:free",
    "qwen/qwen-2.5-7b-instruct:free" # Ultimate stable fallback
]

async def ask_llm(prompt: str, system_msg: str = "You are a senior DevSecOps AI assistant.") -> str:
    """Wrapper for OpenRouter requests with a fallback mechanism"""
    last_error = ""
    for model in MODELS:
        try:
            logging.info(f"Attempting inference with model: {model}")
            response = await llm_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            last_error = str(e)
            logging.warning(f"Model {model} failed: {last_error}. Trying next...")
            continue
            
    return f"🚨 LLM Error: All fallback models failed. Last error: {last_error}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ALERT_CHAT_ID
    ALERT_CHAT_ID = update.effective_chat.id
    welcome_msg = f"🟢 SecOps AI Agent Online.\nBound to Chat ID: `{ALERT_CHAT_ID}`.\n\nCommands:\n/siem - Audit recent Elasticsearch logs\n/pipelines - Check GitLab CI/CD status"
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def check_siem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Querying Elasticsearch for recent anomalies...")
    try:
        query = {
            "query": {
                "bool": {
                    "should": [{"match": {"message": "401"}}, {"match": {"message": "error"}}],
                    "minimum_should_match": 1
                }
            },
            "size": 5,
            "sort": [{"@timestamp": {"order": "desc"}}]
        }
        res = es.search(index="filebeat-*", body=query)
        hits = res['hits']['hits']
        
        if not hits:
            await update.message.reply_text("✅ SIEM is quiet. No recent 401s or errors.")
            return

        logs = json.dumps([h['_source']['message'] for h in hits], indent=2)
        prompt = f"Analyze these recent SIEM logs. Summarize the threat level and what is happening:\n{logs}"
        
        analysis = await ask_llm(prompt)
        await update.message.reply_text(f"🚨 **SIEM Analysis:**\n\n{analysis}", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"❌ SIEM Query Failed: {str(e)}")

async def check_pipelines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚙️ Checking GitLab for failed pipelines...")
    try:
        gl.auth()
        projects = gl.projects.list(owned=True)
        if not projects:
            await update.message.reply_text("No projects found.")
            return
            
        project = projects[0] 
        pipelines = project.pipelines.list(status='failed', get_all=False, per_page=1)
        
        if not pipelines:
            await update.message.reply_text("✅ All recent pipelines succeeded.")
            return
            
        latest_failed = pipelines[0]
        jobs = latest_failed.jobs.list()
        failed_job_summary = next((j for j in jobs if j.status == 'failed'), None)
        
        if failed_job_summary:
            # THE FIX: Fetch the full job object by ID to unlock the .trace() method
            full_job = project.jobs.get(failed_job_summary.id)
            trace = full_job.trace().decode('utf-8')[-2000:]
            
            prompt = f"This GitLab CI/CD job failed. Analyze the trace and tell me the exact commands to fix it:\n\n{trace}"
            analysis = await ask_llm(prompt)
            await update.message.reply_text(f"❌ **Pipeline Failed (Job {full_job.id}):**\n\n{analysis}", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"❌ GitLab Query Failed: {str(e)}")

async def monitor_background(context: ContextTypes.DEFAULT_TYPE):
    """Runs every 60 seconds to actively hunt threats and push AI analysis"""
    if not ALERT_CHAT_ID: return
    
    try:
        # Search for spikes in the last 60 seconds
        query = {
            "query": {
                "bool": {
                    "must": [{"match": {"message": "401"}}],
                    "filter": [{"range": {"@timestamp": {"gte": "now-1m"}}}] 
                }
            },
            "size": 5, # Grab the logs to show the AI
            "sort": [{"@timestamp": {"order": "desc"}}]
        }
        res = es.search(index="filebeat-*", body=query)
        hits = res['hits']['hits']
        
        # If we see more than 3 failed attempts in 60 seconds, trigger the AI!
        if res['hits']['total']['value'] > 3:
            # 1. Grab the raw logs
            logs = json.dumps([h['_source']['message'] for h in hits], indent=2)
            
            # 2. Build the prompt
            prompt = f"URGENT: I am detecting a spike in 401 Unauthorized errors in my SIEM right now. Analyze these logs and give me a 3-bullet-point incident report:\n{logs}"
            
            # 3. Ask the LLM proactively
            analysis = await ask_llm(prompt)
            
            # 4. Push the AI response directly to Telegram
            msg = f"🚨 **PROACTIVE THREAT ALERT** 🚨\n\n{analysis}"
            await context.bot.send_message(chat_id=ALERT_CHAT_ID, text=msg, parse_mode='Markdown')
            
    except Exception as e:
        logging.error(f"Background monitor failed: {e}")
if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("siem", check_siem))
    app.add_handler(CommandHandler("pipelines", check_pipelines))
    
    job_queue = app.job_queue
    job_queue.run_repeating(monitor_background, interval=60, first=10)
    
    print("🤖 SecOps AI Agent is booting...")
    app.run_polling()
