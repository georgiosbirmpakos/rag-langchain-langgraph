#!/usr/bin/env python3
"""
Vector Database Monitor
Monitors the health and status of the vector database updater
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'standalone-service'))

class VectorDBMonitor:
    """Monitors the vector database updater health and status"""
    
    def __init__(self):
        self.log_file = "vector_db_updater.log"
        self.update_log_file = "update_logs.log"
    
    def check_log_files(self) -> Dict[str, Any]:
        """Check if log files exist and are recent"""
        status = {
            "main_log_exists": os.path.exists(self.log_file),
            "update_log_exists": os.path.exists(self.update_log_file),
            "main_log_size": 0,
            "update_log_size": 0,
            "last_update": None
        }
        
        if status["main_log_exists"]:
            status["main_log_size"] = os.path.getsize(self.log_file)
        
        if status["update_log_exists"]:
            status["update_log_size"] = os.path.getsize(self.update_log_file)
            
            # Try to find the last update time
            try:
                with open(self.update_log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in reversed(lines):
                        if "Update completed successfully" in line:
                            # Extract timestamp from log line
                            timestamp_str = line.split(' - ')[0]
                            status["last_update"] = timestamp_str
                            break
            except Exception as e:
                print(f"Error reading update log: {e}")
        
        return status
    
    def check_database_stats(self) -> Dict[str, Any]:
        """Check current database statistics"""
        try:
            from update_vector_db import VectorDBUpdater
            updater = VectorDBUpdater()
            stats = updater.get_database_stats()
            return {
                "success": True,
                "stats": stats
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def check_recent_errors(self, hours: int = 24) -> List[str]:
        """Check for recent errors in log files"""
        errors = []
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        for log_file in [self.log_file, self.update_log_file]:
            if not os.path.exists(log_file):
                continue
                
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if "ERROR" in line or "FAILED" in line:
                            # Extract timestamp and check if recent
                            try:
                                timestamp_str = line.split(' - ')[0]
                                log_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                                if log_time > cutoff_time:
                                    errors.append(line.strip())
                            except:
                                # If timestamp parsing fails, include the line anyway
                                errors.append(line.strip())
            except Exception as e:
                errors.append(f"Error reading {log_file}: {e}")
        
        return errors
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive health report"""
        print("🔍 Generating vector database health report...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "log_status": self.check_log_files(),
            "database_stats": self.check_database_stats(),
            "recent_errors": self.check_recent_errors(),
            "health_status": "unknown"
        }
        
        # Determine overall health status
        if not report["log_status"]["main_log_exists"]:
            report["health_status"] = "critical"
        elif not report["log_status"]["update_log_exists"]:
            report["health_status"] = "warning"
        elif not report["database_stats"]["success"]:
            report["health_status"] = "critical"
        elif len(report["recent_errors"]) > 0:
            report["health_status"] = "warning"
        else:
            report["health_status"] = "healthy"
        
        return report
    
    def print_report(self, report: Dict[str, Any]):
        """Print a formatted health report"""
        print("\n" + "="*60)
        print("🔍 VECTOR DATABASE HEALTH REPORT")
        print("="*60)
        print(f"📅 Generated: {report['timestamp']}")
        print(f"🏥 Status: {report['health_status'].upper()}")
        print()
        
        # Log file status
        print("📋 LOG FILES:")
        log_status = report["log_status"]
        print(f"  Main Log: {'✅' if log_status['main_log_exists'] else '❌'} ({log_status['main_log_size']} bytes)")
        print(f"  Update Log: {'✅' if log_status['update_log_exists'] else '❌'} ({log_status['update_log_size']} bytes)")
        if log_status['last_update']:
            print(f"  Last Update: {log_status['last_update']}")
        print()
        
        # Database stats
        print("🗄️  DATABASE STATS:")
        if report["database_stats"]["success"]:
            stats = report["database_stats"]["stats"]
            print(f"  Total Vectors: {stats.get('total_vectors', 'Unknown')}")
            print(f"  Dimension: {stats.get('dimension', 'Unknown')}")
            print(f"  Index Fullness: {stats.get('index_fullness', 'Unknown')}")
        else:
            print(f"  ❌ Error: {report['database_stats']['error']}")
        print()
        
        # Recent errors
        print("⚠️  RECENT ERRORS (24h):")
        if report["recent_errors"]:
            for error in report["recent_errors"][:5]:  # Show last 5 errors
                print(f"  {error}")
        else:
            print("  ✅ No recent errors found")
        print()
        
        # Recommendations
        print("💡 RECOMMENDATIONS:")
        if report["health_status"] == "critical":
            print("  🚨 Immediate action required!")
            print("  - Check environment variables")
            print("  - Verify Pinecone connection")
            print("  - Check log files for errors")
        elif report["health_status"] == "warning":
            print("  ⚠️  Monitor closely")
            print("  - Check recent errors")
            print("  - Verify update schedule")
        else:
            print("  ✅ System is healthy")
            print("  - Continue monitoring")
        print("="*60)

def main():
    """Main function to run the monitor"""
    monitor = VectorDBMonitor()
    
    # Generate and print report
    report = monitor.generate_report()
    monitor.print_report(report)
    
    # Save report to file
    report_file = f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Full report saved to: {report_file}")
    
    # Exit with appropriate code
    if report["health_status"] == "critical":
        sys.exit(2)
    elif report["health_status"] == "warning":
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
