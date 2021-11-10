## Data-value Tables



### CQRS
- command and query responsibility segregation
- separate interfaces for R/W operations
	- Reads usually 1000x more frequent than Writes
	- different datastructure for Reads and Writes
	
- **materialized views**
	- denormalized data(bases)
	- optimized for frequent queries


### Access structure
- Account / Table / Partition / Entity / Property

#### Table
- set of rows
- unique id - PartitionKey/RowKey

...

### Partitioning
- operations atomic on a single partition
- operations across partitions slow
- more advanced operations (join, ..) also slow
- data distribution (sharding) managed by data nodes


### Event-sourcing
- design pattern
- append-only store
- add A, add B, delete A, add C => {B, C}
	- doesn't have to modify DB
- useful for shopping cart content representation
- performance, scalability, analytics


### Column stores
- rows - **many many values** (thousands, millions)
- C-Store, Cassandra, MonetDB, HBase
- support for collections
- no support for joins
- sort by row and column - fast access
- **replication**
	- custom level of consistency per-request (sequential, external, eventual)
	
### Document stores
- storage unit
	- XML, JSON, BSON, RDF, CSV
	- DB **understands** the format
- sharding
- journaling
	- append-only, write-ahead redo logs

### Graph DB
- Neo4j, OrientDB, Oracle Sp7 Graph, Virtuoso, GraphX AllegroGraph, Janus Graph
- optimized for storing and more importantly **request** of graph structures
- social networks
	- find friend-of-friends
	- in relation db - sequence of many expensive joins
- in-memory / distributed
- fast subgraph matching, shortest paths, isomorphism, wildcards
- **Entity**
	- nodes
	- properties
	
	
### Binary Large Objects (blob)
- unstructured large (TB) binary data
- combined into replicated BLOB-containers
	- integration with filesystems, persistance
- virtual disk VM
- video, backup - cheap
	- Static Content Hosting
	
- **types**
	- Block Blob
		- sequential reads, fast write appends - streams
	- Page Blob
		- page-oriented
		- random read/write  (seek into middle)
		- larger overhead compared to Block Blob
		
### Business Analytics
- SQL reporting - RDL language


	
### Map/Reduce paradigm
- Distributed Data processing
	- BigData
		- data which cannot fit into single DBMS
- massive paralelization, distributed computation
- data stored on Distrubuted 
- Hadoop (not very good), Spark, MR-MPI
- input data -> Split into shards
- Reduce node - performs computation on 
- intermediate results can be duplicated
- fault-tolerant
- [MapReduce diagram](https://0x0fff.com/wp-content/uploads/2014/12/MapReduce-v3.png)
- example Map/Reduce tasks
	-  **Word frequency on many document** - very simple
	- **Common Friends**
		- map(person, [friends]) -> ([person1, person2], [friends])
		- reduce( [person1, person2], [friends]) -> [person1, person2], [common friends]

#### Map node
- every node independent
- input -> (key, value)

#### Reduce node
- (key, list of values []) -> output
- union of values for each key
- computation, outputs results

#### Master/Slave architecture
- jobtracker - single master server
- takstrackers - slave servers - transfer data between map and reduce

#### Pros
- NoSQL data
- BigData
- batch/offline mode

#### Cons
- small data - large overhead
- inter-node communication & synchronization
- low latency
- transaction-requiring apps


### Hadoop Zoo

#### HDFS
- Hadoop distributed file system
- ~$10^4$ nodes, $10^6$ files, PB dat
- **properties**
	- **fault-tolerant** 
		- failure is not an exception
		- replication, error-detection and recovery
		- optimized for large amount of cheap HW
	- file streams
		- optimizing throughput, not latency
	- write-once, read-many
		- written files are non-modifiable
		
#### Pig (Latin)
- Pig - core runtime
- Pig latin - higher-level imperative language on top of Hadoop
	- up to 50x smaller source-codes
	- but usually slower, cannot express everything
- map/reduce is too low-level
- compilation to MapReduce jobs
- building MapReduce pipelines - MapReduce1 -> MapReduce2 -> MapReduce3

#### Hive, HiveQL
- Hive is runtime, HiveQL the language
- SQL-like query language
- very easy-to-write, very very slow
- useful for fast prototyping


#### Apach Spark
- MapReduce not optimized for iterative operations  
- fast MapReduce pipelines 


#### Presto
- *not only SQL on Hadoop*
- developed by Facebook, 2013 open-sourced
- data connectors / pluggable backends
- top performance 
- pipeline-oriented

#### BigData landscape
- huge
- [diagram](https://46eybw2v1nh52oe80d3bi91u-wpengine.netdna-ssl.com/wp-content/uploads/2020/09/2020-Data-and-AI-Landscape-Matt-Turck-at-FirstMark-v1.pdf)