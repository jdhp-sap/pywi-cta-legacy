from extract_and_crop_simtel_images import crop_astri_image

old=False
old=True

''' old '''
from datapipe.denoising.wavelets_mrtransform import WaveletTransform as WaveletTransformOld
''' new '''                                                           
from datapipe.denoising.wavelets_mrfilter import WaveletTransform    as WaveletTransformNew


import numpy as np

from math import log10
from random import random
from itertools import chain

from astropy import units as u

from ctapipe.io import CameraGeometry
from ctapipe.instrument.InstrumentDescription import load_hessio

from ctapipe.utils import linalg
from ctapipe.utils.fitshistogram import Histogram

from ctapipe.reco.hillas import hillas_parameters,HillasParameterizationError
from ctapipe.reco.cleaning import tailcuts_clean, dilate


from datapipe.utils.EfficiencyErrors import get_efficiency_errors

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import svm

from random import random



import pyhessio
def apply_mc_calibration_ASTRI(adcs, tel_id, adc_tresh=3500):
    """
    apply basic calibration
    """
    gains = pyhessio.get_calibration(tel_id)
    
    calibrated = [ (adc0-971)*gain0 if adc0 < adc_tresh else (adc1-961)*gain1 for adc0, adc1, gain0, gain1 in zip(adcs[0], adcs[1], gains[0],gains[1]) ]
    return np.array(calibrated)




