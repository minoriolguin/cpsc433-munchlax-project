
# CPSC 433 - Artificial Intelligence - Fall 2024

## And-Tree AI Search Model for Scheduling Problem

This repository contains the implementation of an **And-Tree AI Search Model** designed to solve complex scheduling problems. The project was developed as part of the **CPSC 433: Artificial Intelligence** course at the University of Calgary, Fall 2024.

---

## Overview

The model tackles the scheduling of events such as games and practices, ensuring that both hard and soft constraints are satisfied. The problem involves assigning events to time slots while adhering to rules such as compatibility, capacity limits, and priority requirements.

---

## Key Features

- **And-Tree Search Framework**: Efficiently explores possible schedules using a recursive, depth-first search approach.
- **Constraint Handling**:
  - **Hard Constraints**: Ensures that schedules are feasible (e.g., avoiding slot conflicts, respecting capacity limits, and satisfying minimum requirements).
  - **Soft Constraints**: Optimizes schedules for preferences like slot usage and event spreading.
- **Slot Prioritization**: Implements heuristics to prioritize high-value slots, such as evening availability for certain divisions.
- **Interrupt Handling**: Safely exits and prints the best partial schedule if interrupted (e.g., via `Ctrl+C`).

---

## How It Works

1. **Input Parsing**: The program reads the scheduling data, including events, slots, and constraints, from a file.
2. **Tree Construction**: Builds an And-Tree structure to explore possible schedules, checking constraints at each level.
3. **Evaluation**: Scores schedules based on penalties for unmet constraints and preferences.
4. **Output**: Prints the best schedule found and its evaluation score.

---

## Usage

Run the program with the input file and desired constraints:

```bash
python3 main.py <input_file> 1 1 1 1 1 1 1 1
```

 <p>
  The numbers following the input file are in the following order:
  wminfilled wpref wpair wsecdiff pengamemin penpracticemin pennotpaired pensection 
 </p>

 Due to the random aspect of the program, to ensure that the program arrives at a complete solution, run for 10 seconds, if the prgram arrives at no complete solutions, terminate and retry until it arrives at complete


---
  
## Contributors
- Aditi Yadav
- Jaden Myers
- Minori Olguin
- Monica Nguyen
- Thi Ngoc Anh Nguyen
