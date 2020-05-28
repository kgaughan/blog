Title: Reactor
Category: Project Ideas
Date: 2006-05-09 18:28
Status: published

**Reactor** is a game I've been meaning to write for a while. It's a conversion of a board game I originally wrote on the C-64 called _Reaction_ (not to be confused with _[Reaxion](http://www.gamebase64.com/game.php?id=6254&d=18)_, a rather good tile flipping game).

Here's some graphics I knocked out showing the various grid square states:

![Image showing the various states a grid square can be in]({static}../images/reactor-states.png)
{: .figure }

I think I'll make them smaller, but they're fine for now.

## Gameplay

The object of the game is to remove all your opponent's tokens from the grid.

The game is played on a square grid, and each of the two players puts tokens on the various squares on the grid in turn. They can place them on empty squares or squares containing tokens of with their colouring.

Squares can only hold so many tokens and remain _stable_, and that number is determined by the number of vertically and horizontally adjacent squares. So a corner square is stable if it holds less than two tokens, an edge piece if it holds less than three, and any other square if it holds less than four. If their token limit is exceeded, they become _unstable_ and a _reaction_ throws the tokens on the square onto the adjacent squares. A _chain reaction_ starts if those adjacent squares also exceed the number of tokens they can stablely hold. The chain reaction continues until either all squares are stable or the grid contains tokens of only one colour: yours.

It's important to note how you get rid of your opponents tokens. If a square containing your tiles goes off next to a square containing tokens belonging to your opponent, the tokens in that square switch sides and become yours.

Quite a simple game, and a good one.

## History

The original was written in Commodore BASIC and used a numeric grid. I later converted it to the Acorn Archimedes (confusingly calling it _!Reaxion_) and wrote it in BBC BASIC (I hadn't learned ARM assembly language or C yet) as I'd picked up enough of the language from reading other people's programs to write it (thank you, Acorn User, and in particular the two Daves who ran `*INFO`).

I never did get to convert it to a desktop application like I intended, and the half-arsed AI engine was based on a poor description of [Minimax](http://en.wikipedia.org/wiki/Minimax) I cogged from a book on AI for children, and a better version of the same game was submitted by another reader, it languished in `MODE 13` hell on a floppy.

## Today

I'd like to rewrite the game, possibly in Haskell. All I have right now is some graphics a drew while I was watching _Lost_, and a vague recollection of the AI algorithm I designed for the computer player. Network play would be nice too. And on top of that, I have to decide if I should make it shareware or open source it. Either way, it'd be a nice exercise to write a proper piece of software in a language I've only ever written short programs in, usually converting the result to another language.

And I've a chance to make the computer player _much_ better now.

So, here's the question: going off the what you've read and seen so far, would you buy a networked version of the game if I was to make the non-networked version free and released the game's core logic so people could read and learn from it?

And does anybody know the proper name for the game?
