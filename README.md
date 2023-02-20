## Test some Strategies for Liar's dice(Bluff Dice Game) 

The game Bluff (Liar's dice) with each player rolling 5 dice, that only they can see.
Now players take turns either making bets, or calling a bluff on the last bet.
Each bet is on the total number of a certain face in all rolled die.
The face with the 6 takes a special role as it is a joker.
The number of sixes gets added to the number of other faces.

Bet1 is higher than bet2 if they claim the same number but a higher face, or a higher number of any face.
For the face 6 there are special rules. If bet1 claims face 6, bet 2 can either claim a higher number of 6 faces
or must choose a higher number than the number of 6 faces times two. If bet2 claims six faces and bet1 doesn't
then the number of 6 faces must be at least the number claimed in bet1 divided by 2 plus 0.5 rounded up.

A bluff can be called only on the previous bet.
If a bluff is called all players show their die and the difference of the correct number of faces is calculated.
Now there are some variations in the rules.
If the difference is positive the challenger (or all players but the better) must remove 1 dic (or difference+1 dice)
and otherwise the better must remove 1 die (or the difference dice).

After the bluff is called, all players roll their remaining dice and the game continues.

The last player to have dice wins.

### Some Ideas for the Future:
- Depending on the payoff if it is preferred to become second, in the rule set that all players but the better
        have to pay for wrong bluff calls, one might try to purposefully kick out a player who has less dice, by
        calling a bluff on plays that are below the expectation.
- One of the bots here tries to guess when players have 1 more than the expectation of a certain face. 
    This is done when a player bets above the expectation. But one could go one step further since other players might
    have also guessed that a third player has more than the expectation and only be using this information for his bet.
    Also if another player uses this tactic, one might approximate his expectations more accurately knowing one's own
    bets and dice.
- It would be interesting to train a reinforcement algoirthm to see the differences to these strategies.

#### Playground

Feel free to add bots and have them clash it out!