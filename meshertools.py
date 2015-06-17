#!/usr/bin/env python
#
# some tools for meshing, sampling, and convolving grids.
# standard licensing: OpenSource, not guaranteed to work, and as it so happens, totally incomplete at this time. probably untested too.
#
import numpy
import matplotlib as mpl
import pylab as plt
import datetime as dtm
import matplotlib.dates as mpd
import math
#
# some simple grid meshing and convolving.
#
#
def get_grid(x_min=0., x_max=1., y_min=0., y_max=1., dx=.1, dy=.1, Z=None):
	#
	if Z==None:
		Z = numpy.zeros((x_max-x_min) * (y_max-y_min)/(dy*dx))
	#
	if Z!=None:
		#print "Z inputs not yet enabled. you're getting zeros."
		Z = numpy.array(Z)
		Z.shape=(1,Z.size)
	#
	X = [[x,y,Z[0][j*i + j]] for i,y in enumerate(numpy.arange(y_min, y_max, dy)) for j,x in enumerate(numpy.arange(x_min, x_max, dx))]
	#
	return X

#
def mesher_token1(grid_from, grid_to, W=1.0, r0=None, w_max = 1.0):
	# a sort of token based grid mesher.
	# first time through will be messy and slow. then, we can improve it.
	# review the w_max != 1 scenario...
	# weighting algorithm is like while W>0: w = (1-dr/r0); W-=w
	#
	# for now, assume both grids are like [ [x,y,z]...]
	#
	if r0==None: r0=abs(grid_from[1][1]-grid_from[0][1])
	if r0==0.:   r0=abs(grid_from[1][0]-grid_from[0][0])
	#
	for j,rw_to in enumerate(grid_to):
		#
		# first, find distances from this point to points on other grid.
		# ... and the smart thing to do is find a way to reduce this "dists" domain. we only need to look at the closest elements.
		dists = sorted([[jj, (rw[0]-rw_to[0])**2. + (rw[1]-rw_to[1])**2] for jj,rw in enumerate(grid_from)])
		#
		#print dists[0:5]
		#
		W0 = W
		k=0
		#for k,dist in enumerate(dists):
		while W0>0.:
			# for now, just get the closest value. we'll also need to check for ties, and it would be smart to consider float error.
			#
			# average over ties:
			fr_index = dists[k][0]
			w=0.0
			n_w = 0.
			this_dist = dists[k][1]
			while dists[k][1]==this_dist:
				w += min(W, w_max-min(this_dist/r0, w_max) )
				n_w += 1.
				k+=1
			w/=n_w
			#
			W0-=w
			#
			grid_to[j][2]+=w*grid_from[fr_index][2]
			#
			#if W0<=0: break
			#k+=1

		#
	#
	return grid_to
#
	
#
#####################################
if __name__=='__main__':
	print "do __main__ stuff..."
	vc_parser.mpl.use('Agg')
else:
	plt.ion()
