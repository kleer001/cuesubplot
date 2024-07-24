<div align="center">
<img src="/images/masks_base_banner_01.png" alt="Logo">
</div>

# **cuesubplot:** *A web interface for procedurally branching results from three promptlets*

# <code>*Craft complex stories, simply, reliably*</code>

# :speech_balloon: What? 
Cuesubplot is a hardcoded (sadly not generalized yet) network for creating branching results **reliably** from a local LLM.

# :bulb: Why? 

Over a several months I became increasing frustrated with the inability of the current crop of free online LLMs to manage generating very long and complicated multistep outputs, such as a 12-week program to learn a new skill like salesmanship or to generate a critique a famous song, line by line, from multiple angles. 

I used copy and paste to some success, but found that the LLM would get distracted and the quality would nose dive. Not to mention that it felt wrong to manually copy-paste as part of a workflow.

Then (thanks to wise words from Jonathan Mast) I set out to manually program a solution. 

Through [Automatic1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui) I'd been introduced to the gui package *[Gradio](https://www.gradio.app/)*. And by the silicone grace of Nvidia blessed with multiple free online LLMs that could, with some deft work, generate code. Big up and thanks to the massive big brains over at [ChatGPT](https://chatgpt.com/) , [Perplexity](https://www.perplexity.ai/) , and [Claude](https://claude.ai/) . Kind of ironic that this project excludes them (for the moment).

*Additionally, I wanted to join the local LLM evolution and contribute to the community of programmers and users that loving doing what I loved to do to, generate text and push what these LLMs could do.*

# :zap: How 
> [!TIP]
> ## **1** - Set a ***role***
> ## **2** - Create a ***list***
> ## **3** - Elaborate (or "***riff***") on the list
 

# :sparkles: Start (manual) 
* 1 - Make sure you have git installed.  
<code> https://github.com/git-guides/install-git </code>
* 2 - Copy the repo  
<code>git clone https://github.com/kleer001/cuesubplot ; cd cuesubplot
</code>
* 3 - load the dependencies (local venv?) 
* 4 - Run the program  
<code> python3 stage.py</code>

## :package: Currently supported LLMS platforms 
*in  settings.cfg*  

| LLM Platform | URL             | Endpoint             |
|--------------|-----------------|----------------------|
| [Ollama](https://ollama.ai/)       | localhost:11434 | /api/generate        |
| [LM Studio](https://lmstudio.ai/)    | localhost:1234  | /v1/chat/completions |
| [GPT4All](https://gpt4all.io/)      | localhost:4891  | /v1/completions      |
| [LocalAI](https://localai.io/)      | localhost:8080  | /v1/chat/completions |
| [llama.cpp](https://github.com/ggerganov/llama.cpp)    | localhost:8080  | /completion          |
| [oobabooga](https://github.com/oobabooga/text-generation-webui)    | localhost:5000  | /v1/chat/completions |

* Please suggest more free local LLMs if you like. And feel free to change your local settings.cfg to fit your own purposes. The structure should be self evident from the examples in it.  
* Support for Chat-GPT, Perplexity, Claude, and other paid platforms is imminent, though not guaranteed. 

## :walking: GUI WALK THROUGH 
### :eyes: THE STAGE 
* 1 - At ***Role*** enter a role you want the LLM to take, a perspective, personality.   
This will be added as a prefix mini-prompt (forthwith to be known as a **cue**) to the rest of the prompts you'll create.   
* 2 - At ***List generation*** enter the list you would like to generate. For best results use the phrasing something like
**"give me an ordered list of ..."**  

*I've done my best to be able to handle many types of list formats than an LLM can generate. 
But they can be very clever and create an edge case I hadn't anticipated. In that case feel free to hit submit again and wish for the best.*  
* 3 - Hit the ***Submit*** button to generate your list.   
* 4 - At ***Riff on the list*** enter a prompt to process items you've created. I purposefully didn't create a 'Riff on all the items' because LLMs can be a little unpredictable and prompt creation is an art that requires iteration, sometimes.    
* 5 - Once you're happy with your 3rd cue (your Riffing promptlet) feel free to process the rest of your items.  
I recommend processing the first one a few times until you're happy, then proceeding to the fallowing ones.    

![Tab 1, The Stage](/images/Stage_02.png "Tab 1, The Stage")

### :writing_hand: THE LIBRARY 

Here we can Save, Load, and clear the Stage.   
* **Save Results**: The files are named automagically based on your prompts, the date, and time.  
* **File to Open**: You'll need to select a file to open first. Drop file or Click to upload.  
* **Opening**: You'll need to select a file to open first. Drop file or Click to upload. After that you can open it.  
* **Library Status**: Feedback is important in any creative venture. (though this part is non-standard and will likely atrophy in further versions)

![Tab 2, The Library](/images/Library_02.png "Tab 2, The Library")

### :brain: THE SETTINGS 
**Settings for XXX** Will be based on the local LLM the program detects that is currently running.  
If there are more than one running it will pick the first one it finds.   
* Model: Not all local LLMs let you specify the model through the API. Some require the user to load the model before the api will return a query.  
* Messy: Off by default. Messy on will display all the of the hidden Process Buttons, List Item text boxes, and Riffing Results. Gradio cannot create them on the fly. So, they're hidden until they're needed.  
* Maximum number of items: Default of 5. The number of List Items that are created with the interface (hidden by default).  
* Max Tokens, Temperature, etc... : Settings based on the API call of your specific LLM  

* Update Settings: Will write out your selected settings to a settings.cfg file so that it can be used over on the Stage.   
* Update Status: Again, feedback is important.   

![Tab 3, The Settings](/images/Settings_02.png "Tab 3, the Settings")

### :performing_arts: A FULL STAGE 

![Tab 1, The Stage](/images/Stage_01.png "Tab 1, The Stage")

### :chart_with_upwards_trend: THE FLOW CHART

This, of course, leaves out important parts, but aims at addressing the important creative process flow.  
Like, there's a lot of work that goes into separating the results of the List cue results into separate list items that can be addressed individually.   
And there's nothing about the LLM settings or the APIs.  

![Program Flow, more or less](/images/flowChart_01.png "Flowchart")

## :bug: COMMON PROBLEMS: 

**Q:** Why isn't my LLM responding?   
**A:** Please double-check that it's properly serving up API goodness.   
The settings.cfg file contains multiple popular local LLMs and their API end points.   
The findLLM.py uses that list to quickly search your system for a recognizable local LLM.  
If you run 'python3 findLLM' and it can't find anything then we need to turn on your local LLM.

**Q:**: My LLM is recognized. Why am I not getting output from cuesubplot?     
**A:** It might be that your local LLM hasn't loaded a model to working with.  
Please make sure that you have loaded up a model file that we can send a request to.   

**Q:** Anything else?  
**A:** We're still in early Alpha release, so, it's probably a bug and should be squashed. Please submit an issue, and we'll put it in the pile to be processed.   

## :wrench: CREDITS: 

stopwords.data file from: 
https://countwordsfree.com/stopwords

## :art: Inspirations 

- [Allison Parrish](https://www.decontextualize.com) (thematically)  
- [Kate Compton](https://github.com/galaxykate) (structurally)  
- [Kurt Schwitters](https://en.wikipedia.org/wiki/Kurt_Schwitters) (graphically)  
- [Rick Rubin](https://en.wikipedia.org/wiki/Rick_Rubin) (musically)  
- [Jonathan Mast](https://jonathanmast.com/) (promptly)  
- [Douglas Hofstadter](https://en.wikipedia.org/wiki/Douglas_Hofstadter) (subconsciously)  

My family, friends, and other loved ones. :heart: 


