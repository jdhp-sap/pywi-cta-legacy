import sys
sys.path.append("/local/home/tmichael/software/jeremie_cta/snippets/ctapipe")
from extract_and_crop_simtel_images import crop_astri_image


from itertools import combinations,permutations

import numpy as np

from scipy.optimize import minimize

from astropy import units as u
u.dimless = u.dimensionless_unscaled

from ctapipe.io import CameraGeometry
#from ctapipe.io.camera import _guess_camera_type

from ctapipe.reco.hillas import hillas_parameters
from ctapipe.reco.cleaning import tailcuts_clean, dilate
from ctapipe.utils import linalg

from guessPixDirection import guessPixDirection
from Telescope_Mask import TelDict


''' old '''
from datapipe.denoising.wavelets_mrtransform import wavelet_transform as wavelet_transform_old
''' new '''                                                           
from datapipe.denoising.wavelets_mrfilter import wavelet_transform    as wavelet_transform_new



__all__ = ["FitGammaHillas"]



def remove_isolated_pixels(self, img, threshold=0):
    max_val = np.max(img)
    for idx, foo in enumerate(img):
        for idy, bar in enumerate(foo):
            threshold=3
            is_island=0
            if idx>0:
                is_island += img[idx-1,idy]
            if idx<len(img)-1:
                is_island += img[idx+1,idy]
            if idy>0:
                is_island += img[idx,idy-1]
            if idy<len(foo)-1:
                is_island += img[idx,idy+1]
            
            if is_island < threshold and bar != max_val: img[idx,idy] = 0


