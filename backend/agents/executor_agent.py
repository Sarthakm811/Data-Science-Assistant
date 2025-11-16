"""
Executor Agent - Executes tool calls in sandboxed environment
"""
import logging
import time
from typing import Dict, Any, Optional
from ..a2a.protocol import (
    A2AMessage, MessageType,
    create_task_status, create_task_result
)
from ..a2a.redis_transport import RedisA2ATransport
from ..mcp.tool_registry import tool_registry

logger = logging.getLogger(__name__)

class ExecutorAgent:
    """
    Executor Agent receives TASK_REQUEST messages and executes tools
    """
    
    def __init__(self, agent_id: str = "executor.agent.v1"):
        self.agent_id = agent_id
        self.transport = RedisA2ATransport()
        self.running_tasks = {}
    
    def handle_message(self, message: A2AMessage):
        """Handle incoming A2A messages"""
        logger.info(f"Executor received {message.type} from {message.from_agent}")
        
        if message.type == MessageType.TASK_REQUEST:
            self._handle_task_request(message)
        elif message.type == MessageType.APPROVAL_RESPONSE:
            self._handle_approval_response(message)
    
    def _handle_task_request(self, message: A2AMessage):
        """Handle TASK_REQUEST message"""
        payload = message.payload
        task_id = payload.get('task_id')
        tool_id = payload.get('tool_id')
        inputs = payload.get('inputs', {})
        
        logger.info(f"Executing task {task_id} with tool {tool_id}")
        
        # Get tool manifest
        tool = tool_registry.get_tool(tool_id)
        if not tool:
            self._send_error(message, f"Tool not found: {tool_id}")
            return
        
        # Validate inputs
        valid, error = tool_registry.validate_inputs(tool_id, inputs)
        if not valid:
            self._send_error(message, f"Invalid inputs: {error}")
            return
        
        # Check if approval required
        if tool.get('approval_required', False):
            self._request_approval(message, tool)
            return
        
        # Execute tool
        self._execute_tool(message, tool, inputs)
    
    def _execute_tool(self, message: A2AMessage, tool: Dict, inputs: Dict):
        """Execute the tool"""
        task_id = message.payload.get('task_id')
        tool_id = tool['tool_id']
        
        # Send status: running
        status_msg = create_task_status(
            from_agent=self.agent_id,
            to_agent=message.from_agent,
            task_id=task_id,
            status="running",
            progress=0.0,
            message=f"Starting {tool_id}",
            trace_id=message.trace_id
        )
        self.transport.publish(status_msg)
        
        try:
            # Execute based on tool type
            if tool_id == "kaggle.dataset.download":
                outputs = self._execute_kaggle_download(inputs)
            elif tool_id == "analyzer.eda":
                outputs = self._execute_eda(inputs)
            elif tool_id == "executor.run_code":
                outputs = self._execute_code(inputs)
            else:
                outputs = {"message": f"Tool {tool_id} not implemented yet"}
            
            # Send progress updates
            for progress in [0.3, 0.6, 0.9]:
                status_msg = create_task_status(
                    from_agent=self.agent_id,
                    to_agent=message.from_agent,
                    task_id=task_id,
                    status="running",
                    progress=progress,
                    trace_id=message.trace_id
                )
                self.transport.publish(status_msg)
                time.sleep(0.5)  # Simulate work
            
            # Send result
            result_msg = create_task_result(
                from_agent=self.agent_id,
                to_agent=message.from_agent,
                task_id=task_id,
                status="completed",
                outputs=outputs,
                trace_id=message.trace_id
            )
            self.transport.publish(result_msg)
            
            logger.info(f"Task {task_id} completed successfully")
        
        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")
            result_msg = create_task_result(
                from_agent=self.agent_id,
                to_agent=message.from_agent,
                task_id=task_id,
                status="failed",
                error=str(e),
                trace_id=message.trace_id
            )
            self.transport.publish(result_msg)
    
    def _execute_kaggle_download(self, inputs: Dict) -> Dict:
        """Execute Kaggle dataset download"""
        dataset_ref = inputs.get('dataset_ref')
        
        # Mock implementation
        logger.info(f"Downloading dataset: {dataset_ref}")
        
        return {
            "dataset_path": f"/data/{dataset_ref}",
            "files": ["data.csv"],
            "size_mb": 10.5
        }
    
    def _execute_eda(self, inputs: Dict) -> Dict:
        """Execute EDA analysis"""
        dataset_path = inputs.get('dataset_path')
        
        # Mock implementation
        logger.info(f"Running EDA on: {dataset_path}")
        
        return {
            "summary_stats": {"mean": 42, "std": 10},
            "missing_data": {"col1": 5},
            "correlations": {"col1_col2": 0.85},
            "visualizations": ["/outputs/corr_heatmap.png"],
            "report_path": "/outputs/eda_report.md"
        }
    
    def _execute_code(self, inputs: Dict) -> Dict:
        """Execute code in sandbox"""
        script_path = inputs.get('script_path')
        
        # Mock implementation
        logger.info(f"Executing script: {script_path}")
        
        return {
            "stdout": "Execution completed",
            "stderr": "",
            "artifacts": ["/outputs/result.csv"],
            "exit_code": 0
        }
    
    def _request_approval(self, message: A2AMessage, tool: Dict):
        """Request approval for dangerous operation"""
        task_id = message.payload.get('task_id')
        
        # Store task for later
        self.running_tasks[task_id] = {
            "message": message,
            "tool": tool,
            "status": "awaiting_approval"
        }
        
        # Send approval request
        from ..a2a.protocol import ApprovalRequest
        approval_payload = ApprovalRequest(
            task_id=task_id,
            reason=f"Tool {tool['tool_id']} requires approval",
            estimated_risk="medium"
        ).model_dump()
        
        approval_msg = A2AMessage.create(
            msg_type=MessageType.APPROVAL_REQUEST,
            from_agent=self.agent_id,
            to_agent="director",  # Send to orchestrator/director
            payload=approval_payload,
            trace_id=message.trace_id
        )
        self.transport.publish(approval_msg)
        
        logger.info(f"Approval requested for task {task_id}")
    
    def _handle_approval_response(self, message: A2AMessage):
        """Handle approval response"""
        payload = message.payload
        task_id = payload.get('task_id')
        decision = payload.get('decision')
        
        if task_id not in self.running_tasks:
            logger.warning(f"Unknown task in approval response: {task_id}")
            return
        
        task_info = self.running_tasks[task_id]
        
        if decision:
            # Approved - execute
            logger.info(f"Task {task_id} approved, executing")
            self._execute_tool(
                task_info['message'],
                task_info['tool'],
                task_info['message'].payload.get('inputs', {})
            )
        else:
            # Rejected
            logger.info(f"Task {task_id} rejected")
            result_msg = create_task_result(
                from_agent=self.agent_id,
                to_agent=task_info['message'].from_agent,
                task_id=task_id,
                status="rejected",
                error="Approval denied",
                trace_id=task_info['message'].trace_id
            )
            self.transport.publish(result_msg)
        
        # Clean up
        del self.running_tasks[task_id]
    
    def _send_error(self, message: A2AMessage, error: str):
        """Send error response"""
        task_id = message.payload.get('task_id')
        result_msg = create_task_result(
            from_agent=self.agent_id,
            to_agent=message.from_agent,
            task_id=task_id,
            status="failed",
            error=error,
            trace_id=message.trace_id
        )
        self.transport.publish(result_msg)
    
    def start(self):
        """Start listening for messages"""
        logger.info(f"Starting Executor Agent: {self.agent_id}")
        self.transport.subscribe(self.agent_id, self.handle_message)
