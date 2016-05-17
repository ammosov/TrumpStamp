-- ---------------------------------------------------------------
-- Arcomage Tribute Card Script library
--
-- File: 79_acid_cloud.lua
-- Desc.: If enemy wall > 0, 10 damage, else 7
-- ---------------------------------------------------------------

local wall 	= arcomage:getEnemyAttribute("Wall");

if wall > 0 then
	arcomage:setEnemyAttribute("Damage", 10);
else
	arcomage:setEnemyAttribute("Damage", 7);
end