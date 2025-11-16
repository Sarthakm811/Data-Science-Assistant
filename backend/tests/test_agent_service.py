import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.services.agent_service import AgentService
from app.services.redis_service import RedisService

@pytest.fixture
def mock_redis():
    redis = Mock(spec=RedisService)
    redis.get_history = AsyncMock(return_value=[])
    redis.get_session = AsyncMock(return_value={})
    redis.append_to_history = AsyncMock()
    redis.set_session = AsyncMock()
    return redis

@pytest.mark.asyncio
async def test_handle_query_basic(mock_redis):
    """Test basic query handling"""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_response = Mock()
        mock_response.text = """
PLAN:
Test plan

CODE:
```python
print("test")
```

EXPLANATION:
Test explanation
"""
        mock_model.return_value.generate_content.return_value = mock_response
        
        agent = AgentService(mock_redis)
        result = await agent.handle_query(
            session_id="test-session",
            query="Test query"
        )
        
        assert result['status'] == 'completed'
        assert 'job_id' in result
        assert result['plan'] == 'Test plan'
        assert 'print("test")' in result['code']

@pytest.mark.asyncio
async def test_parse_response():
    """Test response parsing"""
    agent = AgentService(Mock(spec=RedisService))
    
    response_text = """
PLAN:
This is a plan

CODE:
```python
x = 1
y = 2
```

EXPLANATION:
This is an explanation
"""
    
    plan, code, explanation = agent._parse_response(response_text)
    
    assert plan == "This is a plan"
    assert "x = 1" in code
    assert "y = 2" in code
    assert explanation == "This is an explanation"
