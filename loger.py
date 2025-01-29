from functools import wraps
import logging

class botloger:

    def __init__(self):
        # Set up logging
        logging.basicConfig(level=logging.INFO)

    @staticmethod
    def log_command(func):
        @wraps(func)
        async def wrapper(ctx, *args, **kwargs):
            # Log the command name and who called it
            if ctx.guild != None:
                logging.info(f"Command '{func.__name__}' called by {ctx.author} in guild {ctx.guild}(id:{ctx.guild.id}).")
            else:
                logging.info(f"Command '{func.__name__}' called by {ctx.author}.")
            return await func(ctx, *args, **kwargs)
        return wrapper