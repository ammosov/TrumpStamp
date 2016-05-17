-- ---------------------------------------------------------------
-- Arcomage Tribute Card Script library
--
-- File: 8_stolen_knowledge.lua
-- Desc.: If own quarry < enemy quarry, quarry = enemy quarry
-- ---------------------------------------------------------------

local quarry_player = arcomage:getPlayerAttribute("Brick Modifier");
local quarry_enemy	= arcomage:getEnemyAttribute("Brick Modifier");

if quarry_player < quarry_enemy then
	arcomage:setPlayerAttribute("Brick Modifier", quarry_enemy);
end