class EventClassifier:
        
    
    def __init__(self, class_list=['g','p']):

        self.class_list = class_list

        self.wrong = self.create_histogram_class_dict()
        self.total = self.create_histogram_class_dict()
    
        self.Features  = self.create_empty_class_dict()
        self.MCEnergy  = self.create_empty_class_dict()
    
        self.wave_out_name = "/tmp/wavelet_{}_".format(random())
    
        self.total_images    = 0
        self.selected_images = 0
    
    def setup_geometry(self, h_telescopes, h_cameras, h_optics, phi=180.*u.deg, theta=20.*u.deg):
        Ver = 'Feb2016'
        TelVer = 'TelescopeTable_Version{}'.format(Ver)
        CamVer = 'CameraTable_Version{}_TelID'.format(Ver)
        OptVer = 'OpticsTable_Version{}_TelID'.format(Ver)
        
        self.telescopes = h_telescopes[TelVer]
        self.cameras    = lambda tel_id : h_cameras[CamVer+str(tel_id)]
        self.optics     = lambda tel_id : h_optics [OptVer+str(tel_id)]

        self.tel_phi   =  phi 
        self.tel_theta =  theta
        
        self.tel_geom = {}
        for tel_idx, tel_id in enumerate(self.telescopes['TelID']):
            self.tel_geom[tel_id] = CameraGeometry.guess(self.cameras(tel_id)['PixX'].to(u.m),
                                                         self.cameras(tel_id)['PixY'].to(u.m),
                                                         self.telescopes['FL'][tel_idx] * u.m) 

        
    
    def create_empty_class_dict(self):
        mydict = {}
        for cl in self.class_list:
            mydict[cl] = []
        return mydict
    
    def create_histogram_class_dict(self):
        axisNames = [ "log(E / GeV)" ]
        ranges    = [ [2,8] ]
        nbins     = [ 6 ]
        mydict = {}
        for cl in self.class_list:
            mydict[cl] = Histogram( axisNames=axisNames, nbins=nbins, ranges=ranges)
        return mydict
    
    
    def get_event(self, event, cl, **kwargs):
        features = self.get_features(event, **kwargs )
        if len(features): 
            self.Features[cl].append( features )
            self.MCEnergy[cl].append( event.mc.energy )
        
    
    def get_features(self, event, mode="wave", skip_edge_events=True,edge_thresh=1.5):
        mc_shower = event.mc
        mc_shower_core = np.array( [mc_shower.core_x.value, mc_shower.core_y.value] )
        
        
        tel_data = {}
        tot_signal = 0
        for tel_id in set(event.trig.tels_with_trigger) & set(event.dl0.tels_with_data):
            data = apply_mc_calibration_ASTRI(event.dl0.tel[tel_id].adc_sums, tel_id)
            tel_data[tel_id] = data
            tot_signal += sum(data)

        features = []
        
        for tel_id, pmt_signal in tel_data.items():

            self.total_images += 1
            
            tel_idx = np.searchsorted( self.telescopes['TelID'], tel_id )
            tel_pos = np.array( [self.telescopes["TelX"][tel_idx], self.telescopes["TelY"][tel_idx]] )
            impact_dist = linalg.length(tel_pos-mc_shower_core)
            
            if mode == "wave":
                try:
                    # for now wavelet library works only on rectangular images
                    cropped_img = crop_astri_image(pmt_signal)
                    if old:
                        wavelet_transform_old = WaveletTransformOld()
                        cleaned_img = wavelet_transform_old(cropped_img, 4, self.wave_out_name)
                    else:
                        wavelet_transform_new = WaveletTransformNew()
                        cleaned_img = wavelet_transform_new(cropped_img)

                except FileNotFoundError:
                    continue
                
                
                if old:
                    ''' old wavelet_transform did leave constant background; remove '''
                    cleaned_img -= np.mean(cleaned_img)
                    cleaned_img[cleaned_img<0] = 0
                
                ''' old wavelet_transform did leave some isolated pixels; remove '''
                self.remove_isolated_pixels(cleaned_img)


                
                
                
                #import matplotlib.pyplot as plt
                #fig = None
                #if fig == None:
                    #fig = plt.figure()
                #plt.subplot(121)
                #plt.imshow(cropped_img,interpolation='none',cmap=plt.cm.afmhot)
                #plt.colorbar()
                #plt.subplot(122)
                #plt.imshow(cleaned_img,interpolation='none',cmap=plt.cm.afmhot)
                #plt.colorbar()
                #plt.pause(.1)
                #response = input()
                
                
                if skip_edge_events:
                    edge_thresh = np.max(cleaned_img)/5.
                    if (cleaned_img[0,:]  > edge_thresh).any() or  \
                       (cleaned_img[-1,:] > edge_thresh).any() or  \
                       (cleaned_img[:,0]  > edge_thresh).any() or  \
                       (cleaned_img[:,-1] > edge_thresh).any(): 
                        continue
                pmt_signal = cleaned_img.flatten()
                ''' hillas parameter function requires image and x/y arrays to be of the same dimension '''
                pix_x = crop_astri_image(self.tel_geom[tel_id].pix_x).flatten()
                pix_y = crop_astri_image(self.tel_geom[tel_id].pix_y).flatten()
    
            elif mode == "tail":
                mask = tailcuts_clean(self.tel_geom[tel_id], pmt_signal, 1,picture_thresh=10.,boundary_thresh=8.)
                if True not in mask: continue
                dilate(self.tel_geom[tel_id], mask)
                
                if skip_edge_events:
                    skip_event=False
                    for pixid in self.tel_geom[tel_id].pix_id[mask]:
                        if len(self.tel_geom[tel_id].neighbors) < 8:
                            skip_event=True
                            break
                    if skip_event: continue
                        


                pmt_signal[mask==False] = 0
                pix_x = self.tel_geom[tel_id].pix_x
                pix_y = self.tel_geom[tel_id].pix_y
            else: 
                raise Exception('cleaning mode "{}" not found'.format(mode))

            try:
                moments, h_moments = hillas_parameters(pix_x, pix_y, pmt_signal)
                features.append( [ moments.size, moments.width, moments.length, impact_dist, h_moments.Skewness, h_moments.Kurtosis, h_moments.Asymmetry ] )
                self.selected_images += 1
            except HillasParameterizationError as e:
                print(e)
                print("ignoring this camera")
                pass

        return features


    def equalise_nevents(self, NEvents):
        for cl in ["p", "g"]:
            self.Features[cl] = self.Features[cl][:NEvents]
            self.MCEnergy[cl] = self.MCEnergy[cl][:NEvents]


    def learn(self, clf=None):
        trainFeatures   = []
        trainClasses    = []
        for cl in self.Features.keys():
            for ev in self.Features[cl]:
                trainFeatures += ev
                trainClasses  += [cl]*len(ev)
        
        if clf == None:
            clf = RandomForestClassifier(n_estimators=40, max_depth=None,min_samples_split=1, random_state=0)
        clf.fit(trainFeatures, trainClasses)
        self.clf = clf


    def save(self, path):
        from sklearn.externals import joblib
        joblib.dump(self.clf, path) 
        
    def load(self, path):
        from sklearn.externals import joblib
        self.clf = joblib.load(path)
    
    def predict(self, ev):
        return self.clf.predict(ev)

    def self_check(self, min_tel=3, agree_threshold=.75, split_size=10, clf=None, verbose=True):
        import matplotlib.pyplot as plt
        
        right_ratio = self.create_empty_class_dict()
        
        start   = 0
        NEvents = min( len(features) for features in self.Features.values() )
        while start+split_size <= NEvents:
            trainFeatures   = []
            trainClasses    = []
            for cl in self.Features.keys():
                for ev in chain( self.Features[cl][:start], self.Features[cl][start+split_size:] ):
                    trainFeatures += ev
                    trainClasses  += [cl]*len(ev)


            if clf == None:
                clf = RandomForestClassifier(n_estimators=40, max_depth=None,min_samples_split=1, random_state=0)
            clf.fit(trainFeatures, trainClasses)
            
            
            for cl in self.Features.keys():
                for ev, en in zip( self.Features[cl][start:start+split_size], 
                                   self.MCEnergy[cl][start:start+split_size]
                                 ):
                
                    log_en = np.log10(en/u.GeV)
                    
                    PredictTels = clf.predict(ev)
                    
                    
                    right = [ 1 if (cl == tel) else 0 for tel in PredictTels ]
                    right_ratio[cl].append(sum(right) / len(right))

                    isGamma = [ 1 if (tel == "g") else 0 for tel in PredictTels ]
                    if sum(isGamma) / len(isGamma) > agree_threshold: PredictClass = "g"
                    else: PredictClass = "p"
                    if PredictClass != cl and len(ev) >= min_tel:
                    
                    #''' check if prediction was right '''
                    #right_ratio[cl].append( np.count_nonzero(PredictTels==cl)/len(PredictTels) )

                    #''' check if prediction returned gamma '''
                    #isGamma = PredictTels == "g"
                    #try:
                        #if np.count_nonzero(isGamma)/len(isGamma) > agree_threshold: PredictEvent = "g"
                        #else: PredictEvent = "!g"
                    #except:
                        #print(ev)
                        #print(PredictTels)
                        #print(isGamma)
                        #sys.exit()
                    #if PredictEvent != cl and len(ev) >= min_tel:
                        self.wrong[cl].fill( [log_en] )
                    self.total[cl].fill( [log_en] )
                
                
                if verbose and sum(self.total[cl].hist) > 0:
                    print( "wrong {}: {} out of {} => {}".format(cl, sum(self.wrong[cl].hist), 
                                                                     sum(self.total[cl].hist),
                                                                     sum(self.wrong[cl].hist) / 
                                                                     sum(self.total[cl].hist) *100*u.percent))
            start += split_size
                    
            print()

        print()
        print("-"*30)
        print()
        y_eff         = self.create_empty_class_dict()
        y_eff_lerrors = self.create_empty_class_dict()
        y_eff_uerrors = self.create_empty_class_dict()
        
        try:    from efficiency_errors import get_efficiency_errors_scan as get_efficiency_errors
        except ImportError: pass
    
        for cl in self.Features.keys():
            if sum(self.total[cl].hist) > 0:
                print( "wrong {}: {} out of {} => {}".format(cl, sum(self.wrong[cl].hist), 
                                                                 sum(self.total[cl].hist),
                                                                 sum(self.wrong[cl].hist) / 
                                                                 sum(self.total[cl].hist) *100*u.percent))
            
            for wr, tot in zip( self.wrong[cl].hist, self.total[cl].hist):
                try:
                    errors = get_efficiency_errors( wr, tot )
                except:
                    errors = [wr/tot if tot > 0 else 0,0,0]
                y_eff        [cl].append( errors[0] )
                y_eff_lerrors[cl].append( errors[1] )
                y_eff_uerrors[cl].append( errors[2] )
        
        
        plt.style.use('seaborn-talk')
        fig, ax = plt.subplots(3,2)
        tax = ax[0,0]
        tax.errorbar(self.wrong["g"].bin_centers(0), y_eff["g"], yerr=[y_eff_lerrors["g"], y_eff_uerrors["g"]])
        tax.set_title("gamma misstag")
        tax.set_xlabel("log(E/GeV)")
        tax.set_ylabel("incorrect / all")
        
        tax = ax[0,1]
        tax.errorbar(self.wrong["p"].bin_centers(0), y_eff["p"], yerr=[y_eff_lerrors["p"], y_eff_uerrors["p"]])
        tax.set_title("proton misstag")
        tax.set_xlabel("log(E/GeV)")
        tax.set_ylabel("incorrect / all")
        
        tax = ax[1,0]
        tax.bar(self.total["g"].bin_lower_edges[0][:-1], self.total["g"].hist, 
                width=(self.total["g"].bin_lower_edges[0][-1] - self.total["g"].bin_lower_edges[0][0])/
                len(self.total["g"].bin_centers(0)))
        tax.set_title("gamma numbers")
        tax.set_xlabel("log(E/GeV)")
        tax.set_ylabel("events")
        
        tax = ax[1,1]
        tax.bar(self.total["p"].bin_lower_edges[0][:-1], self.total["p"].hist, 
                width=(self.total["p"].bin_lower_edges[0][-1] - self.total["p"].bin_lower_edges[0][0])/
                len(self.total["p"].bin_centers(0)))
        tax.set_title("proton numbers")
        tax.set_xlabel("log(E/GeV)")
        tax.set_ylabel("events")
        
        
        tax = ax[2,0]
        tax.hist(right_ratio['g'],bins=20,range=(0,1), normed=True)
        tax.set_title("fraction of classifiers per event agreeing to gamma")
        tax.set_xlabel("agree ratio")
        tax.set_ylabel("PDF")
        
        tax = ax[2,1]
        tax.hist(right_ratio['p'],bins=20,range=(0,1), normed=True)
        tax.set_title("fraction of classifiers per event agreeing to proton")
        tax.set_xlabel("agree ratio")
        tax.set_ylabel("PDF")

        plt.tight_layout()
        plt.show()

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
