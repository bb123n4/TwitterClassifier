Usage of files:
type python run.py to execute both two files at the same time

Both used first 4000 data items as trainning set and the last 2444 items as test data.

By conducting some experiments, the sklearn library perform better than my implemented version, 
the reason may be different choice of alpha-the smoothing priors. In my implementation, the 
absent features are simply ignored.