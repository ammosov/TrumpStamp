-- ---------------------------------------------------------------
-- Arcomage Tribute Card Script library
--
-- File: 5_mother_lode.lua
-- Desc.: If own quarry < enemy quarry, quarry +2, else quarry +1
-- ---------------------------------------------------------------

local quarry_player = arcomage:getPlayerAttribute("Brick Modifier");
local quarry_enemy	= arcomage:getEnemyAttribute("Brick Modifier");

if quarry_player < quarry_enemy then
	arcomage:setPlayerAttribute("Brick Modifier", 2);
else
	arcomage:setPlayerAttribute("Brick Modifier", 1);
end