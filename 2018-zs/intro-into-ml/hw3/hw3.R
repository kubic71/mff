library("data.table")
library(FSelector)

# load development data
d1 = fread("devel1.csv")
d2 = fread("devel2.csv")
d = rbind(d1, d2)
t.blind = fread("test.blind.csv")


#------------------------------------
#-------------- TASK 1 --------------
#------------------------------------

n_d1 = NROW(d1)
n_d2 = NROW(d2)
n_features = dim(d1)[2]

# --- task 1a ---
message("--- task 1a ---")
# proportion of active ligands in d1 and d2
td1 = table(d1$active)
td2 = table(d2$active)

message("Proportion of active ligands in d1 is ", td1[2] / td1[1])
message("Proportion of active ligands in d2 is ", td2[2] / td2[1])


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

frt = 4
frt_condition = function(x) {
  frq = sum(x > 0)
  return((min(frq, NROW(x) - frq)) >= frt)
}

bin_features_names = names(get_discrete_features(d))[ sapply(discrete_features, n_unique_vals) == 2] 
bin_features = d[, colnames(d) %in% bin_features_names, with=FALSE]


features_to_remove = names(bin_features)[ sapply(bin_features, frt_condition) == FALSE ] 
message("Removing these binary features:")
print(features_to_remove)
d = subset(d, select=names(d)[ !(names(d) %in% features_to_remove) ])
message("Using ", NCOL(d) - 1 , " features")


# --- task 1f ---
discrete = get_discrete_features(d)
discrete$active = d$active

inf_gain = data.frame(f_name=rownames(inf), i_gain=information.gain(active~., discrete)[, 1])
inf_gain = inf_gain[order(inf_gain$i_gain, decreasing=TRUE), ]

plot(1:NROW(inf_gain), inf_gain$i_gain, xlab="x", ylab="y", main = "discrete feature information gain",pch=16)
lines(1:NROW(inf_gain), inf_gain$i_gain, pch=16)



#------------------------------------
#-------------- TASK 2 --------------
#------------------------------------

















