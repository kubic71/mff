## Cisco
- handles 30% of world internet traffic
- 250 billion $ market cap

## Cisco Cognitive intelligence
- division founded in 2013 when Cisco acquired COSE (25 employees)
- team in Prague - 100 researchers, engineers, data scientists

### Security
- focus on data (leaking)
	- analysis of network traffic
- security is not only end the security of end devices
- Cisco has many product covering all aspects of computer security
	- can integrate insights from its suite of products
- **ML in the Cloud applied to the Edge**
	- models run in cloud
	
	
### Incident detection pipeline
- automatic detection of IoCs (Indicator of Compromise)
- focus on **false positives**
- raw data -> Layer 1 -> anomalies -> Layer 2 -> threats -> Layers 3 -> campaigns
- AI^2 loop, external data-sources
- Layer 1 
	- Anomaly detection
		- simple ML, rule-based
	- Trust modeling
- Layer 2
	- Event classification
	- Entity modeling
- Layer 3
	- relationship modeling
	

### Attack vectors
- email - user clicks on some link
- USB drives - candy drop

### Malware life-cycle
- many life-stages
- what Cisco can detect - network perimeter
	- reconaissance
	- initial access
	- command and control
	- exfiltration
- now they added 
	- network-lateral - analytics inside LAN
	- endpoint - mobile, laptops
	
### Email detection (example)
- sender reputation
- sender location
- text recognition & analysis
- image recognition


### Framework scheme
- input modalities (multiple) -> Unimodal detectors (multiple) -> Entity matching (multiple) ->  Multi-modal detector (integrates signals from detectors)  -> Threat detection
- multiple weak signals
	- raw ip address access
	- large upload
	- connections to China


### Types of detectors

#### Signature/targeted based
- simple table matching, decision trees

#### Classifier-based
- supervised classifier trained on historical data

#### Anomaly-based
- anomaly detection engine combining 200 individual detectors

#### Contextual detector
- describes various potentially problematic or suspicious network behaviours 

### Targeted detectors
- histogram-based
- sigma-distance
	- network  - SMB burst, LDAP burst
	- endpoint - cmd burst
- parent-child process discrepancy detector
	- Word scanning network
	- Excel downloading something from network
	
### Entity matching
- how to combine multiple sources, detectors?
- identifying 


### FP-growth
- automatic behavior pattern recognition
- trained on known malware behaviours

### OSX/Shlayer


### Kevin Meetnik
- famous, convicted hacker
- read his book

### Fancy thing
- Dynamic entity representation - changing representation over time
	
### Open/Closed source?
- mostly closed-source, but their RnD publish papers
- [Fast distributed random forests](https://github.com/cisco/oraf)

	
## Questions
- do they have hardware optimized for fast anomaly detection? (as in CERN)
	- they usually send only analytics, telemetry
	- thin clients
- detectors run on LAN, or where do they collect the raw data?
