from sys import path

path.append("/local/home/tmichael/software/jeremie_cta/snippets/ctapipe")
from extract_and_crop_simtel_images import crop_astri_image

path.append("/local/home/tmichael/software/jeremie_cta/data-pipeline-standalone-scripts")
from datapipe.denoising.wavelets_mrtransform import wavelet_transform


import numpy as np

from math import log10
from random import random
from itertools import chain

from astropy import units as u

from ctapipe.io import CameraGeometry
from ctapipe.instrument.InstrumentDescription import load_hessio

from ctapipe.utils import linalg
from ctapipe.utils.fitshistogram import Histogram

from ctapipe.reco.hillas import hillas_parameters
from ctapipe.reco.cleaning import tailcuts_clean, dilate



from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import svm

from random import random


import signal
stop = None
def signal_handler(signal, frame):
    global stop
    if stop:
        print('you pressed Ctrl+C again -- exiting NOW')
        exit(-1)
    print('you pressed Ctrl+C!')
    print('exiting current loop after this event')
    stop = True




import pyhessio
def apply_mc_calibration_ASTRI(adcs, tel_id, adc_tresh=3500):
    """
    apply basic calibration
    """
    gains = pyhessio.get_calibration(tel_id)
    
    calibrated = [ (adc0-971)*gain0 if adc0 < adc_tresh else (adc1-961)*gain1 for adc0, adc1, gain0, gain1 in zip(adcs[0], adcs[1], gains[0],gains[1]) ]
    return np.array(calibrated)




