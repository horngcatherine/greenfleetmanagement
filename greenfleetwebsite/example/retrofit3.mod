#######################################################################
#                                                                     #
# AMPL representation of retrofit/replacement mathematical model      #
# Developed by Timon Stasko                                           #
#                                                                     #
#######################################################################

param numVehicleTypes >=0; # number of vehicle types
param numRetrofitTypes >=0; # number of retrofit types
#param numPeriods >=1; # number of time periods (not used yet)
param numPollutants >=1; # number of pollutants to track

set I = 1..numVehicleTypes; # set of vehicle types
set J = 1..numRetrofitTypes; # set of retrofit types
#set T = 1..numPeriods; # set of time periods (not used yet)
set P = 1..numPollutants; # set of pollutants to track


param u{i in I,j in J,k in J}>=0; # upper bound on number of vehicles of type i to go from retrofit package j to k
param f{i in I,j in J}>=0; # number of vehicles of type i with retrofit package j in intial fleet

param m{i in I}>=0; # remaining number of miles a vehicle of type i will travel
param w{i in I}>=0; # remaining number of hours vehicle of type i will idle

param c{i in I,j in J, k in J}; # discounted cost of switching from retrofit j to k on vehicle type i
param d{i in I,j in J, k in J}; # initial cost of switching from retrofit j to k on vehicle type i

param rer{i in I,j in J,p in P}; # g/mile running emission rate for pollutant p by vehicle of type i w/ retrofit package j
param ier{i in I,j in J,p in P}; # g/hour idling emission rate for pollutant p by vehicle of type i w/ retrofit package j

param B>=0;	# short term budget for retrofits and early retirements
param LB>=0; 	# long term budget

param frac{p in P}; # fraction reduction required for pollutant p
						
var r{i in I, j in J, k in J} integer;	# number of vehicles of type i to go from retrofit package j to k

var Ebase{p in P} =  sum{i in I, j in J, k in J} (r[i,j,k]*m[i]*rer[i,j,p]+r[i,j,k]*w[i]*ier[i,j,p]);	# emissions if no retrofits changed
var Eretrofit{p in P} = sum{i in I, j in J, k in J} (r[i,j,k]*m[i]*rer[i,k,p]+r[i,j,k]*w[i]*ier[i,k,p]);	# emissions w/ retrofit changes


# begin optional parameters/variables for solution interpretation
param Eoptions1{i in I, j in J, p in P} =  (m[i]*rer[i,j,p]+w[i]*ier[i,j,p]);	# remaining emissions of every option, for 1 veh

param PMeff{i in I, j in J, k in J} = (Eoptions1[i,j,1]-Eoptions1[i,k,1])/(c[i,j,k]+0.01);	# gram reduction PM2.5/$spent (.01 is to keep pos denom)
param COeff{i in I, j in J, k in J} = (Eoptions1[i,j,2]-Eoptions1[i,k,2])/(c[i,j,k]+0.01);	# gram reduction CO/$spent (.01 is to keep pos denom)
param NOxeff{i in I, j in J, k in J} = (Eoptions1[i,j,3]-Eoptions1[i,k,3])/(c[i,j,k]+0.01);	# gram reduction NOx/$spent (.01 is to keep pos denom)
param VOCeff{i in I, j in J, k in J} = (Eoptions1[i,j,4]-Eoptions1[i,k,4])/(c[i,j,k]+0.01);	# gram reduction VOC/$spent (.01 is to keep pos denom)

param dPMeff{i in I, j in J, k in J} = (Eoptions1[i,j,1]-Eoptions1[i,k,1])/(d[i,j,k]+0.01);	# gram reduction PM2.5/initial$spent (.01 is to keep pos denom)
param dCOeff{i in I, j in J, k in J} = (Eoptions1[i,j,2]-Eoptions1[i,k,2])/(d[i,j,k]+0.01);	# gram reduction CO/initial$spent (.01 is to keep pos denom)
param dNOxeff{i in I, j in J, k in J} = (Eoptions1[i,j,3]-Eoptions1[i,k,3])/(d[i,j,k]+0.01);	# gram reduction NOx/initial$spent (.01 is to keep pos denom)
param dVOCeff{i in I, j in J, k in J} = (Eoptions1[i,j,4]-Eoptions1[i,k,4])/(d[i,j,k]+0.01);	# gram reduction VOC/initial$spent (.01 is to keep pos denom)

# end of optional variables

minimize long_term_cost:
	sum{i in I, j in J, k in J} (r[i,j,k]*c[i,j,k]);
	# the long term cost of all retrofit changes

minimize short_term_cost:
	sum{i in I, j in J, k in J} (r[i,j,k]*d[i,j,k]);
	# the initial cost of all retrofit changes

minimize PM_emission:
	Eretrofit[1];
	# grams of PM emitted post retrofit

subject to r_non_neg {i in I, j in J, k in J}:
	r[i,j,k]>=0;
	# only a non-negative number of retrofit package changes have been performed

subject to r_cap {i in I, j in J, k in J}:
	r[i,j,k]<=u[i,j,k];
	# the number of vehicles of type i changing from retrofit package j to k cannot exceed cap

subject to retrofit_all {i in I, j in J}:
	f[i,j]=sum{k in J} r[i,j,k];
	# all vehicles must recieve a retrofit (including the null retrofit)

subject to percent_reduction {p in P}:
	sum{i in I, j in J, k in J}(r[i,j,k]*m[i]*rer[i,k,p]+r[i,j,k]*w[i]*ier[i,k,p]) <= (1-frac[p])*(sum{i in I, j in J, k in J} (r[i,j,k]*m[i]*rer[i,j,p]+r[i,j,k]*w[i]*ier[i,j,p]));
	# pollutant percentage reduction requirement

# begin optional constraints

subject to budget:
	sum{i in I, j in J, k in J} (r[i,j,k]*d[i,j,k])<=B;
	#short term budget 

subject to long_budget:
	sum{i in I, j in J, k in J} (r[i,j,k]*c[i,j,k])<=LB;
	#long term budget