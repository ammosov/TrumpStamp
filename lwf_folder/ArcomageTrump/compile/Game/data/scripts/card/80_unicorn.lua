-- ---------------------------------------------------------------
-- Arcomage Tribute Card Script library
--
-- File: 80_unicorn.lua
-- Desc.: If magic > enemy magic, 12 damage, else 7 damage
-- ---------------------------------------------------------------

local player_magic 	= arcomage:getPlayerAttribute("Gem Modifier");
local enemy_magic	= arcomage:getEnemyAttribute("Gem Modifier");

if player_magic > enemy_magic then
	arcomage:setEnemyAttribute("Damage", 12);
else
	arcomage:setEnemyAttribute("Damage", 7);
end