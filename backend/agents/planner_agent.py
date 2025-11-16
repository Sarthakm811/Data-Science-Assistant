"""
Planner Agent - LLM-based query understanding and planning
"""
import google.generativeai as genai
import json
import logging
from typing import Dict, List, Any, Optional
from ..a2a.protocol import create_task_request, A2AMessage
from ..a2a.redis_transport import RedisA2ATransport
from ..mcp.tool_registry import tool_registry

logger = logging.getLogger(__name__)

class PlannerAgent:
    """
    Planner Agent uses LLM to understand user queries and create execution plans
    """
    
    def __init__(self, agent_id: str = "planner.agent.v1", gemini_api_key: str = None):
        self.agent_id = agent_id
        self.transport = RedisA2ATransport()
        
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            self.model = genai.GenerativeModel('models/gemini-2.0-flash')
        else:
            self.model = None
    
    def create_plan(self, user_query: str, context: Optional[Dict] = None) -> Dict:
        """
        Create execution plan from user query
        Returns: {
            "plan_id": str,
            "steps": [{"step_id": str, "tool_id": str, "inputs": dict}]
        }
        """
        # Get available tools
        tools = tool_registry.list_tools()
        tools_summary = self._format_tools_for_prompt(tools)
        
        # Build prompt
        prompt = self._build_planning_prompt(user_query, tools_summary, context)
        
        # Call LLM
        if self.model:
            try:
                response = self.model.generate_content(prompt)
                plan = self._parse_plan_response(response.text)
                return plan
            except Exception as e:
                logger.error(f"Error generating plan: {e}")
                return self._create_fallback_plan(user_query)
        else:
            return self._create_fallback_plan(user_query)
    
    def _build_planning_prompt(
        self,
        user_query: str,
        tools_summary: str,
        context: Optional[Dict]
    ) -> str:
        """Build prompt for LLM planner"""
        context_str = json.dumps(context, indent=2) if context else "No context"
        
        return f"""You are a Planner Agent for a data science research assistant.

Your task is to create an execution plan to answer the user's query.

Available Tools:
{tools_summary}

User Query: {user_query}

Context: {context_str}

Create a JSON plan with the following structure:
{{
  "plan_id": "unique-id",
  "description": "brief description of the plan",
  "steps": [
    {{
      "step_id": "s1",
      "tool_id": "tool.id.here",
      "description": "what this step does",
      "inputs": {{
        "param1": "value1"
      }},
      "depends_on": []
    }}
  ]
}}

Rules:
1. Use only tools from the available tools list
2. Each step must have a unique step_id
3. Steps can depend on previous steps (use depends_on)
4. Provide realistic input values based on the query
5. Keep the plan simple and efficient

Return ONLY the JSON plan, no other text.
"""
    
    def _format_tools_for_prompt(self, tools: List[Dict]) -> str:
        """Format tools list for prompt"""
        lines = []
        for tool in tools:
            lines.append(f"- {tool['tool_id']}: {tool['description']}")
            inputs = tool.get('inputs', {})
            if inputs:
                lines.append(f"  Inputs: {', '.join(inputs.keys())}")
        return "\n".join(lines)
    
    def _parse_plan_response(self, response_text: str) -> Dict:
        """Parse LLM response to extract plan"""
        try:
            # Try to find JSON in response
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response_text[start:end]
                plan = json.loads(json_str)
                return plan
        except Exception as e:
            logger.error(f"Error parsing plan: {e}")
        
        return {"plan_id": "error", "steps": []}
    
    def _create_fallback_plan(self, user_query: str) -> Dict:
        """Create a simple fallback plan"""
        import uuid
        
        # Simple heuristic-based planning
        plan = {
            "plan_id": str(uuid.uuid4()),
            "description": "Fallback plan for: " + user_query,
            "steps": []
        }
        
        # If query mentions dataset, add download step
        if "dataset" in user_query.lower() or "data" in user_query.lower():
            plan["steps"].append({
                "step_id": "s1",
                "tool_id": "kaggle.dataset.download",
                "description": "Download dataset",
                "inputs": {"dataset_ref": "example/dataset"},
                "depends_on": []
            })
        
        # Add EDA step
        plan["steps"].append({
            "step_id": "s2",
            "tool_id": "analyzer.eda",
            "description": "Perform exploratory data analysis",
            "inputs": {"dataset_path": "/data/dataset.csv"},
            "depends_on": ["s1"] if plan["steps"] else []
        })
        
        return plan
    
    def execute_plan(self, plan: Dict, trace_id: str) -> List[str]:
        """
        Execute plan by sending TASK_REQUEST messages to executor
        Returns list of task IDs
        """
        task_ids = []
        
        for step in plan.get('steps', []):
            import uuid
            task_id = str(uuid.uuid4())
            
            # Create TASK_REQUEST message
            message = create_task_request(
                from_agent=self.agent_id,
                to_agent="executor.agent.v1",
                task_id=task_id,
                tool_id=step['tool_id'],
                inputs=step['inputs'],
                trace_id=trace_id
            )
            
            # Publish message
            self.transport.publish(message)
            task_ids.append(task_id)
            
            logger.info(f"Published task {task_id} for step {step['step_id']}")
        
        return task_ids
    
    def handle_message(self, message: A2AMessage):
        """Handle incoming A2A messages"""
        logger.info(f"Planner received {message.type} from {message.from_agent}")
        
        # Handle TASK_RESULT messages
        if message.type == "TASK_RESULT":
            payload = message.payload
            task_id = payload.get('task_id')
            status = payload.get('status')
            
            logger.info(f"Task {task_id} completed with status: {status}")
            
            # Could trigger next steps or evaluator here
    
    def start(self):
        """Start listening for messages"""
        logger.info(f"Starting Planner Agent: {self.agent_id}")
        self.transport.subscribe(self.agent_id, self.handle_message)
