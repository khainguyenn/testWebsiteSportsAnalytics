// This is a framework to handle server-side content

// You have to do an 'npm install express' to get the package
// Documentation in: https://expressjs.com/en/starter/hello-world.html
import express from 'express';
import * as db from './db_mysql.mjs';

const app = express();
const port = 3001;

db.connect();

// Serve static HTML files in the current directory (called '.')
app.use(express.static('.'));


app.get('/player', function (request, response) {
  let playerName = request.query["player_name"];

  db.fetchPlayer(playerName, (results) => {
    response.json(results);
  });
});

app.get('/tourney', function (request, response) {
  let date = request.query["date"]

  db.fetchTourney(date, (results) => {
    response.json(results)
  })
});

app.get('/playerStats', function (request, response) {
  let player = request.query["player"]
  let start = request.query["start"]
  let end = request.query["end"]

  db.fetchStats(player, start, end, (results) => {
    response.json(results)
  })
});


app.listen(port, () => {
  console.log('Server is starting on PORT', port);
});

process.on('exit', () => {
  db.disconnect();
});
