"""
Redis Streams Transport for A2A Messages
"""

import redis
import logging
from typing import Callable
from .protocol import A2AMessage

logger = logging.getLogger(__name__)


class RedisA2ATransport:
    """Redis Streams-based A2A message transport"""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        self.running = False

    def publish(self, message: A2AMessage) -> bool:
        """Publish message to agent's stream"""
        try:
            stream_name = f"agents:{message.to_agent}"
            message_data = {"message": message.to_json()}

            self.redis_client.xadd(stream_name, message_data)
            logger.info(f"Published {message.type} to {stream_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            return False

    def subscribe(
        self,
        agent_id: str,
        handler: Callable[[A2AMessage], None],
        consumer_group: str = "default",
    ):
        """Subscribe to messages for an agent"""
        stream_name = f"agents:{agent_id}"
        consumer_name = f"{agent_id}-consumer"

        # Create consumer group if it doesn't exist
        try:
            self.redis_client.xgroup_create(
                stream_name, consumer_group, id="0", mkstream=True
            )
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP" not in str(e):
                logger.error(f"Failed to create consumer group: {e}")

        logger.info(f"Subscribed to {stream_name}")
        self.running = True

        while self.running:
            try:
                # Read messages
                messages = self.redis_client.xreadgroup(
                    consumer_group,
                    consumer_name,
                    {stream_name: ">"},
                    count=10,
                    block=1000,
                )

                for stream, msg_list in messages:
                    for msg_id, msg_data in msg_list:
                        try:
                            # Parse message
                            message_json = msg_data.get("message")
                            if message_json:
                                message = A2AMessage.from_json(message_json)

                                # Handle message
                                handler(message)

                                # Acknowledge message
                                self.redis_client.xack(
                                    stream_name, consumer_group, msg_id
                                )
                        except Exception as e:
                            logger.error(f"Error processing message: {e}")

            except Exception as e:
                logger.error(f"Error reading from stream: {e}")

    def stop(self):
        """Stop subscribing"""
        self.running = False

    def get_pending_count(self, agent_id: str, consumer_group: str = "default") -> int:
        """Get count of pending messages"""
        try:
            stream_name = f"agents:{agent_id}"
            pending = self.redis_client.xpending(stream_name, consumer_group)
            return pending["pending"]
        except Exception as e:
            logger.error(f"Error getting pending count: {e}")
            return 0
