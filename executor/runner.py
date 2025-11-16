"""
Executor worker that runs sandboxed Python code
Listens to Redis queue for execution jobs
"""
import os
import sys
import json
import subprocess
import tempfile
import redis
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
MAX_EXECUTION_TIME = int(os.getenv('MAX_EXECUTION_TIME', '45'))

def execute_code(code: str, job_id: str) -> Dict[str, Any]:
    """Execute code in isolated environment"""
    with tempfile.TemporaryDirectory() as workdir:
        outputs_dir = os.path.join(workdir, "outputs")
        os.makedirs(outputs_dir, exist_ok=True)
        
        script_path = os.path.join(workdir, "script.py")
        with open(script_path, 'w') as f:
            f.write(code)
        
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=MAX_EXECUTION_TIME,
                cwd=workdir
            )
            
            return {
                'job_id': job_id,
                'status': 'success' if result.returncode == 0 else 'error',
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'job_id': job_id,
                'status': 'timeout',
                'error': f'Execution exceeded {MAX_EXECUTION_TIME}s'
            }
        except Exception as e:
            return {
                'job_id': job_id,
                'status': 'error',
                'error': str(e)
            }

def main():
    """Main worker loop"""
    logger.info(f"Executor worker starting, connecting to {REDIS_URL}")
    r = redis.from_url(REDIS_URL, decode_responses=True)
    
    logger.info("Waiting for execution jobs...")
    while True:
        try:
            # Block and wait for jobs
            _, job_data = r.brpop('execution_queue', timeout=5)
            if not job_data:
                continue
            
            job = json.loads(job_data)
            job_id = job.get('job_id')
            code = job.get('code')
            
            logger.info(f"Executing job {job_id}")
            result = execute_code(code, job_id)
            
            # Store result
            r.setex(f"result:{job_id}", 3600, json.dumps(result))
            logger.info(f"Job {job_id} completed with status {result['status']}")
            
        except Exception as e:
            logger.error(f"Worker error: {str(e)}")

if __name__ == '__main__':
    main()
