import string
import random
import datetime
import json
import click
import time
# mock competition class
class Competition:
    def __init__(self):
        self.matches = []  # initialize match lists
        self.name = ""
        pass
    def get_all_matches(self):
        return self.matches
    def add_match(self, match):
        """
        add match to competition
        """
        self.matches.append(match)
    def set_name(self,name):
        self.name = name
    def get_name(self):
        return self.name
    
# mock 
def fetch_matches_by_comp_id(id):
    matches = []
    for i in range(id):
        match = Match()
        match.set_name("Match "+str(i+1))
        matches.append(match)
    return matches

# mock 
def fetch_competitions(date=datetime.datetime.now()):
    num=3
    comps = []
    for i in range(num):
        comp = Competition()
        comp.set_name("League "+string.ascii_uppercase[i])
        matches = fetch_matches_by_comp_id(random.randint(3,20))  # make match list
        for match in matches:  # add match to each competition
            comp.add_match(match)
        comps.append(comp)
    return comps

# mock match class
class Match:
    def __init__(self) :
        self.name = ""
        pass
    def get_name(self):
        return self.name
    def set_name(self,name):
        self.name = name

class Solution:
    def __init__(self) :
        self.trial_no = 0
        self.comp_id = "League A"
        self.prob_id = ""
        self.indi_id = ""
        self.prob_env = ""
        self.indi_env = ""
        self.match_id = "Match 1"
        self.created_at = datetime.datetime.now()
        self.user_id = ""
        self.var =[]
        pass
    def set_all(self,num):
        self.prob_id = "Problem " + str(num)
        self.indi_id = "Indicator "+ str(num)
        self.prob_env = "ProblemEnv " + str(num)
        self.indi_env = "IndicatorEnv " + str(num)
        self.created_at = datetime.datetime(2024,2,25,12,num,num)
        self.user_id = "User "+ str(num)
        self.var =[num,num**2,num**3,num+1,num+2]

def fetch_solution(num=0):
    sol = Solution()
    sol.set_all(num)
    return sol

class Evaluation:
    def __init__(self):
        self.trial_no = 0
        self.comp_id = "League A"
        self.prob_id = ""
        self.indi_id = ""
        self.prob_env = ""
        self.indi_env = ""
        self.match_id = "Match 1"
        self.created_at = datetime.datetime.now()
        self.user_id = ""
        self.started_at = datetime.datetime.now()
        self.finished_at = datetime.datetime.now()
        self.status = True
        self.obj = 0
        self.constraint = 0
        pass
    def set_all(self,num):
        self.prob_id = "Problem " + str(num)
        self.indi_id = "Indicator "+ str(num)
        self.prob_env = "ProblemEnv " + str(num)
        self.indi_env = "IndicatorEnv " + str(num)
        self.created_at = datetime.datetime(2024,2,25,12,num,num)
        self.user_id = "User "+ str(num)
        self.started_at = datetime.datetime(2024,2,25,12,num,num)
        self.finished_at = datetime.datetime(2024,2,25,13,num+10,num+10)
        self.obj = num
        self.constraint = num
        
def fetch_eval(num = 0):
    eval = Evaluation()
    eval.set_all(num)
    return eval
     
class Score:
    def __init__(self):
        self.trial_no = 0
        self.comp_id = "League A"
        self.prob_id = ""
        self.indi_id = ""
        self.prob_env = ""
        self.indi_env = ""
        self.match_id = "Match 1"
        self.created_at = datetime.datetime.now()
        self.user_id = ""
        self.started_at = datetime.datetime.now()
        self.finished_at = datetime.datetime.now()
        self.status = True
        self.score = 0
        pass
    
    def set_all(self,num):
        self.trial_no = num
        self.prob_id = "Problem " + str(num)
        self.indi_id = "Indicator "+ str(num)
        self.prob_env = "ProblemEnv " + str(num)
        self.indi_env = "IndicatorEnv " + str(num)
        self.created_at = datetime.datetime(2024,2,25,12,num,num)
        self.user_id = "User "+ str(num)
        self.started_at = datetime.datetime(2024,2,25,12,num,num)
        self.finished_at = datetime.datetime(2024,2,25,13,num+10,num+10)
        self.score = num
        
def fetch_score(num = 0):
    score = Score()
    score.set_all(num)
    return score
     
class Trial:
    def __init__(self):
        self.solution = Solution()
        self.evaluation = Evaluation()
        self.score = Score()
        pass
   
def fetch_trial(num):
    trial = Trial()
    trial.solution = fetch_solution(num)
    trial.evaluation = fetch_eval(num)
    trial.score = fetch_score(num)
    return trial
        
def fetch_trials(num=20):
    trials = []
    for i in range(num):
        trial = fetch_trial(random.randint(1,20))
        trials.append(trial)
    return trials

def create_sol(file_path = None):
    if file_path is not None and file_path.suffix == ".json":
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                click.echo(click.style(f"Contents of the JSON file: {json.dumps(data, indent=2)}",fg="black",bg="white"))
        except Exception as e:
            click.echo(click.style(f"Failed to read JSON file: {e}",bg="red"))
    elif file_path is not None:
        click.echo(click.style("The submitted file is not a JSON file.",bg="red"))
        return
    sol = Solution()
    sol.set_all(1)
    time.sleep(1)
    return sol