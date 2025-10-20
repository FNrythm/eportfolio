# Unit 6 Activity: Agent Dialogue with KQML and KIF

## Activity Overview

This activity demonstrates agent-to-agent communication using KQML (Knowledge Query and Manipulation Language) and KIF (Knowledge Interchange Format).

**Scenario:** Alice (procurement agent) queries Bob (warehouse stock control agent) about 50-inch television inventory and specifications.

---

## Dialogue Implementation

### Message 1: Alice Queries Bob About Stock Availability

**Alice → Bob: Check if 50-inch TVs are in stock**

```kqml
(ask-if
  :sender Alice
  :receiver Bob
  :content (exists ?tv
              (and (television ?tv)
                   (screen-size ?tv 50)
                   (in-stock ?tv)))
  :language KIF
  :ontology warehouse-inventory
  :reply-with query-001)
```

**Explanation:**
- Alice uses `ask-if` to query whether a statement is true
- The content is a KIF expression asking if there exists a television (`?tv`) with a 50-inch screen that is in stock
- `exists ?tv` - quantifier indicating "there exists a television"
- `and` - logical conjunction of multiple conditions
- Reply identifier allows Alice to match responses to queries

---

### Message 2: Bob's Response - TVs Are Available

**Bob → Alice: Confirm stock availability**

```kqml
(reply
  :sender Bob
  :receiver Alice
  :content (exists ?tv
              (and (television ?tv)
                   (screen-size ?tv 50)
                   (in-stock ?tv)
                   (stock-quantity ?tv 45)))
  :language KIF
  :ontology warehouse-inventory
  :in-reply-to query-001
  :reply-with response-001)
```

**Explanation:**
- Bob responds with `reply` performative
- Confirms that 50-inch TVs are in stock
- Adds additional information: quantity available (45 units)
- `in-reply-to` links this response to Alice's original query

---

### Message 3: Alice Queries About HDMI Slots

**Alice → Bob: Request information about HDMI specifications**

```kqml
(ask-all
  :sender Alice
  :receiver Bob
  :content (and (television ?tv)
                (screen-size ?tv 50)
                (in-stock ?tv)
                (hdmi-slots ?tv ?slots))
  :language KIF
  :ontology warehouse-inventory
  :reply-with query-002)
```

**Explanation:**
- Alice uses `ask-all` to retrieve all matching answers
- Queries for the number of HDMI slots (`?slots`) on 50-inch TVs that are in stock
- Variables `?tv` and `?slots` will be bound to actual values in the response
- `ask-all` is appropriate when multiple products might have different specifications

---

### Message 4: Bob's Response - HDMI Information

**Bob → Alice: Provide HDMI slot information for all matching TVs**

```kqml
(reply
  :sender Bob
  :receiver Alice
  :content (
    (and (television tv-model-sony-x90j)
         (screen-size tv-model-sony-x90j 50)
         (in-stock tv-model-sony-x90j)
         (hdmi-slots tv-model-sony-x90j 4)
         (hdmi-version tv-model-sony-x90j "HDMI 2.1")
         (stock-quantity tv-model-sony-x90j 25))
    (and (television tv-model-samsung-qn50)
         (screen-size tv-model-samsung-qn50 50)
         (in-stock tv-model-samsung-qn50)
         (hdmi-slots tv-model-samsung-qn50 3)
         (hdmi-version tv-model-samsung-qn50 "HDMI 2.0")
         (stock-quantity tv-model-samsung-qn50 20)))
  :language KIF
  :ontology warehouse-inventory
  :in-reply-to query-002
  :reply-with response-002)
```

**Explanation:**
- Bob provides detailed information for all 50-inch TVs in stock
- Two models are available with different specifications:
  - Sony X90J: 4 HDMI slots (HDMI 2.1), 25 units
  - Samsung QN50: 3 HDMI slots (HDMI 2.0), 20 units
- Additional information provided: HDMI version and exact quantities
- This allows Alice to make an informed procurement decision

---

### Message 5: Alice Requests Specific Model Details

**Alice → Bob: Query specific model for more details**

```kqml
(ask-one
  :sender Alice
  :receiver Bob
  :content (and (television tv-model-sony-x90j)
                (price tv-model-sony-x90j ?price)
                (warranty tv-model-sony-x90j ?warranty))
  :language KIF
  :ontology warehouse-inventory
  :reply-with query-003)
```

**Explanation:**
- Alice uses `ask-one` to request a single answer
- Queries for price and warranty information for the Sony model
- This demonstrates follow-up queries based on previous responses

---

### Message 6: Bob's Final Response

**Bob → Alice: Provide pricing and warranty information**

```kqml
(reply
  :sender Bob
  :receiver Alice
  :content (and (television tv-model-sony-x90j)
                (price tv-model-sony-x90j 799.99)
                (currency price-usd)
                (warranty tv-model-sony-x90j 24)
                (warranty-unit months))
  :language KIF
  :ontology warehouse-inventory
  :in-reply-to query-003
  :reply-with response-003)
```

**Explanation:**
- Bob provides pricing ($799.99 USD) and warranty (24 months) information
- Alice now has complete information to make procurement decision

---

## Complete Dialogue Sequence

### Visual Flow Diagram

```
Alice                                                Bob
  |                                                   |
  |-----(1) ask-if: 50" TVs in stock?--------------->|
  |                                                   |
  |<----(2) reply: Yes, 45 units available-----------|
  |                                                   |
  |-----(3) ask-all: HDMI slots info?--------------->|
  |                                                   |
  |<----(4) reply: Sony (4 HDMI), Samsung (3 HDMI)---|
  |                                                   |
  |-----(5) ask-one: Sony price & warranty?--------->|
  |                                                   |
  |<----(6) reply: $799.99, 24-month warranty--------|
  |                                                   |
```

---

**Activity Completed:** October 2024  
**Added to E-Portfolio:** October 2024

