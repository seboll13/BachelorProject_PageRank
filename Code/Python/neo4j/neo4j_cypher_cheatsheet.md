# Neo4j Tutorial

## Fundamentals

Store any kind of data using the following graph concepts:

* **Node**: Graph data records
* **Relationship**: Connect nodes (has direction and a type)
* **Property**: Stores data in key-value pair in nodes and relationships
* **Label**: Groups nodes and relationships (optional)

---

## Browser editor

### CLI

Examples: `:help` `:clear`

---

# Cypher

## Match

### Match node

```cypher
MATCH (ee:Person)
WHERE ee.name = "Emil"
RETURN ee;
```

* **MATCH** clause to specify a pattern of nodes and relationships
* **(ee:Person)** a single node pattern with label 'Person' which will assign matches to the variable `ee`
* **WHERE** clause to constrain the results
* **ee.name = "Emil"** compares name property to the value "Emil"
* **RETURN** clause used to request particular results

Gets gets the id<5> and id<0> nodes and creates a `:KNOWS` relationship between them

### Match nodes and relationships

```cypher
MATCH (ee:Person)-[:KNOWS]-(friends)
WHERE ee.name = "Emil"
RETURN ee, friends
```

* **MATCH** clause to describe the pattern from known Nodes to found Nodes
* **(ee)** starts the pattern with a Person (qualified by WHERE)
* **-[:KNOWS]-** matches "KNOWS" relationships (in either direction)
* **(friends)** will be bound to Emil's friends

### Match labels

```cypher
MATCH (n:Person)
RETURN n
```

or

```cypher
MATCH (n)
WHERE n:Person
RETURN n
```

### Match multiple labels

`:Car` **OR** `:Person` labels

```cypher
MATCH (n)
WHERE n:Person OR n:Car
RETURN n
```

`:Car` **AND** `:Person` labels

```cypher
MATCH (n)
WHERE n:Person:Car
RETURN n
```

### Match same properties

```cypher
MATCH (a:Person)
WHERE a.from = "Sweden"
RETURN a
```

Returns every node (and their relationships) where there's a property `from` with "Sweden" value

### Match friends of friends with same hobbies

Johan is learning surfing, and wants to know any friend of his friends who already knows surfing

```cypher
MATCH (js:Person)-[:KNOWS]-()-[:KNOWS]-(surfer)
WHERE js.name = "Johan" AND surfer.hobby = "surfing"
RETURN DISTINCT surfer
```

* **()** empty parenthesis to ignore these nodes
* **DISTINCT** because more than one path will match the pattern
* **surfer** will contain Allison, a friend of a friend who surfs

### Match by ID

Every node and relationship has an internal autonumeric ID, which can be queried using **<**, **<=**, **=**, **=>**, **<>** and **IN** operators:

**Search node by ID**

```cypher
MATCH (n)
WHERE id(n) = 0
RETURN n
```

**Search multiple nodes by ID**

```cypher
MATCH (n)
WHERE id(n) IN [1, 2, 3]
RETURN n
```

**Search relationship by ID**

```cypher
MATCH ()-[n]-()
WHERE id(n) = 0
RETURN n
```

---

## Create

### Create node

```cypher
CREATE (ee:Person { name: "Emil", from: "Sweden", klout: 99 })
```

* **CREATE** clause to create data
* **()** parenthesis to indicate a node
* **ee:Person** a variable `ee` and label `Person` for the new node
* **{}** brackets to add properties (key-value pairs) to the node

### Create nodes and relationships

```cypher
MATCH (ee:Person) WHERE ee.name = "Emil"
CREATE (js:Person { name: "Johan", from: "Sweden", learn: "surfing" }),
(ir:Person { name: "Ian", from: "England", title: "author" }),
(rvb:Person { name: "Rik", from: "Belgium", pet: "Orval" }),
(ally:Person { name: "Allison", from: "California", hobby: "surfing" }),
(ee)-[:KNOWS {since: 2001}]->(js),(ee)-[:KNOWS {rating: 5}]->(ir),
(js)-[:KNOWS]->(ir),(js)-[:KNOWS]->(rvb),
(ir)-[:KNOWS]->(js),(ir)-[:KNOWS]->(ally),
(rvb)-[:KNOWS]->(ally)
```

* **MATCH** clause to get "Emil" in `ee` variable
* **CREATE** clause to create multiple nodes (comma separated) with their labels and properties. Also creates directed relationships `(a)-[:Label {key: value}]->(b)`

### Create relationship between 2 unrelated nodes

```cypher
MATCH (n), (m)
WHERE n.name = "Allison" AND m.name = "Emil"
CREATE (n)-[:KNOWS]->(m)
```

