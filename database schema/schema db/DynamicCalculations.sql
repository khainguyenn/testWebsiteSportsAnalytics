-- Active: 1695938287216@@127.0.0.1@3306@TennisSchema
-- Functions, Procedures, Triggers, Views
-- Author: Khai Nguyen 

USE TennisSchema;
-- 1. A function aceCount(name, start, finish) that calculates the average number of aces, 
-- given a player name and a time frame between two dates.
DROP FUNCTION IF EXISTS aceCount;
DELIMITER //
CREATE FUNCTION aceCount(name VARCHAR(200), start DATE, finish DATE) RETURNS FLOAT
    DETERMINISTIC
BEGIN
    DECLARE avg_aces FLOAT;
    SELECT AVG(player_ace)
    INTO avg_aces
    FROM player
    JOIN played ON player.player_id = played.player_id
    JOIN matchL ON played.match_num = matchL.match_num AND played.tourney_id = matchL.tourney_id
    JOIN tournament ON matchL.tourney_id = tournament.tourney_id
    WHERE player.player_name = name
      AND tournament.tourney_date BETWEEN start AND finish;
    RETURN avg_aces;
END 

DELIMITER ;

SELECT aceCount('Galo Blanco', '1960-01-01', '2022-12-31');



-- 2. A procedure showAggregateStatistics(name, start, finish) that yields a result set 
-- containing all aggregate statistics of a player during a specific time frame.
DROP PROCEDURE IF EXISTS showAggregateStatistics;
CREATE PROCEDURE showAggregateStatistics(IN playerName VARCHAR(255), IN startDate DATE, IN endDate DATE)
BEGIN
    SELECT
        p.player_name,
        COUNT(*) AS matches_played,
        SUM(CASE WHEN pl.win_loss = 'W' THEN 1 ELSE 0 END) AS matches_won,
        SUM(CASE WHEN pl.win_loss = 'L' THEN 1 ELSE 0 END) AS matches_lost,
        SUM(pl.player_ace) AS total_aces,
        AVG(pl.player_ace) AS avg_aces_per_match,
        SUM(pl.player_df) AS total_double_faults,
        AVG(pl.player_df) AS avg_double_faults_per_match,
        SUM(pl.player_bpSaved) AS total_break_points_saved,
        AVG(pl.player_bpSaved) AS avg_break_points_saved_per_match
    FROM
        player AS p
    JOIN
        played AS pl ON p.player_id = pl.player_id
    JOIN
        tournament AS t ON pl.tourney_id = t.tourney_id
    WHERE
        p.player_name = playerName
        AND t.tourney_date BETWEEN startDate AND endDate
    GROUP BY
        p.player_name;
END
DELIMITER ;

CALL showAggregateStatistics('Galo Blanco', '1960-01-01', '2022-12-31');



-- 3. A view TopAces that lists the top 10 players based on number of aces, across all matches.
DROP VIEW IF EXISTS TopAces;
CREATE VIEW TopAces AS
SELECT p.player_name, SUM(CASE WHEN pa.player_ace >= 0 THEN pa.player_ace ELSE 0 END) AS total_aces
FROM player p
JOIN played pa ON p.player_id = pa.player_id
GROUP BY p.player_name
ORDER BY total_aces DESC
LIMIT 10;

SELECT * FROM TopAces;

-- 4. A trigger onInsertionPlayer that, upon inserting players, replaces a reference 
-- to the country code ’RUS’ (and another former country of the block, say ’EST’) to ’USR’,
-- for the former USSR2.
DROP PROCEDURE IF EXISTS onInsertionPlayer;
DELIMITER //
CREATE TRIGGER onInsertionPlayer BEFORE INSERT ON player
FOR EACH ROW
BEGIN
    IF NEW.player_ioc IN ('RUS', 'EST') THEN
        SET NEW.player_ioc = 'USR';
    END IF;
END 
DELIMITER ;





