import google.generativeai as genai
from typing import Dict, Any, Optional
import uuid
import logging

from app.utils.config import settings
from app.services.redis_service import RedisService
from app.tools.kaggle_tool import KaggleTool
from app.tools.execution_tool import ExecutionTool

logger = logging.getLogger(__name__)


class AgentService:
    def __init__(self, redis_service: RedisService):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel("models/gemini-2.0-flash")
        self.redis = redis_service
        self.kaggle_tool = KaggleTool()
        self.execution_tool = ExecutionTool()

    async def handle_query(
        self, session_id: str, query: str, dataset_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Main orchestration logic"""
        job_id = str(uuid.uuid4())

        try:
            # Get session context
            history = await self.redis.get_history(session_id, limit=5)
            session_data = await self.redis.get_session(session_id) or {}

            # Get dataset info if provided
            dataset_summary = ""
            if dataset_id:
                dataset_summary = await self.kaggle_tool.get_dataset_summary(dataset_id)
                session_data["current_dataset"] = dataset_id

            # Build prompt
            prompt = self._build_prompt(query, dataset_summary, history)

            # Call Gemini
            logger.info(f"Calling Gemini for job {job_id}")
            response = self.model.generate_content(prompt)

            # Parse response
            plan, code, explanation = self._parse_response(response.text)

            # Execute code if generated
            results = None
            artifacts = []
            if code:
                logger.info(f"Executing code for job {job_id}")
                exec_result = await self.execution_tool.execute(
                    code=code, dataset_id=dataset_id, job_id=job_id
                )
                results = exec_result.get("results")
                artifacts = exec_result.get("artifacts", [])

            # Update session
            await self.redis.append_to_history(
                session_id, {"query": query, "response": explanation, "job_id": job_id}
            )
            await self.redis.set_session(session_id, session_data)

            return {
                "job_id": job_id,
                "status": "completed",
                "plan": plan,
                "code": code,
                "results": results,
                "artifacts": artifacts,
                "explanation": explanation,
            }

        except Exception as e:
            logger.error(f"Error in job {job_id}: {str(e)}")
            return {"job_id": job_id, "status": "failed", "error": str(e)}

    def _build_prompt(self, query: str, dataset_summary: str, history: list) -> str:
        """Build prompt for Gemini"""
        context = "\n".join(
            [f"Q: {h.get('query')}\nA: {h.get('response')}" for h in history[-3:]]
        )

        return f"""You are an expert data scientist assistant. Given a dataset and user question, provide:

1. ANALYSIS PLAN: A brief plan (2-3 sentences)
2. PYTHON CODE: A complete Python code block that:
   - Loads data from DATA_PATH variable
   - Performs the analysis using pandas, numpy, sklearn, matplotlib, plotly
   - Saves figures to /outputs/ as PNG
   - Returns results as a dictionary saved to /outputs/results.json
   - NO external network calls or OS commands
3. EXPLANATION: Natural language summary of expected results

DATASET SUMMARY:
{dataset_summary if dataset_summary else "No dataset loaded yet"}

RECENT CONTEXT:
{context if context else "No previous context"}

USER QUESTION: {query}

Format your response as:
PLAN:
[your plan]

CODE:
```python
[your code]
```

EXPLANATION:
[your explanation]
"""

    def _parse_response(self, response_text: str) -> tuple:
        """Extract plan, code, and explanation from response"""
        plan = ""
        code = ""
        explanation = ""

        lines = response_text.split("\n")
        current_section = None
        code_block = False

        for line in lines:
            if line.startswith("PLAN:"):
                current_section = "plan"
                continue
            elif line.startswith("CODE:"):
                current_section = "code"
                continue
            elif line.startswith("EXPLANATION:"):
                current_section = "explanation"
                continue

            if current_section == "code":
                if "```python" in line:
                    code_block = True
                    continue
                elif "```" in line:
                    code_block = False
                    continue
                if code_block:
                    code += line + "\n"
            elif current_section == "plan":
                plan += line + "\n"
            elif current_section == "explanation":
                explanation += line + "\n"

        return plan.strip(), code.strip(), explanation.strip()