Alternative with `MERGE`, which ensures that the relationship is created only **once**

```cypher
MATCH (n:User {name: "Allison"}), (m:User {name: "Emil"})
MERGE (n)-[:KNOWS]->(m)
```

### Create node with multiple labels

```cypher
CREATE (n:Actor:Director)
```

---

## Update

### Update node properties (add new or modify)

Add new `.owns` property or modify (if exists)

```cypher
MATCH (n)
WHERE n.name = "Rik"
SET n.owns = "Audi"
```

### Replace all node properties for the new ones

**Danger**: It will delete all previous properties and create `.plays` and `.age` properties

```cypher
MATCH (n)
WHERE n.name = "Rik"
SET n = {plays: "Piano", age: 23}
```

### Add new node properties without deleting old ones

**Danger**: If `.plays` or `.age` properties are already set, it will overwrite them

```cypher
MATCH (n)
WHERE n.name = "Rik"
SET n += {plays: "Piano", age: 23}
```

### Add new node property if property not already set

```cypher
MATCH (n)
WHERE n.plays = "Guitar" AND NOT (EXISTS (n.likes))
SET n.likes = "Movies"
```

### Rename a property in all nodes

```cypher
MATCH (n)
WHERE NOT (EXISTS (n.instrument))
SET n.instrument = n.plays
REMOVE n.plays
```

Alternative

```cypher
MATCH (n)
WHERE n.instrument is null
SET n.instrument = n.plays
REMOVE n.plays
```

### Add label to existing node

Adds the `:Food` label to nodes id<7> and id<8>

```cypher
MATCH (n)
WHERE id(n) IN [7, 8]
SET n:Food
```

### Creates the node if not exists and updates (or creates) a property

```cypher
MERGE (n:Person {name: "Rik"})
SET n.owns = "Audi"
```

---

## Delete

### Delete nodes

To **delete a node** (p.e. id<5>), first we need to **delete its relationships**. Then, the node can be deleted

```cypher
MATCH (n)-[r]-()
WHERE id(n) = 5
DELETE r, n
```

To **delete multiple nodes** (must have their relationships previously deleted)

```cypher
MATCH (n)
WHERE id(n) IN [1, 2, 3]
DELETE n
```


### Deletes a property in a specific node

```cypher
MATCH (n)
WHERE n:Person AND n.name = "Rik" AND n.plays is NOT null
REMOVE n.plays
```

Alternative

```cypher
MATCH (n)
WHERE n:Person AND n.name = "Rik" AND EXISTS (n.plays)
REMOVE n.plays
```


### Delete a label from all nodes

Deletes the `:Person` label from **all** nodes

```cypher
MATCH (n)
REMOVE n:Person
```

### Delete a label from nodes with specific labels

Deletes the `:Person` label from nodes with `:Food` and `:Person` labels

```cypher
MATCH (n)
WHERE n:Food:Person
REMOVE n:Person
```

### Delete multiple labels from nodes

Deletes the `:Food` and `:Person` labels from nodes which have **both** labels

```cypher
MATCH (n)
WHERE n:Food:Person
REMOVE n:Food:Person
```

**Danger**: Deletes the `:Food` and `:Person` labels from nodes which have `:Food` or `:Person` or `:Food:Person` labels

```cypher
MATCH (n)
REMOVE n:Food:Person
```

### Delete entire database

```cypher
MATCH (n)
OPTIONAL MATCH (n)-[r]-()
DELETE n, r
```

---

## Other clauses

### Show execution plan

Use `PROFILE` or `EXPLAIN` before the query

`PROFILE`: Shows the execution plan, query information and **db hits**. Example: Cypher version: CYPHER 3.0, planner: COST, runtime: INTERPRETED. 84 total db hits in 32 ms.

`EXPLAIN`: Shows the execution plan and query information. Example: Cypher version: CYPHER 3.0, planner: COST, runtime: INTERPRETED.

### Count

Count all nodes

```cypher
MATCH (n)
RETURN count(n)
```

Count all relationships

```cypher
MATCH ()-->()
RETURN count(*);
```

### Limit

Returns up to 2 nodes (and their relationships) where there's a property `from` with "Sweden" value

```cypher
MATCH (a:Person)
WHERE a.from = "Sweden"
RETURN a
LIMIT 2
```

### Create unique property constraint

Make `.name` property unique on nodes with `:Person` label

```cypher
CREATE CONSTRAINT ON (n:Person)
ASSERT n.name IS UNIQUE
```

### Drop unique property constraint

Make `.name` property unique on nodes with `:Person` label

```cypher
DROP CONSTRAINT ON (n:Person)
ASSERT n.name IS UNIQUE
```
