-- ----------------------------------------------
--
-- This file is executed upon creation of a
-- new game.
--
--

-- ----------------------------------------------
-- functions

-- ----------------------------------------------
-- Initialization function. Sets the resource 
-- values players have at the start.
function Arcomage:initialize()
	limit = arcomage:getTowerlimit()

	if limit == 75 then
		arcomage:saveLogMessage("Tower Limit set to 75");
		arcomage:setAttribute("Tower", 			10);
		arcomage:setAttribute("Wall", 			5);
		arcomage:setAttribute("Bricks", 		10);
		arcomage:setAttribute("Gems", 			10);
		arcomage:setAttribute("Beasts", 		10);
		arcomage:setAttribute("Brick Modifier",	1);
		arcomage:setAttribute("Gem Modifier", 	1);
		arcomage:setAttribute("Beast Modifier",	1);
		
		arcomage:setResourceLimit(150);
		
	elseif limit == 100 then
		arcomage:saveLogMessage("Tower Limit set to 100");
		arcomage:setAttribute("Tower", 			15);
		arcomage:setAttribute("Wall", 			10);
		arcomage:setAttribute("Bricks", 		12);
		arcomage:setAttribute("Gems", 			12);
		arcomage:setAttribute("Beasts", 		12);
		arcomage:setAttribute("Brick Modifier",	2);
		arcomage:setAttribute("Gem Modifier", 	2);
		arcomage:setAttribute("Beast Modifier",	2);

		arcomage:setResourceLimit(225);
		
	elseif limit == 125 then
		arcomage:saveLogMessage("Tower Limit set to 125");
		arcomage:setAttribute("Tower", 			20);
		arcomage:setAttribute("Wall", 			15);
		arcomage:setAttribute("Bricks", 		15);
		arcomage:setAttribute("Gems", 			15);
		arcomage:setAttribute("Beasts", 		15);
		arcomage:setAttribute("Brick Modifier",	3);
		arcomage:setAttribute("Gem Modifier", 	3);
		arcomage:setAttribute("Beast Modifier",	3);

		arcomage:setResourceLimit(350); 
		end

end
 
-- ----------------------------------------------
-- This command chain is executed upon creation 
-- of a new game:

arcomage:initialize(); 

-- ..

-- ----------------------------------------------
-- eof