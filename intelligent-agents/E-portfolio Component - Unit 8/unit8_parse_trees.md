# Unit 8 Activity: Constituency-Based Parse Trees

## Activity Overview

This activity demonstrates the application of constituency-based parsing to natural language sentences. Constituency parsing breaks down sentences into nested constituents (phrases) based on their syntactic structure, which is fundamental to natural language understanding in intelligent agent systems.

---

## Parse Tree 1: "The government raised interest rates."

### Tree Structure

```
                    S
         ___________|___________
        |                       VP
        |            ___________|___________
        NP          |           |           NP
    ____|____       |           |       ____|____
   DT        N      V          N       N         N
   |         |      |          |       |         |
  The   government raised   interest rates      .
```

### Breakdown

- **S (Sentence)**: The root of the parse tree
- **NP (Noun Phrase)**: "The government"
  - **DT (Determiner)**: "The"
  - **N (Noun)**: "government"
- **VP (Verb Phrase)**: "raised interest rates"
  - **V (Verb)**: "raised"
  - **NP (Noun Phrase)**: "interest rates"
    - **N (Noun)**: "interest"
    - **N (Noun)**: "rates"

### Analysis

This is a straightforward sentence with a simple Subject-Verb-Object (SVO) structure. The verb phrase contains a transitive verb "raised" followed by its direct object, the noun phrase "interest rates," which is a compound noun.

---

## Parse Tree 2: "The internet gives everyone a voice."

### Tree Structure

```
                         S
         ________________|________________
        |                                 VP
        |                  _______________|_______________
        NP                |               |               NP
    ____|____             |               NP          ____|____
   DT        N            V           ____|____      DT       N
   |         |            |           |         |     |       |
  The     internet      gives     everyone     .     a     voice
```

### Breakdown

- **S (Sentence)**: The root of the parse tree
- **NP (Noun Phrase)**: "The internet"
  - **DT (Determiner)**: "The"
  - **N (Noun)**: "internet"
- **VP (Verb Phrase)**: "gives everyone a voice"
  - **V (Verb)**: "gives"
  - **NP (Noun Phrase)**: "everyone" (indirect object)
    - **N (Pronoun/Noun)**: "everyone"
  - **NP (Noun Phrase)**: "a voice" (direct object)
    - **DT (Determiner)**: "a"
    - **N (Noun)**: "voice"

### Analysis

This sentence follows a ditransitive verb structure (Subject-Verb-Indirect Object-Direct Object). The verb "gives" takes two objects: the indirect object "everyone" and the direct object "a voice."

---

## Parse Tree 3: "The man saw the dog with the telescope."

### Tree Structure (Ambiguous - Interpretation 1: PP attaches to VP)

```
                              S
         _____________________|_____________________
        |                                           VP
        |                      _____________________|_____________________
        NP                    |                     |                     PP
    ____|____                 |                     NP              ______|______
   DT        N                V                 ____|____          |            NP
   |         |                |                |         |         |        ____|____
  The       man              saw              DT        N         P       DT        N
                                              |         |         |       |         |
                                             the       dog      with     the    telescope
```

**Meaning**: The man used the telescope to see the dog.

### Tree Structure (Ambiguous - Interpretation 2: PP attaches to NP)

```
                              S
         _____________________|_____________________
        |                                           VP
        |                      _____________________|___
        NP                    |                         NP
    ____|____                 |          _______________|_______________
   DT        N                V         |                               PP
   |         |                |         NP                        ______|______
  The       man              saw    ____|____                    |            NP
                                   |         |                   |        ____|____
                                  DT        N                    P       DT        N
                                  |         |                    |       |         |
                                 the       dog                 with     the    telescope
```

**Meaning**: The man saw the dog that had/was holding the telescope.

### Analysis

This sentence demonstrates **structural ambiguity** in natural language processing. The prepositional phrase "with the telescope" can attach to either:

1. **VP (Verb Phrase) Attachment**: The telescope is the instrument used by the man for seeing (he used the telescope to see the dog).
2. **NP (Noun Phrase) Attachment**: The telescope is associated with the dog (the dog has or is holding the telescope).

Both interpretations are grammatically valid, and disambiguation requires:
- **Semantic knowledge**: Understanding the likelihood of each scenario
- **Contextual information**: Previous sentences or world knowledge
- **Pragmatic reasoning**: What makes sense in the given situation

This ambiguity is a classic example in computational linguistics and highlights the challenges intelligent agents face in natural language understanding.


