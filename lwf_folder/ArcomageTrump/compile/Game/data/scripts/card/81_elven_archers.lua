-- ---------------------------------------------------------------
-- Arcomage Tribute Card Script library
--
-- File: 81_elven_archers.lua
-- Desc.: If wall > enemy wall, enemy tower -6, else 6 damage
-- ---------------------------------------------------------------

local player_wall	= arcomage:getPlayerAttribute("Wall");
local enemy_wall	= arcomage:getEnemyAttribute("Wall");

if player_wall > enemy_wall then
	arcomage:setEnemyAttribute("Tower", -6);
else
	arcomage:setEnemyAttribute("Damage", 6);
end