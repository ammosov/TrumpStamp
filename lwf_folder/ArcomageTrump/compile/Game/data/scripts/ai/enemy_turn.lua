-- ---------------------------------------------------------------
-- Arcomage Game AI
-- 
-- This script executes the computer's turn.
--
-- ---------------------------------------------------------------

-- Functions...

-- ---------------------------------------------------------------
-- Check whether there are enough resources to play the card
function Arcomage:checkCard(card)
	local type = arcomage:getValueFromCard(card, "Type"); 
	
	-- red card
	if type == 0 then
		return arcomage:getEnemyAttribute("Bricks") >= arcomage:getValueFromCard(card, "Requirements")
		
	-- blue card
	elseif type == 1 then
		return arcomage:getEnemyAttribute("Gems") >= arcomage:getValueFromCard(card, "Requirements")

	-- green card
	elseif type == 2 then
		return arcomage:getEnemyAttribute("Beasts") >= arcomage:getValueFromCard(card, "Requirements")

	end
end

-- ---------------------------------------------------------------
-- Selects a card
function Arcomage:selectCard()
	local temp = arcomage:selectRandomCard();
	-- randomize cards until one with sufficient requirements is found
	while arcomage:checkCard(temp) ~= true do
		temp = arcomage:selectRandomCard();
	end
	-- return the card ID
	return temp;
end

-- ---------------------------------------------------------------
-- Applies all changes to the enemy and player
function Arcomage:doTurn(card)
	local type = arcomage:getValueFromCard(card, "Type"); 
		
	-- Animate the card to fly to the center of the screen within 0.5 seconds
	arcomage:animateCard(card, 0.5);
	
	-- Play the card sound
	arcomage:playSound("card");
	
	-- Apply changes to computer player
	
	-- We won't need this anymore, for now.
	--[[
	
	if type == 0 then
			arcomage:setEnemyAttribute("Bricks", -arcomage:getValueFromCard(card, "Requirements")); 
	elseif type == 1 then
			arcomage:setEnemyAttribute("Gems", -arcomage:getValueFromCard(card, "Requirements")); 
	elseif type == 2 then
			arcomage:setEnemyAttribute("Beasts", -arcomage:getValueFromCard(card, "Requirements")); 
	end

	arcomage:setEnemyAttribute("Tower", arcomage:getValueFromCard(card, "Player Tower Changes")); 
	arcomage:setEnemyAttribute("Wall", arcomage:getValueFromCard(card, "Player Wall Changes")); 
	arcomage:setEnemyAttribute("Brick Modifier", arcomage:getValueFromCard(card, "Player Brick Modifier")); 
	arcomage:setEnemyAttribute("Gem Modifier", arcomage:getValueFromCard(card, "Player Gem Modifier")); 
	arcomage:setEnemyAttribute("Beast Modifier", arcomage:getValueFromCard(card, "Player Beast Modifier")); 
	arcomage:setEnemyAttribute("Bricks", arcomage:getValueFromCard(card, "Player Brick Changes")); 	
	arcomage:setEnemyAttribute("Gems", arcomage:getValueFromCard(card, "Player Gem Changes")); 
	arcomage:setEnemyAttribute("Beasts", arcomage:getValueFromCard(card, "Player Beast Changes")); 
	arcomage:setEnemyAttribute("Damage", arcomage:getValueFromCard(card, "Damage to Self")); 
	
	-- Apply changes / damage to player

	arcomage:setPlayerAttribute("Tower", arcomage:getValueFromCard(card, "Enemy Tower Changes")); 
	arcomage:setPlayerAttribute("Wall", arcomage:getValueFromCard(card, "Enemy Wall Changes")); 
	arcomage:setPlayerAttribute("Brick Modifier", arcomage:getValueFromCard(card, "Enemy Brick Modifier")); 
	arcomage:setPlayerAttribute("Gem Modifier", arcomage:getValueFromCard(card, "Enemy Gem Modifier")); 
	arcomage:setPlayerAttribute("Beast Modifier", arcomage:getValueFromCard(card, "Enemy Beast Modifier")); 
	arcomage:setPlayerAttribute("Bricks", arcomage:getValueFromCard(card, "Enemy Brick Changes")); 	
	arcomage:setPlayerAttribute("Gems", arcomage:getValueFromCard(card, "Enemy Gem Changes")); 
	arcomage:setPlayerAttribute("Beasts", arcomage:getValueFromCard(card, "Enemy Beast Changes")); 
	arcomage:setPlayerAttribute("Damage", arcomage:getValueFromCard(card, "Damage to Enemy")); 
	]]--
end

-- ---------------------------------------------------------------
-- The main script:

local card = arcomage:selectCard();
arcomage:doTurn(card);

if arcomage:getAdditionalTurn(card) == true then
	-- do something...
	
	card = arcomage:selectCard();
	arcomage:doTurn(card);
end
-- ---------------------------------------------------------------
-- eof
