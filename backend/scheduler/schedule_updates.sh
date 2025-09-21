#!/bin/bash
# Cron job script to update vector database every hour
# Add this to your crontab with: crontab -e
# Then add: 0 * * * * /path/to/rag-langchain-langgraph/backend/scheduler/schedule_updates.sh

# Set the working directory
cd "$(dirname "$0")/.."

# Set environment variables (adjust paths as needed)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Log file location
LOG_FILE="$(pwd)/scheduler/update_logs.log"

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Run the update script
echo "$(date): Starting vector database update..." >> "$LOG_FILE"
python3 scheduler/update_vector_db.py >> "$LOG_FILE" 2>&1

# Check if the update was successful
if [ $? -eq 0 ]; then
    echo "$(date): Vector database update completed successfully" >> "$LOG_FILE"
else
    echo "$(date): Vector database update failed" >> "$LOG_FILE"
fi

echo "$(date): Update cycle finished" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