class FitGammaHillas:
    
    def __init__(self):
        self.tel_geom = {}
        self.circles = {}
    
    
    def setup_geometry(self, telescopes, cameras, optics, phi=180.*u.deg, theta=20.*u.deg):
        self.Ver = 'Feb2016'
        self.TelVer = 'TelescopeTable_Version{}'.format(self.Ver)
        self.CamVer = 'CameraTable_Version{}_TelID'.format(self.Ver)
        self.OptVer = 'OpticsTable_Version{}_TelID'.format(self.Ver)
        
        self.telescopes = telescopes[self.TelVer]
        self.cameras    = lambda tel_id : cameras[self.CamVer+str(tel_id)]
        self.optics     = lambda tel_id : optics [self.OptVer+str(tel_id)]
    
        self.tel_phi   = phi
        self.tel_theta = theta


    def get_great_circles(self,tel_data, mode="wave", old=False, do_dilate=False):
        self.circles = {}
        for tel_id, pmt_signal in tel_data.items():

            if tel_id not in self.tel_geom:
                self.tel_geom[tel_id] = CameraGeometry.guess(self.cameras(tel_id)['PixX'].to(u.m),
                                                             self.cameras(tel_id)['PixY'].to(u.m),
                                                             self.telescopes['FL'][tel_id-1] * u.m) 
            
            
            
            
            
            
            if mode == "wave":
                try:
                    # for now wavelet library works only on rectangular images
                    cropped_img = crop_astri_image(pmt_signal)
                    if old:
                        cleaned_img = wavelet_transform_old(cropped_img, 4,"wave_5")
                    else:
                        cleaned_img = wavelet_transform_new(cropped_img)

                except FileNotFoundError:
                    continue
                
                
                if old:
                    ''' old wavelet_transform did leave constant background; remove '''
                    cleaned_img -= np.mean(cleaned_img)
                    cleaned_img[cleaned_img<0] = 0
                
                
                ''' wavelet_transform still leaves some isolated pixels; remove '''
                remove_isolated_pixels(None,cleaned_img)

            
                pmt_signal = cleaned_img.flatten()
                ''' hillas parameter function requires image and x/y arrays to be of the same dimension '''
                pix_x = crop_astri_image(self.tel_geom[tel_id].pix_x).flatten()
                pix_y = crop_astri_image(self.tel_geom[tel_id].pix_y).flatten()
    
            elif mode == "tail":
                mask = tailcuts_clean(self.tel_geom[tel_id], pmt_signal, 1,picture_thresh=10.,boundary_thresh=5.)
                if True not in mask: continue
                if do_dilate:
                    dilate(self.tel_geom[tel_id], mask)
                
                pmt_signal[mask==False] = 0
                pix_x = self.tel_geom[tel_id].pix_x
                pix_y = self.tel_geom[tel_id].pix_y
            elif mode == "none":
                pix_x = self.tel_geom[tel_id].pix_x
                pix_y = self.tel_geom[tel_id].pix_y
            else: 
                raise Exception('cleaning mode "{}" not found'.format(mode))            
            
                
                
            try:
                moments, moms2 = hillas_parameters(pix_x, pix_y,
                                                    pmt_signal)
            except :
                print("caught error, ignoring this camera")
                continue

            
            camera_rotation = -90.*u.deg
            #if tel_id in TelDict["LST"]          : camera_rotation = -110.893*u.deg
            #else: camera_rotation = -90.*u.deg
            #if tel_id in TelDict["MST_NectaCam"] : camera_rotation = -90.*u.deg
            #if tel_id in TelDict["MST_FlashCam"] : camera_rotation = -90.*u.deg
            #if tel_id in TelDict["SST_ASTRI"]    : camera_rotation = -90.*u.deg
            #if tel_id in TelDict["SST_GCT"]      : camera_rotation = -90.*u.deg    
            #if tel_id in TelDict["SST_GCT-S"]    : camera_rotation = -90.*u.deg    
            #if tel_id in TelDict["SST_DC"]       : camera_rotation = -90.*u.deg    
            #if tel_id in TelDict["SCT"]          : camera_rotation = -90.*u.deg    
            
            
            #camera_rotation_s = _guess_camera_type(len(self.cameras(tel_id)['PixX']), self.telescopes['FL'][tel_id-1]*u.m )[4]
            circle = GreatCircle(guessPixDirection( np.array([ moments.cen_x, (moments.cen_x + moments.length * np.cos( moments.psi + np.pi/2 ))] ) * u.m,
                                                    np.array([ moments.cen_y, (moments.cen_y + moments.length * np.sin( moments.psi + np.pi/2 ))] ) * u.m,
                                                    self.tel_phi, self.tel_theta, self.telescopes['FL'][tel_id-1] * u.m, camera_rotation=camera_rotation
                                                  )
                                )
            circle.weight = moments.size
            self.circles[tel_id] = circle
    
    
    def fit_origin_crosses(self):
        """ calculates the origin of the gamma as the weighted average direction
            of the intersections of all great circles
        """
        
        assert len(self.circles) >= 2, "need at least two telescopes, have {}".format(len(self.circles))
        
        crossings = []
        for perm in combinations(self.circles.values(), 2):
            n1,n2 = perm[0].norm, perm[1].norm
            # cross product automatically weighs in the angle between the two vectors
            # narrower angles have less impact, perpendicular angles have the most
            crossing = np.cross(n1,n2)
            # two great circles cross each other twice
            # (one would be the origin, the other one the direction of the gamma)
            # it doesn't matter which we pick but it should at least be consistent
            # make sure to always take the "upper" solution
            if crossing[2] < 0: crossing *= -1
            crossings.append( crossing  )
        # averaging over the solutions of all permutations
        return linalg.normalise(sum(crossings))*u.dimless, crossings
            
            

    def fit_origin_minimise(self, seed=[0,0,1], test_function=None):
        """ fits the origin of the gamma with a minimisation procedure
            this function expects that get_great_circles has been run already
            a seed should be given otherwise it defaults to "straight up"
            supperted functions to minimise are an M-estimator and the 
            negative sum of the angles to all normal vectors of the 
            great circles 
            
            Parameters:
            -----------
            seed : length-3 array
                starting point of the minimisation
            test_function : member function if this class
                either _n_angle_sum or _MEst
                defaults to _n_angle_sum if none is given
                _n_angle_sum seemingly superior to _MEst
            
            Returns:
            --------
            direction : length-3 numpy array as dimensionless quantity
                best fit for the origin of the gamma from the minimisation process
        """
        
        if test_function == None: test_function = self._n_angle_sum
        
        # using the sum of the cosines of each direction with every other direction
        # don't use the product -- with many steep angles, the product will become too small and the weight (and the whole fit) useless
        weights = [ np.sum( [ linalg.length( np.cross(A.norm,B.norm) ) for A in self.circles.values() ] ) for B in self.circles.values() ]
        
        # minimising the test function
        self.fit_result_origin = minimize( test_function, seed, args=(weights),
                                           method='BFGS', options={'disp': False}
                                         )
            
        return np.array(linalg.normalise(self.fit_result_origin.x))*u.dimless
        
    def _MEst(self, origin, weights):
        """ calculates the M-Estimator:
            a modified chi2 that becomes asymptotically linear for high values
            and is therefore less sensitive to outliers
            
            the test is performed to maximise the angles between the fit direction
            and the all the normal vectors of the great circles
            
            Parameters:
            -----------
            origin : length-3 array
                direction vector of the gamma's origin used as seed
            circles : GreatCircle array
                collection of great circles created from the camera images
            weights : array
                list of weights for each image/great circle
                
            Returns:
            --------
            MEstimator : float
                
                
            Algorithm:
            ----------
            M-Est = sum[  weight * sqrt( 2 * chi**2 ) ]
            
            
            Note:
            -----
            seemingly inferior to negative sum of angles...
            
        """

        ang = np.array([linalg.angle(origin,circ.norm) for circ in self.circles.values()])
        ang[ang>np.pi/2.] = np.pi-ang[ang>np.pi/2]
        return sum( weights*np.sqrt( 2.+ (ang-np.pi/2.)**2) )
    
    def _n_angle_sum(self, origin, weights):
        """ calculates the negative sum of the angle between the fit direction 
            and all the normal vectors of the great circles
            
            Parameters:
            -----------
            origin : length-3 array
                direction vector of the gamma's origin used as seed
            circles : GreatCircle array
                collection of great circles created from the camera images
            weights : array
                list of weights for each image/great circle
                
            Returns:
            --------
            n_sum_angles : float
                negative of the sum of the angles between the test direction
                and all normal vectors of the given great circles
        """
        #sin_ang = np.array([np.dot(origin,circ.norm) for circ in self.circles.values()])
        sin_ang = np.array([linalg.length(np.cross(origin,circ.norm)) for circ in self.circles.values()])
        return -sum(weights*sin_ang)
    
        ang = np.array([linalg.angle(origin,circ.norm) for circ in self.circles.values()])
        ang[ang>np.pi/2.] = np.pi-ang[ang>np.pi/2]
        return -sum( weights*ang )
    
    
    
    def fit_core(self, seed=[0,0]*u.m, test_function=None):
        if test_function == None: test_function = self._dist_to_traces
        zdir = np.array([0,0,1])
        
        # the core of the shower lies on the cross section of the great circle with the horizontal plane
        # the direction of this cross section is the cross-product of the normal vectors of the circle and the horizontal plane
        # here we only care about the direction; not the orientation...
        for circle in self.circles.values():
            circle.trace = normalise( np.cross( circle.norm, zdir) )
        

        # minimising the test function
        self.fit_result_core = minimize( test_function, seed,
                                         method='BFGS', options={'disp': False}
                                       )
        return np.array(self.fit_result_core.x) * u.m
    
    def _dist_to_traces(self, core):
        sum_dist = 0.
        for tel_id, circle in self.circles.items():
            # the distance of the core to the trace line is the scalar product of 
            # • the connecting vector between the core and a random point on the line 
            #   (e.g. the position of the telescope)
            # • and a normal vector of the trace in the same plane as the trace and the core
            #   (e.g. { trace[1], -trace[0] } )
            D = [core[0]-self.telescopes["TelX"][tel_id-1], core[1]-self.telescopes["TelY"][tel_id-1]]
            sum_dist += np.sqrt( 2 + (D[0]*circle.trace[1] - D[1]*circle.trace[0])**2 / 5 ) 
        return sum_dist
    

class GreatCircle:
    """ a tiny helper class to collect some parameters for each great great circle """
    
    def __init__(self, dirs):
        """ the constructor takes two directions on the circle and creates
            the normal vector belonging to that plane
            
            Parameters:
            -----------
            dirs : shape (2,3) narray
                contains two 3D direction-vectors
                
            Algorithm:
            ----------
            c : length 3 narray
                c = (a x b) x a -> a and c form an orthogonal base for the great circle
                (only orthonormal if a and b are of unit-length)
            norm : length 3 narray
                normal vector of the circle's plane, perpendicular to a, b and c
        """
        
        self.a      = dirs[0]
        self.b      = dirs[1]
        
        # a and c form an orthogonal basis for the great circle
        # not really necessary since the norm can be calculated with a and b just as well
        self.c      = np.cross( np.cross(self.a,self.b), self.a ) 
        # normal vector for the plane the great circle is in
        self.norm   = linalg.normalise( np.cross(self.a,self.c) )
        # some weight for this circle 
        # (put e.g. uncertainty on the Hillas parameters or number of PE in here)
        self.weight = 1.
        
        
