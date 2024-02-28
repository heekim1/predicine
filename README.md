The instrument produces measurements for a set of biological samples over multiple timepoints. The data is stored in CSV files in a directory, with one file per time point.

The raw data files are difficult for scientists to work with, so they need you to write a command-line program or script that reads all the CSV files in the given directory, and produces a single output CSV file that concatenates all the data. It would also be helpful to generate a summary output file that records the average value across samples at each time point.

Input:

Path to a directory containing CSV files named with the convention: “t[timepoint].csv”. Each CSV file has the format “sample_id, measurement”. Take a look at the example input directory attached to this email.

Output

A file that concatenates all the data into a new CSV table with columns arranged like so:

sample_id, t01, t02, t03, …

(bonus) Summary CSV output file that records the average value of all the samples present at each time point recorded. The columns can be arranged like so:

time_point, average

