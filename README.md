# Python_Classes_Parser

## Output parsed results into csv

```
python parse_classes.py dir1 dir2 dir3
```
##  Visulize the results in Neo4j

#### Download Neo4j

#### Put the output.csv into the Databases' import folder

####  In neo4j, run the following codes

delete existing nodes in the database
```
MATCH (n)
DETACH DELETE n
```
load csv
```
LOAD CSV WITH HEADERS FROM 'file:///output.csv' AS row
WITH row
WHERE row["Class Name"] IS NOT NULL AND  row["Base Class Name"] IS NOT NULL
MERGE (class:Class {name: row["Class Name"]})
MERGE (base:Class {name: row["Base Class Name"]})
CREATE (base)-[:r]->(class)
```
filter the class names
```
MATCH (m:Class) MATCH (n:Class) 
WHERE m.name contains 'Articulation' 
OR  n.name contains 'Articulation' 
OR  m.name contains 'Controller' 
OR  n.name contains 'Controller'  
MATCH (m)-[r]->(n)  
Return m,r,n
```

