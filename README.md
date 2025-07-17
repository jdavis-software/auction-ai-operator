# auction-ai-operator

An orchestrator that coordinates:
1. **Scraper agents** – collect auction data  
2. **Compliance checks** – verify data meets policy/legality  
3. **Normalization** – structure and clean the data  
4. **Outreach** – send alerts, notifications, or updates  

The orchestrator runs a central async loop and can be triggered either on a schedule or by external events.

## Quick start
```bash
pip install -r requirements.txt
python run.py
```
