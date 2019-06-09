# Naive-Bayes-Word-Sense-Disambiguation

Python program WSD.py that implements the Naive Bayes algorithm for word sense disambiguation, as discussed in class. Specifically, your program will have to assign a given target word with its correct sense in a number of test examples.

Train and test your program on a dataset consisting of textual examples for the noun “plant,” drawn from the British National Corpus, where each example is manually annotated with its correct sense of “plant.” Consider for example the following instance:

<instance id="plant.1000002" docsrc = "BNC/A0G">
<answer instance="plant.1000002" senseid="plant%living"/>
<context>
September 1991 1.30 You can win a great new patio Pippa Wood How to cope with a slope Bulbs
<head>plant</head> now for spring blooms
</context>
</instance>

The target word is identified by the SGML tag <head>, and the sense corresponding to this particular instance is that of plant%living.

Programming guidelines:
Your program should perform the following steps:

❖	Take one argument consisting of the name of one file, which includes the annotated instances.
 
❖	Determine from the entire file the total number of instances and the possible sense labels.
❖	Create five folds, for a five-fold cross-validation evaluation of your Naive Bayes WSD implementation. Specifically, divide the total number of instances into five, round up to determine the number of instances in folds 1 through 4, and include  the  remaining  instances in fold 5. E.g., if you have 122 total instances, you will have five folds with sizes 25, 25, 25, 25, and 22 respectively.
❖	Implement and run the Naive Bayes WSD algorithm using a five-fold cross-validation scheme. In each run, you will:

(1)	use one of the folds as your test data, and the remaining folds together as your training data (e.g., in the first run, use fold 1 as test, and folds 2 through 5 as training; etc.);

(2)	collect the counts you need from the training data, and use the Naive Bayes algorithm to predict the senseid-s for the instances in the test data;

(3)	evaluate the performance of your system by comparing the predictions made by your Naive Bayes word sense disambiguation system on the test data fold against the ground truth annotations (available as senseid-s in the test data).

Considerations for the Naive Bayes implementation:

➔ All the words found in the context of the target word will represent the features to be considered
➔ Address zero counts using add-one smoothing
➔ Work in log space to avoid underflow due to repeated multiplication of small numbers

The WSD.py program should be run using a command like this:
% python WSD.py plant.wsd

The program should produce at the standard output the accuracies of the system (as a percentage)  for each of the five folds, as well as the average accuracy. It should also generate a file called plant.wsd.out, which includes for each fold the id of the words in the test file along with the  senseid predicted by the system. Clearly delineate each fold with a line like this “Fold 1”, “Fold 2”, etc. For instance, the following are examples of lines drawn from a plant.wsd.out file

Fold 1
plant.1000000 plant%factory plant.1000001 plant%factory plant.1000002 plant%living
…
Fold 2
plant.1000041 plant%living plant.1000042 plant%living
...
 

