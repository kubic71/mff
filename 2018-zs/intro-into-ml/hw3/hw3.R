library(data.table)
library(FSelector)
library(rpart)
library(rpart.plot)
library(ROCR)
library(randomForest)

# load development data
d1 = fread("devel1.csv")
d2 = fread("devel2.csv")
d = rbind(d1, d2)
t.blind = fread("test.blind.csv")

#####################################
######### some functions ############
#####################################

# get stratified folds from data
get_folds = function(data, k) {
  #shuffle data
  data = data[sample(nrow(data)),]
  
  positive = data[data$active == 1 , ]
  negative = data[data$active == 0 , ]
  
  pos.folds = cut(seq(1,nrow(positive)),breaks=k,labels=FALSE)
  neg.folds = cut(seq(1,nrow(negative)),breaks=k,labels=FALSE)
  
  #list initialization
  folds = vector("list", k)
  
  for(i in 1:k) {
    pos.fold = positive[which(pos.folds==i,arr.ind=TRUE), ]
    neg.fold = negative[which(neg.folds==i,arr.ind=TRUE), ]
    folds[[i]] = rbind(pos.fold, neg.fold)
  }
  
  return(folds)
}

get_auc01 = function(pred) {
  auc01 = performance(pred, measure = "auc", fpr.stop=0.1)
  return(as.numeric(auc01@y.values))
}

#####################################
#####################################




#####################################
#-------------- TASK 1 --------------
#####################################

n_d1 = NROW(d1)
n_d2 = NROW(d2)
n_features = dim(d1)[2]

# --- task 1a ---
message("--- task 1a ---")
# proportion of active ligands in d1 and d2
td1 = table(d1$active)
td2 = table(d2$active)

message("the ratio active/non-active ligands in d1 is ", td1[2] / td1[1])
message("the ratio active/non-active ligands in d2 is ", td2[2] / td2[1])


# --- task 1b ---
message("\n\n\n--- task 1b ---")
feature_types = as.vector(sapply(d, typeof))
print(table(feature_types))

discrete_indeces = which(feature_types == "integer")
continuous_indeces = which(feature_types == "double")

message("Number of discrete features: ", NROW(discrete_indeces) - 1)
message("Number of continuous features: ", NROW(continuous_indeces))


# --- task 1c ---
message("\n\n\n--- task 1c ---")

n_unique_vals = function(x) {
  return (NROW(table(x)))
}

get_discrete_features = function (data) {
  discrete_indeces = which(as.vector(sapply(data[, colnames(data) != "active", with=FALSE], typeof)) == "integer")
  return(data[, ..discrete_indeces])
}

constant_features = sapply(get_discrete_features(d), n_unique_vals) == 1
constant_features = names(constant_features[ constant_features == TRUE])
message("Constant features are: ")
print(constant_features)

d = d[, !(colnames(d)  %in% constant_features), with=FALSE]
t.blind = t.blind[, !(colnames(t.blind)  %in% constant_features), with=FALSE]

message("After removing constant features, there is ", NCOL(d) - 1 , " features remaining")

# --- task 1d ---
message("\n\n\n--- task 1d ---")
val_feature_table = table(sort(as.vector(sapply(get_discrete_features(d), n_unique_vals))))
message("Table showing how many features have a certain number of values:")
print(val_feature_table)
barplot(val_feature_table, xlab = "number of distinct values", ylab = "number of features")


# --- task 1e ---
message("\n\n\n--- task 1e ---")
frt = 4
frt_condition = function(x) {
  frq = sum(x > 0)
  return((min(frq, NROW(x) - frq)) >= frt)
}

discrete_features = get_discrete_features(d)
bin_features_names = names(discrete_features)[ sapply(discrete_features, n_unique_vals) == 2] 
bin_features = d[, colnames(d) %in% bin_features_names, with=FALSE]


features_to_remove = names(bin_features)[ sapply(bin_features, frt_condition) == FALSE ] 
message("Removing these binary features:")
print(features_to_remove)

