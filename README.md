# cuesubplot
Branching ai prompts and results procedurally.

Thank you for joining the alpha release. I apologize for the roughness of the program. 

Hopefully it will provide some entertainment, if not other value as we explore what LLMs can bring us. 

## HOW-TO Start

#1 Make sure you have git installed. 

<code> https://github.com/git-guides/install-git </code>

#2 Copy the repo

<code>  </code>

## GUI WALK THROUGH

* 1 - At ***Role*** enter a role you want the LLM to take, a perspective, personality. 
This will be added as a prefix mini-prompt (forthwith to be known as a **cue**) to the rest of the prompts you'll create. 
* 2 - At ***List generation*** enter the list you would like to generate. For best results use the phrasing something like
**"give me an ordered list of ..."**

*I've done my best to be able to handle many types of list formats than an LLM can generate. 
But they can be very clever and create an edge case I hadn't anticipated. In that case feel free to hit submit again and wish for the best.*

* 3 - Hit the ***Submit*** button to generate your list. 

* 4 - At ***Riff on the list*** enter a prompt to process items you've created. I purposefully didn't create a 'Riff on all the items' because LLMs can be a little unpredictable and prompt creation is an art that requires iteration, sometimes.

* 5 - Once you're happy with your 3rd cue (your Riffing promptlet) feel free to process the rest of your items.

![Tab 1, The Stage](/images/Stage_01.png "Tabe 1, The Stage")

![Tab 2, The Library](/images/Library_01.png "Tab 2, The Library")

![Tab 3, The Settings](/images/Settings_01.png "Tab 3, the Settings")


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

jonathanmast
