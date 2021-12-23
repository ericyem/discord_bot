import asyncio

class Timer:
    """ asynchrous timer """
    def __init__(self,seconds: int) -> None:
        self.seconds = seconds
    
    def countdown(self):
        self.seconds -= 1
    
    async def run(self):
        self.countdown()
        await asyncio.sleep(1)  
        
    def seconds_remaining(self):
        return self.seconds