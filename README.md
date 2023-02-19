# Chess game

The game is still under development.
- You are now able to interact with chess board through the CLI
- Most of the basic legal-move-checks has been implemented

Here is a sneak peak to how the game will work in the CLI (January 2, 2022):

![AnimationSkak](https://user-images.githubusercontent.com/51048135/147890366-43fe6e1e-4e33-449d-b684-5ab605037458.gif)

# Implementation Progress
This section describes and overview of the development progress and what is in the backlog.

## Implemented
- Rules for legal movement of:
    - King
    - Queen
    - Pawn
    - Rook
    - Knight
    - Bishop
- Kill events, when a piece attacks opponent piece
- Chess board is viewable in the terminal
- Special game rules:
    - Checkmate

## Missing implementation that is planned:
- Special game rules, for example:
    - Promotion
    - En Passant
    - Castling 
    - Check
    - stalemate
- Logging of actions taken by players
- Other chess board UI using for example Pygame (future ideas)

# Installation
