-- ---------------------------------------------------------------
-- Arcomage Tribute Card Script library
--
-- File: 12_fundament.lua
-- Desc.: If wall = 0, wall +6, else wall +3
-- ---------------------------------------------------------------

local wall = arcomage:getPlayerAttribute("Wall");

if wall ~= 0 then
	arcomage:setPlayerAttribute("Wall", 3);
else
 	arcomage:setPlayerAttribute("Wall", 6);
end