My day started with a question. "How can I get consistent results from AI" Didnt know I'll learn about evals.

Why should you care?

Everyone is working on AI or AI agents these days. AI systems arent a direct function- there are lot of parameters- the model, the weights, the prompt quality, inputs etc. which honestly makes reliability questionable.

Before we start getting inference involved, every statement needs a human labelled truth. Its using the domain knowledge, experience and wahtever other tools they have at their disposal. Without this, evals is as good as comparing AI with itself. Spideman meme. 

First term:

* Ground truth (GT) -> Its what a expert human has said the benchmark should be. 

What comes next is what does AI say in relation to nto this GT. Thats what has amazingly confusing names. and since a ground truth can be Risk/OK (think any 2 binary on-off values), we have 4 combinations.

| Ground Truth | AI Response | Base Metric                                                  | Example                                                      |
| ------------ | ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Risk         | Risk        | True Positive **TP** (See positive has nothing to do that groudn truth is negatuve) | I have cancer and AI concurs.                                |
| Risk         | OK          | False Negative **FN** (Missed assessment)                    | Congrats you dont have cancer. You go home and die a few days later |
| OK           | Risk        | False Positive **FP** (False alarm)                          | Hey you have cancer. I go home and cry when I am actually healthy. |
| OK           | OK          | True Negative **TN**                                         | Both AI and I concur you are cancer free.                    |

## Mapping use cases and what to minimise on

Real world is messy so not all use cases can follow same requirement for metric to optimise on. Obviously the intersting ones are going to be where there are deviations liek FP and FN. Lets see a few examples.

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

A) Safety critical? Minimse FN. Defend the bad ones.

B)User Experience? Minimise FP. Protect the good ones.

C)Business tradeoff? depends on cost of review vs cost of missing.

### So can we measure? 

We might ask a few questions like how many bad ones did I not detect? how many good ones did I miss? 

Thankfully for us, we have some simple metrics that help us answer this.  Interestingly, all metrics are jsut a comparision and ranking wrt to other base metrics.

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

Precision is best defined as the noise in our space. If Im fishing for fish, I get tyres, bottles, shipwreck then my precison goes down. Expectedly then, precision is a measure of FP. 
$$
precision = TP/(TP+FP)
$$
My fishing expediation got me total of 10 items. 5 fishes, 1 tyre, 3 plastic bottles, 1 captain hook's crutch. 
$$
precision = 5/(10) = 0.5 = 50%
$$
As precision goes lower, we end up with results we dont need. Which again adds time and effort on humans. 



## Accuracy

I dont care for accuracy much because it takse both sides. FP and FN. The issue with taking both sides is that in large volumes, a small error goes un-noticed. I didnt test this so giving it a miss.

## F1

F1 is interesting because it tries to penalise imbalanced recall and precision. F1 is also great because we have several parameters- model, prompt and F1 gives one number to make sense of it all before deciding.

| Recall         | Precision     | F1   |
| -------------- | ------------- | ---- |
| 100            | 100           | 100  |
| 100            | 0 (all dirty) | 0    |
| 0 (all misses) | 100           | 0    |
| 75             | 90            | 82   |

## Consistency

But what about getting *same* results every time? Consistency is hardest. And there is no mathetmtical forumal because its inherently reliant on the data and the results both. And it compunds over time. Some types of approaches that my be useful:

A) Making an average check from total rules or policies we have defined. example - If I say 5 of  these 10 tickets are classified as P1 ticket because of security and AI also flags it as security, we can call it consistent.

B) An extension of A. Storing consistency results over time so they can become a knolwedge base for AI context injection. 

C) LLM as a judge. 

## Code & Test

How I learnt all of this isnt y theory.I didnt search for evals for AI because frameworks dont tell the real what and how. I wrote some python code for the support ticket example to do evals harness from scratch. All code included here. 

## Process

```
graph TD
    %% Phase 1: Ground Truth & Initial Evals
    subgraph P1 [Phase 1: Baseline & Evaluation Loop]
        A[50 Human-Labeled Examples<br><b>Ground Truth</b>] --> B(Run AI Evaluations)
        B --> C{Metrics Pass?}
        C -- No --> D[Tweak Prompt / Model]
        D --> B
        C -- Yes --> E[Identify Best Prompt/Model]
    end

    %% Phase 2: Controlled Go-Live
    subgraph P2 [Phase 2: Controlled Go-Live & HITL]
        E --> F[Controlled Go-Live<br><b>Production</b>]
        F --> G[AI Generates Response]
        G --> H[Human-in-the-Loop Review]
        H --> I[Assess Metrics vs. Ground Truth]
    end

    %% Phase 3: Continuous Improvement
    subgraph P3 [Phase 3: Continuous Improvement]
        I --> J{Metrics Degraded /<br>Response Different?}
        J -- Yes --> K[Push to Benchmark Dataset]
        K --> L[(Benchmark Dataset)]
        L --> M[RAG Context / Future Training]
        M --> D
        J -- No --> N[Maintain Production]
    end

    %% Style Adjustments
    style A fill:#d4edda,stroke:#28a745,stroke-width:2px
    style E fill:#fff3cd,stroke:#ffc107,stroke-width:2px
    style F fill:#cce5ff,stroke:#007bff,stroke-width:2px
    style L fill:#f8d7da,stroke:#dc3545,stroke-width:2px
```



## Key Takeways

1. Finding the metric that matters most is important. It different for different use case. 

2. Store benchmarks. This the golden truth and key context for AI request.

   