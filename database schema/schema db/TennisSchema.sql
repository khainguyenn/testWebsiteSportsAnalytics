
-- Schema Title: TennisSchema
-- Author: Khai Nguyen

-- This program creates a database schema  
-- to manage the information about the tennis matches

DROP SCHEMA IF EXISTS TennisSchema;
CREATE SCHEMA TennisSchema;
USE TennisSchema;

-- Create a table to store player information.
-- Attributes: player_id, player_name, player_hand, player_height, player_ioc.
CREATE TABLE player (
    player_id       VARCHAR(50),
    player_name     VARCHAR(200),
    player_hand     VARCHAR(50),
    player_height   VARCHAR(50),
    player_ioc      VARCHAR(5),
    PRIMARY KEY (player_id)
);

-- Create a table to store tournament information.
-- Attributes: tourney_id, tourney_name, surface, draw_size, tourney_level, tourney_date.
CREATE TABLE tournament (
    tourney_id      VARCHAR(50),
    tourney_name    VARCHAR(200),
    surface         VARCHAR(50),
    draw_size       VARCHAR(50),
    tourney_level   VARCHAR(5),
    tourney_date    DATE,
    PRIMARY KEY (tourney_id)
);

-- Create a table to store match information.
-- Attributes: match_num, tourney_id, round, minutes, best_of, score.
CREATE TABLE matchL (
    match_num       VARCHAR(50),
    tourney_id      VARCHAR(50),
    round           VARCHAR(50),
    minutes         VARCHAR(50),
    best_of         VARCHAR(50),
    score           VARCHAR(100),
    PRIMARY KEY (match_num, tourney_id),
    FOREIGN KEY (tourney_id) REFERENCES tournament(tourney_id) ON DELETE CASCADE
);

-- Create a table to store player information on each match.
-- Attributes: tourney_id, match_num, player_id, win_loss, player_seed, player_entry,
-- player_rank, player_rank_points.
CREATE TABLE played (
    tourney_id      VARCHAR(50),
    match_num       VARCHAR(50),
    player_id       VARCHAR(50),
    win_loss        CHAR(5) CHECK (win_loss IN ('W', 'L')),
    player_seed     VARCHAR(5),
    player_ace      VARCHAR(5), 
    player_entry    VARCHAR(5),
    player_df       VARCHAR(5),
    player_svpt     VARCHAR(5),
    player_bpSaved 	VARCHAR(5),
    player_rank     VARCHAR(5) CHECK (player_rank >= '0' AND player_rank NOT LIKE '-%'),
    player_rank_points VARCHAR(5),
    PRIMARY KEY (match_num, tourney_id, player_id),
    FOREIGN KEY (match_num, tourney_id) REFERENCES matchL(match_num, tourney_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id) 
);





