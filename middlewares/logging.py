from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Update
import logging

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = getattr(event.from_user, 'id', 'unknown')
        state = data.get('state')
        state_name = await state.get_state() if state else 'no FSM'
        update_type = type(event).__name__
        handler_name = getattr(handler, '__name__', str(handler))
        logger.info(f"📥 Update: {update_type} от user_id={user_id} | FSM: {state_name} | Handler: {handler_name}")
        return await handler(event, data)
