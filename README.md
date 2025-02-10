# online-shopping-agentic-ai

## Introduction

I recommend that you through this repository in the following order:
1. A Little Philosophy
    - [A thought experiment](./a_little_philosophy/a_thought_experiment.md)
    - [My Intuition of agentic AI](./a_little_philosophy/my_intuition_of_agentic_ai.md)

2. Non Coding Components
    - [Conceptual Map](./non_coding_components/1_conceptual_map.md)
    - [Analysis](./non_coding_components/2_analysis.md)
    - [Open Questions and Research Directions](./non_coding_components/3_open_questions_and_research_directions.md)

3. Coding Components
    - [system_prompt.py](./coding_components/system_prompt.py)
    - [tools.py](./coding_components/tools.py)
    - [agent.py](./coding_components/agent.py)
    - [app.py](./coding_components/app.py) (Optional)


I have provided a Dockerfile so that you can seamlessly launch an interactive app.

1. Build a docker image
    ```docker
    docker build -t agentic-ai .
    ```

2. Run a container
    ```
    docker run -it --rm -v $(pwd):/workspace -p 8501:8501 --name agentic_container agentic-ai
    ```

## Contact
- Name: Shreyas D Bangera
- Email: shreyasdb99@gmail.com 

## References

- **ReAct: Synergizing Reasoning and Acting in Language Models**  
  Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao  
  *arXiv:2210.03629*, 2022  
  [Link](https://arxiv.org/abs/2210.03629)

- **Toolformer: Language Models Can Teach Themselves to Use Tools**  
  Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, Thomas Scialom  
  *arXiv:2302.04761*, 2023  
  [Link](https://arxiv.org/abs/2302.04761)

- **ReST meets ReAct: Self-Improvement for Multi-Step Reasoning LLM Agent**  
  Renat Aksitov, Sobhan Miryoosefi, Zonglin Li, Daliang Li, Sheila Babayan, Kavya Kopparapu, Zachary Fisher, Ruiqi Guo, Sushant Prakash, Pranesh Srinivasan, Manzil Zaheer, Felix Yu, Sanjiv Kumar  
  *arXiv:2312.10003*, 2023  
  [Link](https://arxiv.org/abs/2312.10003)

- **Chain of Tools: Large Language Model is an Automatic Multi-tool Learner**  
  Zhengliang Shi, Shen Gao, Xiuyi Chen, Yue Feng, Lingyong Yan, Haibo Shi, Dawei Yin, Zhumin Chen, Suzan Verberne, Zhaochun Ren 
  *arXiv:2405.16533*, 2023  
  [Link](https://arxiv.org/abs/2405.16533)

- **Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models**  
  Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, Yu-Xiong Wang 
  *arXiv:2310.04406*, 2023  
  [Link](https://arxiv.org/abs/2310.04406)