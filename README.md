# SoftwareCarpentryLazorProject

Authors: Kuan-Lin Chen, Josh Cole, Katherine Miller, Yi Li

This is a project in which, we write algorithms solving the "Lazor" game, helping those who are having a hard time cracking the game.

The code reads in .bff files for the information of the board, laser, laser direction, and the positions of the target points. Examples of the format of the .bff file can be found in the mad_1.bff file.

To run the code, all you need is the .bff file for the board and the Lazor.py file. To solve the game, run the function in Lazor.py with the name lazors_cheat(filename), where filename is, for example, "mad_1.bff" or "mad_1".

After running the code, you'll see if the board is successfully loaded, all the possible solutions, and please patiently wait for it to solve, the code should usually be able to solve every problem within 30 seconds if the board is not incredibly complicated or large. After solution is found, and output .png file containing the filename of the board will be saved within the same directory. The png file shows the position of the block and differentiates different blocks with diffect colors. The Reflect blocks will be in white. The Refrect block will be in gray. The Opaque block will be in black. Please follow the instruction of the .png file to place the blocks in order to beat the level.

Good luck.
