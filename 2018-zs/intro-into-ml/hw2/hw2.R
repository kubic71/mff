library(e1071)
library(ISLR)
library(rpart)
library(rpart.plot)
library(class)

entropy = function(vector) { 
  dist = table(vector) / NROW(vector)
  return (-sum(dist * log2(dist)))
}

set.seed(1)
data = Auto
data$name = NULL

message("--------------------")
message("-------TASK 1-------")
message("--------------------")



message("\n\n 1.1 \n")

message("Performing multiple linear regression...")
lm1 = lm(mpg~ ., data)
print(lm1)

message("\n\n 1.2 \n")
message("Fitting mpg ~ acceleration with polynomials")


plot(mpg ~ acceleration, data, main="Polynomial regression")
colors = c("red", "blue", "green", "yellow", "pink")
for (degree in 1:5) {
  fit = lm(mpg ~ poly(acceleration,degree), data)
  fr = data.frame(acceleration = seq(0, 30, 0.1))
  fr$pred = predict(fit, fr)
  lines(fr, col=colors[degree], lwd=3)
  
  message("polynomial degree: ", degree, ", R^2: ", summary(fit)$r.squared)
}



legend("topleft",
       legend = c("degree 1", "degree 2", "degree 3", "degree 4", "degree 5"),
       col = colors,
       lty = 1,
       lwd = 2,
)





message("--------------------")
message("-------TASK 2-------")
message("--------------------")

# make results deterministic
set.seed(1)

message("2.1")
d = Auto
mpg.median = median(d$mpg)
d$mpg01 = as.numeric(d$mpg > mpg.median)
d$name = NULL
d$mpg = NULL


message("Entropy of d$mpg01: ", entropy(d$mpg01))

message("\n\n2.2")
message("splitting dataset to train/test set\n")
# lets shuffle the data, to make the distribution equal across all parts of dataset
d = d[sample(1:NROW(d)), ]

# split dataset to train and test sets in ration 80:20
train_size = round(NROW(d) * 0.8)
d.train = d[1:train_size, ]

d.test = d[(train_size+1):NROW(d), ]

message("2.3 - MFC")

# most frequent classifier on test data

# get the most frequent value in train dataset
most_frequent = as.numeric(names(sort(table(d.train$mpg01),decreasing=TRUE))[1])

# compute the accuracy in test dataset
accuracy = sum(d.test$mpg01 == most_frequent) / NROW(d.test)
message("Accuracy of MFC is: ", accuracy, "\n\n")


message("2.4 - logistic regression")

glm.model = glm(mpg01 ~ ., data=d.train, family= binomial(link = 'logit'))
d.train.pred = as.numeric(predict(glm.model, newdata=d.train, type='response') > 0.5)
d.train.er = sum(d.train$mpg01 != d.train.pred) / NROW(d.train)

d.test.pred = as.numeric(predict(glm.model, newdata=d.test, type='response') > 0.5)
d.test.er = mean(d.test$mpg01 != d.test.pred)





print(glm.model)

message("GLM error rate on training data: ", d.train.er)
message("GLM error rate on test data: ", d.test.er, "\n\n")

message("Confusion matrix test.true vs test.predicted:")
true = d.test$mpg01
predicted = d.test.pred
print(table(true, predicted))


message("\n\n2.5 - decision tree")

tree.fit = rpart(mpg01 ~ ., data=d.train, cp=0.0001)
d.train.tree.pred = as.numeric(predict(tree.fit, newdata=d.train) > 0.5)
d.train.tree.er = sum(d.train$mpg01 != d.train.tree.pred) / NROW(d.train)

d.test.tree.pred = as.numeric(predict(tree.fit, newdata=d.test) > 0.5)
d.test.tree.er = sum(d.test$mpg01 != d.test.tree.pred) / NROW(d.test)

message("train err:", d.train.tree.er)
message("test err:", d.test.tree.er)

rpart.plot(tree.fit)

message("\n\noptimal cp: 0.0348950")
tree.fit = rpart(mpg01 ~ ., data=d.train, cp=0.034)
d.train.tree.pred = as.numeric(predict(tree.fit, newdata=d.train) > 0.5)
d.train.tree.er = sum(d.train$mpg01 != d.train.tree.pred) / NROW(d.train)

d.test.tree.pred = as.numeric(predict(tree.fit, newdata=d.test) > 0.5)
d.test.tree.er = sum(d.test$mpg01 != d.test.tree.pred) / NROW(d.test)

message("optimal cp train err:", d.train.tree.er)
message("optimal cp test err:", d.test.tree.er)
rpart.plot(tree.fit)


message("\n\n2.6 - Naive Bayes algorithm")

bayes.fit = naiveBayes(as.factor(mpg01) ~ ., data=d.train)
train.pred = predict(bayes.fit, newdata = d.train)
train_accuracy = sum(train.pred == d.train$mpg01) / NROW(d.train)
message("train accuracy: ", train_accuracy)

test.pred = predict(bayes.fit, newdata=d.test)

# compute confusion matrix
true = d.test$mpg01
conf_matrix = table(test.pred, true)

test_accuracy = sum(diag(conf_matrix)) / sum(conf_matrix)
message("test accuracy: ", test_accuracy)

message("confusion matrix:")
print(conf_matrix)

# precision = TP / (TP + FP)
test_precision = conf_matrix[2, 2] / sum(conf_matrix[, 2])

# recall (hit rate) = TP / (TP + FN)
test_recall = conf_matrix[2, 2] / sum(conf_matrix[2, ])

message("test precision:\t", test_precision)
message("test recall:\t\t", test_recall)


message("\n\n2.7 - k-NN + 8-fold crossvalidation")

perform_kNN = function(k) {
  n_folds = 8
  d.train = d.train[sample(nrow(d.train)),]
  
  folds <- cut(seq(1,nrow(d.train)),breaks=n_folds,labels=FALSE)
  #Perform 8 fold cross validation
  err = 0
  for(i in 1:n_folds){
    
    #Segement your data by fold using the which() function 
    testIndexes <- which(folds==i,arr.ind=TRUE)
    
    testData <- d.train[testIndexes, ]
    true_test = testData$mpg01
    testData$mpg01 = NULL
    
    trainData <- d.train[-testIndexes, ]
    true_train = trainData$mpg01
    trainData$mpg01 = NULL
    
    # perform knn
    pred = knn(trainData, testData, true_train, k=k)
    err = err +  1 - (sum(pred == true_test) / NROW(true_test))

  }
  
  return (err / n_folds)
}


MAX_K = 300
errors = c()

for (k in 1:MAX_K) {
  errors = c(errors, perform_kNN(k))
}

k = 1:MAX_K
plot(k, errors, type='l', main="kNN 8-fold crossvalidation error rate for different k", xlab="k", ylab="error", lwd=3)
