My day started with a question. "How can I get **consistent** results from AI". Didnt know I'll learn about evals.

## Why should you care?

Everyone is working on AI or AI agents these days. AI systems arent a direct function- there are lot of parameters- the model, the weights, the prompt quality, inputs etc. which honestly makes reliability questionable.

Before we start getting inference involved, every statement needs a human labelled truth. Its using the domain knowledge, experience and whatever other tools they have at their disposal. Without this, evals is as good as comparing AI with itself. Spiderman meme. 

First term:

* Ground truth (GT) -> Its what a expert human has said the benchmark should be. 

What comes next is what does AI say in relation to not this GT. Thats what has amazingly confusing names. and since a ground truth can be Risk/OK (think any 2 binary on-off values), we have 4 combinations.

| Ground Truth | AI Response | Base Metric                                                  | Example                                                      |
| ------------ | ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Risk         | Risk        | True Positive **TP** (See positive has nothing to do that groudn truth is negatuve) | I have cancer and AI concurs.                                |
| Risk         | OK          | False Negative **FN** (Missed assessment)                    | Congrats you dont have cancer. You go home and die a few days later |
| OK           | Risk        | False Positive **FP** (False alarm)                          | Hey you have cancer. I go home and cry when I am actually healthy. |
| OK           | OK          | True Negative **TN**                                         | Both AI and I concur you are cancer free.                    |

## Mapping use cases and what to minimise on

Real world is messy so not all use cases can follow same requirement for metric to optimise on. Obviously the interesting ones are going to be where there are deviations like FP and FN. Lets see a few examples.

| Use Case                          | GT         | Minimise On                 | Rationale                                                    |
| --------------------------------- | ---------- | --------------------------- | ------------------------------------------------------------ |
| Email spam filter                 | not spam   | FP (AI says spam)           | I'm ok someone wanting to send me a million dollars from Africa, but not OK for an email from my boss to end up in junk. |
| Credit card Fraud detection       | suspicious | FN (AI says not suspicious) | Im not ok with a fraudulent transaction and loss for customer & potential risk ownership. Its a mild annoyance for blocking a correct on so FP isnt all that bad |
| Contract risk review              | Flag       | FN (AI says no problem)     | You are welcoming future lawsuits or accepting liability. congrats. |
| netflix recommendation            | "for you"  | FP (AI says not for you)    | Homepage is garbage(like Dubai bling), i will stop my subscription so revenue loss. |
| Content moderation                | "18+ only" | FN (AI says all ages)       | Congrats our children are scarred for life.                  |
| ATS screening                     | Good match | FN( AI says not good match) | Missing out on good candidates.                              |
| self driving Pedestrian detection | Pedestrian | FN(Not a pedestrian)        | Death toll +1. AI driving scrapped.                          |
| Medical symptom checker           | Match      | FN (No match found)         | Congrats, you have disease.                                  |
| Detects property has flood risk   | Risk       | FN( No risk)                | You were watching Titanic and you didnt catch the ending.    |
| Support ticket is P1              | P1         | FN(not P1)                  | Production down.                                             |

If this is too much, generally they fall under these themes.

A) Safety critical? Minimise FN. Defend the bad ones.

B)User Experience? Minimise FP. Protect the good ones.

C)Business tradeoff? depends on cost of review vs cost of missing.

### So can we measure? 

We might ask a few questions like how many bad ones did I not detect? how many good ones did I miss? 

Thankfully for us, we have some simple metrics that help us answer this.  Interestingly, all metrics are just a comparision and ranking wrt to other base metrics.

### Recall

No its not recalling like memory. recall simply means how many right ones did I get. Its just derived from counts of TP. Any guesses what it focusses on? its FN.
$$
recall  = TP/(TP+FN)
$$
I made 100 requests for a credit card fraud check and only 90 of them came out as fraud. 10  of them were fraud but not picked up. so my 
$$
recall = 90(90+10) = 90/100 =0.9
$$
So if I dont have any FN, my recall is 100%. What we aspire for when we want to minimise FN.

## Precision

Precision is best defined as the noise in our space. If Im fishing for fish, I get tyres, bottles, shipwreck then my precision goes down. Expectedly then, precision is a measure of FP. 
$$
precision = TP/(TP+FP)
$$
My fishing expedition got me total of 10 items. 5 fishes, 1 tyre, 3 plastic bottles, 1 captain hook's crutch. 
$$
precision = 5/(10) = 0.5 = 50%
$$
As precision goes lower, we end up with results we dont need. Which again adds time and effort on humans. 



## Accuracy

Accuracy takes both sides. FP and FN. The issue with taking both sides is that in large volumes, a small error goes un-noticed. Not exploring further in this essay.

## F1

F1 is interesting because it tries to penalise imbalanced recall and precision. F1 is also great because we have several parameters- model, prompt and F1 gives one number to make sense of it all before deciding.
$$
2 * (Precision*Recall)/(Precision+Recall)
$$

| Recall         | Precision     | F1   |
| -------------- | ------------- | ---- |
| 100            | 100           | 100  |
| 100            | 0 (all dirty) | 0    |
| 0 (all misses) | 100           | 0    |
| 75             | 90            | 82   |

### **Threshold sensitivity**

 LLMs produce probabilistic outputs. In production evals, you'd vary the decision threshold and plot a precision-recall curve. 

Decided this is going to be step 2 and depending on specific context so not exploring it here today.

## Consistency

But what about getting *same* results every time? Consistency is hardest. And there is no mathematical formula because its inherently reliant on the data and the results both. And it compunds over time. Some types of approaches that my be useful:

A) Category Agreement: Making an average check from total rules or policies we have defined. example - If I say 5 of  these 10 tickets are classified as P1 ticket because of security and AI also flags it as security, we can call it consistent. Th sample code measures this as reason_consistency.

B) An extension of A. Storing consistency results over time so they can become a knowledge base for AI context injection. 

C) LLM as a judge. 

## Code & Test

How I learnt all of this isnt by theory.I didnt search for evals for AI because frameworks dont tell the real what and how. I wrote some python code for the support ticket example to do evals harness from scratch. All code free to use. 

## Benchmarks

**Benchmark = use cases worth remembering. ** It's a **high-signal dataset**. We need one because over time we need to know if we doing better or worse from where we started and catch any degradation. What makes something high-signal:

- AI got it **wrong** → definitely add (failure to learn from)
- AI got it **right but it was a hard/ambiguous case** → add (edge case coverage)
- AI got it **right on an easy case** → don't bother (no new information)

Lets explore this with a simple agent where AI reviews a case for clauses and needs to flag them correctly.

| Case                   | AI Says | Human Says | Add to Benchmark? | Why?              |
| ---------------------- | ------- | ---------- | ----------------- | ----------------- |
| Clear breaches         | Reject  | Reject     | No                | no signal         |
| Ambiguous statement    | Accept  | Reject     | Yes               | FN case.          |
| New Legislation clause | Reject  | Accept     | Yes               | latest knowledge. |

## Pipeline

https://mermaid.ai/d/a6cb5217-436e-4b04-8206-9c7e83199d84



## Takeaways

1. Finding the metric that matters most is important. It different for different use case. 

2. 50 examples are generally a good starting point because they give enough rom to explore edge cases and drifts in behaviour (especially if we are doing any kind of semantic checks).

3. Store benchmarks. This the golden truth and key context for AI request.

   