[WIP] Generate ascii art for an image based on the "currier new" font.
The reason why currier new is the font of choise is that it is both singlespaced (easier to program) and the default font for Notepad++ which is a great tool for viewing your generated art in its full splendour.

Images should be in JPG format (.jpg or .jpeg extension). Other formats will probably be added later.

Letters are mapped to the greyscale in accordance with the letters.ranked file found in the assets folder. They are ordered darkest to lightest. To add your own letters just insert them into that file at the appropriate line. The letters are sepperated by the newline symbol and only the first letter of each line is included to avoid including random whitespaces in the art. 

Input images specified with the "-i \<name\>.\<extension\>" argument will be read from the assets folder.

Output text files specified with the "-o \<name\>.\<extension\>" will be placed in the out folder .

TODO:
 - Parametize better
 - Comments
 - Cleanup
 - ??
 - Profit
