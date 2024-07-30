First, run "npm install" to get all the dependencies
listed in the project's description (package.json).

Then, you can run the backend and frontend using VSCode.
You can even debug your client-code (inside the HTML) and server!


# Tennis ATP Matches Statistics

## Overview
This project provides a full-stack dynamic website that allows users to view statistics of tennis ATP matches based on a real dataset. The website lists all players, tournaments, and matches with reasonable attributes for each entity.

## Key Features
### Players, Tournaments, and Matches:
- List all players, tournaments, and matches.
- Identify reasonable attributes for players, tournaments, and matches.
- Matches should store the score and number of sets.

### Aggregate Statistics:
- The statistics about winners and losers, provided in the CSV files, refer to players in the match.
- Obtain aggregate statistics about a specific player, for example: “How many double faults player X had, on average, in matches won between 1971 and 1975”.
- The model should support this kind of query dynamically by user input.

## Technology Stack
### Frontend:
- HTML
- CSS
- JavaScript

### Backend:
- Node.js
- Express.js

### Database:
- MySQL
- SQL
