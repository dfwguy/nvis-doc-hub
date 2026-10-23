### AI Software Factory

The goal is to pull us out of the review loop. An ideal workflow would look like: we message a chat bot with what a feature request should do → agent implements it all on its own, running integration tests and creating a whole MR workflow.

Things to look out for and research how to improve:

* AI often starts overanalyziing when it is responsible for checking itself  
  * Sometimes it will underanalyze itself as well  
* LLM context has a recency bias.LLMs tend to get caught in the most recent context and forget everything that came before, which is how they get trapped in loops and keep iterating.   
  * One way to overcome this is to force the LLM to have a memory of everything it’s done and keep checklists  
  * Need to complete the next item on the checklist  
  * If the checklist gets too big → context is too big → next token prediction is recency bias  
  * Instead of having one checklist/one context, spawn agents that have 1 job. These agents can be luna/haiku – cheaper models.  
    * Then, Sol can have an agent that looks at the overall code quality.  
    * Will have to compromise on how to set up agents so that Sol is not too strict but that we are still checking the luna/haiku agents well enough.  
* Research imperative, functional program, procedural programming paradigms  
* What linters/mechanical tests can we add to make sure the code is understandable

Things to implement in the next AI Software Factory 

* TDD red/green workflow (TDD=test driven development)  
  * Red → labels functions  
  * Green → rewrites passing stuff; writes code that makes the tests pass  
  * Test-driven development refers to development where we focus on writing tests first. This process is owned by separate agents (red vs green)  
  * We will have to figure out how to do TDD red/green in large projects where there’s not 100% test coverage  
* We want everything to be single purpose functions  
* Functions should also be parameterized (decorators) so that we have consistent inputs/outputs  
* Figure out Bryan’s coding standards  
  * Look at the code it produces → figure out what makes sense for maintainable code  
  * Figure out what can be salvaged from the copier repo  
* Make sure we still have diataxis in the repo  
* Code stuff/docs should be kept in function docstrings  
* Architect \+ candidate architects  
  * 2 haiku agents take a stab at architecting  
  * TDD red should name functions  
  * Is there anything in the luna/haiku agents that we need to merge into the main repo → find the simplest way to do things

What to keep from Agentic Copier Repo

* [code-quality.md](http://code-quality.md)   
  * Go through each of these concepts; prompt your agent for an example of what this looks like, then decide if you want to keep it or not.  
* docs/agentic workflow diagram  
  * Keep the structure of the architect, 3 proposals, TDD red/green  
  * This describes how the copier repo works  
* [Readme.md](http://Readme.md)   
* docs/explanation/agentic\_workflow  
* Ask your agent what are best practices worth saving from the agentic copier repo  
* 