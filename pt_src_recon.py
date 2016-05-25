from __future__ import division
import numpy as np
from scipy import linalg
import os
from tools_fri_doa import sph_distance, sph_gen_diracs_param, load_dirac_param, \
    sph_gen_mic_array, sph_gen_visibility, sph_recon_2d_dirac, sph_plot_diracs


if __name__ == '__main__':
    save_fig = True
    save_param = False
    stop_cri = 'max_iter'  # can be 'mse' or 'max_iter'

    # number of point sources
    K = 4
    K_est = 4  # estimated number of Diracs

<<<<<<< HEAD
    num_bands = 4  # number of sub-bands considered
    num_mic = 9  # number of microphones
=======
    num_bands = 3  # number of sub-bands considered
    num_mic = 16  # number of microphones
>>>>>>> hanjie_local

    # generate source parameters at random
    # alpha_ks, theta_ks, phi_ks, time_stamp = \
    #     sph_gen_diracs_param(K, num_bands=num_bands,
    #                          semisphere=False,
    #                          log_normal_amp=False,
    #                          save_param=save_param)

    # load saved Dirac parameters
<<<<<<< HEAD
    # dirac_file_name = './data/sph_Dirac_' + '18-05_00_01' + '.npz'
    # alpha_ks, theta_ks, phi_ks, time_stamp = load_dirac_param(dirac_file_name)
=======
    dirac_file_name = './data/sph_Dirac_' + '20-05_09_16' + '.npz'
    alpha_ks, theta_ks, phi_ks, time_stamp = load_dirac_param(dirac_file_name)
    alpha_ks = np.hstack((alpha_ks, np.tile(alpha_ks[:, -1][:, np.newaxis],
                                            (1, num_bands - alpha_ks.shape[1]))
                          ))
>>>>>>> hanjie_local

    print('Dirac parameter tag: ' + time_stamp)

    # generate microphone array layout
    radius_array = 0.3  # maximum baseline in the microphone array is twice this value
    r_mic_x, r_mic_y, r_mic_z, layout_time_stamp = \
        sph_gen_mic_array(radius_array, num_mic, num_bands=num_bands,
                          max_ratio_omega=5, save_layout=save_param)
    print('Array layout tag: ' + layout_time_stamp)

    # simulate the corresponding visibility measurements
    visi_noiseless = sph_gen_visibility(alpha_ks, theta_ks, phi_ks,
                                        r_mic_x, r_mic_y, r_mic_z)

    # add noise
<<<<<<< HEAD
    # TODO: finish this part!!
    P = float('inf')
    noise = 0
    visi_noisy = visi_noiseless + noise
=======
    var_noise = np.tile(.1, num_bands)  # noise amplitude
    visi_noisy, P_bands, noise, visi_noiseless_off_diag = \
        add_noise(visi_noiseless, var_noise, num_mic, num_bands, Ns=256)
    P = 20 * np.log10(linalg.norm(visi_noiseless_off_diag, 'fro') / linalg.norm(noise, 'fro'))
    print(P)
>>>>>>> hanjie_local

    # reconstruct point sources with FRI
    L = 6  # maximum degree of spherical harmonics
    max_ini = 20  # maximum number of random initialisation
    noise_level = np.max([1e-10, linalg.norm(noise)])
    thetak_recon, phik_recon, alphak_recon = \
        sph_recon_2d_dirac(visi_noisy, r_mic_x, r_mic_y, r_mic_z, K_est, L,
                           noise_level, max_ini, stop_cri,
<<<<<<< HEAD
                           num_rotation=1, verbose=True,
                           update_G=True, G_iter=10)
=======
                           num_rotation=3, verbose=True,
                           update_G=True, G_iter=2)
>>>>>>> hanjie_local

    dist_recon, idx_sort = sph_distance(1, theta_ks, phi_ks, thetak_recon, phik_recon)

    # print reconstruction results
    np.set_printoptions(precision=3, formatter={'float': '{: 0.3f}'.format})
    print('Reconstructed spherical coordinates (in degrees) and amplitudes:')
    print('Original colatitudes     : {0}'.format(np.degrees(theta_ks[idx_sort[:, 0]])))
    print('Reconstructed colatitudes: {0}\n'.format(np.degrees(thetak_recon[idx_sort[:, 1]])))
    print('Original azimuths        : {0}'.format(np.degrees(phi_ks[idx_sort[:, 0]])))
    print('Reconstructed azimuths   : {0}\n'.format(np.degrees(phik_recon[idx_sort[:, 1]])))
    print('Original amplitudes      : \n{0}'.format(alpha_ks[idx_sort[:, 0], :]))
    print('Reconstructed amplitudes : \n{0}\n'.format(np.real(alphak_recon[idx_sort[:, 1], :])))
    print('Reconstruction error (great-circle distance) : {0:.3e}'.format(dist_recon))
    # reset numpy print option
    np.set_printoptions(edgeitems=3, infstr='inf',
                        linewidth=75, nanstr='nan', precision=8,
                        suppress=False, threshold=1000, formatter=None)

    # plot results
    fig_dir = './result/'
    if save_fig and not os.path.exists(fig_dir):
        os.makedirs(fig_dir)
    file_name = (fig_dir + 'sph_K_{0}_numSta_{1}_' +
                 'noise_{2:.0f}dB_locations' +
                 time_stamp + '.pdf').format(repr(K), repr(num_mic), P)
    sph_plot_diracs(theta_ks, phi_ks, thetak_recon, phik_recon,
                    num_mic, P, save_fig, file_name)
