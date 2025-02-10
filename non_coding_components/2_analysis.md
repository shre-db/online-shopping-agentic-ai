# Analysis

|⬇ Papers / characteristics ➡ |Agent Design |Reasoning Steps |Tool Use |Real-World Applicability|
|:-|:-|:-|:-|:-|
|**ReAct**|Focuses on interleaving reasoning and actions in a single model, promoting an interactive loop for problem-solving.|Focuses on iterative reasoning|Uses tools indirectly as part of the action component but do not emphasize tool learning or chaining|Fundamental concept that other frameworks build upon, might not be suitable all by itself for complex usecases.|
|**Toolformer**|Emphasizes learning tool usage, where the agent design must accomodate for training with API interactions.|Tool selection becomes a part of the reasoning process|directly addresses tool use with a focus on learning how to use tools|Might be practical where APIs are prevalent, like in software development or data analysis|
|**ReST meets ReAct**|Adds a layer of self-improvement (through a reward model and reinforcement learning) to ReAct, making the agent design more adaptive.|Focuses on iterative reasoning and self-training|Indirect tool use similar to ReAct|Suitable for tasks that require adaptation to new contexts throught self-improvement|
|**Chain of Tools**|Requires an agent capable of recognizing when and how to use different tools in sequence.|Similar to Toolformer but incorporates multi-tool selection in its learning and reasoning process|Directly addresses tool use with a focus on orchestration|Similar to Toolformer, but might be limited by the number of tools available.|
|**LATS**|Uses a tree search structure, suggesting a more complex agent design for exploring multiple solution paths.|Explores multiple reasoning pathways|Not directly related to Tool use|Scalability is a challenge for LATS due to higher computational complexity.|


