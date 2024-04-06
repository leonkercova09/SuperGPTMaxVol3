import os
# Loading configurations from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')  
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
TOP_P = float(os.getenv('TOP_P', '1.0'))
MODEL = os.getenv('MODEL', 'text-davinci-003')
SHOW_TOKEN_COST = os.getenv('SHOW_TOKEN_COST', 'True') == 'True'  # Example of converting string to boolean
