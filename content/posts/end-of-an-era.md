+++
title = 'End of an Era'
date = 2026-10-02T09:38:48+02:00
draft = true
tags = []
# crosspost = ['x']   # uncomment to publish this post as an X Article when it goes live
+++

A decade ago, I spent a few months deciding a new career path for myself. I carefully considered factors like earning potential, enjoyment, talent and "future-proofness".

I prototyped 3 different career paths. One of them was as a data scientist. It had been dubbed "The sexiest job of the 21st century" in an HBR article a few years prior.

This prototyping involved getting my hands dirty with Kaggle competitions. And I quickly fell in love with it. I could spend hours wrangling data in pandas, feature engineering, and cross-validating model ensembles.

Most Kaggle competitions, like most ML business challenges/opportunities at the time, were on tabular data.

I have realized that many people new to the AI world may need a closer explanation, so this is for you:

In ML on tabular data, where the task is given some data with features and a training set with values for a target variable, you predict the target variable for new data points from only the features.

(Add table with example)

Typical business problems involve churn prediction (binary classification), customer LTV, price estimation, segmentation, fraud prediction, profitability prediction etc.

I was hooked, and determined to make this a rewarding career for myself, I set myself a goal of becoming the "Best Data Science consultant in Norway".

This, of course, is a difficult goal to evaluate, but I only cared about the identity this allowed me to adopt, and the habits it forced me to instill.

I got my 10 000 hours of deliberate practice(footnote Anders Ericsson, peak) in during the first 5 years, and reached a lot of milestones on the way. Some of them were:

- Become Team Leader
- Win tender for project X
- Get offer from company Y
- Get a Master's degree in CS with AI specialization with grade A average. (I already had a Bachelor's degree)
- Earn 1M NOK/year

## The GBDT dominance

I quickly realized that gradient boosted trees were the dominant method for prediction and classification tasks. They consistently outperformed other methods in most cases. Deep learning was sometimes used as part of an ensemble, especially if the problem involved some unstructured data. When they were used, they usually involved training from scratch, required a lot of data and there were many attempts to design fancy new architectures, but they failed many more times than not. 

Boosted trees were a lot simpler to work with, and became the default way of doing it for real projects where you were expected to create business value with limited resources.

And it stayed that way for more than a decade.

## Enter MLOps

I spent most of my consulting career working with MLOps and data engineering.

Fitting the model was not a lot of code.

Wrapping the model in a docker container, serving it through web endpoints, blue/green deployments, continuous retraining, and monitoring was a big part of the work.

And this work usually needed to be tailored to each and every use case, as they had different data sources, output sinks, consumers or different retraining frequency needs. 

Translating what the technical metrics would mean in terms of actual business value to the client was also a significant part.

## The bitter lesson

With the advent of transformers and LLMs, we learned the bitter lesson. Naturally, this also applies to tabular ML. The part that took some time was from where (and how) to source the training data (text was available in abundance).
One solution is to generate it synthetically. More details on how in this blogpost: https://huggingface.co/blog/nvidia/kumo-tabular

And now, we have tabular foundation models. They can predict target values for a dataset _without_ any training, similarly to how LLMs predict tokens.

And now, it seem to really work, with kumo tabular climbing to the top of the leaderboard on all 4 tabular data benchmarks. (todo insert links)

## 