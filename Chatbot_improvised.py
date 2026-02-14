import random
import datetime
import re
import os

class SimpleChatBot:
    def __init__(self, name="Buddy"):
        self.name = name
        self.conversation_history = []
        
        # Command Center - All available commands with descriptions
        self.command_center = {
            # Chat Commands
            '/help': {
                'description': 'Show all available commands',
                'category': '📋 General',
                'usage': '/help',
                'example': '/help'
            },
            '/commands': {
                'description': 'Show command center (this menu)',
                'category': '📋 General',
                'usage': '/commands',
                'example': '/commands'
            },
            '/clear': {
                'description': 'Clear the screen',
                'category': '📋 General',
                'usage': '/clear',
                'example': '/clear'
            },
            
            # Conversation Management
            '/history': {
                'description': 'Show conversation history',
                'category': '💬 Conversation',
                'usage': '/history',
                'example': '/history'
            },
            '/save': {
                'description': 'Save conversation to file',
                'category': '💬 Conversation',
                'usage': '/save',
                'example': '/save'
            },
            '/load': {
                'description': 'Load a previous conversation file',
                'category': '💬 Conversation',
                'usage': '/load <filename>',
                'example': '/load chat_history_20240101_120000.txt'
            },
            '/clear_history': {
                'description': 'Clear conversation history',
                'category': '💬 Conversation',
                'usage': '/clear_history',
                'example': '/clear_history'
            },
            '/export': {
                'description': 'Export conversation as text file',
                'category': '💬 Conversation',
                'usage': '/export',
                'example': '/export'
            },
            
            # Information & Stats
            '/stats': {
                'description': 'Show conversation statistics',
                'category': '📊 Information',
                'usage': '/stats',
                'example': '/stats'
            },
            '/time': {
                'description': 'Show current time',
                'category': '📊 Information',
                'usage': '/time',
                'example': '/time'
            },
            '/date': {
                'description': 'Show current date',
                'category': '📊 Information',
                'usage': '/date',
                'example': '/date'
            },
            '/info': {
                'description': 'Show bot information',
                'category': '📊 Information',
                'usage': '/info',
                'example': '/info'
            },
            
            # Fun Commands
            '/joke': {
                'description': 'Tell me a random joke',
                'category': '🎮 Fun',
                'usage': '/joke',
                'example': '/joke'
            },
            '/quote': {
                'description': 'Get an inspirational quote',
                'category': '🎮 Fun',
                'usage': '/quote',
                'example': '/quote'
            },
            '/fact': {
                'description': 'Get a random fact',
                'category': '🎮 Fun',
                'usage': '/fact',
                'example': '/fact'
            },
            '/roll': {
                'description': 'Roll a dice (1-6)',
                'category': '🎮 Fun',
                'usage': '/roll',
                'example': '/roll'
            },
            '/coin': {
                'description': 'Flip a coin',
                'category': '🎮 Fun',
                'usage': '/coin',
                'example': '/coin'
            },
            
            # Utility Commands
            '/search': {
                'description': 'Search in conversation history',
                'category': '🔧 Utility',
                'usage': '/search <keyword>',
                'example': '/search hello'
            },
            '/repeat': {
                'description': 'Repeat last bot response',
                'category': '🔧 Utility',
                'usage': '/repeat',
                'example': '/repeat'
            },
            '/count': {
                'description': 'Count messages in history',
                'category': '🔧 Utility',
                'usage': '/count',
                'example': '/count'
            },
            '/echo': {
                'description': 'Echo your message',
                'category': '🔧 Utility',
                'usage': '/echo <message>',
                'example': '/echo Hello World'
            },
            
            # Exit
            '/quit': {
                'description': 'Exit the chatbot',
                'category': '🚪 Exit',
                'usage': '/quit',
                'example': '/quit'
            },
            '/exit': {
                'description': 'Exit the chatbot',
                'category': '🚪 Exit',
                'usage': '/exit',
                'example': '/exit'
            }
        }
        
        # Define response patterns
        self.responses = {
            'greeting': {
                'patterns': [r'hi', r'hello', r'hey', r'greetings', r'good morning', r'good afternoon', r'good evening'],
                'responses': [
                    f"Hello! I'm {name}. How can I help you?",
                    f"Hi there! Nice to meet you!",
                    f"Hey! What's on your mind?",
                    f"Greetings! How are you today?"
                ]
            },
            'how_are_you': {
                'patterns': [r'how are you', r'how do you do', r'how\'s it going', r'how are things'],
                'responses': [
                    "I'm doing great, thanks for asking!",
                    "I'm fantastic! How about you?",
                    "Doing well, ready to chat with you!",
                    "I'm good! Always happy to talk."
                ]
            },
            'name': {
                'patterns': [r'your name', r'who are you', r'what are you', r'tell me about yourself'],
                'responses': [
                    f"My name is {name}. I'm your personal chatbot assistant!",
                    f"I'm {name}, created to chat with you and help where I can.",
                    f"You can call me {name}. I'm here to keep you company!"
                ]
            },
            'weather': {
                'patterns': [r'weather', r'temperature', r'hot outside', r'cold outside'],
                'responses': [
                    "I wish I could tell you the weather! But I don't have internet access.",
                    "Weather information requires an internet connection, which I don't have.",
                    "Sorry, I can't check the weather right now. You might want to look outside! 😊"
                ]
            },
            'thanks': {
                'patterns': [r'thanks', r'thank you', r'appreciate it', r'good bot'],
                'responses': [
                    "You're welcome!",
                    "Happy to help!",
                    "Anytime!",
                    "My pleasure!"
                ]
            },
            'feeling': {
                'patterns': [r'i am (.*)', r'i\'m (.*)', r'i feel (.*)', r'feeling (.*)'],
                'responses': [
                    "Thanks for sharing that with me.",
                    "I understand how you feel.",
                    "That's interesting. Tell me more.",
                    "I see. How long have you felt that way?"
                ]
            },
            'age': {
                'patterns': [r'how old are you', r'your age'],
                'responses': [
                    "I'm brand new! Just created recently.",
                    "I don't have an age like humans do. I'm just code!",
                    "I'm as old as this conversation! 😊"
                ]
            },
            'hobby': {
                'patterns': [r'what do you like', r'your hobby', r'what do you do for fun'],
                'responses': [
                    "I love chatting with people like you!",
                    "My favorite thing is having conversations and learning new things.",
                    "I enjoy helping people and making them smile."
                ]
            },
            'default': {
                'patterns': [],
                'responses': [
                    "That's interesting! Tell me more.",
                    "I see. What else is on your mind?",
                    "Hmm, I'm not sure I understand fully. Could you explain?",
                    "Interesting point! Go on...",
                    "I'd love to hear more about that.",
                    "That's a good conversation topic!"
                ]
            }
        }
        
        # Collection of jokes
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call a fake noodle? An impasta!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a sleeping bull? A bulldozer!",
            "Why did the math book look sad? Because it had too many problems!",
            "What do you call a fish with no eyes? A fsh!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What do you call a can opener that doesn't work? A can't opener!"
        ]
        
        # Collection of inspirational quotes
        self.quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "It does not matter how slowly you go as long as you do not stop. - Confucius",
            "Everything you've ever wanted is on the other side of fear. - George Addair",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt"
        ]
        
        # Collection of random facts
        self.facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!",
            "A day on Venus is longer than a year on Venus. It takes 243 Earth days to rotate once but only 225 Earth days to orbit the sun.",
            "Bananas are technically berries, while strawberries are not!",
            "Octopuses have three hearts and blue blood!",
            "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion!"
        ]

    def show_command_center(self):
        """Display the command center with all available commands"""
        print("\n" + "="*70)
        print("🎮 COMMAND CENTER - All Available Commands")
        print("="*70)
        
        # Group commands by category
        categories = {}
        for cmd, info in self.command_center.items():
            category = info['category']
            if category not in categories:
                categories[category] = []
            categories[category].append((cmd, info))
        
        # Display commands by category
        for category in sorted(categories.keys()):
            print(f"\n{category}:")
            print("-" * 50)
            for cmd, info in sorted(categories[category]):
                print(f"  {cmd:<15} - {info['description']}")
                print(f"      📝 Usage: {info['usage']}")
                if info['example'] != info['usage']:
                    print(f"      💡 Example: {info['example']}")
        
        print("\n" + "="*70)
        print("💡 Tip: Type any command directly in the chat")
        print("="*70 + "\n")

    def show_quick_commands(self):
        """Show a quick reference of most used commands"""
        print("\n" + "="*50)
        print("⚡ QUICK COMMANDS REFERENCE")
        print("="*50)
        quick_commands = {
            '/help': 'Show all commands',
            '/history': 'View chat history',
            '/save': 'Save conversation',
            '/stats': 'Show statistics',
            '/joke': 'Tell a joke',
            '/time': 'Current time',
            '/clear': 'Clear screen',
            '/quit': 'Exit chatbot'
        }
        for cmd, desc in quick_commands.items():
            print(f"{cmd:<12} - {desc}")
        print("="*50 + "\n")

    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_time_response(self):
        """Generate current time response"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"🕐 The current time is {current_time}"

    def get_date_response(self):
        """Generate current date response"""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"📅 Today is {current_date}"

    def get_joke(self):
        """Return a random joke"""
        return f"😄 {random.choice(self.jokes)}"

    def get_quote(self):
        """Return a random inspirational quote"""
        return f"💫 {random.choice(self.quotes)}"

    def get_fact(self):
        """Return a random fact"""
        return f"🔍 Did you know? {random.choice(self.facts)}"

    def get_bot_info(self):
        """Return bot information"""
        info = [
            f"🤖 Bot Name: {self.name}",
            f"📅 Created: {datetime.datetime.now().strftime('%B %Y')}",
            f"⚙️ Version: 2.0",
            f"💬 Commands Available: {len(self.command_center)}",
            f"📝 Conversation Length: {len(self.conversation_history)} messages",
            f"🎯 Purpose: Your friendly chat assistant"
        ]
        return "\n".join(info)

    def search_history(self, keyword):
        """Search for keyword in conversation history"""
        results = []
        for i, (speaker, message) in enumerate(self.conversation_history, 1):
            if keyword.lower() in message.lower():
                results.append(f"{i}. {speaker}: {message}")
        
        if results:
            return f"Found {len(results)} matches:\n" + "\n".join(results[:10])  # Show first 10
        else:
            return f"No matches found for '{keyword}'"

    def get_response(self, user_input):
        """Process user input and return appropriate response"""
        user_input_lower = user_input.lower().strip()
        
        # Add to conversation history
        self.conversation_history.append(("You", user_input))
        
        # Check each category for matching patterns
        for category, data in self.responses.items():
            if category != 'default':
                for pattern in data['patterns']:
                    if re.search(pattern, user_input_lower):
                        response = random.choice(data['responses'])
                        self.conversation_history.append((self.name, response))
                        return response
        
        # If no pattern matches, use default responses
        response = random.choice(self.responses['default']['responses'])
        self.conversation_history.append((self.name, response))
        return response

    def save_conversation(self):
        """Save conversation history to a file"""
        try:
            filename = f"chat_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("=== Chat Conversation History ===\n")
                file.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Bot: {self.name}\n")
                file.write("=" * 40 + "\n\n")
                
                for speaker, message in self.conversation_history:
                    file.write(f"{speaker}: {message}\n")
                
                file.write("\n" + "=" * 40 + "\n")
                file.write(f"Total Messages: {len(self.conversation_history)}")
            
            return filename, True
        except Exception as e:
            return str(e), False

    def show_history(self):
        """Display current conversation history"""
        if not self.conversation_history:
            return "\n📝 No conversation history yet."
        
        history = []
        history.append("\n" + "="*50)
        history.append("📝 CONVERSATION HISTORY")
        history.append("="*50)
        
        for i, (speaker, message) in enumerate(self.conversation_history, 1):
            history.append(f"{i:3d}. {speaker}: {message}")
        
        history.append("="*50)
        history.append(f"Total: {len(self.conversation_history)} messages")
        
        return "\n".join(history)

    def show_stats(self):
        """Show conversation statistics"""
        if not self.conversation_history:
            return "\n📊 No conversation statistics available."
        
        user_messages = sum(1 for speaker, _ in self.conversation_history if speaker == "You")
        bot_messages = sum(1 for speaker, _ in self.conversation_history if speaker == self.name)
        total_messages = len(self.conversation_history)
        
        # Calculate average message length
        user_words = sum(len(message.split()) for speaker, message in self.conversation_history if speaker == "You")
        bot_words = sum(len(message.split()) for speaker, message in self.conversation_history if speaker == self.name)
        
        stats = []
        stats.append("\n" + "="*50)
        stats.append("📊 CONVERSATION STATISTICS")
        stats.append("="*50)
        stats.append(f"Total messages: {total_messages}")
        stats.append(f"Your messages: {user_messages}")
        stats.append(f"{self.name}'s messages: {bot_messages}")
        stats.append(f"Your average words/message: {user_words/user_messages:.1f}" if user_messages > 0 else "Your average words/message: 0")
        stats.append(f"Bot average words/message: {bot_words/bot_messages:.1f}" if bot_messages > 0 else "Bot average words/message: 0")
        stats.append(f"Conversation turns: {total_messages // 2}")
        stats.append("="*50)
        
        return "\n".join(stats)

    def chat(self):
        """Main chat loop"""
        self.clear_screen()
        print("\n" + "="*70)
        print(f"🤖 WELCOME TO {self.name.upper()}'S CHATBOT!")
        print("="*70)
        print(f"Hi! I'm {self.name}, your intelligent chat assistant.")
        print("\n📌 QUICK START:")
        print("   • Type '/commands' to see ALL available commands")
        print("   • Type '/quick' for most used commands")
        print("   • Just chat naturally with me!")
        print("="*70 + "\n")

        while True:
            try:
                user_input = input("You: ").strip()
                
                # Handle commands
                if user_input.startswith('/'):
                    command = user_input.lower().split()[0]  # Get first part of command
                    
                    # Command Center
                    if command == '/commands' or command == '/help':
                        self.show_command_center()
                    
                    elif command == '/quick':
                        self.show_quick_commands()
                    
                    elif command == '/clear':
                        self.clear_screen()
                        print(f"\n{self.name}: Screen cleared! Ready to continue...\n")
                    
                    # Conversation Management
                    elif command == '/history':
                        print(self.show_history())
                    
                    elif command == '/save':
                        filename, success = self.save_conversation()
                        if success:
                            print(f"\n{self.name}: ✅ Conversation saved to '{filename}'")
                        else:
                            print(f"\n{self.name}: ❌ Error saving: {filename}")
                    
                    elif command == '/load':
                        parts = user_input.split()
                        if len(parts) > 1:
                            filename = parts[1]
                            # Here you would implement load functionality
                            print(f"\n{self.name}: Loading '{filename}'... (feature in development)")
                        else:
                            print(f"\n{self.name}: Please specify filename. Usage: /load <filename>")
                    
                    elif command == '/clear_history':
                        self.conversation_history.clear()
                        print(f"\n{self.name}: ✅ Conversation history cleared!")
                    
                    elif command == '/export':
                        filename, success = self.save_conversation()
                        if success:
                            print(f"\n{self.name}: ✅ Conversation exported to '{filename}'")
                    
                    # Information & Stats
                    elif command == '/stats':
                        print(self.show_stats())
                    
                    elif command == '/time':
                        print(f"\n{self.name}: {self.get_time_response()}")
                    
                    elif command == '/date':
                        print(f"\n{self.name}: {self.get_date_response()}")
                    
                    elif command == '/info':
                        print(f"\n{self.name}:\n{self.get_bot_info()}")
                    
                    # Fun Commands
                    elif command == '/joke':
                        print(f"\n{self.name}: {self.get_joke()}")
                    
                    elif command == '/quote':
                        print(f"\n{self.name}: {self.get_quote()}")
                    
                    elif command == '/fact':
                        print(f"\n{self.name}: {self.get_fact()}")
                    
                    elif command == '/roll':
                        roll = random.randint(1, 6)
                        print(f"\n{self.name}: 🎲 You rolled a {roll}!")
                    
                    elif command == '/coin':
                        result = random.choice(['Heads', 'Tails'])
                        print(f"\n{self.name}: 🪙 It's {result}!")
                    
                    # Utility Commands
                    elif command == '/search':
                        parts = user_input.split(maxsplit=1)
                        if len(parts) > 1:
                            results = self.search_history(parts[1])
                            print(f"\n{self.name}: {results}")
                        else:
                            print(f"\n{self.name}: Please provide a keyword. Usage: /search <keyword>")
                    
                    elif command == '/repeat':
                        # Find last bot message
                        last_bot_msg = None
                        for speaker, msg in reversed(self.conversation_history):
                            if speaker == self.name:
                                last_bot_msg = msg
                                break
                        if last_bot_msg:
                            print(f"\n{self.name}: [Repeated] {last_bot_msg}")
                        else:
                            print(f"\n{self.name}: No previous message to repeat.")
                    
                    elif command == '/count':
                        print(f"\n{self.name}: 📊 Total messages: {len(self.conversation_history)}")
                    
                    elif command == '/echo':
                        parts = user_input.split(maxsplit=1)
                        if len(parts) > 1:
                            print(f"\n{self.name}: Echo: {parts[1]}")
                        else:
                            print(f"\n{self.name}: Nothing to echo. Usage: /echo <message>")
                    
                    # Exit Commands
                    elif command in ['/quit', '/exit']:
                        print(f"\n{self.name}: 👋 Goodbye! Thanks for chatting!")
                        if len(self.conversation_history) > 0:
                            save_choice = input(f"\n{self.name}: Save conversation before exiting? (yes/no): ").strip().lower()
                            if save_choice in ['yes', 'y']:
                                filename, success = self.save_conversation()
                                if success:
                                    print(f"{self.name}: ✅ Saved to '{filename}'")
                        print(f"\n{self.name}: Have a great day!")
                        break
                    
                    else:
                        print(f"\n{self.name}: ❌ Unknown command '{command}'")
                        print(f"{self.name}: Type '/commands' to see all available commands.")
                    
                    continue

                # Handle empty input
                if not user_input:
                    print(f"\n{self.name}: 👂 I'm listening... Say something!")
                    continue

                # Get response for normal input
                response = self.get_response(user_input)
                print(f"\n{self.name}: {response}\n")

            except KeyboardInterrupt:
                print(f"\n\n{self.name}: 👋 Goodbye! Thanks for chatting!")
                break
            except Exception as e:
                print(f"\n{self.name}: ❌ Oops! Something went wrong: {e}")
                print(f"{self.name}: Let's continue chatting!\n")

# Run the chatbot
if __name__ == "__main__":
    # You can change the bot's name here
    bot_name = "ChatBuddy"
    bot = SimpleChatBot(bot_name)
    bot.chat()