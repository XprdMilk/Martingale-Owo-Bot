import discord
from discord.ext import commands
import asyncio
import random
import winsound
import threading
import re
import os
from dotenv import load_dotenv

# Load the hidden .env file
load_dotenv()

# --- CONFIGURATION ---
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
START_BET = 1000         
MAX_BET = 200000        
# ---------------------

class MartingaleBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", self_bot=True)
        self.current_bet = START_BET
        self.total_profit = 0  
        self.current_balance = "Checking..." # NEW: Bankroll tracker
        self.flips_since_cash_check = 0      # NEW: Counter for checking cash
        self.is_running = False
        self.waiting_for_next_flip = False 

    async def on_ready(self):
        print(f"✅ Logged in as {self.user.name}")
        print("Type .start in Discord to begin.")

    def play_alarm(self):
        for _ in range(5):
            winsound.Beep(2500, 800) 
            winsound.Beep(2000, 800)

    async def on_message(self, message):
        # 1. Listen for YOUR Start/Stop
        if message.author.id == self.user.id:
            if message.content == ".start":
                self.is_running = True
                self.total_profit = 0 
                self.flips_since_cash_check = 0
                print("\n🚀 Martingale Activated! (Profit counter reset to 0)")
                
                # Ask OwO for our starting balance immediately
                await asyncio.sleep(1) 
                await message.channel.send("owo cash")
                await asyncio.sleep(2) 
                
                await self.send_flip(message.channel)
                return
            elif message.content == ".stop":
                self.is_running = False
                print(" " * 80, end="\r") # Clears the dashboard line
                print(f"\n🛑 Martingale Stopped. Final Session Profit: {self.total_profit}")
                return

        # 2. EMERGENCY CAPTCHA DETECTOR & BALANCE CHECKER
        if self.is_running and message.author.id == 408785106942164992:
            content = message.content.lower()
            
            # Check for Captcha
            if "captcha" in content:
                print(" " * 80, end="\r")
                print("\n🚨 CAPTCHA DETECTED! STOPPING BOT AND SOUNDING ALARM 🚨")
                self.is_running = False 
                threading.Thread(target=self.play_alarm, daemon=True).start()
                return

            # NEW: Check for Balance updates
            # OwO says: "Zak, you currently have **64,000** cowoncy!"
            if "currently have" in content and "cowoncy" in content:
                # This pulls out just the number, ignoring the bold asterisks OwO uses
                match = re.search(r"have .*?([\d,]+).*? cowoncy", content)
                if match:
                    self.current_balance = match.group(1)

    async def on_message_edit(self, before, after):
        if not self.is_running: return
        if after.channel.id != CHANNEL_ID or after.author.id != 408785106942164992: return
        if self.waiting_for_next_flip: return

        content = after.content.lower()

        # 3. PROFIT MATH & DETECTION 
        if "!!" in content and "won" in content:
            self.total_profit += self.current_bet 
            print(f"\n[+] WIN! Net Profit: {self.total_profit} 💰 | Resetting to {START_BET}")
            self.current_bet = START_BET
            await self.schedule_next_flip(after.channel)
            
        elif ":c" in content and "lost" in content:
            self.total_profit -= self.current_bet 
            print(f"\n[-] LOSS! Net Profit: {self.total_profit} | Doubling next bet to {self.current_bet * 2}")
            self.current_bet *= 2
            await self.schedule_next_flip(after.channel)

    async def schedule_next_flip(self, channel):
        self.waiting_for_next_flip = True 
        delay = random.randint(22, 28) 
        
        # THE LIVE DASHBOARD LOOP
        for remaining in range(delay, 0, -1):
            if not self.is_running: break 
                
            # NEW: Clean, live-updating dashboard at the bottom of your CMD
            status = f"⏳ {remaining}s | 🏦 Bank: {self.current_balance} | 📈 Profit: {self.total_profit}    "
            print(status, end="\r", flush=True)
            await asyncio.sleep(1)
            
        print(" " * 80, end="\r") # Wipe the dashboard cleanly before the next flip prints
        self.waiting_for_next_flip = False 
        
        if self.is_running:
            await self.send_flip(channel)

    async def send_flip(self, channel):
        if not self.is_running: return

        # NEW: Automatically check cash every 10 flips
        self.flips_since_cash_check += 1
        if self.flips_since_cash_check >= 10:
            self.flips_since_cash_check = 0
            async with channel.typing():
                await channel.send("owo cash")
                await asyncio.sleep(2) # Give OwO 2 seconds to reply before we flip

        if self.current_bet > MAX_BET:
            print(f"[!] Max bet hit. Taking the loss and resetting to {START_BET}.")
            self.current_bet = START_BET

        print(f"🎲 Sending flip: owo cf {self.current_bet}")
        
        try:
            async with channel.typing():
                await asyncio.sleep(random.uniform(0.5, 1.5))
                await channel.send(f"owo cf {self.current_bet}")
        except Exception as e:
            print(f"❌ Error sending: {e}")
            self.is_running = False

bot = MartingaleBot()
bot.run(TOKEN)