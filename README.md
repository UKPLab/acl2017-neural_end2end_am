# Neural End-to-End Learning for Computational Argumentation Mining

Sample source code and data for our ACL 2017 [article](http://aclweb.org/anthology/P17-1002):

```
@inproceedings{Eger:2017:ACL,
	title = {Neural End-to-End Learning for Computational Argumentation Mining},
	author = {Eger, Steffen and Daxenberger, Johannes and Gurevych, Iryna},
	publisher = {Association for Computational Linguistics},
	volume = {Volume 1: Long Papers},
	booktitle = {Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (ACL 2017)},
	pages = {(11--22)},
	month = aug,
	year = {2017},
	location = {Vancouver, Canada}
}
```

> **Abstract:** We investigate neural techniques for end-to-end computational argumentation mining (AM). We frame AM both as a token-based dependency parsing and as a token-based sequence tagging problem, including a multi-task learning setup. Contrary to models that operate on the argument component level, we find that framing AM as dependency parsing leads to subpar performance results. In contrast, less complex (local) tagging models based on BiLSTMs perform robustly across classification scenarios, being able to catch long-range dependencies inherent to the AM problem. Moreover, we find that jointly learning ‘natural’ subtasks, in a multi-task learning setup, improves performance. 


* **Contact persons** 
    * Steffen Eger, eger@aiphes.tu-darmstadt.de
    * Johannes Daxenberger, daxenberger@ukp.informatik.tu-darmstadt.de
    * UKP Lab: http://www.ukp.tu-darmstadt.de/

Drop us a line or report an issue if something is broken (and shouldn't be) or if you have any questions.

> This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication. 

## Project structure

* `code` &mdash; Illustrations of how we ran our experimental source codes
* `data` &mdash; Persuasive Essay data set in CONLL format. Essay and paragraph level given. The original data can be found here: https://www.ukp.tu-darmstadt.de/data/argumentation-mining/argument-annotated-essays-version-2/

## Data description and formats

The data come in very intuitive CONLL format. The data columns are TAB separated. The two useful columns are the word and its label. 
The label consists of an BIO indication, a component type indication (MajorClaim, Claim, Premise), as well as relation information, where applicable.
The relation information is coded relatively, as indicated in the paper, or absolutely. In relative encoding, a "-1" for instance means that a component links to the previous
components. In absolute encoding, "75" means that a components links to a component at position 75.
We used absolute encoding only for evaluating the systems' performances.

## Source codes

Besides the external software that we used, the repository also contains the following code:

* Evaluation: see progs/Eval/eval_componentF1.py and progs/Eval/eval_relationF1.py
    * Be sure that your prediction and gold files are in proper format.

* Post correction: We applied simple post-correction to our systems' outputs. Please take a look at:
    * progs/corrector.py
    * progs/corrector2.py
    * progs/LSTM-ER/common/toconll.py

* Conversion between relative and absolute distances:
    * progs/relative2absolute.py

### Requirements

* Python and all the code listed in the progs repository, e.g.:
    * BiLSTM-CNN-CRF: https://github.com/XuezheMax/LasagneNLP
    * LSTM-Parser: https://github.com/clab/lstm-parser
    * LSTM-ER: https://github.com/tticoin/LSTM-ER 

