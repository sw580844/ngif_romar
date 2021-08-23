SW 

Here was an experiment to see if we could save space by packing all the frame files into an SQLite database, applying bzip, etc

It doesn't quite work out, but maybe someone else could figure it out

One of the issues is that the image data is approx 12bit, and we could package as binary but that could be an issue
Given nearly all entries are more than one char we could save some space and hopefully keep quick reads but eh