# cuesubplot
Branching ai prompts and results procedurally.

Thank you for joining the alpha release. I apologize for the roughness of the program. 

Hopefully it will provide some entertainment, if not other value as we explore what LLMs can bring us. 

## HOW-TO Start (manual)

* 1 - Make sure you have git installed. 

<code> https://github.com/git-guides/install-git </code>

* 2 - Copy the repo

<code>  </code>

## HOW-TO Start (automagical)

* 1 - You can quickly setup the project using our setup script:

<code>```bash
curl -sSL https://raw.githubusercontent.com/yourusername/your-repo-name/main/setup.sh | bash</code>

## GUI WALK THROUGH

### THE STAGE

* 1 - At ***Role*** enter a role you want the LLM to take, a perspective, personality. 
This will be added as a prefix mini-prompt (forthwith to be known as a **cue**) to the rest of the prompts you'll create. 
* 2 - At ***List generation*** enter the list you would like to generate. For best results use the phrasing something like
**"give me an ordered list of ..."**

*I've done my best to be able to handle many types of list formats than an LLM can generate. 
But they can be very clever and create an edge case I hadn't anticipated. In that case feel free to hit submit again and wish for the best.*

* 3 - Hit the ***Submit*** button to generate your list. 

* 4 - At ***Riff on the list*** enter a prompt to process items you've created. I purposefully didn't create a 'Riff on all the items' because LLMs can be a little unpredictable and prompt creation is an art that requires iteration, sometimes.

* 5 - Once you're happy with your 3rd cue (your Riffing promptlet) feel free to process the rest of your items. 
I reccomend processing the first one a few times until you're happy, then proceeding to the folling ones.    

![Tab 1, The Stage](/images/Stage_02.png "Tabe 1, The Stage")

### THE LIBRARY

Here we can Save, Load, and clear the Stage. 

**Saving**: The files are named automagically based on your prompts, the date, and time.

**File to Open**: You'll need to select a file to open first. Drop file or Click to upload.

**Opening**: You'll need to select a file to open first. Drop file or Click to upload. After that you can open it.

**Library Status**: Feedback is important in any creative venture. (though this part is non-standard and will likely atrophy in further verseions)

![Tab 2, The Library](/images/Library_02.png "Tab 2, The Library")

### THE SETTINGS

**Settings for XXX** Will be based on the local LLM the program detects that is currently running.
If there are more than one running it will pick the first one it finds. 

* Model: Not all local LLMs let you specify the model through the API. Some require the user to load the model before the api will return a queery.
* Messy: Off by default. Messy on will display all the of the hidden Process Buttons, List Item text boxes, and Riffing Results. Gradio cannot create them on the fly. So, they're hidden until they're needed.
* Maximum number of items: Default of 5. The number of List Items that are created with the interface (hidden by default).
* Max Tokens, Temperature, etc... : Settings based on the API call of your specific LLM


* Update Settings: Will write out your selected settings to a settings.cfg file so that it can be used over on the Stage. 
* Update Status: Again, feedback is important. 

![Tab 3, The Settings](/images/Settings_02.png "Tab 3, the Settings")

### A FULL STAGE

![Tab 1, The Stage](/images/Stage_01.png "Tabe 1, The Stage")

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

Rick Rubin

Jonathan Mast