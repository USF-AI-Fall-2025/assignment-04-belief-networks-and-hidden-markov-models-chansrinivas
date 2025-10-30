# Belief-Networks-Hidden-Markov-Models
Fall 2025 CS 362/562

## Part I - Belief Networks:
### Step 1: Queries in alarm.py
1. The probability of Mary calling given that John called  

| MaryCalls | phi(MaryCalls) |
|------------|--------------|
| no         | 0.96         |
| yes        | 0.04         |

2. The probability of both John and Mary calling given Alarm  

| JohnCalls | MaryCalls | phi(JohnCalls,MaryCalls) |
|------------|------------|--------------|
| no         | no         | 0.0300       |
| no         | yes        | 0.0700       |
| yes        | no         | 0.2700       |
| yes        | yes        | 0.6300       |

3. The probability of both John and Mary calling given Alarm  

| Alarm     | phi(Alarm) |
|------------|-----------|
| no         | 0.8499    |
| yes        | 0.1501    |



### Step 2: Queries in carnet.py
1. Given that the car will not move, what is the probability that the battery is not working?

Before adding the KeyPresent node:
| Battery              | phi(Battery) |
|-----------------------|-------------|
| Works                 | 0.6410      |
| Doesn't work          | 0.3590      |


After adding the KeyPresent node:
| Battery              | phi(Battery) |
|-----------------------|-------------|
| Works                 | 0.6612      |
| Doesn't work          | 0.3388      |

2. Given that the radio is not working, what is the probability that the car will not start?

Before adding the KeyPresent node:
| Starts | phi(Starts) |
|---------|------------|
| yes     | 0.1313     |
| no      | 0.8687     |

After adding the KeyPresent node:
| Starts | phi(Starts) |
|---------|------------|
| yes     | 0.0880     |
| no      | 0.9120     |

3. Given that the battery is working, does the probability of the radio working change if we discover that the car has gas in it?  
=> Does not change

P(Radio | Battery: Works):

| Radio             | phi(Radio) |
|--------------------|-----------|
| turns on           | 0.7500    |
| Doesn't turn on    | 0.2500    |

P(Radio | Battery: Works, Gas: Full):
| Radio             | phi(Radio) |
|--------------------|-----------|
| turns on           | 0.7500    |
| Doesn't turn on    | 0.2500    |

4. Given that the car doesn't move, how does the probability of the ignition failing change if we observe that the car does not have gas in it?  
=> Changes

Before adding the KeyPresent node:  
P(Ignition | Moves=no):
| Ignition        | phi(Ignition) |
|------------------|--------------|
| Works            | 0.4334       |
| Doesn't work     | 0.5666       |

P(Ignition | Moves=no, Gas=Empty):
| Ignition        | phi(Ignition) |
|------------------|--------------|
| Works            | 0.5178       |
| Doesn't work     | 0.4822       |

After adding the KeyPresent node:  
P(Ignition | Moves=no):

| Ignition        | phi(Ignition) |
|------------------|--------------|
| Works            | 0.4657       |
| Doesn't work     | 0.5343       |

P(Ignition | Moves=no, Gas=Empty):

| Ignition        | phi(Ignition) |
|------------------|--------------|
| Works            | 0.5280       |
| Doesn't work     | 0.4720       |

5. What is the probability that the car starts if the radio works and it has gas in it?

Before adding the KeyPresent node:
| Starts | phi(Starts) |
|---------|------------|
| yes     | 0.7212     |
| no      | 0.2788     |

After adding the KeyPresent node:

| Starts | phi(Starts) |
|---------|------------|
| yes     | 0.5216     |
| no      | 0.4784     |

### Step 3: Adding a new node in carnet.py
| KeyPresent | phi(KeyPresent) |
|-------------|----------------|
| yes         | 0.6604         |
| no          | 0.3396         |



## Part II - Markov models:
1. Give an example of a word which was correctly spelled by the user, but which was incorrectly
“corrected” by the algorithm. Why did this happen?  
    + ```hi there -> hy there```  
    + In the above example, ```hi``` gets incorrectly corrected as ```hy``` likely because there are more patterns in our sample data file where 'h' is followed by 'y' like in words - 'hybrid'.
    + The emission probabilities in the training data might also show that when the user types 'i' it’s sometimes mistaken for 'y'.
  

2. Give an example of a word which was incorrectly spelled by the user, but which was still
incorrectly “corrected” by the algorithm. Why did this happen?  
    + ```abouy -> aboly```  
    + The algorithm corrects this as ```aboly``` instead of ```about```.
    + The limited training data is a major factor in why this happens. The letter transitions "ou" -> "ut" were rare in the emission and transition probabilities calculated.

3. Give an example of a word which was incorrectly spelled by the user, and was correctly corrected
by the algorithm. Why was this one correctly corrected, while the previous two were not?  
    + ```baa -> bat```
    + This worked because the emissions and transitions in the data happened to work for the "b -> b", "a -> a", and "a -> t" pattern.
    + The training data had multiple examples of similar typos and the letter to letter transitions were common in the data.
4. How might the overall algorithm’s performance differ in the “real world” if that training dataset is
taken from real typos collected from the internet, versus synthetic typos (programmatically
generated)?
    + If the training data came from real world mistakes, then it would perform much better since human typos often follows a specific typing pattern where we might do things like accidentally clicking on the wrong adjacent key.
    + The programmatically generated typos are in a way random and most words don't actually have the correct misspelled versions. Like for "at" vs "ast" - I think it's less likely someone would type 'at' as 'ast'. Instead, the misspelled version might actually be different.
    + Hence, the training data taken from real world will produce more realistic transition and emission probabilities.