d = subset(d, select=names(d)[ !(names(d) %in% features_to_remove) ])
message("Using ", NCOL(get_discrete_features(d)), " discrete features")


# --- task 1f ---
message("\n\n\n--- task 1f ---")
discrete = get_discrete_features(d)
discrete$active = d$active

inf = information.gain(active~., discrete)
inf_gain = data.frame(f_name=rownames(inf), i_gain=inf[, 1])
inf_gain = inf_gain[order(inf_gain$i_gain, decreasing=TRUE), ]
message("information gain between features and 'active' target class")
print(inf_gain)

plot(1:NROW(inf_gain), inf_gain$i_gain, xlab="feature #", ylab="information gain", main = "discrete feature information gain",pch=16)
lines(1:NROW(inf_gain), inf_gain$i_gain, pch=16)

hist(inf_gain$i_gain, breaks=15, main="Histogram of feature information gain ", xlab="Information gain")



#####################################
#-------------- TASK 2 --------------
#####################################
message("\n\n\n\n\n\n")
message("##############################")
message("----------- TASK 2 -----------")
message("##############################")


d1 = d[1:(n_d1), ]
d2 = d[(n_d1+1):(n_d1 + n_d2)]

       

# --- task 2b ---
message("\n\n\n--- task 2b ---")
set.seed(1)



# k-fold cross-validation
cv = function(data, k=10, cp=NULL) {
  #message("Running ", k, "-fold cross-validation")
  #if(!is.null(cp)) { message("Using cp=", cp)}
  folds = get_folds(data, k)
  auc = c()
  
  for(i in 1:k) {
    d.test = as.data.frame(folds[i])
    d.train = do.call("rbind", folds[-c(i)])
    
    if(is.null(cp)) {
      fit = rpart(active ~ ., data=d.train)
    } else {
      fit = rpart(active ~ ., data=d.train, cp=cp)
    }
    prob = predict(fit, newdata=d.test)
    pred = prediction(prob, d.test$active)
    auc = c(auc, get_auc01(pred))    
    #message("iteration: ", i, ", auc01: ", auc01)
  }
  return(auc)
  
}

auc01.vec = cv(d1, k=10)
auc01 = t.test(auc01.vec, conf.level=0.95)

message("AUC0.1 mean estimate:\t", round(auc01$estimate, 4))
message("Standard deviation:\t", sd(auc01.vec))
message("Confidence interval:\t", auc01$conf.int[1], ", ", auc01$conf.int[2])



# --- task 2c ---
message("\n\n\n--- task 2c ---")
# initial cp parameter
cp = 0.3
k = 10
iterations = 25
means = c()
cps = c()
ses = c()
message("cp\t\tauc01\t\tsd\t\tse")

for(i in 1:iterations) {
  auc01.vec = cv(d1, k=k, cp=cp)
  auc01 = t.test(auc01.vec, conf.level=0.95)
  means = c(means, as.numeric(auc01$estimate))
  cps = c(cps, cp)
  se = sd(auc01.vec)/sqrt(k)
  ses = c(ses, se)
  message(round(cp, 5), "\t\t", round(auc01$estimate, 5), "\t\t",round(sd(auc01.vec), 5), "\t\t", round(se, 5))
  cp = cp * 0.8
  
}

plot(x=-log(cps), y=means)




# --- task 2d ---
message("\n\n\n--- task 2d ---")

optimal_cp = 0.00676

# train on whole d1
fit = rpart(active ~ ., data=d1, cp=optimal_cp)
prob = predict(fit, newdata=d2)
pred = prediction(prob, d2$active)
message("AUC01 on D2: ", get_auc01(pred))

# plot whole ROC curve
perf.dt <- performance(pred ,measure = "tpr", x.measure = "fpr")
plot(perf.dt, main="ROC curve: DT trained on D1, evaluated on D2", col = 2)

