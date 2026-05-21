import os
from dotenv import load_dotenv
from helpers.utils import grab_env_var

PUBLIC_KEY = grab_env_var('PUBLIC_KEY')
DRAW_URL = 'https://www.canada.ca/content/dam/ircc/documents/json/ee_rounds_123_en.json'
PROGRAM_NAMES = {
    "Provincial Nominee Program": "PNP",
    "French-Language Proficiency": "FLP",
    "Canadian Experience Class": "CEC",
    "Trades Occupations": "TO",
    "Senior Managers With Canadian Work Experience": "SMCWE",
    "Healthcare And Social Services Occupations": "HSSO",
    "Physicians With Canadian Work Experience": "PCWE",
    "Education Occupations": "EO",
    "Healthcare Occupations": "HO",
    "General": "GEN",
    "STEM Occupations": "STEM",
    "Transport Occupations": "TRO",
    "Agriculture And Agri-Food Occupations": "AAFO",
    "No Program Specified": "NPS",
    "Federal Skilled Worker": "FSW",
    "Federal Skilled Trades": "FST",
}

def get_timer():

    time = grab_env_var("TIMER")

    if not time:
        time = 300
    else:
        time = int(time)
    
    return time

TIMER= get_timer()