class EventClassifier:
        
    
    def __init__(self):
        axisNames = [ "log(E / GeV)" ]
        ranges    = [ [2,8] ]
        nbins     = [ 6 ]
        self.wrong = { "p":Histogram( axisNames=axisNames, nbins=nbins, ranges=ranges), "g":Histogram( axisNames=axisNames, nbins=nbins, ranges=ranges) }
        self.total = { "p":Histogram( axisNames=axisNames, nbins=nbins, ranges=ranges), "g":Histogram( axisNames=axisNames, nbins=nbins, ranges=ranges) }
    
    
        self.Features  = { "g":[], "p":[] }
        self.Classes   = { "g":[], "p":[] }
        self.MCEnergy  = { "g":[], "p":[] }
    
        self.wave_out_name = "/tmp/wavelet_{}_".format(random())
        
    
    
    def setup_geometry(self, filename, phi=0.*u.deg, theta=20.*u.deg):
        (h_telescopes, h_cameras, h_optics) = load_hessio(filename)
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

        
        

    def get_event(self, event, cl, mode="wave"):
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

            tel_idx = np.searchsorted( self.telescopes['TelID'], tel_id )
            tel_pos = np.array( [self.telescopes["TelX"][tel_idx], self.telescopes["TelY"][tel_idx]] )
            impact_dist = linalg.length(tel_pos-mc_shower_core)
            
            
            if mode == "wave":
                # for now wavelet library works only on rectangular images
                cropped_img = crop_astri_image(pmt_signal)
                pmt_signal = wavelet_transform(cropped_img, 4, self.wave_out_name).flatten()
                
                # hillas parameter function requires image and x/y arrays to be of the same dimension
                pix_x = crop_astri_image(self.tel_geom[tel_id].pix_x).flatten()
                pix_y = crop_astri_image(self.tel_geom[tel_id].pix_y).flatten()
    
            elif mode == "tail":
                mask = tailcuts_clean(self.tel_geom[tel_id], pmt_signal, 1,picture_thresh=10.,boundary_thresh=8.)
                if True not in mask: continue
                dilate(self.tel_geom[tel_id], mask)
                pmt_signal[mask] = 0
                pix_x = self.tel_geom[tel_id].pix_x
                pix_y = self.tel_geom[tel_id].pix_y
            else: 
                raise Exception('cleaning mode "{}" not found'.format(mode))
            
            moments, h_moments = hillas_parameters(pix_x, pix_y, pmt_signal)
            features.append( [ moments.size, moments.width, moments.length, impact_dist, h_moments.Skewness, h_moments.Kurtosis, h_moments.Asymmetry ] )
        
        
        self.Features[cl].append( features )
        self.Classes [cl].append( cl )
        self.MCEnergy[cl].append(log10(mc_shower.energy.to(u.GeV).value))



    def equalise_nevents(self, NEvents):
        for cl in ["p", "g"]:
            self.Features[cl] = self.Features[cl][:NEvents]
            self.Classes [cl] = self.Classes [cl][:NEvents]
            self.MCEnergy[cl] = self.MCEnergy[cl][:NEvents]


    def learn(self):
        trainFeatures   = []
        trainClasses    = []
        for ev, cl in zip( chain(self.Features["p"], self.Features["g"]),
                           chain(self.Classes ["p"], self.Classes ["g"]) ):
            trainFeatures += ev
            trainClasses  += [cl]*len(ev)

        clf = RandomForestClassifier(n_estimators=40, max_depth=None,min_samples_split=1, random_state=0)
        clf.fit(trainFeatures, trainClasses)

    def self_check(self, min_tel=3, agree_threshold=.75, split_size=10):
        import matplotlib.pyplot as plt
        
        
        right_ratio = { 'g': [], 'p':[] }
                
        start      = 0
        NEvents = min(len(self.Features["p"]), len(self.Features["g"]))
        while start+split_size <= NEvents:
                
            
            trainFeatures   = []
            trainClasses    = []
            for ev, cl in zip( chain(self.Features["p"][:start] + self.Features["p"][start+split_size:],  self.Features["g"][:start] + self.Features["g"][start+split_size:]),
                               chain(self.Classes ["p"][:start] + self.Classes ["p"][start+split_size:] + self.Classes ["g"][:start] + self.Classes ["g"][start+split_size:]) ):
                trainFeatures += ev
                trainClasses  += [cl]*len(ev)

            
            
            #clf = svm.SVC(kernel='rbf')
            #clf = RandomForestClassifier(n_estimators=20, max_depth=None,min_samples_split=1, random_state=0)
            clf = RandomForestClassifier(n_estimators=40, max_depth=None,min_samples_split=1, random_state=0)
            clf.fit(trainFeatures, trainClasses)
            
            
            for ev, cl, en in zip( chain(self.Features["p"][start:start+split_size], self.Features["g"][start:start+split_size]), 
                                   chain(self.Classes ["p"][start:start+split_size], self.Classes ["g"][start:start+split_size]),
                                   chain(self.MCEnergy["p"][start:start+split_size], self.MCEnergy["g"][start:start+split_size])
                                ):
            
            
                predict = clf.predict(ev)

                right = [ 1 if (cl == tel) else 0 for tel in predict ]
                right_ratio[cl].append(sum(right) / len(right))

                isGamma = [ 1 if (tel == "g") else 0 for tel in predict ]
                if sum(isGamma) / len(isGamma) > agree_threshold: PredictClass = "g"
                else: PredictClass = "p"
                if PredictClass != cl and len(ev) > min_tel:
                    self.wrong[cl].fill( [en] )
                self.total[cl].fill( [en] )
                
                
            start += split_size
            
            for cl in ["p", "g"]:
                if sum(self.total[cl].hist) > 0:
                    print( "wrong {}: {} out of {} => {}".format(cl, sum(self.wrong[cl].hist), 
                                                                     sum(self.total[cl].hist),
                                                                     sum(self.wrong[cl].hist) / 
                                                                     sum(self.total[cl].hist) *100*u.percent))
                    
            print()
            if stop: break

        print()
        print("-"*30)
        print()
        y_eff         = {"p":[], "g":[]}
        y_eff_lerrors = {"p":[], "g":[]}
        y_eff_uerrors = {"p":[], "g":[]}
        from efficiency_errors import get_efficiency_errors_scan as get_efficiency_errors
        for cl in ["p", "g"]:
            if sum(self.total[cl].hist) > 0:
                print( "wrong {}: {} out of {} => {}".format(cl, sum(self.wrong[cl].hist), 
                                                                 sum(self.total[cl].hist),
                                                                 sum(self.wrong[cl].hist) / 
                                                                 sum(self.total[cl].hist) *100*u.percent))
            
            for wr, tot in zip( self.wrong[cl].hist, self.total[cl].hist):
                #errors = get_efficiency_errors( wr, tot )[:]
                errors = [wr/tot if tot > 0 else 0,0,0]
                y_eff        [cl].append( errors[0] )
                y_eff_lerrors[cl].append( errors[1] )
                y_eff_uerrors[cl].append( errors[2] )
        
            #wrong[cl].hist[total[cl].hist > 0] = wrong[cl].hist[total[cl].hist > 0] / total[cl].hist[total[cl].hist > 0]
        
        plt.style.use('seaborn-talk')
        fig, ax = plt.subplots(3,2, sharex=True)
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
        
        
        #tax = ax[2,0]
        plt.subplot(325)
        plt.hist(right_ratio['g'],bins=20,range=(0,1), normed=True)
        
        #tax = ax[2,1]
        plt.subplot(326)
        plt.hist(right_ratio['p'],bins=20,range=(0,1), normed=True)        