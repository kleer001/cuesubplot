# cuesubplot
Branching ai prompts and results procedurally.

Thank you for joining the alpha release. I apologize for the roughness of the program. 

Hopefully it will provide some entertainment, if not other value as we explore what LLMs can bring us. 


## WORK AROUNDS:

## COMMON PROBLEMS: 

**Q:** Why isn't my LLM responding? 

**A:** Please double check that it's properly serving up API goodness. 
The settings.cfg file contains multiple popular local LLMs and their API end points. 
The findLLM.py uses that list to quickly search your system for a recognizable local LLM.
If you run 'python3 findLLM' and it can't find anything then we need to turn on your local LLM.

**Q**: My LLM is recognized. Why am I not getting output from cuesubplot? 

**A:** It might be that your local LLM hasn't loaded a model to working with.
Please make sure that you have loaded up a model file that we can send a request to. 



## CREDITS: 

stopwords.data file from: 
https://countwordsfree.com/stopwords

## Inspirations

Allison Parrish 

Kate Compton

Kurt Schwitters
