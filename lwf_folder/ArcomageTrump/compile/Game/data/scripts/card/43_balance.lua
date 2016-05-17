-- ---------------------------------------------------------------
-- Arcomage Tribute Card Script library
--
-- File: 43_balance.lua
-- Desc.: Adjusts the magic of both player to the highest value
-- ---------------------------------------------------------------

local player_magic 	= arcomage:getPlayerAttribute("Gem Modifier");
local enemy_magic	= arcomage:getEnemyAttribute("Gem Modifier");

arcomage:setPlayerAttribute("Gem Modifier", -player_magic);
arcomage:setEnemyAttribute("Gem Modifier", -enemy_magic);
	
if player_magic >= enemy_magic then
	arcomage:setPlayerAttribute("Gem Modifier", player_magic);
	arcomage:setEnemyAttribute("Gem Modifier", player_magic);
else
	arcomage:setPlayerAttribute("Gem Modifier", enemy_magic);
	arcomage:setEnemyAttribute("Gem Modifier", enemy_magic);
end