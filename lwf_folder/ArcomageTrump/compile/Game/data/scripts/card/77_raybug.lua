-- ---------------------------------------------------------------
-- Arcomage Tribute Card Script library
--
-- File: 77_raybug.lua
-- Desc.: If enemy wall = 0 -> 10 damage, else 6
-- ---------------------------------------------------------------

local wall 	= arcomage:getEnemyAttribute("Wall");

if wall ~= 0 then
	arcomage:setEnemyAttribute("Damage", 6);
else
	arcomage:setEnemyAttribute("Damage", 10);
end