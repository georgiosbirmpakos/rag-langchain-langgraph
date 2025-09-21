# 🔄 Vector Database Scheduler

Automated system for updating the Pinecone vector database with fresh content from Gazzetta.gr every hour.

## 🚀 Features

- **Automated Updates**: Runs every hour to fetch fresh content
- **Smart Scraping**: Multiple fallback methods for reliable content extraction
- **Error Handling**: Comprehensive error handling and logging
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Logging**: Detailed logs for monitoring and debugging
- **Configurable**: Easy to customize update frequency and settings

## 📁 Files

```
scheduler/
├── update_vector_db.py      # Main updater script
├── schedule_updates.sh      # Linux/macOS cron job script
├── schedule_updates.bat     # Windows batch script
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🛠️ Setup

### **1. Install Dependencies**
```bash
cd backend/scheduler
pip install -r requirements.txt
```

### **2. Configure Environment**
Make sure your `.env` file is set up with:
```env
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_GREEK_DERBY_INDEX_NAME=your_index_name
```

### **3. Test the Updater**
```bash
python update_vector_db.py
```

## ⏰ Scheduling

### **Linux/macOS (Cron)**

1. **Make the script executable:**
   ```bash
   chmod +x schedule_updates.sh
   ```

2. **Add to crontab:**
   ```bash
   crontab -e
   ```

3. **Add this line (update the path):**
   ```bash
   0 * * * * /path/to/rag-langchain-langgraph/backend/scheduler/schedule_updates.sh
   ```

4. **Verify cron job:**
   ```bash
   crontab -l
   ```

### **Windows (Task Scheduler)**

1. **Open Task Scheduler:**
   - Press `Win + R`, type `taskschd.msc`, press Enter

2. **Create Basic Task:**
   - Right-click "Task Scheduler Library" → "Create Basic Task"
   - Name: "Vector DB Updater"
   - Trigger: "Daily" → "Recur every 1 days"
   - Action: "Start a program"
   - Program: `python`
   - Arguments: `C:\path\to\rag-langchain-langgraph\backend\scheduler\update_vector_db.py`
   - Start in: `C:\path\to\rag-langchain-langgraph\backend\scheduler`

3. **Advanced Settings:**
   - Check "Run whether user is logged on or not"
   - Check "Run with highest privileges"

### **Alternative: Python Scheduler**

Create a Python script that runs continuously:

```python
import schedule
import time
from update_vector_db import VectorDBUpdater

def run_update():
    updater = VectorDBUpdater()
    updater.run_update()

# Schedule the job
schedule.every().hour.do(run_update)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

## 📊 Monitoring

### **Log Files**
- **Main Log**: `vector_db_updater.log`
- **Scheduled Log**: `update_logs.log`

### **Log Levels**
- **INFO**: Normal operation messages
- **WARNING**: Non-critical issues
- **ERROR**: Critical errors that prevent updates

### **Example Log Output**
```
2024-01-15 10:00:01 - __main__ - INFO - 🚀 Initializing Vector Database Updater...
2024-01-15 10:00:02 - __main__ - INFO - ✅ Environment variables loaded
2024-01-15 10:00:03 - __main__ - INFO - 📚 Loading fresh content from Gazzetta.gr...
2024-01-15 10:00:05 - __main__ - INFO - Loading: https://www.gazzetta.gr/football/superleague/olympiakos
2024-01-15 10:00:07 - __main__ - INFO -   ✅ Found 3 valid documents from https://www.gazzetta.gr/football/superleague/olympiakos
2024-01-15 10:00:15 - __main__ - INFO - ✅ Successfully stored 45 chunks in vector database
2024-01-15 10:00:16 - __main__ - INFO - ✅ Update completed successfully in 15.23 seconds
```

## ⚙️ Configuration

### **Update Frequency**
Edit `config.py`:
```python
UPDATE_INTERVAL_HOURS = 1  # Update every hour
CLEANUP_INTERVAL_HOURS = 24  # Clean up content older than 24 hours
```

### **Content Settings**
```python
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
MIN_CONTENT_LENGTH = 50
```

### **URLs to Scrape**
```python
GAZZETTA_URLS = [
    "https://www.gazzetta.gr/football/superleague/olympiakos",
    "https://www.gazzetta.gr/football/superleague/panathinaikos",
    "https://www.gazzetta.gr/football/superleague",
    "https://www.gazzetta.gr"
]
```

## 🔧 Troubleshooting

### **Common Issues**

1. **Permission Denied (Linux/macOS)**
   ```bash
   chmod +x schedule_updates.sh
   ```

2. **Python Not Found (Windows)**
   - Use full path to python.exe in Task Scheduler
   - Or add Python to PATH environment variable

3. **Environment Variables Not Found**
   - Ensure `.env` file is in the project root
   - Check file permissions

4. **Pinecone Connection Failed**
   - Verify API key and index name
   - Check internet connection

5. **Gazzetta.gr Blocking Requests**
   - Update USER_AGENT in config.py
   - Increase REQUEST_DELAY

### **Debug Mode**
Run with verbose logging:
```bash
python update_vector_db.py --verbose
```

### **Manual Testing**
```bash
# Test content loading only
python -c "from update_vector_db import VectorDBUpdater; updater = VectorDBUpdater(); docs = updater.load_fresh_content(); print(f'Loaded {len(docs)} documents')"

# Test database connection
python -c "from update_vector_db import VectorDBUpdater; updater = VectorDBUpdater(); stats = updater.get_database_stats(); print(stats)"
```

## 📈 Performance

### **Expected Performance**
- **Update Duration**: 15-30 seconds per update
- **Content Loaded**: 50-100 chunks per update
- **Storage Growth**: ~1-5MB per update
- **CPU Usage**: Low (mostly I/O bound)

### **Optimization Tips**
- Adjust `REQUEST_DELAY` to balance speed vs. politeness
- Modify `CHUNK_SIZE` based on content characteristics
- Use `CLEANUP_INTERVAL_HOURS` to manage storage growth

## 🔒 Security

### **API Key Protection**
- Store keys in `.env` file (not in code)
- Use environment variables in production
- Rotate keys regularly

### **Rate Limiting**
- Respects Gazzetta.gr's servers with delays
- Implements retry logic for failed requests
- Logs all activities for monitoring

## 📝 Maintenance

### **Regular Tasks**
1. **Monitor Logs**: Check for errors or warnings
2. **Verify Updates**: Ensure content is being added
3. **Clean Logs**: Rotate log files periodically
4. **Update Dependencies**: Keep packages current

### **Log Rotation**
```bash
# Linux/macOS
logrotate -f /etc/logrotate.d/vector_db_updater

# Manual rotation
mv vector_db_updater.log vector_db_updater.log.old
touch vector_db_updater.log
```

## 🚀 Advanced Usage

### **Custom Update Frequency**
```python
# Update every 30 minutes
schedule.every(30).minutes.do(run_update)

# Update at specific times
schedule.every().day.at("09:00").do(run_update)
schedule.every().day.at("21:00").do(run_update)
```

### **Multiple Environments**
```bash
# Development
python update_vector_db.py --env dev

# Production
python update_vector_db.py --env prod
```

### **Health Checks**
```python
# Check if updater is working
curl http://localhost:8000/health

# Check database stats
python -c "from update_vector_db import VectorDBUpdater; print(VectorDBUpdater().get_database_stats())"
```

---

**🔄 Keep your vector database fresh with the latest Gazzetta.gr content! 🇬🇷⚽**
