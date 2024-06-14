```Mermaid
flowchart TD
    A[Sudoku] -->  B{have a puzzle?}
    B --> |Yes| D[Input puzzle]
    D --> J{Validate puzzle}
    J --> |Invalid|D
    J -->|Valid| F[Display Grid]
    B -->|No| E{difficulty level?}
    E -->G[Easy]
    E -->H[Medium]
    E -->I[Expert]
    G -->F
    H -->F
    I -->F
```
