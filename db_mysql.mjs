import { createConnection } from 'mysql2';

const connection = createConnection({
  host: 'localhost',
  user: 'root',
  password: '123456',
  database: 'TennisSchema',
});

function connect() {
  connection.connect();
}

function fetchPlayer(playerName, callback) {
  connection.query("SELECT * FROM player WHERE player_name = ?", [playerName], (error, results, fields) => {
    if (error) throw error;

    console.log(results);
    callback(results);
  });
}

function fetchTourney(date, callback) {
  connection.query("SELECT * FROM tournament WHERE tourney_id LIKE ?", [date + '%'], (error, results, fields) => {
    if (error) throw error;

    console.log(results)
    callback(results);
  });
}

function fetchStats(player, start, end, callback) {
	connection.query("call showAggregateStatistics(?, ?, ?)", [player, start, end], (error, results, fields) => {
		if (error) throw error;

		console.log(results)
		callback(results);
	});

}

// Execute the query to calculate average aces with parameters
function disconnect() {
  connection.end();
}

// Setup exports to include the external variables/functions
export {
  connection,
  connect,
  fetchPlayer,
  fetchTourney,
  fetchStats,
  disconnect
}
