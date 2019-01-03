entropy <- function(x){
  # computes H(x)
  # expects a factor
  p <- table(x) / NROW(x)
  return( -sum(p * log2(p)) )
}

entropy.cond <- function(x, y){
  # computes H(x|y)
  # expects two factors of *the same length*
  N <- NROW(x) # should be equal to NROW(y)!
  p.y <- table(y) / N # p(y)
  p.joint <- as.vector(table(y, x)) / N # p(y,x)
  p.cond <- p.joint / rep(p.y, NROW(table(x))) # p(x|y) = p(y,x) / p(y)
  H.cond <- - sum( p.joint[p.joint > 0] * log2(p.cond[p.cond > 0]) ) # H(x|y)
  return( H.cond )
}


# For debugging is commented
source('load-mov-data.R')
message(rep("\n", 200))

message("---------------------------------------")
message("--------------Part 1 ------------------")
message("---------------------------------------")

occup = examples$occupation
rating = examples$rating

message("Conditional entropy H(OCCUPATION|RATING) = ", entropy.cond(occup, rating))


message("\n\n")
message("---------------------------------------")
message("--------------Part 2 ------------------")
message("---------------------------------------")

wrap = function (s) {
  return (gsub('(.{1,20})(\\s|$)', '\\1\n', s))
}

mov_ids = table(examples$movie)
mov_ids = names(mov_ids[mov_ids == 67])

movs = examples[examples$movie %in% mov_ids, ]
mov_names = as.vector(unique(movs$title))

# remove the movie year
mov_names = sapply(mov_names, FUN = function(s) { return (gsub("\\(.*","",s)) } )
# remove ', The'
mov_names = sapply(mov_names, FUN = function(s) { return (gsub(", The*","",s)) } )


message("Movies rated 67 times are:")
for (name in mov_names) {
  message(name)
}
message("\n\n")

# wrap long movie names
mov_names = sapply(mov_names, wrap)
par(mar=c(10,5,3,3))

message("Plotting boxplots of movies rated 67 times...")
boxplot(rating ~ movie, data=movs, names=mov_names, las=2, main="Movies rated 67 times")
means = aggregate(rating ~ movie, movs, mean)
points(1:NROW(means), means$rating, col = 'red',type = 'p',pch = 16)



message("\n\n")
message("---------------------------------------")
message("--------------Part 3 ------------------")
message("---------------------------------------")


# extend users with features "ONE" to "FIVE"
users[,c('ONE', 'TWO', 'THREE', 'FOUR', 'FIVE')]=0


apply(examples[, c(2,3)], 1, FUN=function(x) { 
    user = as.numeric(x[1])
    rating = as.numeric(x[2])
    users[user, 5 + rating] <<- users[user, 5 + rating] + 1 
})


apply(users, 1, FUN=function(x) {
  total = sum(as.numeric(x[6:10]))
  users[as.numeric(x[1]), 6:10] <<- round(as.numeric(users[as.numeric(x[1]), 6:10]) / total, digits=2)
})

distance_matrix = dist(users[, c(2, 6:10)])
dend = hclust(distance_matrix, method='average')

# cut the tree level 20 
clusters = cutree(dend, k=20)
# create new data frame

# add to users dataframe the cluster number
users$cluster = as.vector(clusters)

clus_dataframe = data.frame(average_age=round(aggregate(age ~ cluster, users, mean), 2)$age)
clus_dataframe$number_of_users = table(clusters)

message("Average age in clusters:")
print(clus_dataframe)

# for every cluster, find duplicates (ie. users, that have are the same age and have the same rating distribution )
# note: found no duplicates in given dataset 
message("Duplicate users:")

duplicities = users[duplicated(users[, c(2, 6:11)])]
if (length(duplicities) == 0) {
  message("Found no duplicate users!")
} else {
  message("Found some duplicate users")
}
