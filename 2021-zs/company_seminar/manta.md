# SW development process in MANTA
- how to manage project development in a fast-growing environment
- main points today
	- architecture
	- code repository and modularity
		- branching model
	- CI/CD

## Manta
- CZ-US company
- product: 
	- Understand business data and their flow
	- impact analysis
	- migrations
	- compliance
		- audits (GDPR, financial, HIPAA)
		- incident management
- task is very complex
	- 200 000 DB procedures
	- thousands of business processes
	
	
## Code repo and Modularity
- Subversion to Git migration in 2021
	- took 3 people working full-time 9 months (300 MD)
	
### Mono-repo vs multi-repo
- **Conway's law**
	- Organizations design systems that mirror their communication structure
- Manta chose **monorepo**
- repo -> logical components -> modules
	- component uses multiple modules
	- 1000 modules

#### Architectural design perspective
-  **cohesion** -> encapsulation + well-defined functionality (API)
- **reuse** (utilities, platform code)

#### Implementation perspective
- Maven dependency manaagement
- modularity of compilation units = efficient coding and debugging
- test-driven development

#### Practical challenges
- do not postpone integration testing and end2end testing for too long
- deploy modules often to sync with others fast
- dependency hell
	- direct dependency
	- transitional dependency
	- cyclic dependency
	- will the right version propagate into the final assembly?

- **advice**
	- define review process
	- define release strategy right at the beginning

- versioning schema compliant with branching model
- build configuration - consistent and correct


### Git-flow
- **branches**
	- develop
		- feature branches are based  upon develop branch
	- release branch
		- where I test the release before merging with master
	- master
		- hotfix branch 
			- hotfixes merged also with develop branch
			
#### Feature branches
- no fast forward (--no-ff) - creates a merge commit
- kept in sync - rebase (instead of merge) - eliminates crossroads
- squashing of groups of related commits into one
- merge feature branch as Pull-request 
	- allows code-review in merging feature
- **protect integration branches from force-push**
	- integration branch - develop / release branch

## Continuous integration
- motivation: regularly integrate modules to ensure consistency and correctness
- principles
	- pull changes
	- compile
	- test
	- static analysis
	- deploy to nexus
	- trigger downstream jobs
- SonarQube quality gates
	- set of selected quality metrics and thresholds
	- can fail the build
- Jenkins
	- maven jobs in jenkins
		- builds only one folder in the mono-repo
	- bottom-up dependencies
		- upstream module triggers build of down-stream components
		- dependencies in pom.xml
	- Jenkins multibranch pipeline
		- build automatically feature branches

 
 