rpart.plot(fit)







#####################################
#-------------- TASK 3 --------------
#####################################


message("\n\n\n\n\n\n")
message("##############################")
message("----------- TASK 3 -----------")
message("##############################")

# return auc01 for given train and test data and given hyperparameters
evaluate_rf = function(train, test, ntree, mtry) {
  fit = randomForest(active ~ .,  train, ntree=ntree, mtry=mtry)
  prob = predict(fit, newdata=test)
  pred = prediction(prob, test$active)
  return(get_auc01(pred))
}


plot(c(), c(), xlab="mtry", ylab="auc01 on test set (D2)", main="Dependency of AUC01 on ntree and mtry", xlim = c(0,30), ylim=c(0, 0.1))

for (ntree in c(500)) {
  auc01s = c()
  
  mtries = c(1, 2, 4, 8, 16, 25)
  for(mtry in mtries) {
    auc01.train = evaluate_rf(d1, d1, ntree, mtry)
    auc01.test = evaluate_rf(d1, d2, ntree, mtry)
    auc01s = c(auc01s, auc01.test)
    message("mtry:\t", mtry, "\tntree:\t", ntree, "\tauc01.train:\t", round(auc01.train, 5), "\tauc01.test\t", round(auc01.test, 5))
    
  }
  
  points(mtries, auc01s, pch=16)
  lines(mtries,  auc01s, pch=16)
  
}





#####################################
#-------------- TASK 4 --------------
#####################################


message("\n\n\n\n\n\n")
message("##############################")
message("----------- TASK 4 -----------")
message("##############################")


# --- task 4a ---
message("\n\n\n--- task 4a ---")
### training - 4/5 D1
### testing  - 1/5 D1


ntree = 1000
mtry = 10

# 5-fold cross-validation
cv_rf = function(const_data, var_data, flip_train_test = FALSE) {
  message("ntree: ", ntree, "\tmtry: ", mtry)
  
  folds = get_folds(var_data, 5)
  auc = c()
  
  for(i in 1:5) {
    d.test = as.data.frame(folds[i])
    d.train = do.call("rbind", folds[-c(i)])
    
    # for the 4b task
    if (flip_train_test) {
      temp = d.test
      d.test = d.train
      d.train = temp
    }
    
    d.train = rbind(const_data, d.train)
    
    fit = randomForest(active ~ .,  d.train, ntree=ntree, mtry=mtry)
    prob = predict(fit, newdata=d.test)
    pred = prediction(prob, d.test$active)
    auc = c(auc, get_auc01(pred))    
    #message("iteration: ", i, ", auc01: ", auc01)
  } 
  return(auc)
  
}

report_mean_auc01 = function(auc01.vec) {
  auc01 = t.test(auc01.vec, conf.level=0.95)
  message("AUC0.1 mean estimate:\t", round(auc01$estimate, 5))
  message("Standard deviation:\t", round(sd(auc01.vec), 6))
  message("Confidence interval:\t", round(auc01$conf.int[1], 5), ", ", round(auc01$conf.int[2], 5))
  
}


auc01.vec = cv_rf(NULL, d1)
report_mean_auc01(auc01.vec)

# performance on D2
fit = randomForest(active ~ .,  d1, ntree=ntree, mtry=mtry)
prob = predict(fit, newdata=d2)
pred = prediction(prob, d2$active)
message("performance on whole D2: ", round(get_auc01(pred), 5))



# --- task 4b ---
message("\n\n\n--- task 4b ---")

auc01.vec = cv_rf(d1, d2, TRUE)
report_mean_auc01(auc01.vec)



# --- tak 4c ---
message("\n\n\n--- task 4c ---")

auc01.vec = cv_rf(d1, d2)
report_mean_auc01(auc01.vec)



# --- tak 4d ---
message("\n\n\n--- task 4d ---")

auc01.vec = cv_rf(NULL, d2)
report_mean_auc01(auc01.vec)


